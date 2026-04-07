"""Analysis helpers for release readiness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


VALID_OVERALL = {"ready", "needs_work", "blocked"}
VALID_GATE_STATUS = {"ready", "needs_work", "blocked", "in_progress", "planned"}
VALID_CI = {"green", "yellow", "red"}
REQUIRED_FIELDS = {
    "repo_name",
    "title",
    "release_gate",
    "overall_status",
    "ci_status",
    "docs_status",
    "demo_status",
    "license_status",
    "automation_status",
    "blockers",
}


@dataclass
class ReadinessResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    repo_rows: List[Dict[str, str]]
    blocker_rows: List[Dict[str, str]]


def analyze_releases(records: Sequence[Mapping[str, Any]]) -> ReadinessResult:
    """Validate release readiness records and build export rows."""
    errors: List[str] = []
    warnings: List[str] = []
    _check_duplicate_repos(records, errors)

    repo_rows: List[Dict[str, str]] = []
    blocker_rows: List[Dict[str, str]] = []

    for record in records:
        if not _validate_record(record, errors):
            continue
        blocker_count = len(record["blockers"])
        repo_rows.append(
            {
                "repo_name": record["repo_name"],
                "title": record["title"],
                "release_gate": record["release_gate"],
                "overall_status": record["overall_status"],
                "ci_status": record["ci_status"],
                "docs_status": record["docs_status"],
                "demo_status": record["demo_status"],
                "license_status": record["license_status"],
                "automation_status": record["automation_status"],
                "blocker_count": str(blocker_count),
            }
        )
        for blocker in record["blockers"]:
            blocker_rows.append(
                {
                    "repo_name": record["repo_name"],
                    "release_gate": record["release_gate"],
                    "overall_status": record["overall_status"],
                    "blocker": blocker,
                }
            )
        if record["overall_status"] == "blocked" and record["ci_status"] == "green":
            warnings.append(f"{record['repo_name']}: release is blocked even though CI is green.")

    summary = {
        "repo_count": len(repo_rows),
        "ready_count": sum(1 for row in repo_rows if row["overall_status"] == "ready"),
        "blocked_count": sum(1 for row in repo_rows if row["overall_status"] == "blocked"),
        "blocker_count": len(blocker_rows),
        "release_gate_count": len({row["release_gate"] for row in repo_rows}),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    return ReadinessResult(errors, warnings, summary, repo_rows, blocker_rows)


def _check_duplicate_repos(records: Sequence[Mapping[str, Any]], errors: List[str]) -> None:
    seen = set()
    for record in records:
        repo_name = record.get("repo_name")
        if repo_name in seen:
            errors.append(f"duplicate repo_name '{repo_name}' detected.")
        seen.add(repo_name)


def _validate_record(record: Mapping[str, Any], errors: List[str]) -> bool:
    repo_name = str(record.get("repo_name", "<missing-repo>"))
    missing = sorted(field for field in REQUIRED_FIELDS if record.get(field) in ("", None))
    if missing:
        errors.append(f"{repo_name}: missing required fields: {', '.join(missing)}.")
        return False
    if record["overall_status"] not in VALID_OVERALL:
        errors.append(f"{repo_name}: invalid overall_status '{record['overall_status']}'.")
    if record["ci_status"] not in VALID_CI:
        errors.append(f"{repo_name}: invalid ci_status '{record['ci_status']}'.")
    for field in ("docs_status", "demo_status", "license_status", "automation_status"):
        if record[field] not in VALID_GATE_STATUS:
            errors.append(f"{repo_name}: invalid {field} '{record[field]}'.")
    if not isinstance(record["blockers"], list):
        errors.append(f"{repo_name}: blockers must be a list.")
    return True
