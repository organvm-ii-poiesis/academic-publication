"""Publication metadata management.

Provides the PublicationManager for creating, searching, and organizing
academic publications with structured metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from uuid import uuid4
@dataclass
class Publication:
    """Represents a single academic publication."""

    pub_id: str
    title: str
    authors: list[str]
    year: int
    venue: str
    doi: str | None = None
    abstract: str = ""
    keywords: list[str] = field(default_factory=list)
    created_at: str = ""
class PublicationManager:
    """Manages a collection of academic publications.

    Provides CRUD operations, keyword search, and author filtering
    for a corpus of academic publications.
    """

    def __init__(self) -> None:
        self._publications: dict[str, Publication] = {}

    @property
    def count(self) -> int:
        """Return the number of publications."""
        return len(self._publications)

    def add(
        self,
        title: str,
        authors: list[str],
        year: int,
        venue: str,
        doi: str | None = None,
        abstract: str = "",
        keywords: list[str] | None = None,
    ) -> Publication:
        """Add a new publication.

        Args:
            title: Publication title.
            authors: List of author names.
            year: Publication year.
            venue: Journal or conference name.
            doi: Digital Object Identifier.
            abstract: Publication abstract.
            keywords: Subject keywords.

        Returns:
            The newly created Publication.
        """
        pub = Publication(
            pub_id=uuid4().hex[:10],
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            doi=doi,
            abstract=abstract,
            keywords=keywords or [],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._publications[pub.pub_id] = pub
        return pub

    def get(self, pub_id: str) -> Publication | None:
        """Retrieve a publication by ID."""
        return self._publications.get(pub_id)

    def search_by_keyword(self, keyword: str) -> list[Publication]:
        """Find publications matching a keyword in title, abstract, or keywords.

        Args:
            keyword: Search term (case-insensitive).

        Returns:
            List of matching publications.
        """
        term = keyword.lower()
        results: list[Publication] = []
        for pub in self._publications.values():
            if (
                term in pub.title.lower()
                or term in pub.abstract.lower()
                or any(term in k.lower() for k in pub.keywords)
            ):
                results.append(pub)
        return results

    def filter_by_author(self, author_name: str) -> list[Publication]:
        """Find all publications by a specific author.

        Args:
            author_name: Author name to match (case-insensitive).

        Returns:
            List of publications by the author.
        """
        name = author_name.lower()
        return [
            pub for pub in self._publications.values()
            if any(name in a.lower() for a in pub.authors)
        ]

    def get_venues(self) -> dict[str, int]:
        """Return a frequency map of publication venues."""
        venues: dict[str, int] = {}
        for pub in self._publications.values():
            venues[pub.venue] = venues.get(pub.venue, 0) + 1
        return venues
