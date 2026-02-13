import os
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

from collectors.core.cli_utils import get_project_root, load_dotenv, parse_bool, read_url_from_file
from collectors.core.playwright_client import PlaywrightConfig

def _fetch_html(url: str, config: PlaywrightConfig, storage_state: str | None, wait_selector: str | None, wait_ms: int):
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
        if storage_state:
            context_kwargs["storage_state"] = storage_state

        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        page.set_default_timeout(config.timeout_ms)

        try:
            page.goto(url, wait_until="domcontentloaded")
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=config.timeout_ms)
                except PlaywrightTimeoutError:
                    pass
            if wait_ms > 0:
                page.wait_for_timeout(wait_ms)

            title = page.title()
            html = page.content()
            return title, html
        finally:
            page.close()
            context.close()
            browser.close()

def main() -> int:
    project_root = get_project_root()
    load_dotenv(project_root / ".env")

    url_file = project_root / "fixtures" / "urls" / "rocketpunch.txt"
    url = sys.argv[1] if len(sys.argv) >= 2 else read_url_from_file(url_file)

    if not url:
        print("Usage: python src/collectors/sources/rocketpunch/disc.py <url> [output_path]")
        print(f"Or put URL into: {url_file}")
        return 2

    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = project_root / "fixtures" / "html"
        out_path = out_dir / f"rocketpunch-list-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"

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

    storage_state = os.getenv("ROCKETPUNCH_STORAGE_STATE")
    wait_selector = os.getenv("ROCKETPUNCH_WAIT_SELECTOR")
    wait_ms = int(os.getenv("ROCKETPUNCH_WAIT_MS", "3000"))

    title, html = _fetch_html(url, config, storage_state, wait_selector, wait_ms)

    out_path.write_text(html, encoding="utf-8")

    if "로그인 후 검색 가능" in html:
        print(f"ERROR: login required. Set ROCKETPUNCH_STORAGE_STATE then retry. out={out_path}")
        return 3

    print(f"OK url={url} title={title} bytes={len(html)} out={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
