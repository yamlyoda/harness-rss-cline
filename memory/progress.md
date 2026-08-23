# Progress

Done:
- Created harness structure.
- Removed old `.clinerules` file from repository root.
- Filled docs and service-level AGENTS.md files.
- Verified real stack: NATS, FastStream, FastAPI, PostgreSQL, spaCy, Alembic.
- 002-harness-conformance: service AGENTS.md перенесены из `services/` в `monitor/AGENTS.md` и `worker/AGENTS.md`, каталог `services/` удалён.
- Создан `memory/decisions.md`; добавлен `.gitignore`, `.env` и байткод сняты с трекинга.

Remaining:
- Implement retry/backoff for feed errors.
- Add safe handling of broken XML content.
- Update technical debt after implementation.