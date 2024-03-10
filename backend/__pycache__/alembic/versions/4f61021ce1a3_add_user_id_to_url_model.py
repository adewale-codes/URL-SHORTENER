"""Add user_id to URL model

Revision ID: 4f61021ce1a3
Revises: ded97447563c
Create Date: 2024-03-04 17:24:53.987220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f61021ce1a3'
down_revision: Union[str, None] = 'ded97447563c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the new column
    op.add_column('urls', sa.Column('user_id', sa.Integer(), nullable=True))


def downgrade():
    # Remove the column on rollback
    op.drop_column('urls', 'user_id')