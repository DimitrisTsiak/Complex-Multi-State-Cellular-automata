"""Parameter sweeps: animate how one rule's picture changes as a float parameter varies.

A sweepable rule is a factory: a function that takes the parameter as a keyword argument
and returns a Rule, for example ``directed_percolation(p=0.65)`` in
hall_of_fame/generate_ca.py. From the repository root::

    python -m ca_core sweep hall_of_fame/generate_ca.py:directed_percolation \\
        --start 0.55 --stop 0.75 --frames 41

Every frame starts from the same initial rows and uses the same random numbers: the
starting state and the dynamics each get their own fixed seed, so the only difference
between frames is the parameter. Each frame shows the single-seed run (left) next to the
random run (right), with the quality-gate label of each.
"""
from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from typing import Callable, Optional, Sequence

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .engine import DEFAULT_SEED, DEFAULT_STEPS, DEFAULT_WIDTH, INIT_TYPES, Rule, RuleError, evolve, initial_state, render
from .triage import analyze, classify

BACKGROUND = (17, 17, 22)
TEXT = (235, 235, 240)
MUTED = (150, 150, 162)
TRACK = (55, 55, 66)
ACCENT = (255, 196, 0)
CAPTIONS = {"single_seed": "single seed", "random": "random"}


# ---------------------------------------------------------------- loading

def load_factory(spec: str) -> Callable[..., Rule]:
    """``path/to/file.py:function`` -> the function."""
    path, _, name = spec.rpartition(":")
    if not path or not name:
        raise RuleError(f"expected path/to/file.py:function, got {spec!r}")
    file = Path(path)
    if not file.is_file():
        raise RuleError(f"{file} not found")
    module_spec = importlib.util.spec_from_file_location(f"_ca_sweep_{file.stem}", file)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    factory = getattr(module, name, None)
    if not callable(factory):
        raise RuleError(f"{file} has no function {name!r}")
    return factory


