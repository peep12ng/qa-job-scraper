# Tasks for: qa-job-scraper

## Context
PRD: /tasks/prd-qa-job-scraper.md  
Stack (confirmed): Python, Django, Playwright, MySQL, Celery/Beat, pytest  
Taxonomy (confirmed): [Infra], [DEV], [QA], [CI/CD], [Deploy], [Docs], [Data], [Integrations], [Observability]  
Capabilities (from PRD): ui_e2e=playwright(required), data_store=mysql(required)  
Environment: PROJECT_SHELL=cmd; RUNTIME_DEFAULT=python  
TOOLING_HINTS (optional): none  
Notes: 12h schedule; filters 서울/0~1년/QA/소스별 직종; sources priority=사람인>잡코리아>원티드>인크루트>로켓펀치

## NOTE (중요)
아래 태스크는 PRD 기반으로 생성된 계획 초안이다. 번호/개수는 PRD의 FR/NFR 및 옵션 분류에 맞춰 구성되어 있다.

## Tasks
- [] 1.0 [Infra] 프로젝트 부트스트랩/실행 환경 구성
DoD(Local Verify): 1.1~1.5가 완료되어 기본 실행이 가능하다.  
DoD(Remote Verify, if pushed): CI 기본 단계에서 환경 세팅 실패가 없다.

- [x] 1.1 [Infra] 런타임/가상환경/의존성 설치 기준 확정 (Django, Playwright, MySQL 드라이버, Celery 포함)
DoD(Local Verify): 의존성 설치 절차가 문서화되어 재현 가능하다.  
DoD(Remote Verify, if pushed): CI 환경에서 의존성 설치가 실패하지 않는다.

- [x] 1.2 [Infra] Django 프로젝트/앱 구조 확정 및 기본 설정 모듈 분리
DoD(Local Verify): 프로젝트가 기본 설정으로 실행 가능하다.  
DoD(Remote Verify, if pushed): 기본 테스트 또는 체크가 CI에서 실패하지 않는다.

- [x] 1.3 [Infra] 환경변수 스키마 및 설정 로더 작성 (.env.example)
DoD(Local Verify): DB/스케줄/Playwright 관련 필수 환경변수 누락 시 명확한 오류가 있다.  
DoD(Remote Verify, if pushed): 설정 로딩 검증이 CI에서 실패하지 않는다.

- [x] 1.4 [Infra] 로컬 스모크(웹/워커/비트 중 1개 이상) 실행 증거 남기기
DoD(Local Verify): 최소 1회 실행 증거가 남아 있다(로그/리포트).  
DoD(Remote Verify, if pushed): 동일 스모크가 CI에서도 재현 가능하다.

- [x] 1.5 [Infra] 기본 로그/출력 경로 및 실행 모드(웹/워커/비트) 정리
DoD(Local Verify): 실행 모드별 진입 절차가 문서화되어 있다.  
DoD(Remote Verify, if pushed): 실행 모드 안내가 CI 문서와 충돌하지 않는다.

