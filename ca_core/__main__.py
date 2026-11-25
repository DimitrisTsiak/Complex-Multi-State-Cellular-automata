"""Command line: ``python -m ca_core run|triage|sweep ...`` (from the repository root)."""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from .engine import DEFAULT_SEED, DEFAULT_STEPS, DEFAULT_WIDTH, INIT_TYPES, RuleError, run_loop
from .triage import TRIAGE_MD, find_loop_dirs, gate_line, triage_loop


def _print_report(report: dict) -> None:
    for r in report["rules"]:
        cells = "  |  ".join(
            f"{t}: {r['images'][t]['verdict']} {r['images'][t]['label']} ({r['images'][t]['note']})"
            for t in INIT_TYPES
        )
        print(f"  {r['rule']:02d} {r['gate']:<6} {r['name'][:40]:<40}  {cells}")


def _parse_rules(text: str) -> list:
    try:
        return [int(x) for x in text.replace(" ", "").split(",") if x]
    except ValueError:
        raise SystemExit(f"--rules expects comma-separated numbers like 3,7; got {text!r}") from None


def cmd_run(args) -> int:
    loop_dir = args.loop_dir
    try:
        manifest = run_loop(
            loop_dir, args.width, args.steps, args.seed, only=_parse_rules(args.rules) if args.rules else None
        )
    except RuleError as exc:
        print(f"ERROR: {exc}")
        return 1
    errors = [k for k, v in manifest["rules"].items() if v.get("errors")]
    if not args.no_triage:
        report = triage_loop(loop_dir)
        print(f"\nTriage ({loop_dir / TRIAGE_MD}):")
        _print_report(report)
        print(f"\nGATE: {gate_line(report)}")
    if errors:
        print("\nRules with errors (this run or an earlier one, see manifest.json): "
              + ", ".join(f"{int(k):02d}" for k in errors))
        return 1
    return 0


def cmd_triage(args) -> int:
    loops = [d for p in args.paths for d in find_loop_dirs(p)]
    if not loops:
        print("no loop folders found")
        return 1
    totals, images = Counter(), Counter()
    for loop_dir in loops:
        report = triage_loop(loop_dir, write=not args.no_write)
        totals.update(r["gate"] for r in report["rules"])
        images.update(img["label"] for r in report["rules"] for img in r["images"].values())
        print(f"{loop_dir.name}: {gate_line(report)}")
        if len(loops) == 1 or args.verbose:
            _print_report(report)
    if len(loops) > 1:
        print(f"\nAll {len(loops)} loops, rules: " + ", ".join(f"{k} {v}" for k, v in totals.most_common()))
        print("Images: " + ", ".join(f"{k} {v}" for k, v in images.most_common()))
    return 0


def cmd_sweep(args) -> int:
    from .sweep import load_factory, make_sweep_gif

    try:
        make_sweep_gif(
            load_factory(args.factory), args.start, args.stop, args.frames, args.out, args.param,
            args.width, args.steps, args.seed, args.scale, args.duration, args.hold, args.bounce,
        )
    except RuleError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(prog="python -m ca_core", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="simulate a loop's RULES, render the PNGs, then triage them")
    run.add_argument("loop_dir", type=Path, help="e.g. generations/loop_26")
    run.add_argument("--rules", help="only re-run these rule numbers, e.g. 3,7")
    run.add_argument("--width", type=int, default=DEFAULT_WIDTH, help=f"cells per row (default {DEFAULT_WIDTH})")
    run.add_argument("--steps", type=int, default=DEFAULT_STEPS, help=f"rows per image (default {DEFAULT_STEPS})")
    run.add_argument("--seed", type=int, default=DEFAULT_SEED, help="base seed; per-image seeds derive from it")
    run.add_argument("--no-triage", action="store_true", help="skip the quality gate")
    run.set_defaults(func=cmd_run)

    tri = sub.add_parser("triage", help="score existing images and write triage.md / triage.json")
    tri.add_argument("paths", nargs="+", type=Path, help="loop folders, or a folder that contains loop_* folders")
    tri.add_argument("--no-write", action="store_true", help="print only; don't write triage files")
    tri.add_argument("-v", "--verbose", action="store_true", help="per-rule detail when scoring several loops")
    tri.set_defaults(func=cmd_triage)

    swp = sub.add_parser("sweep", help="GIF of one rule as a float parameter varies (single seed | random)")
    swp.add_argument("factory", help="path/to/file.py:function that takes the parameter and returns a Rule")
    swp.add_argument("--param", help="parameter to sweep (default: the function's only parameter)")
    swp.add_argument("--start", type=float, required=True, help="first parameter value")
    swp.add_argument("--stop", type=float, required=True, help="last parameter value")
    swp.add_argument("--frames", type=int, default=41, help="number of values, evenly spaced (default 41)")
    swp.add_argument("--width", type=int, default=DEFAULT_WIDTH, help=f"cells per row (default {DEFAULT_WIDTH})")
    swp.add_argument("--steps", type=int, default=DEFAULT_STEPS, help=f"rows per image (default {DEFAULT_STEPS})")
    swp.add_argument("--seed", type=int, default=DEFAULT_SEED, help="seed shared by every frame")
    swp.add_argument("--scale", type=float, default=0.5, help="panel size relative to width x steps (default 0.5)")
    swp.add_argument("--duration", type=int, default=150, help="milliseconds per frame (default 150)")
    swp.add_argument("--hold", type=int, default=1200, help="milliseconds on the first and last frame (default 1200)")
    swp.add_argument("--bounce", action="store_true", help="play forward, then backward")
    swp.add_argument("--out", type=Path, help="output GIF (default sweeps/<function>_<param>.gif)")
    swp.set_defaults(func=cmd_sweep)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
