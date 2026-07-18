"""Rebuild the active Chroma collection from the durable PDF catalog.

Run: python -m app.maintenance.reindex --confirm
"""

import argparse
import asyncio
from pathlib import Path

from app.api.deps import embedding_service, vector_service
from app.chunking.splitter import ChunkSplitter
from app.pdf import PDFExtractor, TextCleaner
from app.services.document_catalog import document_catalog


async def rebuild() -> None:
    records = document_catalog.list()
    if not records:
        raise RuntimeError("No catalogued PDFs are available for reindexing")
    await vector_service.reset_for_reindex()
    try:
        for record in records:
            if not Path(record.file_path).exists():
                raise RuntimeError(f"Catalogued PDF is missing: {record.document_id}")
            success, pages = PDFExtractor.extract_text_by_page(record.file_path)
            cleaned = TextCleaner.clean_pages(pages) if success else {}
            if not cleaned:
                raise RuntimeError(f"Could not extract content for: {record.document_id}")
            chunks = ChunkSplitter().split_document(record.document_id, cleaned, {"filename": record.filename})
            vectors = await embedding_service.aembed_documents([chunk["text"] for chunk in chunks])
            await vector_service.add_chunks(chunks, vectors, allow_reindex=True)
            document_catalog.upsert(document_id=record.document_id, filename=record.filename,
                                    file_path=record.file_path, file_hash=record.file_hash,
                                    page_count=len(cleaned), chunk_count=len(chunks), status="reindexed")
        await vector_service.mark_reindex_complete()
    except Exception:
        # Collection remains marked reindexing and therefore unavailable rather than mixed/partially searchable.
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Destructively rebuild the active embedding index")
    parser.add_argument("--confirm", action="store_true", help="Required acknowledgement before clearing the collection")
    args = parser.parse_args()
    if not args.confirm:
        parser.error("--confirm is required because this clears the active Chroma collection")
    asyncio.run(rebuild())


if __name__ == "__main__":
    main()