- [ ] 2.0 [DEV] 기능 구현
DoD(Local Verify): 2.1~2.9의 핵심 동작이 로컬에서 확인된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [x] 2.1 [DEV] FR-1 소스 레지스트리 및 우선순위 오케스트레이션 구현 (FR-1)
DoD(Local Verify): 소스 우선순위에 따라 수집 시도가 순차 수행된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [x] 2.2 [DEV] FR-2 필수 필터 적용 로직 및 소스별 직종 매핑 구현 (FR-2)
DoD(Local Verify): 서울/0~1년/QA 조건이 일관되게 적용된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.3 [DEV] FR-3 표준 모델 정규화 및 저장 파이프라인 구현 (FR-3)
DoD(Local Verify): 표준 필드가 누락 없이 저장된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.4 [DEV] FR-4 중복 감지/병합 로직 구현 (FR-4)
DoD(Local Verify): 중복 판별 기준과 병합 결과가 확인된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.5 [DEV] FR-5 공고 목록 UI 구현 (FR-5)
DoD(Local Verify): 목록 페이지에서 주요 필드가 표시된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.6 [DEV] FR-6 공고 상세 UI 구현 (FR-6)
DoD(Local Verify): 상세 화면에서 원문 링크/출처가 표시된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.7 [DEV] FR-7 12시간 주기 스케줄 실행 및 실행 결과 기록 구현 (FR-7)
DoD(Local Verify): 스케줄 실행과 결과 기록이 동작한다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [x] 2.8 [DEV] FR-8 Playwright 기반 수집 베이스 구현 (FR-8)
DoD(Local Verify): 브라우저 자동화로 데이터 획득이 가능하다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 2.9 [DEV] 실패 격리/재시도/백오프 전략 적용 (NFR)
DoD(Local Verify): 부분 실패 시 전체 파이프라인이 중단되지 않는다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.0 [QA] 요구사항 검증
DoD(Local Verify): 3.1~3.9의 검증 결과가 증거로 남아 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.1 [QA] FR-1 AC 검증 (FR-1)
DoD(Local Verify): AC 검증 결과가 보고서에 남아 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.2 [QA] FR-2 AC 검증 (FR-2)
DoD(Local Verify): 필터 조건 검증 증거가 남아 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.3 [QA] FR-3 AC 검증 (FR-3)
DoD(Local Verify): 저장 필드 누락 여부 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.4 [QA] FR-4 AC 검증 (FR-4)
DoD(Local Verify): 중복 병합 결과 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.5 [QA] FR-5 AC 검증 (FR-5)
DoD(Local Verify): 목록 UI 표시 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.6 [QA] FR-6 AC 검증 (FR-6)
DoD(Local Verify): 상세 UI 표시 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.7 [QA] FR-7 AC 검증 (FR-7)
DoD(Local Verify): 스케줄 실행/기록 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.8 [QA] FR-8 AC 검증 (FR-8)
DoD(Local Verify): Playwright 수집 동작 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 3.9 [QA] NFR 신뢰성/부분 실패 격리 검증
DoD(Local Verify): 실패 시나리오 1~2개 검증 증거가 있다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 4.0 [CI/CD] 자동 검증 파이프라인
DoD(Local Verify): 4.1~4.2 범위가 정리되어 있다.  
DoD(Remote Verify, if pushed): CI 체크가 green이다.

- [ ] 4.1 [CI/CD] 테스트 자동 실행 구성 (pytest)
DoD(Local Verify): 로컬 테스트가 재현 가능하다.  
DoD(Remote Verify, if pushed): CI에서 테스트 체크가 green이다.

- [ ] 4.2 [CI/CD] 린트/정적분석 구성 (도입 시)
DoD(Local Verify): 린트/정적분석 실행 기준이 문서화되어 있다.  
DoD(Remote Verify, if pushed): CI에서 린트 체크가 green이다.

- [ ] 5.0 [Deploy] 실행/배포
DoD(Local Verify): 5.1~5.2가 재현 가능하다.  
DoD(Remote Verify, if pushed): 배포 관련 체크가 green이다.

- [ ] 5.1 [Deploy] 실행 방식 정의(웹/워커/비트)
DoD(Local Verify): 각 실행 모드가 문서화되어 있다.  
DoD(Remote Verify, if pushed): 배포 문서와 충돌이 없다.

- [ ] 5.2 [Deploy] 스모크 테스트 시나리오 작성 및 1회 실행
DoD(Local Verify): 스모크 증거가 남아 있다.  
DoD(Remote Verify, if pushed): 스모크가 CI/배포 후에도 통과한다.

- [ ] 6.0 [Docs] 문서화
DoD(Local Verify): 6.1~6.3 문서가 존재한다.  
DoD(Remote Verify, if pushed): 문서 링크/배지가 깨지지 않는다.

- [ ] 6.1 [Docs] README: 설치/실행/테스트/폴더 구조 정리
DoD(Local Verify): 신규 환경에서 재현 가능한 수준이다.  
DoD(Remote Verify, if pushed): 문서 체크가 CI에서 실패하지 않는다.

