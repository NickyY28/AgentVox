"""Vector similarity retrieval for AgentVox."""

from __future__ import annotations

from models.document_chunk import DocumentChunk
from sqlalchemy import select
from sqlalchemy.orm import Session


class RAGRetriever:
    """Retrieve relevant document chunks using pgvector."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
        resume_id: int | None = None,
        job_context_id: int | None = None,
    ) -> list[DocumentChunk]:
        """Return the most relevant document chunks."""

        distance = DocumentChunk.embedding.cosine_distance(
            embedding
        )

        statement = (
            select(DocumentChunk)
            .order_by(distance)
            .limit(limit)
        )

        if resume_id is not None:
            statement = statement.where(
                DocumentChunk.resume_id == resume_id
            )

        if job_context_id is not None:
            statement = statement.where(
                DocumentChunk.job_context_id == job_context_id
            )

        return list(
            self.db.scalars(statement).all()
        )
