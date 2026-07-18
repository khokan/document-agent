"""Persistence helpers for PDFs that must survive vector-store resets."""

from datetime import datetime
from typing import List, Optional

from app.models.database import DocumentRecord, SessionLocal
from app.utils.config import config


class DocumentCatalog:
    def get(self, document_id: str) -> Optional[DocumentRecord]:
        with SessionLocal() as db:
            return db.get(DocumentRecord, document_id)

    def get_by_hash(self, file_hash: str) -> Optional[DocumentRecord]:
        with SessionLocal() as db:
            return db.query(DocumentRecord).filter(DocumentRecord.file_hash == file_hash).first()

    def list(self) -> List[DocumentRecord]:
        with SessionLocal() as db:
            return db.query(DocumentRecord).order_by(DocumentRecord.upload_date).all()

    def upsert(self, *, document_id: str, filename: str, file_path: str, file_hash: str,
               page_count: int, chunk_count: int, status: str = "indexed") -> None:
        with SessionLocal() as db:
            record = db.get(DocumentRecord, document_id)
            if record is None:
                record = DocumentRecord(document_id=document_id, filename=filename, file_path=file_path, file_hash=file_hash)
                db.add(record)
            record.filename, record.file_path, record.file_hash = filename, file_path, file_hash
            record.page_count, record.chunk_count, record.status = page_count, chunk_count, status
            record.embedding_fingerprint = config.embedding_profile_fingerprint
            record.upload_date = record.upload_date or datetime.utcnow()
            db.commit()

    def delete(self, document_id: str) -> None:
        with SessionLocal() as db:
            record = db.get(DocumentRecord, document_id)
            if record:
                db.delete(record)
                db.commit()


document_catalog = DocumentCatalog()
