# Personal AI Dev Environment v0.3 (사람용)
Last updated: 2026-02-11

## 목적
- 아이디어 1줄로 시작해, 티켓 단위로 SDLC 전 과정을 진행하며 문서+코드+테스트를 포함한 MVP 산출을 돕는다.
- 실제 실행(파일 생성/수정/커밋/PR)은 사용자가 수행하고, AI는 제안/블록 제공/검증 절차 안내를 담당한다.

## 적용 범위
- 모든 프로젝트(언어/도메인 무관). 기본 런타임은 Python(티켓에서 예외 지정 가능).

## 핵심 운영 원칙
- 티켓(T-XXXX) 단위로만 움직인다.
- SDLC 6단계 게이트를 따른다: Intake → Req → Design → Build → Test → Done
- 각 게이트 종료 시 AI는 반드시 멈추고 "OK"를 요청한다(사용자 승인 전 진행 금지).
- AI는 파일을 직접 수정/저장하지 않고, 항상 붙여넣기 블록으로만 제공한다.
- PROJECT_SHELL 단일화: Verify/Operator Steps 명령은 PROJECT_SHELL 기준으로만 출력한다.
- Verify 게이트: Local Verify PASS 전에는 체크박스 업데이트/Commit Text/커밋(및 관련 제안) 금지.
- md 파일 전문은 코드펜스로 감싸지 않고 원문 그대로 제공한다.

## Codex(IDE) 사용 방식
- Codex는 rules/ENV_SPEC.md를 최우선으로 읽고 준수한다.
- 매 티켓 시작 시 부팅 프롬프트로 규칙을 상기시킨다.
- 산출물은 repo에 남기고, Notion에는 요약/회고/스크린샷을 정리한다.

## 산출물 구조(권장)
- /tickets : 티켓(md)
- /docs : 요구사항/설계/테스트 계획
- /src, /tests : 구현/테스트
- /reports : 실행 로그/증거
- /rules : 운영 규칙(ENV_SPEC 포함)

## Output Contract
- Codex가 반드시 지켜야 할 출력 형식과 각 게이트의 DoD는 rules/ENV_SPEC.md에 정의한다.
- 이 문서는 운영 의도/사용 방법을 설명하며, 실행 규칙의 단일 진실원천은 ENV_SPEC이다.

## Notion 기록(권장)
- 페이지 제목: Personal AI Dev Environment v0.1
- 포함 내용:
  - Version(v0.1)
  - repo 링크
  - rules/ENV_SPEC.md 핵심 요약(또는 전체 복붙)
  - 변경점/회고(짧게)

## 부팅 프롬프트(예시)
rules/ENV_SPEC.md를 먼저 읽고, 내용대로 엄격히 따라.
현재 티켓은 tickets/T-____.md 야.
SDLC 게이트(Intake→Req→Design→Build→Test→Done)를 따르고,
각 게이트가 끝나면 반드시 멈추고 "OK"를 요청해.
파일은 절대 직접 수정/저장하지 말고, 항상 붙여넣기 블록으로만 제공해.
출력은 ENV_SPEC의 출력 계약 형식만 사용해.
기본 런타임은 Python이야.
PROJECT_SHELL 기준으로만 Verify/Operator Steps 명령을 출력해(다른 셸 대안 병기 금지).
Local Verify PASS 전에는 체크박스/Commit Text/커밋 관련 제안을 하지 마.
md 파일 전문은 코드펜스로 감싸지 말고 원문 그대로 출력해.
