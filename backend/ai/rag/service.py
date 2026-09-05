"""High-level RAG service for AgentVox."""

from __future__ import annotations

from ai.rag.retriever import RAGRetriever
from ai.services.embedding_service import embedding_service
from sqlalchemy.orm import Session


class RAGService:
    """Create and retrieve semantic document context."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.retriever = RAGRetriever(db)

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        resume_id: int | None = None,
        job_context_id: int | None = None,
    ) -> list[str]:
        """Retrieve relevant text for a query."""

        query_embedding = await embedding_service.embed(
            query
        )

        chunks = self.retriever.search(
            embedding=query_embedding,
            limit=limit,
            resume_id=resume_id,
            job_context_id=job_context_id,
        )

        return [
            chunk.content
            for chunk in chunks
        ]

    async def retrieve_context(
        self,
        query: str,
        limit: int = 5,
        resume_id: int | None = None,
        job_context_id: int | None = None,
    ) -> str:
        """Return retrieved chunks as a single context string."""

        chunks = await self.retrieve(
            query=query,
            limit=limit,
            resume_id=resume_id,
            job_context_id=job_context_id,
        )

        if not chunks:
            return ""

        return "\n\n---\n\n".join(chunks)
