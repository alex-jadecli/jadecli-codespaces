"""CLI for document indexing."""

from pathlib import Path

import click

from doc_index.indexer import DocumentIndexer


@click.group()
def cli():
    """Document indexing and search."""
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--index-name", default="docs", help="Index name")
@click.option("--chunk-size", default=1000, help="Chunk size")
def index(directory: str, index_name: str, chunk_size: int):
    """Index documentation directory."""
    click.echo(f"Indexing {directory}...")

    indexer = DocumentIndexer(
        index_name=index_name,
        chunk_size=chunk_size,
    )

    count = indexer.index_directory(Path(directory))

    click.echo(f"✓ Indexed {count} chunks")

    stats = indexer.get_stats()
    click.echo(f"  Total docs: {stats['total_docs']}")
    click.echo(f"  Total chunks: {stats['total_chunks']}")


@cli.command()
@click.argument("query")
@click.option("--index-name", default="docs", help="Index name")
@click.option("--top-k", default=5, help="Number of results")
def search(query: str, index_name: str, top_k: int):
    """Search indexed documentation."""
    indexer = DocumentIndexer(index_name=index_name)

    results = indexer.search(query, top_k)

    click.echo(f"Found {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        click.echo(f"{i}. {result['source']}")
        click.echo(f"   Score: {result.get('score', 'N/A')}")
        click.echo(f"   {result['content'][:100]}...")
        click.echo()


if __name__ == "__main__":
    cli()
