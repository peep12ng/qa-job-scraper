# Policy: 코드/문서 변경 제안 정책 (code_modification_policy) v0.3
Last updated: 2026-02-11
Compatible ENV: v0.3+

## 1) 목적
AI가 프로젝트의 코드/설정/문서를 변경해야 할 때, 안전하고 일관된 방식으로 "변경 제안"만 수행하도록 규정한다.

- AI는 파일을 직접 생성/수정/저장하지 않는다.
- 사용자가 복사-붙여넣기로 변경을 반영한다.
- 변경 제안에는 항상 검증(Verify) 방법을 포함한다(ENV_SPEC 준수).
- Local Verify(필수): PROJECT_SHELL 기준 명령 + 기대 신호 / 금지: git commit, git push 포함
- Remote Verify(조건부): 사용자가 이미 push 한 경우에만 / 금지: commit/push 절차 섞기
- Commit Text는 Local Verify PASS 후에만(필요 시) 제공한다.
- Paste Blocks: 코드/설정은 코드블록 OK, md 파일 “전문”은 코드펜스로 감싸지 않는다(중첩 ``` 깨짐 방지).

## 2) 적용 범위
이 정책은 소스 코드뿐 아니라 아래 파일에도 동일하게 적용한다.

- 소스/테스트: src/**, tests/**
- 설정/스크립트: .github/workflows/*.yml, Dockerfile, docker-compose.yml, .env*, *.sh, *.ps1
- 문서/산출물: README.md, /docs/*.md, /tasks/*.md, tests/cases/*.md, bugs/*.md

## 3) 우선순위(충돌 해결)
- 최상위 규칙: rules/ENV_SPEC.md
- 충돌 시: ENV_SPEC > 이 정책(code_modification_policy) > workflows/* > tickets/* > docs/* > code

## 4) 절대 규칙(Non-negotiables)
- (직접 수정 금지) AI는 어떤 파일도 직접 생성/수정/저장하지 않는다.
- (제안 방식 고정) 변경이 필요하면 반드시 아래 "변경 제안 포맷" 중 하나로 제시한다.
- (컨텍스트 제공) 적용 위치를 찾을 수 있게 충분한 주변 문맥(함수/클래스/블록 단위)을 포함한다.
- (작업 단위) 큰 변경은 작은 패치로 쪼개 제안한다.
- (OK 게이트) 변경 제안 후 반드시 멈추고 사용자 OK를 받는다. OK 없이는 다음 단계로 진행하지 않는다.
- (Scaffold-first) 자동 생성 가능한 결과물은 Paste Blocks로 통째로 작성하지 않는다.
  - 우선: 공식/표준 scaffold 명령을 제공한다.
  - 그 다음: 생성 결과물 중 “반드시 수정해야 하는 최소 파일”만 Paste Blocks로 제공한다.
- (Large Payload) 대형 HTML/JSON/로그 전문을 채팅에 직접 붙여넣지 않는다(컨텍스트/보안 리스크).
  - fixtures 파일로 저장 후 경로를 공유한다.
  - 채팅에는 핵심 발췌 + 목적만 제공한다.
  - 민감정보(쿠키/토큰/세션/개인식별 정보)는 기본적으로 제거한다.

## 5) 변경 제안 포맷 (Paste Blocks)
변경 제안은 아래 3가지 중 하나로 제공한다.

### 5.1 Old/New 블록 (기본)
- 파일 경로를 먼저 명시한다.
- Old Code / New Code를 각각 제공한다.
- Old에는 교체될 범위(함수/블록)를 포함한다.
- New에는 교체 후 결과를 동일 범위로 제공한다.

형식(템플릿):
- File: path/to/file.ext
- Old Code:
    <여기에 기존 코드 블록을 그대로 붙임>
- New Code:
    <여기에 변경 후 코드 블록을 그대로 붙임>

### 5.2 Unified diff (짧은 변경에만)
- 변경이 작은 경우에만 사용한다(가독성 목적).
- 파일 경로를 포함한다.

형식(템플릿):
- Diff:
    diff --git a/path/to/file.ext b/path/to/file.ext
    --- a/path/to/file.ext
    +++ b/path/to/file.ext
    @@ ...
    - old line
    + new line

### 5.3 전체 파일 본문 제공 (신규 파일/짧은 파일)
- 신규 파일 생성 제안, 또는 파일이 짧아 전체 교체가 더 안전할 때 사용한다.
- 파일 경로 + 전체 본문을 제공한다.

형식(템플릿):
- File: path/to/new_file.ext
- Full Content:
    <파일 전체 내용을 그대로 제공>

## 6) 변경 제안 절차 (ENV_SPEC Output Contract 호환)
변경 제안이 필요한 상황에서 AI는 아래 순서로 출력한다.

### Deliverables
- 생성/수정 대상 파일 목록(경로 포함)

### Paste Blocks
- 각 파일별 변경 제안(5장 포맷 준수)

### Verify
- 사용자가 변경 후 수행할 검증 방법을 제시한다.
  - 실행 명령어(예: pytest, npm test, docker compose up, 린트 등)
  - 통과 기준(어떤 출력/상태면 성공인지)

### Commit Text (선택)
- 사용자가 커밋할 때 쓸 커밋 메시지를 1~2개 제안한다.

### Stop
- "이 변경안을 적용할까요? OK면 다음으로 진행할게요." 라고 묻고 멈춘다.

## 7) 품질/안전 체크리스트(제안 전 자가 점검)
AI는 변경안을 내기 전에 아래를 스스로 확인한 뒤 제안해야 한다.

- 변경 목적이 명확한가? (왜 바꾸는지 한 줄 설명 가능)
- 변경 범위가 최소인가? (필요한 곳만 바꿈)
- 프로젝트 규칙/구조를 깨지 않는가? (경로/네이밍/규칙 준수)
- 테스트/검증 계획이 포함되어 있는가?
- 문서/설정 변경이면 실행 재현성에 도움이 되는가?

## 8) 금지 사항
- "추정으로" 대규모 리팩토링을 한 번에 제안하지 않는다.
- 적용 위치가 불명확한 채로 일부 코드 조각만 던지지 않는다.
- 사용자의 OK 없이 다음 파일/다음 단계로 진행하지 않는다.
