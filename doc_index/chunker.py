"""Chunk markdown documents for embedding."""

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class DocumentChunk:
    """A chunk of a document."""
    chunk_id: str
    source: str
    content: str
    start_pos: int
    end_pos: int


class MarkdownChunker:
    """Chunk markdown files with overlap."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize chunker.

        Args:
            chunk_size: Target size in characters
            overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, content: str, source: str) -> list[DocumentChunk]:
        """
        Chunk content with overlap.

        Args:
            content: Markdown content to chunk
            source: Source file path

        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0

        while start < len(content):
            # Calculate end position
            end = min(start + self.chunk_size, len(content))

            # Extract chunk
            chunk_content = content[start:end]

            # Create chunk object
            chunk = DocumentChunk(
                chunk_id=str(uuid4()),
                source=source,
                content=chunk_content,
                start_pos=start,
                end_pos=end,
            )
            chunks.append(chunk)

            # Move start position (with overlap)
            start = end - self.overlap

            # Avoid infinite loop if overlap >= chunk_size
            if start <= chunks[-1].start_pos if len(chunks) > 1 else False:
                break

        return chunks
