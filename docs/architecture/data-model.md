# Data model

## news

- `id` — SERIAL PRIMARY KEY.
- `source` — VARCHAR, источник (ria, tass, kommersant).
- `title` — TEXT, заголовок новости.
- `link` — TEXT UNIQUE, ссылка на новость; единственный предохранитель от дублей.
- `published_at` — TIMESTAMP, дата публикации.
- `text` — TEXT, текст/описание новости.
- `created_at` — TIMESTAMP, дата добавления в систему.

## entities

- `id` — SERIAL PRIMARY KEY.
- `news_id` — INTEGER FOREIGN KEY, ссылка на новость.
- `text` — TEXT, текст сущности.
- `label` — VARCHAR, тип сущности (PER, ORG, LOC...).
- `count` — INTEGER, количество вхождений.
- `created_at` — TIMESTAMP, дата добавления.

## Дедупликация

Повторная доставка сообщения не должна создавать дубли. Гарантия обеспечивается уникальностью `news.link`.

## Отношения

`news` 1 → many `entities`.