"""Add qr_code_path column

Revision ID: 12eb40be3411
Revises: 088b25135452
Create Date: 2024-02-23 23:28:36.697567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12eb40be3411'
down_revision: Union[str, None] = '088b25135452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column
    op.add_column('urls', sa.Column('qr_code_path', sa.String, nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # Remove the column
    op.drop_column('urls', 'qr_code_path')
    # ### end Alembic commands ###
