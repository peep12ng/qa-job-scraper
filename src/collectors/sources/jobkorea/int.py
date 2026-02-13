import json
import os
import sys
from datetime import datetime
from pathlib import Path

from collectors.core.cli_utils import get_project_root, load_dotenv, parse_bool, read_url_from_file, serialize_items
from collectors.core.filters import apply_required_filters, get_required_filters
from collectors.core.playwright_client import PlaywrightClient, PlaywrightConfig
from collectors.core.registry import get_sources
from collectors.sources.jobkorea.parser import parse_jobkorea_list

def _get_jobkorea_base_url() -> str:
    for source in get_sources(active_only=False):
        if source.code == "jobkorea":
            return source.base_url
    return "https://www.jobkorea.co.kr"

def main() -> int:
    project_root = get_project_root()
    load_dotenv(project_root / ".env")

    url_file = project_root / "fixtures" / "urls" / "jobkorea.txt"
    url = sys.argv[1] if len(sys.argv) >= 2 else read_url_from_file(url_file)

    if not url:
        print("Usage: python src/collectors/sources/jobkorea/int.py <url> [output_path]")
        print(f"Or put URL into: {url_file}")
        return 2

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = project_root / "fixtures" / "json"
        out_path = out_dir / f"jobkorea-items-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    config = PlaywrightConfig(
        browser=os.getenv("PLAYWRIGHT_BROWSER", "chromium"),
        headless=parse_bool(os.getenv("PLAYWRIGHT_HEADLESS"), True),
        timeout_ms=int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "60000")),
    )

    with PlaywrightClient(config) as client:
        title, html = client.fetch(url)

    base_url = _get_jobkorea_base_url()
    items = parse_jobkorea_list(html, base_url=base_url)
    filtered = apply_required_filters(items, get_required_filters())

    payload = {
        "source_code": "jobkorea",
        "collected_at": datetime.now().isoformat(),
        "url": url,
        "title": title,
        "items_total": len(items),
        "items_filtered": len(filtered),
        "items": serialize_items(filtered),
    }

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK items={len(items)} filtered={len(filtered)} out={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
