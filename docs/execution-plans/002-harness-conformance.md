# 002-harness-conformance

Status: done  
Version: 1

## Цель

Привести структуру репозитория в соответствие с `HARNESSTREE.md` и указателями корневого `AGENTS.md`.

## Задачи

- [x] Перенести содержимое `services/monitor/AGENTS.md` в пустой `monitor/AGENTS.md`.
- [x] Перенести содержимое `services/worker/AGENTS.md` в новый `worker/AGENTS.md`.
- [x] Удалить каталог `services/`, отсутствующий в дереве harness.
- [x] Создать отсутствующий `memory/decisions.md` (ссылается `docs/principles/agent-workflow.md`).
- [x] Добавить `.gitignore`; снять с трекинга `.env` и `__pycache__/*.pyc`.
- [x] Обновить `memory/progress.md` и `memory/active-context.md`.

## Критерии готовности

- Все пути из корневого `AGENTS.md` и `HARNESSTREE.md` существуют и непусты.
- Битых ссылок между markdown-документами нет.
