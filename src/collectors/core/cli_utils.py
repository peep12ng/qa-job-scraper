from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

def parse_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

def read_url_from_file(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        return line
    return ""

def serialize_value(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

def serialize_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{k: serialize_value(v) for k, v in item.items()} for item in items]
