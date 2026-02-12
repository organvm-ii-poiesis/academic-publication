"""Dataset cataloging and metadata management.

Provides the DatasetCatalog for registering research datasets
with structured metadata, versioning, and access tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Dataset:
    """A research dataset with metadata."""

    dataset_id: str
    name: str
    description: str
    format: str
    size_bytes: int
    version: str = "1.0.0"
    license: str = "CC-BY-4.0"
    tags: list[str] = field(default_factory=list)
    linked_publications: list[str] = field(default_factory=list)


class DatasetCatalog:
    """Catalog of research datasets with metadata and linking.

    Manages dataset registration, version tracking, and links
    to associated publications.
    """

    def __init__(self) -> None:
        self._datasets: dict[str, Dataset] = {}

    @property
    def count(self) -> int:
        """Return the number of datasets."""
        return len(self._datasets)

    def register(
        self,
        name: str,
        description: str,
        format: str,
        size_bytes: int,
        version: str = "1.0.0",
        license: str = "CC-BY-4.0",
        tags: list[str] | None = None,
    ) -> Dataset:
        """Register a new dataset.

        Args:
            name: Dataset name.
            description: Description of contents.
            format: File format (csv, json, parquet, etc.).
            size_bytes: Size in bytes.
            version: Semantic version string.
            license: License identifier.
            tags: Categorization tags.

        Returns:
            The newly registered Dataset.
        """
        dataset = Dataset(
            dataset_id=uuid4().hex[:10],
            name=name,
            description=description,
            format=format,
            size_bytes=size_bytes,
            version=version,
            license=license,
            tags=tags or [],
        )
        self._datasets[dataset.dataset_id] = dataset
        return dataset

    def link_publication(self, dataset_id: str, pub_id: str) -> bool:
        """Link a publication to a dataset.

        Args:
            dataset_id: The dataset to link.
            pub_id: The publication ID to associate.

        Returns:
            True if the dataset was found and linked.
        """
        dataset = self._datasets.get(dataset_id)
        if dataset is None:
            return False
        if pub_id not in dataset.linked_publications:
            dataset.linked_publications.append(pub_id)
        return True

    def search_by_tag(self, tag: str) -> list[Dataset]:
        """Find datasets with a specific tag."""
        return [d for d in self._datasets.values() if tag in d.tags]

    def get_total_size(self) -> int:
        """Return total size of all datasets in bytes."""
        return sum(d.size_bytes for d in self._datasets.values())

    def export(self) -> list[dict[str, Any]]:
        """Export the catalog as a list of dicts."""
        return [
            {
                "dataset_id": d.dataset_id,
                "name": d.name,
                "format": d.format,
                "size_bytes": d.size_bytes,
                "version": d.version,
                "tags": d.tags,
                "linked_publications": d.linked_publications,
            }
            for d in self._datasets.values()
        ]
