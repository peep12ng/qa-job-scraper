import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable

from collectors.core.filters import apply_required_filters, get_required_filters
from collectors.core.playwright_client import PlaywrightClient, PlaywrightConfig
from collectors.core.registry import get_sources
from collectors.sources.saramin.parser import parse_saramin_list

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

def parse_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

def read_url_from_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()

def _serialize_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

def _serialize_items(items: Iterable[Dict[str, object]]):
    return [{k: _serialize_value(v) for k, v in item.items()} for item in items]

def _get_saramin_base_url() -> str:
    for source in get_sources(active_only=False):
        if source.code == "saramin":
            return source.base_url
    return "https://www.saramin.co.kr"

def main() -> int:
    project_root = Path(__file__).resolve().parents[4]
    load_dotenv(project_root / ".env")

    url_file = project_root / "fixtures" / "urls" / "saramin.txt"
    url = sys.argv[1] if len(sys.argv) >= 2 else read_url_from_file(url_file)

    if not url:
        print("Usage: python src/collectors/sources/saramin/int.py <url> [output_path]")
        print(f"Or put URL into: {url_file}")
        return 2

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = project_root / "fixtures" / "json"
        out_path = out_dir / f"saramin-items-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    config = PlaywrightConfig(
        browser=os.getenv("PLAYWRIGHT_BROWSER", "chromium"),
        headless=parse_bool(os.getenv("PLAYWRIGHT_HEADLESS"), True),
        timeout_ms=int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "30000")),
    )

    with PlaywrightClient(config) as client:
        title, html = client.fetch(url)

    base_url = _get_saramin_base_url()
    items = parse_saramin_list(html, base_url=base_url)
    filtered = apply_required_filters(items, get_required_filters())

    payload = {
        "source_code": "saramin",
        "collected_at": datetime.now().isoformat(),
        "url": url,
        "title": title,
        "items_total": len(items),
        "items_filtered": len(filtered),
        "items": _serialize_items(filtered),
    }

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK items={len(items)} filtered={len(filtered)} out={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
