"""Shared simulation engine for the cellular automata pipeline.

A loop's ``generate_ca.py`` only declares ``RULES``, a list of :class:`Rule`.
Initial conditions, seeding, simulation, rendering, file naming and the run
manifest all live here, so every loop behaves the same way and every image can
be regenerated exactly from its code and seed.

Run a loop from the repository root::

    python -m ca_core run generations/loop_26
"""
from __future__ import annotations

import importlib.util
import json
import re
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Sequence

import numpy as np
from PIL import Image

INIT_TYPES = ("single_seed", "random")
DEFAULT_WIDTH = 800
DEFAULT_STEPS = 800
DEFAULT_SEED = 0
MANIFEST_NAME = "manifest.json"
IMAGE_RE = re.compile(r"^rule_(\d+)_(single_seed|random)\.png$")


class RuleError(Exception):
    """A rule is misconfigured or produced an invalid state."""


@dataclass
class Rule:
    """One cellular automaton rule.

    step(state, rng, t) -> next state
        ``state`` is a 1-D integer array of ``width`` cells with values in
        ``0..n_states-1`` (unless ``init``/``view`` say otherwise). Boundaries are
        periodic by convention: use ``np.roll``. ``rng`` is a seeded
        ``numpy.random.Generator``; use it for all randomness, never ``np.random.*``,
        so runs are reproducible. ``t`` is the index of the row being stepped from.
    palette
        Exactly ``n_states`` distinct RGB triples; the index is the state.
    init(init_type, width, rng) -> state, optional
        Custom starting state for ``"single_seed"`` / ``"random"``. Return ``None`` to
        fall back to the default for that init type.
    view(state) -> 1-D int array, optional
        Maps the state to the visible row. Needed only when the state carries hidden
        channels (e.g. a ``(previous_row, current_row)`` tuple).
    seed_state
        Value of the centre cell in the default single-seed start (background is 0).
    """

    name: str
    n_states: int
    step: Callable[[Any, np.random.Generator, int], Any]
    palette: Sequence[Sequence[int]]
    init: Optional[Callable[[str, int, np.random.Generator], Any]] = None
    view: Optional[Callable[[Any], Any]] = None
    seed_state: int = 1
    description: str = ""

    def validate(self, label: str = "") -> None:
        where = label or self.name
        if isinstance(self.n_states, bool) or not isinstance(self.n_states, (int, np.integer)) or not 2 <= self.n_states <= 32767:
            raise RuleError(f"{where}: n_states must be an int in 2..32767, got {self.n_states!r}")
        if not callable(self.step):
            raise RuleError(f"{where}: step must be a function step(state, rng, t)")
        for attr in ("init", "view"):
            if getattr(self, attr) is not None and not callable(getattr(self, attr)):
                raise RuleError(f"{where}: {attr} must be a function or None")
        try:
            pal = np.asarray(self.palette, dtype=np.int64)
        except (TypeError, ValueError) as exc:
            raise RuleError(f"{where}: palette must be a list of RGB triples ({exc})") from None
        if pal.shape != (self.n_states, 3):
            raise RuleError(
                f"{where}: palette must have exactly n_states={self.n_states} RGB triples, got shape {pal.shape}"
            )
        if pal.min() < 0 or pal.max() > 255:
            raise RuleError(f"{where}: palette values must be in 0..255")
        if len({tuple(c) for c in pal.tolist()}) != self.n_states:
            raise RuleError(f"{where}: palette colours must be distinct (triage decodes states from colours)")
        if not 1 <= self.seed_state < self.n_states:
            raise RuleError(f"{where}: seed_state must be in 1..{self.n_states - 1}, got {self.seed_state!r}")


