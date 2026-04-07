# Release Readiness Command Center

`Release Readiness Command Center` is a systems engineering portfolio repository focused on publication and release discipline. It tracks which repositories are actually presentation-ready, which blockers remain, and which release gates are green.

This repo is useful when you want your portfolio to show not only technical work, but also controlled delivery.

## What This Repo Demonstrates

- release-governance thinking
- blocker tracking across repositories
- CI, licensing, documentation, and demo readiness
- structured reviewer-facing reporting

## Repository Map

```text
.
|-- data/                             # Structured release readiness records
|-- docs/                             # Build plan and release notes
|-- reports/                          # Generated summaries and dashboards
|-- src/release_readiness_center/     # Validation, analysis, export, and CLI logic
|-- tests/                            # Regression tests
|-- .github/workflows/                # CI pipeline
|-- Makefile                          # Common commands
`-- README.md
```

## Quick Start

```bash
make test
make build-center
```

Or run the CLI directly:

```bash
PYTHONPATH=src python3 -m release_readiness_center.cli build --data-file data/releases.json --export-dir reports
```

## Generated Outputs

- `reports/release-summary.md`
- `reports/repo-readiness.csv`
- `reports/blocker-register.csv`
- `reports/release-dashboard.html`

## Documentation

- [docs/README.md](docs/README.md)
- [docs/project_plan.md](docs/project_plan.md)
- [docs/release_notes.md](docs/release_notes.md)

## Why This Matters For A Recruiter

This repo shows maturity around shipping and presentation. It demonstrates that the portfolio is not just technically interesting, but also organized, publishable, and review-ready.
