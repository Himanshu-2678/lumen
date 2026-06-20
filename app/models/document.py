from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(
        String(50),
        default="uploaded"
    )