"""History Tube command line — drive Vitória (the Showrunner) from a terminal.

Examples:
  python cli.py demo                     # build + run the sample episode end-to-end (mock)
  python cli.py init rome --title "..." --angle "..."
  python cli.py run rome                 # step through; pauses at each gate for Fabio
  python cli.py approve rome             # approve the pending gate
  python cli.py run rome --auto          # walk every gate automatically (dry-run)
  python cli.py status rome
  python cli.py crew
"""

from __future__ import annotations

import argparse
import sys

from adapters._mock_content import SAMPLE_ANGLE, SAMPLE_SLUG, SAMPLE_TITLE, SAMPLE_TOPIC
from agents.crew import CREW, FUNCTION
from core.config import load_config
from orchestrator.showrunner import WAITING_GATE, Showrunner


def _force_utf8_output() -> None:
    """Make stdout/stderr UTF-8 so the crew's glyphs (✓, •, ⏸) never crash a run.

    No-op where streams are already UTF-8 (macOS/Linux) or non-reconfigurable
    (e.g. a StringIO under test). Windows' default console codepage (cp1252)
    cannot encode these characters, which would otherwise abort every command.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def _showrunner() -> Showrunner:
    return Showrunner(load_config())


def _print_step(r) -> None:
    if r.ran:
        for summary in r.ran:
            agent = summary.get("agent", "?")
            extras = ", ".join(f"{k}={v}" for k, v in summary.items() if k != "agent")
            print(f"    · {agent}: {extras}")
    if r.action == WAITING_GATE:
        print(f"  ⏸  {r.from_status}  →  awaiting {r.gate}")
    elif r.to_status is not None:
        tag = f" (auto-approved {r.gate})" if r.gate else ""
        print(f"  ✓  {r.from_status}  →  {r.to_status}{tag}")
    else:
        print(f"  •  {r.from_status}: {r.message}")


def cmd_crew(_args) -> int:
    print("David's crew\n")
    for key, name in CREW.items():
        print(f"  {name:<10}  {FUNCTION[key]}")
    return 0


def cmd_init(args) -> int:
    sr = _showrunner()
    ep = sr.create_episode(
        args.slug, title=args.title or "", topic=args.topic or "",
        angle=args.angle or "", target_length_min=args.length,
    )
    print(f"Created '{ep.slug}' — {ep.title} [{ep.status}]")
    return 0


def cmd_list(_args) -> int:
    sr = _showrunner()
    eps = sr.list()
    if not eps:
        print("No episodes yet. Try: python cli.py demo")
        return 0
    for ep in eps:
        gate = f"  (waiting: {ep.pending_gate})" if ep.pending_gate else ""
        print(f"  {ep.slug:<26} {str(ep.status):<18} {ep.title}{gate}")
    return 0


def cmd_status(args) -> int:
    sr = _showrunner()
    ep = sr.get(args.slug)
    print(f"{ep.title}  [{ep.slug}]")
    print(f"  status     : {ep.status}")
    if ep.pending_gate:
        print(f"  waiting on : {ep.pending_gate}")
    print(f"  angle      : {ep.angle}")
    print(f"  artifacts  : {len(ep.artifacts)}")
    for k, v in ep.artifacts.items():
        print(f"      - {k}: {v}")
    print(f"  assets     : {len(ep.assets)}")
    return 0


def cmd_step(args) -> int:
    sr = _showrunner()
    r = sr.step(args.slug, auto_approve=args.auto)
    _print_step(r)
    return 0


def cmd_run(args) -> int:
    sr = _showrunner()
    print(f"Running '{args.slug}' (auto={args.auto})")
    results = sr.run(args.slug, auto_approve=args.auto, with_shorts=not args.no_shorts)
    for r in results:
        _print_step(r)
    ep = sr.get(args.slug)
    print(f"\nNow: {ep.status}" + (f"  (waiting: {ep.pending_gate})" if ep.pending_gate else ""))
    return 0


def cmd_approve(args) -> int:
    sr = _showrunner()
    r = sr.approve(args.slug, args.gate)
    _print_step(r)
    return 0


def cmd_publish(args) -> int:
    sr = _showrunner()
    r = sr.publish(args.slug)
    _print_step(r)
    return 0


def cmd_shorts(args) -> int:
    sr = _showrunner()
    summary = sr.spin_off_shorts(args.slug)
    print(f"  · {summary.get('agent')}: shorts={summary.get('shorts')}")
    return 0


def cmd_demo(args) -> int:
    sr = _showrunner()
    if not sr.store.exists(SAMPLE_SLUG):
        sr.create_episode(SAMPLE_SLUG, title=SAMPLE_TITLE, topic=SAMPLE_TOPIC, angle=SAMPLE_ANGLE)
    print(f"Demo: walking '{SAMPLE_TITLE}' end-to-end (mock, auto-approve)\n")
    for r in sr.run(SAMPLE_SLUG, auto_approve=True, with_shorts=True):
        _print_step(r)
    ep = sr.get(SAMPLE_SLUG)
    print(f"\nFinished: {ep.status} — {len(ep.artifacts)} artifacts, {len(ep.assets)} assets.")
    print(f"Look under: episodes/{SAMPLE_SLUG}/")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="history-tube", description="History Tube production pipeline.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("crew", help="Show David's crew.").set_defaults(func=cmd_crew)
    sub.add_parser("demo", help="Build + run the sample episode end-to-end.").set_defaults(func=cmd_demo)
    sub.add_parser("list", help="List episodes.").set_defaults(func=cmd_list)

    pi = sub.add_parser("init", help="Create a new episode.")
    pi.add_argument("slug")
    pi.add_argument("--title", default="")
    pi.add_argument("--topic", default="")
    pi.add_argument("--angle", default="")
    pi.add_argument("--length", type=int, default=12)
    pi.set_defaults(func=cmd_init)

    ps = sub.add_parser("status", help="Show one episode.")
    ps.add_argument("slug")
    ps.set_defaults(func=cmd_status)

    pst = sub.add_parser("step", help="Advance one phase.")
    pst.add_argument("slug")
    pst.add_argument("--auto", action="store_true", help="Auto-approve a gate hit this step.")
    pst.set_defaults(func=cmd_step)

    pr = sub.add_parser("run", help="Step until a gate (or terminal).")
    pr.add_argument("slug")
    pr.add_argument("--auto", action="store_true", help="Auto-approve every gate (dry-run).")
    pr.add_argument("--no-shorts", action="store_true", help="Skip the Phase 9 Shorts spin-off.")
    pr.set_defaults(func=cmd_run)

    pa = sub.add_parser("approve", help="Approve the pending gate.")
    pa.add_argument("slug")
    pa.add_argument("gate", nargs="?", default=None)
    pa.set_defaults(func=cmd_approve)

    pp = sub.add_parser("publish", help="Publish a Scheduled episode (Fabio's action).")
    pp.add_argument("slug")
    pp.set_defaults(func=cmd_publish)

    psh = sub.add_parser("shorts", help="Spin off Shorts from a finished episode.")
    psh.add_argument("slug")
    psh.set_defaults(func=cmd_shorts)

    return p


def main(argv: list[str] | None = None) -> int:
    _force_utf8_output()
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # surface a clean message, non-zero exit
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
