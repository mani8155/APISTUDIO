"""mode_change

Revision ID: 009030bf78fe
Revises: c21397abbefc
Create Date: 2024-03-13 17:00:04.229624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009030bf78fe'
down_revision: Union[str, None] = 'c21397abbefc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_api_sql_id', table_name='api_sql')
    op.drop_table('api_sql')
    op.add_column('api_core', sa.Column('code_name', sa.Text(), nullable=True))
    op.add_column('api_core_migrations', sa.Column('code_name', sa.Text(), nullable=True))
    op.add_column('api_meta', sa.Column('python_file', sa.LargeBinary(), nullable=True))
    op.add_column('api_meta', sa.Column('code_name', sa.Text(), nullable=True))
    op.add_column('api_meta_migrations', sa.Column('code_name', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_meta_migrations', 'code_name')
    op.drop_column('api_meta', 'code_name')
    op.drop_column('api_meta', 'python_file')
    op.drop_column('api_core_migrations', 'code_name')
    op.drop_column('api_core', 'code_name')
    op.create_table('api_sql',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('psk_uid', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('api_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('api_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('api_method', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('db_connection', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('db_connection_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('api_schema', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sql_text', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('api_header_requests', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('api_header', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('api_header_property', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('document_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='api_sql_pkey')
    )
    op.create_index('ix_api_sql_id', 'api_sql', ['id'], unique=False)
    # ### end Alembic commands ###
