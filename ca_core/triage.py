"""Automatic quality gate for space-time diagrams.

Scores every ``output/rule_XX_<init>.png`` of a loop and labels it:

dead         the last rows are a single colour
frozen       the last rows no longer change
periodic     the last rows repeat with a short period (up to MAX_PERIOD rows)
translating  a rigid pattern sliding sideways with a short period
near-static  aperiodic, but fewer than ~4 cells in 800 change per row (a lone front or glider)
noise        aperiodic but about as compressible as shuffled noise
dynamic      aperiodic and structured

and gives each image a verdict:

FAIL  dead or frozen before the halfway row: most of the image is trivial
WARN  periodic, translating, near-static, noise-like, or dead/frozen only after the halfway row
PASS  dynamic

A rule's gate is REWORK when none of its images PASS or WARN, REVIEW when its best
image is a WARN, and PASS otherwise. Works from the PNGs alone, so it also scores
loops written before the shared engine existed.
"""
from __future__ import annotations

import json
import re
import zlib
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

from .engine import INIT_TYPES, IMAGE_RE, read_manifest

TAIL_ROWS = 200  # rows at the bottom used for the state statistics
PERIOD_WINDOW = 100  # rows that must repeat exactly to count as periodic
MAX_PERIOD = 64
SETTLE_FAIL_FRACTION = 0.5  # dead/frozen before this fraction of the rows -> FAIL
NOISE_THRESHOLD = 0.9  # compressed size / compressed size of the shuffled tail
NEAR_STATIC_ACTIVITY = 0.005  # share of cells changing per row below which a run is near-static

VERDICT_RANK = {"PASS": 0, "WARN": 1, "FAIL": 2, "ERROR": 3}
TRIAGE_MD = "triage.md"
TRIAGE_JSON = "triage.json"


# ---------------------------------------------------------------- metrics

def grid_from_image(path: Path) -> np.ndarray:
    """Decode a rendered diagram back to integer state ids (one id per distinct colour)."""
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.uint32)
    keys = (rgb[..., 0] << 16) | (rgb[..., 1] << 8) | rgb[..., 2]
    _, ids = np.unique(keys, return_inverse=True)
    return ids.reshape(keys.shape).astype(np.int32)


