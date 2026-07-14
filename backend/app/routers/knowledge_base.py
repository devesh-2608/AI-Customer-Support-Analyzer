from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from ..database import get_db, KBDocument
from ..services import rag

router = APIRouter(prefix="/api/kb", tags=["knowledge-base"])

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunk_count = rag.ingest_document(filepath, file.filename)

    doc = KBDocument(filename=file.filename, chunk_count=chunk_count)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"filename": file.filename, "chunks_stored": chunk_count}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(KBDocument).all()
    return [{"filename": d.filename, "chunks": d.chunk_count, "uploaded_at": d.uploaded_at} for d in docs]