- [ ] 6.2 [Docs] 수집 정책/robots 및 약관 준수 문서화
DoD(Local Verify): 준수 기준과 요청 빈도 정책이 명확하다.  
DoD(Remote Verify, if pushed): 문서 체크가 CI에서 실패하지 않는다.

- [ ] 6.3 [Docs] 운영/스케줄/장애 대응 메모 작성
DoD(Local Verify): 운영 절차가 5~10줄로 정리되어 있다.  
DoD(Remote Verify, if pushed): 문서 체크가 CI에서 실패하지 않는다.

- [ ] 7.0 [Data] 데이터 설계/저장소
DoD(Local Verify): 7.1~7.3이 정의되어 있다.  
DoD(Remote Verify, if pushed): DB 관련 체크가 CI에서 실패하지 않는다.

- [x] 7.1 [Data] MySQL 스키마 설계(JobPost, Source, RunLog, DuplicateGroup)
DoD(Local Verify): 테이블/필드/제약이 명확히 정의되어 있다.  
DoD(Remote Verify, if pushed): 마이그레이션 체크가 CI에서 실패하지 않는다.

- [x] 7.2 [Data] 마이그레이션 및 인덱스/유니크 제약 적용
DoD(Local Verify): 중복 방지 및 조회 성능 기준이 충족된다.  
DoD(Remote Verify, if pushed): 마이그레이션이 CI에서 실패하지 않는다.

- [x] 7.3 [Data] 조회 패턴 기반 쿼리/ORM 접근 경로 확정
DoD(Local Verify): 목록/상세 조회가 안정적으로 동작한다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.0 [Integrations] 소스별 수집 어댑터(Slice Ladder)
DoD(Local Verify): 각 소스별 DISC/CORE/INT 산출물이 존재한다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 재현 가능하다.

- [x] 8.1-SAR-DISC [Integrations] 사람인 탐색(요청/셀렉터/샘플 확보)
DoD(Local Verify): fixtures/html 또는 fixtures/json에 샘플이 저장되어 있다.  
DoD(Remote Verify, if pushed): 샘플 기반 재현 문서가 있다.

- [x] 8.1-SAR-CORE [Integrations] 사람인 파서/정규화 로직 구현
DoD(Local Verify): 샘플 입력으로 표준 모델 변환이 된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.1-SAR-INT [Integrations] 사람인 수집 파이프라인 통합
DoD(Local Verify): 실제 실행 파이프라인에서 수집 결과가 확인된다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 green이다.

- [ ] 8.2-JK-DISC [Integrations] 잡코리아 탐색(요청/셀렉터/샘플 확보)
DoD(Local Verify): fixtures/html 또는 fixtures/json에 샘플이 저장되어 있다.  
DoD(Remote Verify, if pushed): 샘플 기반 재현 문서가 있다.

- [ ] 8.2-JK-CORE [Integrations] 잡코리아 파서/정규화 로직 구현
DoD(Local Verify): 샘플 입력으로 표준 모델 변환이 된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.2-JK-INT [Integrations] 잡코리아 수집 파이프라인 통합
DoD(Local Verify): 실제 실행 파이프라인에서 수집 결과가 확인된다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 green이다.

- [ ] 8.3-WANTED-DISC [Integrations] 원티드 탐색(요청/셀렉터/샘플 확보)
DoD(Local Verify): fixtures/html 또는 fixtures/json에 샘플이 저장되어 있다.  
DoD(Remote Verify, if pushed): 샘플 기반 재현 문서가 있다.

- [ ] 8.3-WANTED-CORE [Integrations] 원티드 파서/정규화 로직 구현
DoD(Local Verify): 샘플 입력으로 표준 모델 변환이 된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.3-WANTED-INT [Integrations] 원티드 수집 파이프라인 통합
DoD(Local Verify): 실제 실행 파이프라인에서 수집 결과가 확인된다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 green이다.

