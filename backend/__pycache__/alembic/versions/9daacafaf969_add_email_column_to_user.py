"""Add email column to User

Revision ID: 9daacafaf969
Revises: 10694f22c466
Create Date: 2024-03-01 18:52:18.156032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9daacafaf969'
down_revision: Union[str, None] = '10694f22c466'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('email', sa.String(), unique=True, index=True))


def downgrade():
    op.drop_column('users', 'email')
