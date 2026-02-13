import os
from pathlib import Path

from playwright.sync_api import sync_playwright

from collectors.core.cli_utils import get_project_root, load_dotenv

def main() -> int:
    project_root = get_project_root()
    load_dotenv(project_root / ".env")

    out_path = Path(
        os.getenv(
            "ROCKETPUNCH_STORAGE_STATE",
            project_root / "fixtures" / "auth" / "rocketpunch.json",
        )
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.rocketpunch.com/login", wait_until="domcontentloaded")
        print("로켓펀치 로그인 완료 후 Enter를 누르세요.")
        input()
        context.storage_state(path=str(out_path))
        browser.close()

    print(f"OK storage_state={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
