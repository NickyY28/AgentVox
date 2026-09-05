"""Index resume and job context content into pgvector."""

from __future__ import annotations

from ai.rag.chunker import chunk_text
from ai.services.embedding_service import embedding_service
from models.document_chunk import DocumentChunk
from sqlalchemy.orm import Session


class RAGIndexingService:
    """Create searchable vector chunks."""

    def __init__(self, db: Session) -> None:
        self.db = db

    async def index_resume(self, resume_id: int, text: str,) -> int:
        """Index resume text."""

        chunks = chunk_text(text)

        if not chunks:
            return 0

        embeddings = await embedding_service.embed_many(
            chunks
        )

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            document = DocumentChunk(
                resume_id=resume_id,
                source_type="resume",
                chunk_index=index,
                content=chunk,
                embedding=embedding,
                metadata={
                    "source": "resume",
                    "resume_id": resume_id,
                },
            )

            self.db.add(document)

        self.db.commit()
        return len(chunks)

    async def index_job_context(self, job_context_id: int, text: str) -> int:
        """Index job description/context text."""

        chunks = chunk_text(text)

        if not chunks:
            return 0

        embeddings = await embedding_service.embed_many(chunks)

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            document = DocumentChunk(
                job_context_id=job_context_id,
                source_type="job_context",
                chunk_index=index,
                content=chunk,
                embedding=embedding,
                metadata={
                    "source": "job_context",
                    "job_context_id": job_context_id,
                },
            )

            self.db.add(document)
        self.db.commit()
        return len(chunks)
