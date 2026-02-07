# doc_index/indexer.py
"""High-level document indexing."""

from pathlib import Path

from doc_index.chunker import MarkdownChunker
from doc_index.embedder import AnthropicEmbedder
from doc_index.vector_store import DragonflyVectorStore


class DocumentIndexer:
    """Index documents into vector store."""

    def __init__(
        self,
        index_name: str = "docs",
        chunk_size: int = 1000,
        overlap: int = 200,
        embedding_dim: int = 768,
    ):
        """
        Initialize indexer.

        Args:
            index_name: Name for vector index
            chunk_size: Chunk size in characters
            overlap: Overlap between chunks
            embedding_dim: Embedding dimension
        """
        self.chunker = MarkdownChunker(chunk_size, overlap)
        self.embedder = AnthropicEmbedder()
        self.vector_store = DragonflyVectorStore(index_name=index_name)

        # Create index
        self.vector_store.create_index(embedding_dim)

        # Stats
        self._total_chunks = 0
        self._total_docs = 0

    def index_directory(self, directory: Path, pattern: str = "**/*.md") -> int:
        """
        Index all markdown files in directory.

        Args:
            directory: Directory to index
            pattern: Glob pattern for files

        Returns:
            Number of chunks indexed
        """
        chunks_indexed = 0

        for filepath in Path(directory).glob(pattern):
            if not filepath.is_file():
                continue

            # Read content
            content = filepath.read_text()

            # Chunk
            chunks = self.chunker.chunk(content, str(filepath))

            # Embed
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedder.embed_batch(texts)

            # Store
            for chunk, embedding in zip(chunks, embeddings):
                self.vector_store.add_chunk(chunk, embedding)
                chunks_indexed += 1

            self._total_docs += 1

        self._total_chunks = chunks_indexed
        return chunks_indexed

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Search for relevant chunks.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of matching chunks
        """
        # Embed query
        query_embedding = self.embedder.embed(query)

        # Search
        results = self.vector_store.search(query_embedding, top_k)

        return results

    def get_stats(self) -> dict:
        """Get indexer statistics."""
        return {
            "total_chunks": self._total_chunks,
            "total_docs": self._total_docs,
        }
