"""store price as NUMERIC(10, 2) instead of float

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-03
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Float(),
            type_=sa.Numeric(10, 2),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Numeric(10, 2),
            type_=sa.Float(),
            existing_nullable=False,
        )
