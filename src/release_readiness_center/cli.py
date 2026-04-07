"""CLI for the release readiness command center."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analysis import analyze_releases
from .data import load_releases
from .export import export_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="release-readiness-center",
        description="Validate and export release readiness artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser_cmd = subparsers.add_parser("build", help="Analyze release readiness records and export reports.")
    build_parser_cmd.add_argument("--data-file", default="data/releases.json", help="Path to the readiness JSON file.")
    build_parser_cmd.add_argument("--export-dir", help="Directory where reports should be written.")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "build":
        result = analyze_releases(load_releases(Path(args.data_file)))
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("Release readiness summary")
    print(f"  Repositories: {summary['repo_count']}")
    print(f"  Ready: {summary['ready_count']}")
    print(f"  Blocked: {summary['blocked_count']}")
    print(f"  Blockers: {summary['blocker_count']}")
    print(f"  Release gates: {summary['release_gate_count']}")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for item in result.errors:
            print(f"  - {item}")
    if result.warnings:
        print("Validation warnings:")
        for item in result.warnings:
            print(f"  - {item}")


if __name__ == "__main__":
    raise SystemExit(run())
