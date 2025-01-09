"""table field Change

Revision ID: c35c20beb763
Revises: 685aaf75cec6
Create Date: 2024-02-14 10:51:05.057541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c35c20beb763'
down_revision: Union[str, None] = '685aaf75cec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_cms_page', sa.Column('api_code', sa.Text(), nullable=True))
    op.drop_column('api_cms_page', 'python_code')
    op.add_column('api_cms_page_migrations', sa.Column('api_code', sa.Text(), nullable=True))
    op.add_column('api_cms_page_migrations', sa.Column('api_file', sa.LargeBinary(), nullable=True))
    op.drop_column('api_cms_page_migrations', 'python_file')
    op.drop_column('api_cms_page_migrations', 'python_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_cms_page_migrations', sa.Column('python_code', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('api_cms_page_migrations', sa.Column('python_file', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('api_cms_page_migrations', 'api_file')
    op.drop_column('api_cms_page_migrations', 'api_code')
    op.add_column('api_cms_page', sa.Column('python_code', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('api_cms_page', 'api_code')
    # ### end Alembic commands ###