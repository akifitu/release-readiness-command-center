"""Load release readiness data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ReleaseRecord = Dict[str, Any]


def load_releases(data_file: Path | str) -> List[ReleaseRecord]:
    """Load release readiness data from JSON."""
    return json.loads(Path(data_file).read_text(encoding="utf-8"))
