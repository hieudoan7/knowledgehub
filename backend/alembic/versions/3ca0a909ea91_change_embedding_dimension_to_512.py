"""change embedding dimension to 512

Revision ID: 3ca0a909ea91
Revises: 23e6e22a4204
Create Date: 2026-08-20 21:33:32.248830

"""
from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ca0a909ea91'
down_revision: Union[str, Sequence[str], None] = '23e6e22a4204'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "document_chunks",
        "embedding",
        type_=Vector(512),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "document_chunks",
        "embedding",
        type_=Vector(384),
        existing_nullable=True,
    )