def find_period(grid: np.ndarray) -> Optional[tuple]:
    """Smallest (period, shift) such that the last PERIOD_WINDOW rows satisfy
    row[t] == roll(row[t - period], shift). None if the tail is aperiodic."""
    rows, width = grid.shape
    window = min(PERIOD_WINDOW, rows // 2)
    last = grid[-1]
    last_counts = np.bincount(last, minlength=int(grid.max()) + 1)
    roll_index = None
    for period in range(1, MAX_PERIOD + 1):
        if window + period > rows:
            break
        earlier = grid[-1 - period]
        if np.array_equal(earlier, last):
            candidates = [0]
        elif np.array_equal(np.bincount(earlier, minlength=last_counts.size), last_counts):
            if roll_index is None:
                roll_index = (np.arange(width)[None, :] - np.arange(width)[:, None]) % width
            candidates = np.flatnonzero((earlier[roll_index] == last).all(axis=1)).tolist()
            candidates.sort(key=lambda s: min(s, width - s))
        else:
            continue
        for shift in candidates:
            if np.array_equal(np.roll(grid[-window - period:-period], shift, axis=1), grid[-window:]):
                return period, (shift if shift <= width // 2 else shift - width)
    return None


def settle_row(grid: np.ndarray, period: int, shift: int) -> int:
    """First row from which the (period, shift) regularity holds to the end."""
    mismatch = (grid[period:] != np.roll(grid[:-period], shift, axis=1)).any(axis=1)
    changed = np.flatnonzero(mismatch)
    return 0 if changed.size == 0 else int(changed[-1]) + 1


def normalized_compression(tail: np.ndarray) -> float:
    """zlib size of the tail divided by that of the same cells shuffled.
    ~1.0 means indistinguishable from noise with the same colour histogram."""
    data = tail.astype(np.uint8 if tail.max() < 256 else np.uint16)
    shuffled = np.random.default_rng(0).permutation(data.ravel())
    structured = len(zlib.compress(data.tobytes(), 6))
    baseline = len(zlib.compress(shuffled.tobytes(), 6))
    return structured / baseline if baseline else 0.0


def analyze(grid: np.ndarray) -> dict:
    rows, width = grid.shape
    tail = grid[-min(TAIL_ROWS, rows):]
    _, counts = np.unique(tail, return_counts=True)
    probs = counts / counts.sum()
    metrics = {
        "rows": rows,
        "width": width,
        "tail_states": int(counts.size),
        "entropy_bits": round(float(-(probs * np.log2(probs)).sum()), 3),
        "activity": round(float((tail[1:] != tail[:-1]).mean()), 4) if len(tail) > 1 else 0.0,
        "compression": round(normalized_compression(tail), 3),
        "period": None,
        "shift": None,
        "settle_row": None,
    }
    found = find_period(grid)
    if found:
        period, shift = found
        metrics.update(period=period, shift=shift, settle_row=settle_row(grid, period, shift))
    return metrics


def classify(m: dict) -> tuple:
    """(label, verdict, note) for one image's metrics."""
    rows = m["rows"]
    if m["period"] is not None:
        period, shift, start = m["period"], m["shift"], m["settle_row"]
        early = start < SETTLE_FAIL_FRACTION * rows
        when = f"from row {start}/{rows}"
        if m["tail_states"] == 1:
            return "dead", "FAIL" if early else "WARN", f"single colour {when}"
        if period == 1 and shift == 0:
            return "frozen", "FAIL" if early else "WARN", f"static {when}"
        if shift == 0:
            return "periodic", "WARN", f"repeats every {period} rows {when}"
        return "translating", "WARN", f"rigid pattern moving {shift:+d} cells per {period} rows {when}"
    if m["activity"] < NEAR_STATIC_ACTIVITY:
        return "near-static", "WARN", f"only ~{m['activity'] * m['width']:.1f} cells change per row"
    if m["compression"] >= NOISE_THRESHOLD:
        return "noise", "WARN", f"close to random noise (compression {m['compression']:.2f})"
    return "dynamic", "PASS", "aperiodic and structured"


# ---------------------------------------------------------------- loop reports

def rule_names_from_markdown(path: Path) -> dict:
    """Best-effort {rule index: name} from '### Rule N: Name' headings."""
    names = {}
    if not path.is_file():
        return names
    heading = re.compile(r"^#{2,4}\s*(?:\d+\.\s*)?Rule\s*0*(\d+)\s*[:.\-–—]*\s*(.*)$")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = heading.match(line.strip())
        if match and int(match.group(1)) not in names:
            name = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", r"\1", match.group(2)).strip(" -:")
            names[int(match.group(1))] = name
    return names


def rule_gate(verdicts: list) -> str:
    best = min(VERDICT_RANK[v] for v in verdicts)
    return "PASS" if best == 0 else "REVIEW" if best == 1 else "REWORK"


def triage_loop(loop_dir: Path, write: bool = True) -> dict:
    """Score every image of a loop; optionally write triage.json and triage.md next to it."""
    loop_dir = Path(loop_dir)
    out_dir = loop_dir / "output"
    manifest = read_manifest(loop_dir) or {}
    from_manifest = manifest.get("rules", {})
    names = rule_names_from_markdown(loop_dir / "rules.md")

    found = {}
    for png in sorted(out_dir.glob("rule_*.png")) if out_dir.is_dir() else []:
        match = IMAGE_RE.match(png.name)
        if match:
            found[(int(match.group(1)), match.group(2))] = png
    indices = sorted({i for i, _ in found} | {int(k) for k in from_manifest})

    rules = []
    for index in indices:
        info = from_manifest.get(str(index), {})
        images = {}
        for init_type in INIT_TYPES:
            png = found.get((index, init_type))
            if png is None:
                error = info.get("errors", {}).get(init_type)
                note = (error[:157] + "...") if error and len(error) > 160 else error or "no image in output/"
                label = "crashed" if error else "missing"
                images[init_type] = {"file": None, "label": label, "verdict": "ERROR", "note": note}
                continue
            metrics = analyze(grid_from_image(png))
            label, verdict, note = classify(metrics)
            images[init_type] = {
                "file": f"output/{png.name}", "label": label, "verdict": verdict, "note": note, "metrics": metrics,
            }
        rules.append({
            "rule": index,
            "name": info.get("name") or names.get(index, ""),
            "gate": rule_gate([img["verdict"] for img in images.values()]),
            "images": images,
        })

    report = {
        "loop": loop_dir.resolve().name,
        "rules": rules,
        "rework": [r["rule"] for r in rules if r["gate"] == "REWORK"],
    }
    if write:
        (loop_dir / TRIAGE_JSON).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        (loop_dir / TRIAGE_MD).write_text(to_markdown(report), encoding="utf-8")
    return report


def gate_line(report: dict) -> str:
    rules = report["rules"]
    counts = {g: sum(r["gate"] == g for r in rules) for g in ("PASS", "REVIEW", "REWORK")}
    line = f"{counts['PASS']} pass, {counts['REVIEW']} need review, {counts['REWORK']} need rework"
    if report["rework"]:
        line += " (rules " + ", ".join(f"{i:02d}" for i in report["rework"]) + ")"
    return line


def _cell(image: dict) -> str:
    return f"{image['verdict']} {image['label']}: {image['note']}"


def to_markdown(report: dict) -> str:
    lines = [
        f"# Triage: {report['loop']}",
        "",
        "Automatic quality gate written by `python -m ca_core triage` from the images in `output/`. "
        "Re-run it after any change. It is a guide for the reviewer, not a verdict on beauty.",
        "",
        f"**Gate:** {gate_line(report)}",
        "",
        "| Rule | Name | " + " | ".join(INIT_TYPES) + " | Gate |",
        "|---|---|" + "---|" * len(INIT_TYPES) + "---|",
    ]
    for r in report["rules"]:
        cells = " | ".join(_cell(r["images"][t]) for t in INIT_TYPES)
        gate = f"**{r['gate']}**" if r["gate"] == "REWORK" else r["gate"]
        lines.append(f"| {r['rule']:02d} | {r['name']} | {cells} | {gate} |")
    lines += [
        "",
        "## Metrics",
        "",
        "Computed on the last rows of each image. Activity: share of cells that change per step. "
        "Compression: zlib size relative to the same cells shuffled (about 1.0 means noise-like). "
        "Settle row: first row of the final dead, frozen or periodic regime.",
        "",
        "| Image | Label | Activity | Compression | Entropy (bits) | Period | Shift | Settle row |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in report["rules"]:
        for init_type in INIT_TYPES:
            image = r["images"][init_type]
            m = image.get("metrics")
            if m is None:
                lines.append(f"| rule {r['rule']:02d} {init_type} | {image['label']} | | | | | | |")
                continue
            dash = lambda v: "" if v is None else v  # noqa: E731
            lines.append(
                f"| rule {r['rule']:02d} {init_type} | {image['label']} | {m['activity']} | {m['compression']} | "
                f"{m['entropy_bits']} | {dash(m['period'])} | {dash(m['shift'])} | {dash(m['settle_row'])} |"
            )
    lines += [
        "",
        "## Legend",
        "",
        "- **PASS**: aperiodic and structured to the end of the run.",
        "- **WARN**: periodic, translating, near-static, noise-like, or dead/frozen only after the halfway row. "
        "Can still be a winner; look at it.",
        "- **FAIL**: dead or frozen before the halfway row, so most of the image is trivial.",
        "- **ERROR**: the rule raised an exception or the image is missing.",
        "- Gate **REWORK**: no image of the rule is better than FAIL. **REVIEW**: best image is a WARN.",
        "",
    ]
    return "\n".join(lines)


def find_loop_dirs(path: Path) -> list:
    """A loop folder itself, or every loop_* folder inside ``path`` (sorted by number)."""
    path = Path(path)
    if (path / "output").is_dir() or (path / "generate_ca.py").is_file():
        return [path]
    loops = [p for p in path.glob("loop_*") if p.is_dir()]
    return sorted(loops, key=lambda p: int(re.sub(r"\D", "", p.name) or 0))
