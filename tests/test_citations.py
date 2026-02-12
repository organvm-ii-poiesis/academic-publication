"""Tests for the citations module."""

from src.citations import CitationGraph


class TestCitationGraph:
    def test_add_citation(self) -> None:
        graph = CitationGraph()
        edge = graph.add_citation("a", "b", "As shown by B...")
        assert edge.citing_id == "a"
        assert graph.edge_count == 1

    def test_citation_count(self) -> None:
        graph = CitationGraph()
        graph.add_citation("a", "b")
        graph.add_citation("c", "b")
        assert graph.get_citation_count("b") == 2
        assert graph.get_citation_count("a") == 0

    def test_get_references(self) -> None:
        graph = CitationGraph()
        graph.add_citation("a", "b")
        graph.add_citation("a", "c")
        refs = graph.get_references("a")
        assert "b" in refs
        assert "c" in refs

    def test_get_citers(self) -> None:
        graph = CitationGraph()
        graph.add_citation("x", "z")
        graph.add_citation("y", "z")
        citers = graph.get_citers("z")
        assert "x" in citers
        assert "y" in citers

    def test_compute_impact(self) -> None:
        graph = CitationGraph()
        graph.add_citation("a", "c")
        graph.add_citation("b", "c")
        graph.add_citation("a", "d")
        impact = graph.compute_impact()
        assert impact["c"] == 2
        assert impact["d"] == 1

    def test_find_chain(self) -> None:
        graph = CitationGraph()
        graph.add_citation("a", "b")
        graph.add_citation("b", "c")
        chain = graph.find_chain("a", "c")
        assert chain == ["a", "b", "c"]

    def test_find_chain_returns_none_when_no_path(self) -> None:
        graph = CitationGraph()
        graph.add_citation("a", "b")
        assert graph.find_chain("a", "z") is None
