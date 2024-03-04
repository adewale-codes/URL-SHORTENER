"""create_user_table

Revision ID: db03c70f29f7
Revises: 1bb02dd6af96
Create Date: 2024-03-04 22:37:54.871504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db03c70f29f7'
down_revision: Union[str, None] = '1bb02dd6af96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('email', sa.String(), unique=True, index=True),
        sa.Column('reset_token', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('users')
