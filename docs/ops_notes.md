# 운영/설정 요약 메모

1. 로컬은 `DB_ENGINE=sqlite` 기준으로 동작하며, 운영은 MySQL을 권장.
2. 수집 주기는 `SCRAPE_INTERVAL_HOURS`(기본 12시간)로 제어.
3. Playwright 수집은 `PLAYWRIGHT_BROWSER`와 `PLAYWRIGHT_HEADLESS` 설정에 의존.
4. 수집 결과는 `reports/run_YYYY-MM-DD.md`에 검증 증거로 기록.
5. 실패 격리는 소스 단위로 이루어지며 RunLog에 상태가 남음.
6. CI는 `pytest -q` + `python -m compileall -q src`로 구성.
7. 실행 절차는 `docs/run_modes.md`에 정리됨.
8. robots 준수/요청 빈도 정책은 `docs/scraping_policy.md` 참고.