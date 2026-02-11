# Policy: 커밋 메시지 형식 규칙 (commit_message_policy) v0.3
Last updated: 2026-02-11
Compatible ENV: v0.3+

## 1) 목적
- 커밋 히스토리가 “무엇을/왜/어디를” 바꿨는지 한 눈에 보이게 한다.
- 프로젝트가 바뀌어도 동일한 형식으로 반복 가능하게 한다.

## 2) 절대 규칙(게이트 연동)
- Local Verify PASS 전에는 커밋 메시지를 확정/출력/제안하지 않는다.
- (예외 없음) 트러블슈팅 루프(C-FAIL)에서는 Commit Text를 금지한다.

## 3) 기본 형식(권장 기본값)
- 포맷:
  - `[Type(scope)] Subject`
  - scope가 없으면: `[Type] Subject`

### Type(고정 집합, 영어 대문자/첫글자 대문자 권장)
- Docs, Feat, Fix, Refactor, Test, Chore, CI, Build, Perf, Revert

### scope(선택)
- 소문자/숫자/하이픈만 권장(짧게 1~2단어)
- 예: `rules`, `workflow`, `policy`, `collector`, `saramin`, `db`, `ci`

### Subject(한국어 권장)
- “행동 중심”으로 1줄 요약
  - 권장 동사: `추가/수정/정리/통일/분리/반영/개선/구현/제거`
- 문장부호(마침표) 생략 권장
- 번역투 표현은 지양(강제 치환 없음)
  - 예: `계약` 대신 `규격/명세/형식/스키마` 같은 자연스러운 표현 권장

## 4) 본문(선택)
- 여러 변경이 섞였거나, 나중에 회고가 중요하면 본문을 2~5줄로 추가한다.
- 본문에는 다음 중 1개 이상을 권장:
  - 변경 이유(1줄)
  - 주요 변경 목록(불릿 2~4개)
  - Verify 커맨드(또는 결과) 요약

## 5) 예시
- `[Docs(rules)] Slice Ladder 규칙 추가(복잡 FR 과압축 방지)`
- `[Docs(workflow)] Infra 부트스트랩 템플릿 강화(venv/의존성/스모크)`
- `[Fix(collector)] 사람인 목록 파싱 셀렉터 보정(rec_idx 추출)`
- `[Refactor(service)] 중복 판별 정규화 로직 분리`
- `[CI] pytest 워크플로우 추가`

## 6) 금지 패턴(권장 금지)
- “update”, “misc”, “stuff” 같이 의미 없는 subject
- 커밋 1개에 완전히 다른 성격(Infra+Feature+Docs)을 무리하게 섞기
