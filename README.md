# QA Job Scraper

## 개요
여러 소스에서 공고를 수집하고 정규화한 뒤, 간단한 목록 UI로 보여주는 Django 기반 잡 스크레이퍼 프로젝트입니다.

## 요구 사항
- Python 3.x
- Playwright(브라우저 바이너리 필요)
- (선택) 운영 환경에서는 MySQL, 로컬 개발은 SQLite 사용 가능

## 설치 (cmd)
1. `python -m venv .venv`
2. `.\.venv\Scripts\activate`
3. `python -m pip install -r requirements.txt`
4. `python -m playwright install`
5. `.env.example`을 `.env`로 복사하고 값을 수정: `copy .env.example .env`

## 환경변수 (.env)
로컬 실행 필수 키:
- `DJANGO_SECRET_KEY`
- `DB_ENGINE` (로컬은 `sqlite`)
- `SCRAPE_INTERVAL_HOURS`
- `SCRAPE_TIMEZONE`
- `PLAYWRIGHT_BROWSER`

선택 키:
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `LOG_DIR`

## 로컬 실행 (cmd)
1. DB 마이그레이션  
   `set "DB_ENGINE=sqlite" && .\.venv\Scripts\python src\manage.py migrate`

2. fixtures 적재  
   `set "DB_ENGINE=sqlite" && for %f in (fixtures\json\*-items-*.json) do .\.venv\Scripts\python src\manage.py ingest_jobs %f`

3. 웹 실행  
   `set "PYTHONPATH=src" && .\.venv\Scripts\python src\manage.py runserver 127.0.0.1:8000`

## 수집기 (Playwright)
- 예시 (JobKorea)
1. `fixtures/urls/jobkorea.txt`에 URL 입력
2. 실행: `set "PYTHONPATH=src" && .\.venv\Scripts\python src\collectors\sources\jobkorea\int.py`

## 테스트
- `set "PYTHONPATH=src" && pytest -q`

## 정적 검사
- `set "PYTHONPATH=src" && python -m compileall -q src`

## 리포트
- QA 검증 증거는 `reports/run_YYYY-MM-DD.md`에 기록됩니다.

## 프로젝트 구조
- `src/` Django 앱 + 수집기
- `fixtures/` HTML/JSON fixtures 및 소스 URL
- `reports/` QA run 리포트
- `docs/` 프로젝트 문서
- `tasks/` 작업 목록 및 PRD
- `logs/` 런타임 로그

## 참고
- Windows에서 `mysqlclient` 설치가 실패하면 C++ Build Tools 설치가 필요합니다.