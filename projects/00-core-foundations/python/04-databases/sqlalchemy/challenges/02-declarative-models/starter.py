"""
Challenge 02: Declarative Models — Starter Code
================================================
Implement build_model_versions_model(base): a ModelVersion class with
model_name/version/artifact_uri columns, a (model_name, version)
UniqueConstraint, a CheckConstraint(version >= 1), and a before_insert
event that rejects artifact_uri values not starting with "s3://".
"""

from __future__ import annotations


def build_model_versions_model(base: type) -> type:
    """Return a ModelVersion mapped class on the given declarative base.

    Gold tier requirements (implement all of them):
    - __tablename__ = "model_versions"
    - id PK, model_name String(80) NOT NULL, version int NOT NULL,
      artifact_uri String(300) NOT NULL
    - UniqueConstraint("model_name", "version")
    - CheckConstraint("version >= 1")
    - before_insert event raising ValueError unless artifact_uri
      starts with "s3://"
    """
    raise NotImplementedError
