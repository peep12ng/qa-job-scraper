# Workflows Index v0.3
Last updated: 2026-02-11

## 1) 이 문서의 목적
이 레포는 “개인 맞춤 AI 개발 환경(규칙 + 워크플로우)”을 문서로 고정하고, VS Code Codex에서 그 문서들을 따라 SDLC 전 과정을 진행하기 위한 운영 체계다.

- 규칙(ENV_SPEC/policies): Codex가 반드시 따라야 하는 최상위 운영 원칙
- 워크플로우(workflows): 특정 목적(PRD 생성, 태스크 생성, 태스크 처리)을 수행하는 절차 문서
- 산출물(tasks/docs/reports): 실행 결과로 남기는 파일들(사용자가 복사-붙여넣기로 저장)

> 실행(파일 수정/커밋/실행)은 사용자, 제안(블록/절차)은 AI가 담당한다.

---

## 2) 시작하기(Entry Points)
아래 중 “현재 상태”에 맞는 항목을 선택해 해당 워크플로우부터 시작한다.

### A. 아이디어만 있다(아직 PRD 없음)
- 사용 문서: `rules/workflows/create_prd.md`
- 결과물: `/tasks/prd-[기능-이름].md`
- 종료 조건: “PRD 초안 OK?” 승인

### B. PRD는 있다(이제 계획/태스크가 필요)
- 사용 문서: `rules/workflows/generate_tasks.md`
- 결과물: `/tasks/tasks-[prd-파일-이름].md`
- 종료 조건: “기술 스택 OK?” + “분류 세트 OK?” + “계획 OK?” 승인

### C. 태스크 목록이 있다(이제 실행/구현 진행)
- 사용 문서: `rules/workflows/process_task_lists.md`
- 결과물:
  - 태스크 체크 업데이트(`/tasks/tasks-*.md` 내 체크박스 변경)
  - 실행 증거: `/reports/run_YYYY-MM-DD.md` (권장)
- 종료 조건: 하위 태스크 완료 후 “다음 진행 OK?” 승인

---

## 3) 표준 라우팅(권장 흐름)
Intake(PRD) → generate_tasks(계획) → process_task_lists(실행/분해/진행) → 티켓(T-XXXX) 기반 SDLC(Req→Design→Build→Test→Done)

- create_prd는 Intake(기획) 전용: “무엇/왜” 확정
- generate_tasks는 계획 전용: 태스크 구조/우선순위의 기반 확보
- process_task_lists는 실행 전용: 한 번에 하나의 하위 태스크(WIP=1) 처리

---

## 4) 문서 구조(어디에 뭐가 있나)

### 4.1 최상위 규칙(필수)
- `rules/ENV_SPEC.md`
  - Codex 최상위 운영 스펙: 우선순위, 절대 규칙, Output Contract, SDLC 게이트 정의, 라우팅

### 4.2 전역 정책(policies)
- `rules/policies/code_modification_policy.md`
  - 파일 직접 수정 금지
  - Old/New 또는 diff 또는 전체 본문으로만 변경 제안
  - Verify + OK 게이트 포함
  - `rules/policies/commit_message_policy.md`
    - 커밋 메시지 형식(타입/스코프/한국어 톤) 표준화

### 4.3 워크플로우(workflows)
- `rules/workflows/create_prd.md`
  - 명료화 질문(턴 A) → PRD 생성(턴 B) → OK
- `rules/workflows/generate_tasks.md`
  - PRD 요약 + 기술 스택 후보 + 분류 세트 제안(턴 A) → OK
  - 태스크 초안 + Traceability(턴 B) → OK
  - 저장용 최종 파일 출력(턴 C) → OK
- `rules/workflows/process_task_lists.md`
  - 태스크 하위 항목을 하나씩 처리(WIP=1)
  - 파일 변경 제안 + Verify + 체크박스 업데이트 + OK

---

## 5) 산출물 저장 위치(권장)
- `/tasks/`
  - `prd-*.md` : PRD 산출물
  - `tasks-*.md` : 전체 태스크 목록 산출물
- `/docs/`
  - 요구사항/설계/테스트 계획 등 프로젝트 내부 문서(필요 시)
- `/reports/`
  - 실행/검증 결과 증거(`run_YYYY-MM-DD.md`)

---

## 6) 운영 규칙(요약)
- AI는 파일을 직접 수정/저장하지 않는다(붙여넣기 블록만).
- 각 단계/워크플로우 종료 시 반드시 멈추고 OK를 요청한다.
- 기본 런타임은 Python(예외는 PRD/태스크에서 명시).
- 변경 이력은 “의미 있는 묶음” 단위로 마지막에 로깅한다(CHANGELOG/태그는 필요 시).
- PROJECT_SHELL 단일화: Verify/Operator Steps 명령은 PROJECT_SHELL 기준으로만 출력한다(다른 셸 대안 병기 금지).
- Verify 게이트: Local Verify PASS 전에는 체크박스 업데이트/Commit Text/커밋(및 관련 제안) 금지.
- Verify Local/Remote 분리: Remote Verify는 “이미 push 한 경우에만” 수행(절차에 commit/push 섞지 않기).
- Paste Blocks 안정화: md 파일 전문은 코드펜스로 감싸지 않고 원문 그대로 제공(Verify/Operator Steps는 분리 섹션).
- rules 문서(workflows/policies 포함)를 수정한 커밋에는 해당 문서의 `Last updated: YYYY-MM-DD`를 반드시 갱신한다.
- 규칙 변화가 있으면 `CHANGELOG.md`에 같은 날짜로 항목을 1줄 이상 추가한다(요약만).

---

## 7) Codex 부팅 프롬프트(요약)
매 티켓/워크플로우 시작 시 아래 원칙을 상기시킨다.

- `rules/ENV_SPEC.md`를 먼저 읽고 엄격히 따르기
- 파일 직접 수정/저장 금지(붙여넣기 블록만)
- Output Contract 준수
- 단계 종료 시 OK 요청 후 멈추기
- PROJECT_SHELL 기준으로만 명령 출력
- Verify 게이트(체크박스/Commit Text는 Local Verify PASS 이후)
- md 전문은 코드펜스 금지(원문 출력)
