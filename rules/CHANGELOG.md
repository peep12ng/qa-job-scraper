## v0.3.1 - 2026-02-11
- generate_tasks: Slice Ladder(DISC/CORE/INT) 규칙 추가로 과압축 누락 방지
- generate_tasks: Infra Bootstrap(venv/의존성/형상관리/스모크) 템플릿 강화
- process_task_lists: Architecture Rails 추가(core/tools 경계 선언)
- process_task_lists/policy: Large Payload fixtures 규칙 추가(HTML/JSON 전문 공유 금지)
- process_task_lists/policy: Scaffold-first 규칙 추가(자동 생성 우선)
- policies: commit_message_policy 추가(커밋 메시지 형식 표준화)

## v0.2 - 2026-02-05
- Add PROJECT_SHELL default + shell-single-source rule for Verify/Operator Steps
- Split Verify into Local (mandatory) / Remote (only if pushed); remove commit/push from Verify flow
- Enforce gate: no Commit Text / checkbox updates before Local Verify PASS
- Stabilize Paste Blocks: md full text is not wrapped in code fences
- Add (optional) TOOLING_HINTS metadata and Korean tone guidance (recommended)

## v0.1 - 2026-02-01
- Add ENV_SPEC for Codex (rules, output contract, SDLC gates)
- Add human-readable operating guide

