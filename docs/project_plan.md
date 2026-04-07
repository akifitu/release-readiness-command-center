# Step-By-Step Plan

## Phase 1: Define readiness criteria

1. Decide which gates matter for publication.
2. Choose how blockers should be captured.
3. Define what counts as release-ready.

## Phase 2: Build the source dataset

1. Store one readiness record per repository.
2. Capture release gate, CI, docs, demo, and licensing status.
3. Record blockers explicitly.

## Phase 3: Implement the command center

1. Validate allowed statuses.
2. Roll up ready, needs-work, and blocked repositories.
3. Export repo-level and blocker-level reports.

## Phase 4: Debug and verify

1. Add tests for invalid CI states and missing blocker lists.
2. Verify summary counts match the dataset.
3. Fix report gaps until the repo builds cleanly.

## Phase 5: Publish professionally

1. Write recruiter-facing docs.
2. Commit generated artifacts.
3. Push publicly and keep CI green.

## To-Do

- [x] define the release-readiness schema
- [x] build a realistic portfolio readiness dataset
- [x] implement validation and exporter logic
- [x] add regression tests
- [x] publish the repository