- [ ] 8.4-INCRUIT-DISC [Integrations] 인크루트 탐색(요청/셀렉터/샘플 확보)
DoD(Local Verify): fixtures/html 또는 fixtures/json에 샘플이 저장되어 있다.  
DoD(Remote Verify, if pushed): 샘플 기반 재현 문서가 있다.

- [ ] 8.4-INCRUIT-CORE [Integrations] 인크루트 파서/정규화 로직 구현
DoD(Local Verify): 샘플 입력으로 표준 모델 변환이 된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.4-INCRUIT-INT [Integrations] 인크루트 수집 파이프라인 통합
DoD(Local Verify): 실제 실행 파이프라인에서 수집 결과가 확인된다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 green이다.

- [ ] 8.5-RP-DISC [Integrations] 로켓펀치 탐색(요청/셀렉터/샘플 확보)
DoD(Local Verify): fixtures/html 또는 fixtures/json에 샘플이 저장되어 있다.  
DoD(Remote Verify, if pushed): 샘플 기반 재현 문서가 있다.

- [ ] 8.5-RP-CORE [Integrations] 로켓펀치 파서/정규화 로직 구현
DoD(Local Verify): 샘플 입력으로 표준 모델 변환이 된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 8.5-RP-INT [Integrations] 로켓펀치 수집 파이프라인 통합
DoD(Local Verify): 실제 실행 파이프라인에서 수집 결과가 확인된다.  
DoD(Remote Verify, if pushed): 통합 스모크가 CI에서 green이다.

- [ ] 9.0 [Observability] 수집 상태/로그/가시성
DoD(Local Verify): 9.1~9.2가 확인된다.  
DoD(Remote Verify, if pushed): 관련 체크가 CI에서 실패하지 않는다.

- [ ] 9.1 [Observability] 수집 실행 로그 스키마/포맷 정의
DoD(Local Verify): 수집 실행 결과(성공/실패/시간)가 구조적으로 기록된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

- [ ] 9.2 [Observability] 수집 상태 표시(UI 또는 Admin)
DoD(Local Verify): 최근 실행 시간과 실패 소스가 확인된다.  
DoD(Remote Verify, if pushed): 관련 테스트가 CI에서 green이다.

## Task Execution Order (권장)
Suggested Execution Plan:
1. 1.1 -> 1.5 (Infra 기준 정리 및 스모크)
2. 7.1 -> 7.2 (MySQL 스키마/마이그레이션)
3. 2.8 -> 2.1 -> 2.2 (수집 베이스/오케스트레이터/필터)
4. 8.1-SAR-DISC -> 8.1-SAR-CORE -> 8.1-SAR-INT (최우선 소스 end-to-end)
5. 8.2~8.5 (나머지 소스 Slice Ladder 반복)
6. 2.3 -> 2.7 -> 2.4 -> 2.5 -> 2.6 -> 2.9 (저장/스케줄/중복/UI/안정성)
7. 9.1 -> 9.2 (관측성)
8. 3.x (QA) -> 4.x (CI/CD) -> 5.x (Deploy) -> 6.x (Docs)

## Traceability (FR -> Tasks)
FR-1 -> DEV: 2.1, QA: 3.1, Evidence: reports/run_YYYY-MM-DD.md  
FR-2 -> DEV: 2.2, QA: 3.2, Evidence: reports/run_YYYY-MM-DD.md  
FR-3 -> DEV: 2.3, QA: 3.3, Evidence: reports/run_YYYY-MM-DD.md  
FR-4 -> DEV: 2.4, QA: 3.4, Evidence: reports/run_YYYY-MM-DD.md  
FR-5 -> DEV: 2.5, QA: 3.5, Evidence: reports/run_YYYY-MM-DD.md  
FR-6 -> DEV: 2.6, QA: 3.6, Evidence: reports/run_YYYY-MM-DD.md  
FR-7 -> DEV: 2.7, QA: 3.7, Evidence: reports/run_YYYY-MM-DD.md  
FR-8 -> DEV: 2.8, QA: 3.8, Evidence: reports/run_YYYY-MM-DD.md
