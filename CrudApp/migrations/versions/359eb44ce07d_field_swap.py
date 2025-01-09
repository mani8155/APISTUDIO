"""field_swap

Revision ID: 359eb44ce07d
Revises: aa945c3e6a1a
Create Date: 2024-03-16 16:02:13.946176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '359eb44ce07d'
down_revision: Union[str, None] = 'aa945c3e6a1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_cms_page', 'api_code')
    op.drop_column('api_cms_page_migrations', 'api_code')
    op.drop_column('api_fields', 'field_property')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_fields', sa.Column('field_property', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('api_cms_page_migrations', sa.Column('api_code', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('api_cms_page', sa.Column('api_code', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
