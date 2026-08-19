from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import Document

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    workspace_id: Mapped[str] = mapped_column(String(36), nullable=False)

    chunk_index: Mapped[int]

    page_number: Mapped[int]

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    text: Mapped[str] = mapped_column(
        Text
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks"
    )