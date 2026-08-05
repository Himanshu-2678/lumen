from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    chunk_index: Mapped[int]

    page_number: Mapped[int]

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    text: Mapped[str] = mapped_column(
        Text
    )