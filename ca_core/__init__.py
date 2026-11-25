"""Shared engine and quality gate for the cellular automata pipeline.

    python -m ca_core run generations/loop_26          # simulate, render, triage
    python -m ca_core run generations/loop_26 --rules 3,7
    python -m ca_core triage generations                # score existing images of every loop
    python -m ca_core sweep hall_of_fame/generate_ca.py:directed_percolation --start 0.55 --stop 0.75

A loop's generate_ca.py only declares RULES; see ca_core/template_generate_ca.py.
"""
from .engine import INIT_TYPES, Rule, RuleError, render, run_loop, simulate
from .triage import analyze, classify, triage_loop
from .sweep import make_sweep_gif

__all__ = [
    "INIT_TYPES", "Rule", "RuleError", "analyze", "classify", "make_sweep_gif", "render", "run_loop", "simulate",
    "triage_loop",
]
