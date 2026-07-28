from __future__ import annotations

from collections import Counter

import spacy
from spacy.language import Language


class NERExtractor:
    def __init__(self, model: str = "ru_core_news_sm") -> None:
        self._nlp: Language = spacy.load(model)

    def extract(self, text: str) -> list[dict]:
        doc = self._nlp(text)
        entities: list[tuple[str, str]] = [(ent.text, ent.label_) for ent in doc.ents]
        counter = Counter(entities)
        return [
            {"text": ent_text, "label": label, "count": count}
            for (ent_text, label), count in counter.items()
        ]
