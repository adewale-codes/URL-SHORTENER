"""initial

Revision ID: 088b25135452
Revises: 
Create Date: 2024-02-20 12:08:38.080181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '088b25135452'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('original_url', sa.String, index=True),
        sa.Column('short_url', sa.String, index=True, unique=True),
        sa.Column('custom_alias', sa.String, index=True, nullable=True),
        sa.Column('click_count', sa.Integer, default=0),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('urls') 
