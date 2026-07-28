# RSS Cline — Event-Driven News Monitoring System

Система мониторинга новостей из RSS-лент российских информационных агентств с извлечением именованных сущностей (NER).

## Архитектура

```
RSS-ленты → Monitor (FastAPI) → NATS → Worker (FastStream + SpaCy) → PostgreSQL
```

- **Monitor** — опрашивает RSS-ленты раз в 5 минут (и по запросу `/refresh`), публикует новые записи в NATS.
- **NATS** — брокер сообщений (лёгкий, производительный, нативно поддерживается FastStream).
- **Worker** — потребляет сообщения из NATS через FastStream, запускает NER (SpaCy, `ru_core_news_sm`), записывает результат в PostgreSQL.
- **PostgreSQL** — хранит новости и извлечённые сущности.

## RSS-ленты

| Агентство     | URL                                                                 |
|---------------|---------------------------------------------------------------------|
| РИА Новости   | https://ria.ru/export/rss2/archive/index.xml                       |
| ТАСС          | https://tass.ru/rss/v2.xml                                          |
| Коммерсантъ   | https://www.kommersant.ru/RSS/news.xml                              |

Если какая-то лента недоступна, замените URL в переменных окружения (`RSS_URL_*`).

## Быстрый старт

1. Скопируйте `.env.example` в `.env` и при необходимости отредактируйте:
   ```bash
   cp .env.example .env
   ```

2. Запустите все сервисы:
   ```bash
   docker-compose up -d
   ```

3. Проверьте здоровье монитора:
   ```bash
   curl http://localhost:8000/health
   ```

4. Принудительный опрос RSS-лент:
   ```bash
   curl -X POST http://localhost:8000/refresh
   ```

## Эндпоинты Monitor

| Метод | Путь        | Описание                          |
|-------|-------------|-----------------------------------|
| GET   | `/health`   | Проверка состояния сервиса        |
| POST  | `/refresh`  | Внеочередной опрос всех RSS-лент  |

## Схема базы данных

### `news`
| Поле          | Тип         | Описание                        |
|---------------|-------------|---------------------------------|
| id            | SERIAL PK   | Идентификатор                   |
| source        | VARCHAR     | Источник (ria, tass, kommersant)|
| title         | TEXT        | Заголовок новости               |
| link          | TEXT UNIQUE | Ссылка на новость               |
| published_at  | TIMESTAMP   | Дата публикации                 |
| text          | TEXT        | Текст/описание новости          |
| created_at    | TIMESTAMP   | Дата добавления в систему       |

### `entities`
| Поле       | Тип         | Описание                        |
|------------|-------------|---------------------------------|
| id         | SERIAL PK   | Идентификатор                   |
| news_id    | INTEGER FK  | Ссылка на новость               |
| text       | TEXT        | Текст сущности                  |
| label      | VARCHAR     | Тип сущности (PER, ORG, LOC...) |
| count      | INTEGER     | Количество вхождений            |
| created_at | TIMESTAMP   | Дата добавления                 |

## Технологии

- **Python 3.12**
- **UV** — пакетный менеджер
- **Ruff** — форматтер и линтер
- **FastAPI** — HTTP-сервер монитора
- **FastStream** — фреймворк воркера (подписка на NATS)
- **NATS** — брокер сообщений
- **SpaCy** — NER (русскоязычная модель `ru_core_news_sm`)
- **PostgreSQL 16** — хранилище
- **Docker Compose** — оркестрация сервисов