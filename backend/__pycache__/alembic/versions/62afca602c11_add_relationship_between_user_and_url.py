"""add relationship between User and URL

Revision ID: 62afca602c11
Revises: 4f61021ce1a3
Create Date: 2024-03-04 17:28:12.789446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62afca602c11'
down_revision: Union[str, None] = '4f61021ce1a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_urls_custom_alias', table_name='urls')
    op.drop_index('ix_urls_original_url', table_name='urls')
    op.drop_index('ix_urls_short_url', table_name='urls')
    op.drop_table('urls')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('original_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('short_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('custom_alias', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('click_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('qr_code_path', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='urls_pkey')
    )
    op.create_index('ix_urls_short_url', 'urls', ['short_url'], unique=True)
    op.create_index('ix_urls_original_url', 'urls', ['original_url'], unique=False)
    op.create_index('ix_urls_custom_alias', 'urls', ['custom_alias'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('reset_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