def default_initial_state(rule: Rule, init_type: str, width: int, rng: np.random.Generator) -> np.ndarray:
    """single_seed: one cell of ``seed_state`` in the centre of a 0 background.
    random: each cell uniform over all states."""
    if init_type == "single_seed":
        row = np.zeros(width, dtype=np.int32)
        row[width // 2] = rule.seed_state
        return row
    if init_type == "random":
        return rng.integers(0, rule.n_states, size=width, dtype=np.int32)
    raise ValueError(f"unknown init type {init_type!r}; expected one of {INIT_TYPES}")


def _visible_row(rule: Rule, state: Any, width: int, where: str) -> np.ndarray:
    row = rule.view(state) if rule.view is not None else state
    row = np.asarray(row)
    if row.shape != (width,):
        hint = " (state has hidden channels? give the rule a view function)" if rule.view is None else ""
        raise RuleError(f"{where}: expected a 1-D row of {width} cells, got shape {row.shape}{hint}")
    if row.dtype == bool:
        row = row.astype(np.int32)
    if not np.issubdtype(row.dtype, np.integer):
        raise RuleError(f"{where}: states must be integers, got dtype {row.dtype}; cast with .astype(np.int32)")
    lo, hi = int(row.min()), int(row.max())
    if lo < 0 or hi >= rule.n_states:
        bad = lo if lo < 0 else hi
        raise RuleError(f"{where}: state {bad} is outside 0..{rule.n_states - 1}")
    return row


def simulate(
    rule: Rule,
    init_type: str,
    width: int = DEFAULT_WIDTH,
    steps: int = DEFAULT_STEPS,
    seed: int = DEFAULT_SEED,
    label: Optional[str] = None,
) -> np.ndarray:
    """Return the ``(steps, width)`` space-time grid of visible states. Row 0 is the start.

    One generator, seeded with ``seed``, draws the starting state and then the dynamics.
    """
    rng = np.random.default_rng(seed)
    state = initial_state(rule, init_type, width, rng)
    return evolve(rule, state, init_type, width, steps, rng, label)


def initial_state(rule: Rule, init_type: str, width: int, rng: np.random.Generator) -> Any:
    """The rule's starting state for ``init_type``: its own ``init``, else the default."""
    state = rule.init(init_type, width, rng) if rule.init is not None else None
    return default_initial_state(rule, init_type, width, rng) if state is None else state


def evolve(
    rule: Rule,
    state: Any,
    init_type: str,
    width: int,
    steps: int,
    rng: np.random.Generator,
    label: Optional[str] = None,
) -> np.ndarray:
    """Run ``steps - 1`` steps from ``state``; return the ``(steps, width)`` grid of visible states."""
    label = label or rule.name
    grid = np.empty((steps, width), dtype=np.uint8 if rule.n_states <= 256 else np.int16)
    grid[0] = _visible_row(rule, state, width, f"{label} [{init_type}] row 0")
    for t in range(steps - 1):
        state = rule.step(state, rng, t)
        grid[t + 1] = _visible_row(rule, state, width, f"{label} [{init_type}] row {t + 1}")
    return grid


def render(grid: np.ndarray, palette: Sequence[Sequence[int]]) -> Image.Image:
    """One pixel per cell: x = space, y = time (downwards)."""
    return Image.fromarray(np.asarray(palette, dtype=np.uint8)[grid])


def image_name(rule_index: int, init_type: str) -> str:
    return f"rule_{rule_index:02d}_{init_type}.png"


def image_seed(base_seed: int, loop: int, rule_index: int, init_type: str) -> int:
    """Seed for one image, derived from (base seed, loop, rule, init type)."""
    entropy = [base_seed, loop, rule_index, INIT_TYPES.index(init_type)]
    return int(np.random.SeedSequence(entropy).generate_state(1)[0])


def loop_number(loop_dir: Path) -> int:
    match = re.search(r"loop_(\d+)$", Path(loop_dir).resolve().name)
    return int(match.group(1)) if match else 0


def load_rules(loop_dir: Path) -> list:
    """Import ``loop_dir/generate_ca.py`` and return its validated ``RULES``."""
    path = Path(loop_dir) / "generate_ca.py"
    if not path.is_file():
        raise RuleError(f"{path} not found")
    spec = importlib.util.spec_from_file_location(f"_ca_loop_{loop_number(loop_dir)}_rules", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rules = getattr(module, "RULES", None)
    if not isinstance(rules, (list, tuple)) or not rules:
        raise RuleError(
            f"{path} must define RULES = [Rule(...), ...]. Loops 1-25 predate ca_core: "
            "run those scripts directly instead."
        )
    for i, rule in enumerate(rules, 1):
        if not isinstance(rule, Rule):
            raise RuleError(f"{path}: RULES[{i - 1}] is a {type(rule).__name__}, expected ca_core.Rule")
        rule.validate(f"rule {i:02d} ({rule.name})")
    return list(rules)


def read_manifest(loop_dir: Path) -> Optional[dict]:
    path = Path(loop_dir) / MANIFEST_NAME
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def run_loop(
    loop_dir: Path,
    width: int = DEFAULT_WIDTH,
    steps: int = DEFAULT_STEPS,
    base_seed: int = DEFAULT_SEED,
    only: Optional[Iterable[int]] = None,
    log: Callable[[str], None] = print,
) -> dict:
    """Simulate and render every rule x init type; write PNGs and ``manifest.json``.

    A rule that raises is recorded in the manifest and its stale images are deleted,
    so the other rules still run and triage reports the failure.
    """
    loop_dir = Path(loop_dir)
    rules = load_rules(loop_dir)
    loop = loop_number(loop_dir)
    out_dir = loop_dir / "output"
    out_dir.mkdir(exist_ok=True)
    settings = {"width": width, "steps": steps, "base_seed": base_seed}

    selected = sorted(set(only)) if only else list(range(1, len(rules) + 1))
    unknown = [i for i in selected if not 1 <= i <= len(rules)]
    if unknown:
        raise RuleError(f"no such rule(s): {unknown}; RULES has {len(rules)} entries")

    manifest = read_manifest(loop_dir) if only else None
    if manifest is not None and manifest.get("settings") != settings:
        raise RuleError(
            f"settings {settings} differ from the previous run {manifest.get('settings')}; re-run all rules"
        )
    if manifest is None:
        manifest = {"loop": loop, "settings": settings, "rules": {}}
        if not only:  # drop images of rules that no longer exist
            for png in out_dir.glob("rule_*.png"):
                match = IMAGE_RE.match(png.name)
                if match and int(match.group(1)) > len(rules):
                    png.unlink()
    manifest["rules"] = {k: v for k, v in manifest["rules"].items() if int(k) <= len(rules)}

    if len(rules) != 10:
        log(f"note: RULES has {len(rules)} entries (the pipeline expects 10)")

    for index in selected:
        rule = rules[index - 1]
        entry = {"name": rule.name, "n_states": int(rule.n_states), "images": {}, "errors": {}}
        for init_type in INIT_TYPES:
            name = image_name(index, init_type)
            seed = image_seed(base_seed, loop, index, init_type)
            started = time.perf_counter()
            try:
                grid = simulate(rule, init_type, width, steps, seed, label=f"rule {index:02d} ({rule.name})")
            except Exception as exc:  # noqa: BLE001 - report and keep going with the other rules
                (out_dir / name).unlink(missing_ok=True)
                entry["errors"][init_type] = f"{type(exc).__name__}: {exc}"
                log(f"rule {index:02d} {init_type:<11}  ERROR  {type(exc).__name__}: {exc}")
                if not isinstance(exc, RuleError) and len(entry["errors"]) == 1:
                    log(traceback.format_exc().rstrip())
                continue
            render(grid, rule.palette).save(out_dir / name)
            seconds = round(time.perf_counter() - started, 2)
            entry["images"][init_type] = {"file": f"output/{name}", "seed": seed}  # no timings: keeps re-runs diff-free
            log(f"rule {index:02d} {init_type:<11}  {seconds:6.2f}s  output/{name}")
        manifest["rules"][str(index)] = entry

    manifest["rules"] = dict(sorted(manifest["rules"].items(), key=lambda kv: int(kv[0])))
    (loop_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
