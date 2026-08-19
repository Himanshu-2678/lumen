from sqlalchemy.orm import Session

from app.models.chunk import Chunk


def save_chunks(
    db: Session,
    chunks: list[dict],
):
    db_chunks = []

    for chunk in chunks:

        db_chunk = Chunk(
            document_id=chunk["document_id"],
            workspace_id=chunk["workspace_id"],
            filename=chunk["filename"],
            page_number=chunk["page_number"],
            chunk_index=chunk["chunk_index"],
            text=chunk["text"],
        )

        db_chunks.append(db_chunk)

    db.add_all(db_chunks)
    db.commit()

    return db_chunks


def get_all_chunks(db: Session):
    return db.query(Chunk).all()