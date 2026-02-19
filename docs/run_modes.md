# Run Modes & Logging

## Log Output
- 기본 로그 디렉터리: `logs/` (환경변수 `LOG_DIR`로 변경 가능)
- 기본 로그 파일: `logs/app.log`
- 콘솔 출력은 동시에 표시됨

## Collection RunLog Schema
- 기록 단위: 소스 1개당 1개 RunLog 생성
- 필드 정의:
  - `source`: 수집 소스(`Source.code`, 예: `saramin`, `jobkorea`)
  - `status`: `success` | `partial` | `fail`
  - `started_at`: 수집 시작 시간
  - `finished_at`: 수집 종료 시간
  - `items_collected`: 수집된 공고 수
  - `error_message`: 에러 요약(있으면 문자열, 없으면 빈 문자열)

## Run Modes (cmd)
- Web: `set "PYTHONPATH=src" && .\.venv\Scripts\python src\manage.py runserver 127.0.0.1:8000`
- Worker: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper worker -l INFO`
- Beat: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper beat -l INFO`

## Deploy & Run (Local)
- 필수 환경변수(.env): `DJANGO_SECRET_KEY`, `DB_ENGINE`, `SCRAPE_INTERVAL_HOURS`, `SCRAPE_TIMEZONE`, `PLAYWRIGHT_BROWSER`
- DB 마이그레이션: `set "DB_ENGINE=sqlite" && .\.venv\Scripts\python src\manage.py migrate`
- fixtures 적재: `set "DB_ENGINE=sqlite" && for %f in (fixtures\json\*-items-*.json) do .\.venv\Scripts\python src\manage.py ingest_jobs %f`
- Web UI: `set "PYTHONPATH=src" && .\.venv\Scripts\python src\manage.py runserver 127.0.0.1:8000`
- Worker/Beat: `CELERY_BROKER_URL` 설정 시 Run Modes 명령으로 실행

## Static Checks (cmd)
- Syntax check: `set "PYTHONPATH=src" && python -m compileall -q src`
