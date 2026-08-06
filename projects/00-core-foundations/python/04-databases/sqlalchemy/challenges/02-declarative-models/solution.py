"""
Challenge 02: Declarative Models — Reference Solution
======================================================
Why this approach: constraints live in the SCHEMA (unique, check) so
the database enforces them for every writer; the before_insert event
handles the rule that is application policy, not schema (uri scheme).
"""

from __future__ import annotations

from sqlalchemy import CheckConstraint, String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column


def build_model_versions_model(base: type) -> type:
    """Return a ModelVersion mapped class with schema + event constraints."""

    class ModelVersion(base):
        __tablename__ = "model_versions"
        __table_args__ = (
            UniqueConstraint("model_name", "version", name="uq_model_version"),
            CheckConstraint("version >= 1", name="ck_version_positive"),
        )

        id: Mapped[int] = mapped_column(primary_key=True)
        model_name: Mapped[str] = mapped_column(String(80), nullable=False)
        version: Mapped[int] = mapped_column(nullable=False)
        artifact_uri: Mapped[str] = mapped_column(String(300), nullable=False)

    @event.listens_for(ModelVersion, "before_insert")
    def _require_s3_uri(mapper, connection, target) -> None:
        if not target.artifact_uri.startswith("s3://"):
            raise ValueError(f"artifact_uri must start with s3://: {target.artifact_uri}")

    return ModelVersion