def factory_param(factory: Callable[..., Rule], param: Optional[str] = None) -> str:
    """The parameter to sweep: ``param`` if given, else the factory's only parameter."""
    names = [p.name for p in inspect.signature(factory).parameters.values()
             if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
    if param is not None:
        if param not in names:
            raise RuleError(f"{factory.__name__}() has no parameter {param!r}; it takes {names}")
        return param
    if len(names) != 1:
        raise RuleError(f"{factory.__name__}() takes {names}; choose one with --param")
    return names[0]


# ---------------------------------------------------------------- simulation

def sweep_seeds(seed: int, init_type: str) -> tuple:
    """Separate, fixed seeds for the starting state and for the dynamics of one init type."""
    i = INIT_TYPES.index(init_type)
    return np.random.SeedSequence([seed, i, 0]), np.random.SeedSequence([seed, i, 1])


def run_sweep(
    factory: Callable[..., Rule],
    param: str,
    values: Sequence[float],
    width: int = DEFAULT_WIDTH,
    steps: int = DEFAULT_STEPS,
    seed: int = DEFAULT_SEED,
) -> list:
    """Simulate both init types at every value. Returns [{value, rule, grids, labels}, ...]."""
    frames = []
    for value in values:
        rule = factory(**{param: float(value)})
        if not isinstance(rule, Rule):
            raise RuleError(f"{factory.__name__}({param}={value}) returned {type(rule).__name__}, not a Rule")
        rule.validate(f"{rule.name} [{param}={value:g}]")
        grids, labels = {}, {}
        for init_type in INIT_TYPES:
            init_seed, step_seed = sweep_seeds(seed, init_type)
            state = initial_state(rule, init_type, width, np.random.default_rng(init_seed))
            grid = evolve(rule, state, init_type, width, steps, np.random.default_rng(step_seed),
                          label=f"{rule.name} [{param}={value:g}]")
            grids[init_type] = grid
            labels[init_type] = classify(analyze(grid))
        frames.append({"value": float(value), "rule": rule, "grids": grids, "labels": labels})
    return frames


def varying_starts(frames: list) -> list:
    """Init types whose starting row differs between frames (the parameter affects the start)."""
    return [t for t in INIT_TYPES
            if any(not np.array_equal(f["grids"][t][0], frames[0]["grids"][t][0]) for f in frames[1:])]


# ---------------------------------------------------------------- rendering

def _font(size: int, bold: bool = False):
    names = ("arialbd.ttf", "DejaVuSans-Bold.ttf") if bold else ("arial.ttf", "DejaVuSans.ttf")
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def compose_frame(frame: dict, param: str, lo: float, hi: float, scale: float = 0.5) -> Image.Image:
    """One GIF frame: title and parameter value, a progress bar, then the two panels."""
    rule = frame["rule"]
    panels = [render(frame["grids"][t], rule.palette) for t in INIT_TYPES]
    if scale != 1:
        size = (max(1, round(panels[0].width * scale)), max(1, round(panels[0].height * scale)))
        panels = [p.resize(size, Image.Resampling.BOX) for p in panels]
    pw, ph = panels[0].size
    margin, gap, header = 16, 12, 104
    width, height = 2 * pw + gap + 2 * margin, header + ph + margin

    img = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(img)
    title, value_font, small = _font(20, bold=True), _font(20, bold=True), _font(14)

    draw.text((margin, 12), rule.name, font=title, fill=TEXT)
    value_text = f"{param} = {frame['value']:.4f}"
    draw.text((width - margin - draw.textlength(value_text, font=value_font), 12), value_text,
              font=value_font, fill=ACCENT)

    bar_top, bar_bottom = 46, 52
    fraction = 0.0 if hi == lo else (frame["value"] - lo) / (hi - lo)
    draw.rectangle([margin, bar_top, width - margin, bar_bottom], fill=TRACK)
    draw.rectangle([margin, bar_top, margin + fraction * (width - 2 * margin), bar_bottom], fill=ACCENT)
    draw.text((margin, bar_bottom + 4), f"{lo:g}", font=small, fill=MUTED)
    hi_text = f"{hi:g}"
    draw.text((width - margin - draw.textlength(hi_text, font=small), bar_bottom + 4), hi_text, font=small, fill=MUTED)

    for k, init_type in enumerate(INIT_TYPES):
        x = margin + k * (pw + gap)
        label = frame["labels"][init_type][0]
        caption = CAPTIONS[init_type]
        draw.text((x, header - 22), caption, font=small, fill=TEXT)
        draw.text((x + draw.textlength(caption + "  ", font=small), header - 22), label, font=small, fill=MUTED)
        img.paste(panels[k], (x, header))
    return img


def save_gif(images: list, out: Path, duration: int = 150, hold: int = 1200, bounce: bool = False) -> None:
    """Write the frames as a looping GIF with one shared palette (no dithering)."""
    order = list(range(len(images)))
    if bounce and len(images) > 2:
        order += order[-2:0:-1]
    durations = [hold if i in (0, len(images) - 1) else duration for i in order]

    sample = images[:: max(1, len(images) // 8)] + [images[-1]]
    montage = Image.new("RGB", (images[0].width, images[0].height * len(sample)))
    for k, im in enumerate(sample):
        montage.paste(im, (0, k * images[0].height))
    palette = montage.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images]

    out.parent.mkdir(parents=True, exist_ok=True)
    indexed[order[0]].save(out, save_all=True, append_images=[indexed[i] for i in order[1:]],
                           duration=durations, loop=0)


def make_sweep_gif(
    factory: Callable[..., Rule],
    start: float,
    stop: float,
    frames: int = 41,
    out: Optional[Path] = None,
    param: Optional[str] = None,
    width: int = DEFAULT_WIDTH,
    steps: int = DEFAULT_STEPS,
    seed: int = DEFAULT_SEED,
    scale: float = 0.5,
    duration: int = 150,
    hold: int = 1200,
    bounce: bool = False,
    log: Callable[[str], None] = print,
) -> Path:
    if frames < 2:
        raise RuleError("a sweep needs at least 2 frames")
    if start == stop:
        raise RuleError("--start and --stop must differ")
    param = factory_param(factory, param)
    out = Path(out) if out else Path("sweeps") / f"{factory.__name__}_{param}.gif"
    values = np.linspace(start, stop, frames)

    log(f"Sweeping {factory.__name__}({param}) from {start:g} to {stop:g} in {frames} frames, seed {seed}")
    results = run_sweep(factory, param, values, width, steps, seed)
    for f in results:
        cells = "   ".join(f"{t}: {f['labels'][t][0]:<11}" for t in INIT_TYPES)
        log(f"  {param} = {f['value']:<8.4f} {cells}")
    for init_type in varying_starts(results):
        log(f"note: the {init_type} starting row changes with {param}; the factory's init depends on it")

    save_gif([compose_frame(f, param, start, stop, scale) for f in results], out, duration, hold, bounce)
    log(f"Saved {out} ({out.stat().st_size / 1e6:.1f} MB)")
    return out
