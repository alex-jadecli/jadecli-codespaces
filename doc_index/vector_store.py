"""Vector storage using Dragonfly/Redis."""

import redis

from doc_index.chunker import DocumentChunk


class DragonflyVectorStore:
    """Store and search document embeddings in Dragonfly."""

    def __init__(self, host: str = "localhost", port: int = 6379, index_name: str = "docs"):
        """
        Initialize vector store.

        Args:
            host: Redis host
            port: Redis port
            index_name: Name for the vector index
        """
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.index_name = index_name
        self._dimension = None

    def create_index(self, dimension: int):
        """
        Create vector index if it doesn't exist.

        Args:
            dimension: Embedding dimension
        """
        self._dimension = dimension

        # Check if index exists
        if self.index_exists():
            return

        # Create index using RediSearch
        # FT.CREATE idx_name ON HASH PREFIX 1 doc: SCHEMA ...
        try:
            self.client.execute_command(
                "FT.CREATE", self.index_name,
                "ON", "HASH",
                "PREFIX", "1", f"doc:{self.index_name}:",
                "SCHEMA",
                "chunk_id", "TEXT",
                "source", "TEXT",
                "content", "TEXT",
                "embedding", "VECTOR", "FLAT", "6",
                "TYPE", "FLOAT32",
                "DIM", str(dimension),
                "DISTANCE_METRIC", "COSINE"
            )
        except redis.exceptions.ResponseError as e:
            if "Index already exists" not in str(e):
                raise

    def index_exists(self) -> bool:
        """Check if index exists."""
        try:
            self.client.execute_command("FT.INFO", self.index_name)
            return True
        except redis.exceptions.ResponseError:
            return False

    def add_chunk(self, chunk: DocumentChunk, embedding: list[float]):
        """
        Add chunk with embedding to store.

        Args:
            chunk: Document chunk
            embedding: Embedding vector
        """
        key = f"doc:{self.index_name}:{chunk.chunk_id}"

        # Convert embedding to bytes
        import struct
        embedding_bytes = struct.pack(f'{len(embedding)}f', *embedding)

        # Store as hash
        self.client.hset(key, mapping={
            "chunk_id": chunk.chunk_id,
            "source": chunk.source,
            "content": chunk.content,
            "start_pos": chunk.start_pos,
            "end_pos": chunk.end_pos,
            "embedding": embedding_bytes,
        })

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        """
        Search for similar chunks.

        Args:
            query_vector: Query embedding
            top_k: Number of results to return

        Returns:
            List of chunks with scores
        """
        import struct
        query_bytes = struct.pack(f'{len(query_vector)}f', *query_vector)

        # FT.SEARCH idx "*=>[KNN k @embedding $vec]" PARAMS 2 vec <blob> DIALECT 2
        try:
            result = self.client.execute_command(
                "FT.SEARCH", self.index_name,
                f"*=>[KNN {top_k} @embedding $vec AS score]",
                "PARAMS", "2", "vec", query_bytes,
                "SORTBY", "score",
                "DIALECT", "2",
                "RETURN", "4", "chunk_id", "source", "content", "score"
            )

            # Parse results
            # Format: [count, key1, fields1, key2, fields2, ...]
            _count = result[0]  # noqa: F841
            results = []

            for i in range(1, len(result), 2):
                _key = result[i]  # noqa: F841
                fields = result[i + 1]

                # fields is list: [field1, value1, field2, value2, ...]
                doc = {}
                for j in range(0, len(fields), 2):
                    doc[fields[j]] = fields[j + 1]

                results.append(doc)

            return results

        except redis.exceptions.ResponseError as e:
            # Index might not exist yet
            if "no such index" in str(e).lower():
                return []
            raise

    def delete_index(self):
        """Delete the index."""
        try:
            self.client.execute_command("FT.DROPINDEX", self.index_name, "DD")
        except redis.exceptions.ResponseError:
            pass  # Index doesn't exist
