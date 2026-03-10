"""Tests for the publication module."""

from src.publication import PublicationManager


class TestPublicationManager:
    def test_add_publication(self) -> None:
        mgr = PublicationManager()
        pub = mgr.add("Test Paper", ["Author A"], 2025, "NeurIPS")
        assert pub.title == "Test Paper"
        assert mgr.count == 1

    def test_get_publication(self) -> None:
        mgr = PublicationManager()
        pub = mgr.add("Paper", ["A"], 2025, "ICML")
        result = mgr.get(pub.pub_id)
        assert result is not None
        assert result.title == "Paper"

    def test_get_unknown_returns_none(self) -> None:
        mgr = PublicationManager()
        assert mgr.get("fake") is None

    def test_search_by_keyword_in_title(self) -> None:
        mgr = PublicationManager()
        mgr.add("Machine Learning Survey", ["A"], 2025, "Nature")
        mgr.add("Quantum Computing", ["B"], 2024, "Science")
        results = mgr.search_by_keyword("machine")
        assert len(results) == 1
        assert results[0].title == "Machine Learning Survey"

    def test_search_by_keyword_in_keywords(self) -> None:
        mgr = PublicationManager()
        mgr.add("Paper A", ["A"], 2025, "Venue", keywords=["recursion", "theory"])
        results = mgr.search_by_keyword("recursion")
        assert len(results) == 1

    def test_filter_by_author(self) -> None:
        mgr = PublicationManager()
        mgr.add("Paper 1", ["Smith", "Jones"], 2025, "V1")
        mgr.add("Paper 2", ["Jones", "Lee"], 2025, "V2")
        mgr.add("Paper 3", ["Lee"], 2025, "V3")
        results = mgr.filter_by_author("Jones")
        assert len(results) == 2

    def test_get_venues(self) -> None:
        mgr = PublicationManager()
        mgr.add("P1", ["A"], 2025, "NeurIPS")
        mgr.add("P2", ["B"], 2025, "NeurIPS")
        mgr.add("P3", ["C"], 2025, "ICML")
        venues = mgr.get_venues()
        assert venues["NeurIPS"] == 2
        assert venues["ICML"] == 1
