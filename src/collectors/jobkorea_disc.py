import os
import sys
from datetime import datetime
from pathlib import Path

from collectors.playwright_client import PlaywrightClient, PlaywrightConfig

def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or "=" not in line:
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
        if not line or line.startswith('#'):
            continue
        return line
    return ""

def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    url_file = project_root / "fixtures" / "urls" / "jobkorea.txt"
    url = sys.argv[1] if len(sys.argv) >= 2 else read_url_from_file(url_file)

    if not url:
        print("Usage: python src/collectors/jobkorea_disc.py <url> [output_path]")
        print(f"Or put URL into: {url_file}")
        return 2
    
    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = project_root / "fixtures" / "html"
        out_path = out_dir / f"jobkorea-list-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    
    out_path.parent.mkdir(parents=True, exist_ok=True)

    config = PlaywrightConfig(
        browser=os.getenv("PLAYWRIGHT_BROWSER", "chromium"),
        headless=parse_bool(os.getenv("PLAYWRIGHT_HEADLESS"), True),
        timeout_ms=int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "60000")),
    )

    with PlaywrightClient(config) as client:
        title, html = client.fetch(url)

    out_path.write_text(html, encoding="utf-8")
    print(f"OK url={url} title={title} bytes={len(html)} out={out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
