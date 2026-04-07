"""Export release readiness outputs."""

from __future__ import annotations

from csv import DictWriter
from html import escape
from pathlib import Path
from typing import Iterable, Mapping

from .analysis import ReadinessResult


def export_reports(result: ReadinessResult, export_dir: Path | str) -> None:
    """Write report artifacts."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    _write_text(export_path / "release-summary.md", _render_summary_markdown(result))
    _write_csv(export_path / "repo-readiness.csv", result.repo_rows)
    _write_csv(export_path / "blocker-register.csv", result.blocker_rows)
    _write_text(export_path / "release-dashboard.html", _render_dashboard_html(result))


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def _render_summary_markdown(result: ReadinessResult) -> str:
    summary = result.summary
    repos = "\n".join(
        f"- {row['title']} ({row['repo_name']}) | status: {row['overall_status']} | blockers: {row['blocker_count']}"
        for row in result.repo_rows
    ) or "- None"
    errors = "\n".join(f"- {item}" for item in result.errors) or "- None"
    warnings = "\n".join(f"- {item}" for item in result.warnings) or "- None"
    return (
        "# Release Readiness Summary\n\n"
        f"- Repositories: {summary['repo_count']}\n"
        f"- Ready: {summary['ready_count']}\n"
        f"- Blocked: {summary['blocked_count']}\n"
        f"- Total blockers: {summary['blocker_count']}\n"
        f"- Release gates: {summary['release_gate_count']}\n"
        f"- Errors: {summary['error_count']}\n"
        f"- Warnings: {summary['warning_count']}\n\n"
        "## Repo Readiness\n\n"
        f"{repos}\n\n"
        "## Errors\n\n"
        f"{errors}\n\n"
        "## Warnings\n\n"
        f"{warnings}\n"
    )


def _render_dashboard_html(result: ReadinessResult) -> str:
    summary = result.summary
    cards = [
        ("Repositories", str(summary["repo_count"])),
        ("Ready", str(summary["ready_count"])),
        ("Blocked", str(summary["blocked_count"])),
        ("Blockers", str(summary["blocker_count"])),
    ]
    card_html = "\n".join(
        f"<article class=\"card\"><span>{escape(label)}</span><strong>{escape(value)}</strong></article>"
        for label, value in cards
    )
    repo_table = _render_table(
        result.repo_rows,
        ["repo_name", "release_gate", "overall_status", "ci_status", "blocker_count"],
        "No repositories available.",
    )
    blocker_table = _render_table(
        result.blocker_rows,
        ["repo_name", "release_gate", "overall_status", "blocker"],
        "No blockers available.",
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in (result.warnings or ["None"]))
    errors = "".join(f"<li>{escape(item)}</li>" for item in (result.errors or ["None"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Release Readiness Command Center</title>
  <style>
    :root {{
      --bg: #f6f2eb;
      --panel: rgba(255,255,255,0.9);
      --ink: #2f241e;
      --muted: #73675f;
      --accent: #c2410c;
      --line: rgba(47,36,30,0.12);
      --shadow: 0 18px 40px rgba(47, 36, 30, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background: linear-gradient(180deg, #faf6ef, #ede2d3);
    }}
    main {{
      width: min(1100px, calc(100% - 28px));
      margin: 0 auto;
      padding: 28px 0 54px;
    }}
    .hero, section, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      border-radius: 24px;
    }}
    .hero {{
      padding: 28px;
      background: linear-gradient(135deg, rgba(194,65,12,0.95), rgba(154,52,18,0.95));
      color: #fff8f3;
    }}
    h1, h2 {{
      margin: 0 0 12px;
      font-family: "Georgia", serif;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 18px 0;
    }}
    .card {{
      padding: 20px;
      min-height: 116px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card span {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.84rem;
      letter-spacing: 0.07em;
    }}
    .card strong {{
      color: var(--accent);
      font-size: 1.9rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }}
    section {{
      padding: 22px;
      overflow: hidden;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.8rem;
      letter-spacing: 0.06em;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>Release Readiness Command Center</h1>
      <p>Publication and release-governance hub for a multi-repository systems engineering portfolio.</p>
    </section>
    <div class="metrics">{card_html}</div>
    <div class="grid">
      <section>
        <h2>Repository Readiness</h2>
        {repo_table}
      </section>
      <section>
        <h2>Blocker Register</h2>
        {blocker_table}
      </section>
      <section>
        <h2>Warnings</h2>
        <ul>{warnings}</ul>
      </section>
      <section>
        <h2>Errors</h2>
        <ul>{errors}</ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def _render_table(rows: Iterable[Mapping[str, str]], columns: list[str], empty_message: str) -> str:
    row_list = list(rows)
    if not row_list:
        return f"<p>{escape(empty_message)}</p>"
    header_html = "".join(f"<th>{escape(column.replace('_', ' '))}</th>" for column in columns)
    body_html = []
    for row in row_list:
        body_html.append(
            "<tr>" + "".join(f"<td>{escape(str(row.get(column, '')))}</td>" for column in columns) + "</tr>"
        )
    return f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"
