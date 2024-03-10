"""create_user_table

Revision ID: 10694f22c466
Revises: 12eb40be3411
Create Date: 2024-02-29 16:52:35.034489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10694f22c466'
down_revision: Union[str, None] = '12eb40be3411'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
    )


def downgrade():
    op.drop_table('users')
