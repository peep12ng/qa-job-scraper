from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

_TIMESTAMP_RE = re.compile(r"^(?P<source>.+)-items-(?P<ts>\d{8}-\d{6})\.json$")

def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]

def _parse_timestamp(name: str) -> Optional[datetime]:
    match = _TIMESTAMP_RE.match(name)
    if not match:
        return None
    ts = match.group("ts")
    try:
        return datetime.strptime(ts, "%Y%m%d-%H%M%S")
    except ValueError:
        return None

def find_latest_fixture(source_code: str, base_dir: Optional[Path] = None) -> Tuple[Optional[Path], Optional[str]]:
    root = base_dir or (_project_root() / "fixtures" / "json")
    if not root.exists():
        return None, f"fixture dir not found: {root}"

    candidates = list(root.glob(f"{source_code}-items-*.json"))
    if not candidates:
        return None, f"fixture not found for source: {source_code} in {root}"

    scored = []
    for path in candidates:
        ts = _parse_timestamp(path.name)
        if ts:
            scored.append((ts, path))
        else:
            scored.append((datetime.fromtimestamp(path.stat().st_mtime), path))

    scored.sort(key=lambda item: item[0])
    return scored[-1][1], None

def load_latest_fixture(
    source_code: str,
    base_dir: Optional[Path] = None,
) -> Tuple[Optional[Any], Optional[str], Optional[str]]:
    path, error = find_latest_fixture(source_code, base_dir=base_dir)
    if error:
        return None, None, error

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, str(path), f"invalid json: {exc}"

    return payload, str(path), None
