from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from playwright.sync_api import Browser, Playwright, TimeoutError as PlaywrightTimeoutError, sync_playwright

@dataclass
class PlaywrightConfig:
    browser: str = "chromium"
    headless: bool = True
    timeout_ms: int = 30000
    user_agent: Optional[str] = None
    locale: str = "ko-KR"
    timezone_id: str = "Asia/Seoul"
    extra_http_headers: Optional[Dict[str, str]] = None

class PlaywrightClient:
    def __init__(self, config: PlaywrightConfig):
        self.config = config
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.close()
    
    def start(self) -> None:
        if self._playwright is not None:
            return
        self._playwright = sync_playwright().start()
        browser_type = getattr(self._playwright, self.config.browser, None)
        if browser_type is None:
            self.close()
            raise ValueError(f"Unsupported browser: {self.config.browser}")
        self._browser = browser_type.launch(headless=self.config.headless)
    
    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._browser = None
        self._playwright = None
    
    def fetch(self, url: str) -> Tuple[str, str]:
        self.start()
        assert self._browser is not None

        context_kwargs = {
            "locale": self.config.locale,
            "timezone_id": self.config.timezone_id,
        }
        if self.config.user_agent:
            context_kwargs["user_agent"] = self.config.user_agent
        if self.config.extra_http_headers:
            context_kwargs["extra_http_headers"] = self.config.extra_http_headers

        context = self._browser.new_context(**context_kwargs)
        page = context.new_page()
        page.set_default_timeout(self.config.timeout_ms)

        try:
            try:
                page.goto(url, wait_until="domcontentloaded")
            except PlaywrightTimeoutError:
                page.goto(url, wait_until="commit")
            title = page.title()
            html = page.content()
            return title, html
        finally:
            page.close()
            context.close()
