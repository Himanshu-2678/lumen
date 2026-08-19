"""add workspace isolation to documents and chunks

Revision ID: c3a1b7e9d2f4
Revises: 84fbd72ab35e
Create Date: 2026-08-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3a1b7e9d2f4"
down_revision: Union[str, Sequence[str], None] = "84fbd72ab35e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "documents",
        sa.Column(
            "workspace_id",
            sa.String(length=36),
            nullable=False,
            server_default="legacy",
        ),
    )
    inspector = sa.inspect(op.get_bind())
    unique_constraints = inspector.get_unique_constraints("documents")
    for constraint in unique_constraints:
        columns = constraint.get("column_names") or []
        if columns == ["document_hash"]:
            op.drop_constraint(
                constraint["name"],
                "documents",
                type_="unique",
            )
            break
    op.create_unique_constraint(
        "uq_documents_workspace_hash",
        "documents",
        ["workspace_id", "document_hash"],
    )
    op.alter_column("documents", "workspace_id", server_default=None)

    op.add_column(
        "chunks",
        sa.Column(
            "workspace_id",
            sa.String(length=36),
            nullable=False,
            server_default="legacy",
        ),
    )
    op.alter_column("chunks", "workspace_id", server_default=None)


def downgrade() -> None:
    op.drop_column("chunks", "workspace_id")
    op.drop_constraint(
        "uq_documents_workspace_hash",
        "documents",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_documents_document_hash",
        "documents",
        ["document_hash"],
    )
    op.drop_column("documents", "workspace_id")
