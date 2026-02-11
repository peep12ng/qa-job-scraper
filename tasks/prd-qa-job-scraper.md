# PRD: qa-job-scraper (QA 신입 공고 수집 웹사이트)

## 1) 개요/소개
qa-job-scraper는 여러 채용공고 사이트에서 QA 신입 공고를 수집해 한 곳에서 조회할 수 있게 하는 웹사이트다. 목표는 QA 신입 공고 탐색 시간을 줄이고, 조건에 맞는 공고를 빠르게 확인하는 것이다.

## 2) Goals (측정 가능한 목표)
- 지정된 5개 소스(사람인, 잡코리아, 원티드, 인크루트, 로켓펀치)에서 QA 신입 공고를 수집해 통합 리스트로 제공한다.
- 12시간 주기로 신규/변경 공고가 반영된다.
- 수집 결과가 데이터 저장소(MySQL)에 보존되어 웹에서 재조회 가능하다.

## 3) 사용자/페르소나 (간단)
- QA 신입 구직자: 여러 사이트를 돌아다니기 어렵고, 조건에 맞는 공고를 빠르게 찾고 싶다.
- QA 전직 준비자: 신입/주니어 공고의 범위와 조건을 비교하고 싶다.

## 4) User Stories
- QA 신입 구직자로서 여러 사이트를 오가지 않고 한 곳에서 공고를 보고 싶다. 이유는 탐색 시간을 줄이기 위해서다.
- 취업 준비생으로서 서울 지역의 QA 신입 공고를 빠르게 확인하고 싶다. 이유는 내 조건에 맞는 공고만 보고 싶기 때문이다.
- 구직자로서 동일 공고가 중복되어 보이지 않길 원한다. 이유는 혼동을 줄이기 위해서다.

## 5) Functional Requirements
- FR-1: 수집 대상 사이트와 우선순위를 고정한다: 사람인 → 잡코리아 → 원티드 → 인크루트 → 로켓펀치.
- FR-2: 수집 시 필수 필터를 적용한다: 지역=서울, 경력=신입+경력(0~1년), 검색어=QA, 소스별 직종 필터가 있으면 사용한다.
- FR-3: 수집 결과를 표준 필드로 정규화하고 데이터 저장소(MySQL)에 저장한다.
- FR-4: 동일 공고를 중복 감지해 하나의 항목으로 병합하고 출처 목록을 유지한다.
- FR-5: 웹 UI에서 공고 리스트를 제공하고 주요 필드를 표시한다.
- FR-6: 공고 상세 화면에서 원문 링크와 출처 정보를 표시한다.
- FR-7: 수집 작업은 12시간 주기로 자동 실행되며 실행 결과(성공/실패/시간)가 기록된다.
- FR-8: 동적 페이지/스크립트 기반 페이지 수집을 위해 브라우저 자동화(Playwright)를 사용한다.

## 6) Acceptance Criteria (테스트 가능한 형태)
- AC-1 (FR-1): Given 수집 대상이 설정되어 있을 때, When 수집을 실행하면, Then 지정된 5개 소스만 우선순위 순서로 시도하고 각 공고에 `source_site`가 기록된다.
- AC-2 (FR-2): Given 수집된 공고가 있을 때, When 필터 조건을 확인하면, Then 지역=서울, 경력=0~1년, 키워드=QA 조건을 충족하는 공고만 저장된다.
- AC-3 (FR-3): Given 수집이 완료되었을 때, When 저장된 공고를 조회하면, Then 표준 필드가 모두 존재한다.
- AC-4 (FR-4): Given 동일 공고가 여러 소스에 존재할 때, When 리스트가 표시되면, Then 중복 항목이 하나로 병합되고 복수 출처가 확인된다.
- AC-5 (FR-5): Given 사용자가 목록 페이지에 진입했을 때, When 리스트가 표시되면, Then 제목/회사/지역/경력/게시일 등의 주요 필드가 보인다.
- AC-6 (FR-6): Given 특정 공고를 선택했을 때, When 상세 페이지를 확인하면, Then 원문 링크와 출처 사이트가 표시된다.
- AC-7 (FR-7): Given 12시간 주기가 설정되어 있을 때, When 스케줄 시간이 도래하면, Then 수집 작업이 자동 실행되고 마지막 실행 시간/상태가 기록된다.
- AC-8 (FR-8): Given 동적 페이지 소스가 있을 때, When 수집을 수행하면, Then Playwright 기반 브라우저 자동화로 공고 데이터를 획득할 수 있다.

## 7) Non-functional Requirements
- 준수: 각 소스의 robots.txt 및 이용약관을 준수하고 요청 빈도를 제한한다.
- 신뢰성: 특정 소스 수집 실패 시에도 다른 소스의 결과는 계속 제공된다.
- 안정성: 요청 실패 시 재시도/백오프 전략이 적용된다.

## 8) Non-goals / Out of Scope
- 지원서 작성/제출 기능
- 사용자 계정/로그인/개인화 추천 기능
- QA 외 직무 전체 범위 수집
- 알림/구독 기능

## 9) 디자인/UX 고려사항 (선택)
- 최소 화면: 공고 목록, 공고 상세
- 목록에서 필수 필터(서울/신입/QA)가 적용된 상태임을 명확히 표시한다.

## 10) 데이터 요구사항 (선택)
- source_site
- source_job_id
- title
- company
- location
- experience_level
- experience_max_years
- employment_type
- posting_date
- closing_date
- url
- description_snippet
- tags
- source_category_path
- collected_at
- updated_at
- duplicate_group_id

## 11) 성공 지표 (Success Metrics)
- 5개 소스 각각에 대해 수집 시도가 성공 로그로 남고, UI에서 소스별 공고가 1건 이상 확인된다(가능한 경우).
- 중복 공고가 병합되어 단일 항목으로 노출된다.

## 12) Environment & Tooling
- PROJECT_SHELL: cmd
- RUNTIME_DEFAULT: python
- TOOLING_HINTS: none

## 13) Capabilities & Dependencies
```yaml
capabilities:
  ui_e2e: { choice: playwright, level: required }
  data_store: { choice: mysql, level: required }
  cache: { choice: none, level: optional }
  queue: { choice: none, level: optional }
  auth: { choice: none, level: optional }
  observability: { choice: none, level: optional }
```

## 14) Open Questions
- None
