# Run Modes & Logging

## Log Output
- 기본 로그 디렉터리: `logs/` (환경변수 `LOG_DIR`로 변경 가능)
- 기본 로그 파일: `logs/app.log`
- 콘솔 출력도 동시에 활성화됨

## Run Modes (cmd)
- Web: `set "PYTHONPATH=src" && .\.venv\Scripts\python src\manage.py runserver 127.0.0.1:8000`
- Worker: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper worker -l INFO`
- Beat: `set "PYTHONPATH=src" && .\.venv\Scripts\python -m celery -A qa_job_scraper beat -l INFO`

## Notes
- Celery는 `CELERY_BROKER_URL`의 브로커가 실행 중이어야 한다.
- 로컬 스모크는 `DB_ENGINE=sqlite`로 실행 가능하다.
