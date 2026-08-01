"""enable pgvector extension

Revision ID: 69046f3a2679
Revises: ee80cf3f48c8
Create Date: 2026-08-01 09:00:25.604271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69046f3a2679'
down_revision: Union[str, Sequence[str], None] = 'ee80cf3f48c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS vector")
