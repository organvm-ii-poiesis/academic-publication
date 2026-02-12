"""Citation graph construction and analysis.

Provides the CitationGraph for building and querying citation
relationships between publications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CitationEdge:
    """A directed citation from one publication to another."""

    citing_id: str
    cited_id: str
    context: str  # The sentence or paragraph where the citation appears


class CitationGraph:
    """Directed graph of citation relationships between publications.

    Supports adding citations, computing impact metrics, and
    finding citation chains.
    """

    def __init__(self) -> None:
        self._edges: list[CitationEdge] = []
        self._outgoing: dict[str, list[str]] = {}  # pub_id -> cited pub_ids
        self._incoming: dict[str, list[str]] = {}  # pub_id -> citing pub_ids

    @property
    def edge_count(self) -> int:
        """Return the number of citation edges."""
        return len(self._edges)

    def add_citation(self, citing_id: str, cited_id: str, context: str = "") -> CitationEdge:
        """Add a citation edge.

        Args:
            citing_id: The publication doing the citing.
            cited_id: The publication being cited.
            context: The citation context text.

        Returns:
            The created CitationEdge.
        """
        edge = CitationEdge(citing_id=citing_id, cited_id=cited_id, context=context)
        self._edges.append(edge)
        self._outgoing.setdefault(citing_id, []).append(cited_id)
        self._incoming.setdefault(cited_id, []).append(citing_id)
        return edge

    def get_citation_count(self, pub_id: str) -> int:
        """Return how many times a publication has been cited."""
        return len(self._incoming.get(pub_id, []))

    def get_references(self, pub_id: str) -> list[str]:
        """Return IDs of publications cited by the given publication."""
        return list(self._outgoing.get(pub_id, []))

    def get_citers(self, pub_id: str) -> list[str]:
        """Return IDs of publications that cite the given publication."""
        return list(self._incoming.get(pub_id, []))

    def compute_impact(self) -> dict[str, int]:
        """Compute citation count for all publications.

        Returns:
            Mapping of pub_id to citation count, sorted by count descending.
        """
        impact: dict[str, int] = {}
        for pub_id, citers in self._incoming.items():
            impact[pub_id] = len(citers)
        return dict(sorted(impact.items(), key=lambda x: x[1], reverse=True))

    def find_chain(self, start_id: str, end_id: str, max_depth: int = 5) -> list[str] | None:
        """Find a citation chain from start to end publication.

        Uses BFS to find the shortest path through citation edges.

        Args:
            start_id: Starting publication.
            end_id: Target publication.
            max_depth: Maximum chain length to search.

        Returns:
            List of pub_ids forming the chain, or None if not found.
        """
        if start_id == end_id:
            return [start_id]

        visited: set[str] = {start_id}
        queue: list[tuple[str, list[str]]] = [(start_id, [start_id])]

        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue

            for neighbor in self._outgoing.get(current, []):
                if neighbor == end_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None
