from __future__ import annotations

from worker.ner import NERExtractor


class TestNERExtractor:
    def test_extract_returns_entities(self, ner_extractor: NERExtractor):
        mock_doc = ner_extractor._nlp.return_value
        mock_ent_1 = type("Ent", (), {"text": "Москва", "label_": "LOC"})()
        mock_ent_2 = type("Ent", (), {"text": "Путин", "label_": "PER"})()
        mock_doc.ents = [mock_ent_1, mock_ent_2]

        result = ner_extractor.extract("Путин посетил Москву")

        assert len(result) == 2
        assert {"text": "Москва", "label": "LOC", "count": 1} in result
        assert {"text": "Путин", "label": "PER", "count": 1} in result

    def test_extract_empty_text(self, ner_extractor: NERExtractor):
        mock_doc = ner_extractor._nlp.return_value
        mock_doc.ents = []

        result = ner_extractor.extract("")

        assert result == []

    def test_extract_aggregates_counts(self, ner_extractor: NERExtractor):
        mock_doc = ner_extractor._nlp.return_value
        ent = type("Ent", (), {"text": "Москва", "label_": "LOC"})()
        mock_doc.ents = [ent, ent]

        result = ner_extractor.extract("Москва — столица. Москва — большой город.")

        assert len(result) == 1
        assert result[0] == {"text": "Москва", "label": "LOC", "count": 2}

    def test_extract_multiple_labels(self, ner_extractor: NERExtractor):
        mock_doc = ner_extractor._nlp.return_value
        mock_entities = [
            type("Ent", (), {"text": "Россия", "label_": "LOC"})(),
            type("Ent", (), {"text": "Газпром", "label_": "ORG"})(),
            type("Ent", (), {"text": "Иванов", "label_": "PER"})(),
        ]
        mock_doc.ents = mock_entities

        result = ner_extractor.extract("Россия, Газпром и Иванов")

        assert len(result) == 3
        labels = {e["label"] for e in result}
        assert labels == {"LOC", "ORG", "PER"}

    def test_extract_text_only_title(self, ner_extractor: NERExtractor):
        mock_doc = ner_extractor._nlp.return_value
        mock_doc.ents = []

        result = ner_extractor.extract("Новость без именованных сущностей")

        assert result == []
