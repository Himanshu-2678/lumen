"""add document metadata fields

Revision ID: f6e19b06896d
Revises: 
Create Date: 2026-08-08 23:27:44.706788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6e19b06896d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "documents",
        sa.Column(
            "document_hash",
            sa.String(length=64),
            nullable=True
        )
    )

    op.add_column(
        "documents",
        sa.Column(
            "chunk_count",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )

    op.add_column(
        "documents",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )

    op.add_column(
        "documents",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True
        )
    )

    op.create_unique_constraint(
        "uq_documents_document_hash",
        "documents",
        ["document_hash"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_constraint(
        "uq_documents_document_hash",
        "documents",
        type_="unique"
    )

    op.drop_column(
        "documents",
        "updated_at"
    )

    op.drop_column(
        "documents",
        "created_at"
    )

    op.drop_column(
        "documents",
        "chunk_count"
    )

    op.drop_column(
        "documents",
        "document_hash"
    )
    # ### end Alembic commands ###
