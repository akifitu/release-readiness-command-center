"""Regression tests for the release readiness command center."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from release_readiness_center.analysis import analyze_releases
from release_readiness_center.cli import run
from release_readiness_center.data import load_releases


DATA_FILE = ROOT / "data" / "releases.json"


class ReleaseReadinessTests(unittest.TestCase):
    def test_clean_dataset_passes(self) -> None:
        result = analyze_releases(load_releases(DATA_FILE))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["repo_count"], 6)

    def test_invalid_ci_status_is_detected(self) -> None:
        records = load_releases(DATA_FILE)
        records[0]["ci_status"] = "blue"
        result = analyze_releases(records)
        self.assertTrue(any("invalid ci_status" in item for item in result.errors))

    def test_cli_exports_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(["build", "--data-file", str(DATA_FILE), "--export-dir", temp_dir])
            self.assertEqual(exit_code, 0)
            export_dir = Path(temp_dir)
            self.assertTrue((export_dir / "release-summary.md").exists())
            self.assertTrue((export_dir / "repo-readiness.csv").exists())
            self.assertTrue((export_dir / "blocker-register.csv").exists())
            self.assertTrue((export_dir / "release-dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
