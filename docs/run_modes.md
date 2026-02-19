# Run Modes & Logging

## Log Output
- 기본 로그 디렉터리: `logs/` (환경변수 `LOG_DIR`로 변경 가능)
- 기본 로그 파일: `logs/app.log`
- 콘솔 출력도 동시에 활성화됨

## Collection RunLog Schema
- 기록 단위: 소스 1개당 1개 RunLog 레코드
- 필드 정의:
  - `source`: 수집 소스(`Source.code`, 예: `saramin`, `jobkorea`)
  - `status`: `success` | `partial` | `fail`
  - `started_at`: 수집 시작 시간
  - `finished_at`: 수집 종료 시간
  - `items_collected`: 저장된 공고 수
  - `error_message`: 에러 요약(있으면 문자열, 없으면 빈 문자열)

## Run Modes (cmd)
- Web: `set "PYTHONPATH=src" && .\.venv\Scripts\python src\manage.py runserver 127.0.0.1:8000`
- Worker: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper worker -l INFO`
- Beat: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper beat -l INFO`