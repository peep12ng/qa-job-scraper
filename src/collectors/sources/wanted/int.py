import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable, Tuple

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

from collectors.core.filters import apply_required_filters, get_required_filters
from collectors.core.playwright_client import PlaywrightConfig
from collectors.core.registry import get_sources
from .parser import parse_wanted_list

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
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        return line
    return ""

def _serialize_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

def _serialize_items(items: Iterable[Dict[str, object]]):
    return [{k: _serialize_value(v) for k, v in item.items()} for item in items]

def _get_wanted_base_url() -> str:
    for source in get_sources(active_only=False):
        if source.code == "wanted":
            return source.base_url
    return "https://www.wanted.co.kr"

def _fetch_wanted_json(list_url: str, config: PlaywrightConfig) -> Tuple[str, str, Dict]:
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, config.browser, None)
        if browser_type is None:
            raise ValueError(f"Unsupported browser: {config.browser}")

        browser = browser_type.launch(headless=config.headless)
        context_kwargs = {
            "locale": config.locale,
            "timezone_id": config.timezone_id,
        }
        if config.user_agent:
            context_kwargs["user_agent"] = config.user_agent
        if config.extra_http_headers:
            context_kwargs["extra_http_headers"] = config.extra_http_headers

        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        page.set_default_timeout(config.timeout_ms)

        def is_target_response(response) -> bool:
            return "/api/chaos/navigation/v1/results" in response.url and response.status == 200

        try:
            with page.expect_response(is_target_response) as resp_info:
                page.goto(list_url, wait_until="domcontentloaded")
            response = resp_info.value
            data = response.json()
            title = page.title()
            return title, response.url, data
        finally:
            page.close()
            context.close()
            browser.close()

def main() -> int:
    project_root = Path(__file__).resolve().parents[4]
    load_dotenv(project_root / ".env")

    url_file = project_root / "fixtures" / "urls" / "wanted.txt"
    list_url = sys.argv[1] if len(sys.argv) >= 2 else read_url_from_file(url_file)

    if not list_url:
        print("Usage: python src/collectors/sources/wanted/int.py <list_url> [output_path]")
        print(f"Or put URL into: {url_file}")
        return 2

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = project_root / "fixtures" / "json"
        out_path = out_dir / f"wanted-items-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    user_agent = os.getenv(
        "PLAYWRIGHT_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    )
    extra_headers = {
        "Accept-Language": os.getenv(
            "PLAYWRIGHT_ACCEPT_LANGUAGE",
            "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        ),
    }

    config = PlaywrightConfig(
        browser=os.getenv("PLAYWRIGHT_BROWSER", "chromium"),
        headless=parse_bool(os.getenv("PLAYWRIGHT_HEADLESS"), True),
        timeout_ms=int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "60000")),
        user_agent=user_agent,
        extra_http_headers=extra_headers,
    )

    try:
        title, api_url, data = _fetch_wanted_json(list_url, config)
    except PlaywrightTimeoutError:
        print("ERROR: timeout waiting for wanted api response. Increase PLAYWRIGHT_TIMEOUT_MS or check the list URL.")
        return 1

    base_url = _get_wanted_base_url()
    items = parse_wanted_list(data, base_url=base_url)
    filtered = apply_required_filters(items, get_required_filters())

    payload = {
        "source_code": "wanted",
        "collected_at": datetime.now().isoformat(),
        "url": list_url,
        "title": title,
        "api_url": api_url,
        "items_total": len(items),
        "items_filtered": len(filtered),
        "items": _serialize_items(filtered),
    }

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK items={len(items)} filtered={len(filtered)} api_url={api_url} out={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
