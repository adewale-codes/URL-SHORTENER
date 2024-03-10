"""Add reset_token to User

Revision ID: ded97447563c
Revises: 9daacafaf969
Create Date: 2024-03-01 19:03:36.451834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ded97447563c'
down_revision: Union[str, None] = '9daacafaf969'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'reset_token')
