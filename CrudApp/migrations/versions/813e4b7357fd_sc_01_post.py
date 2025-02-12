"""sc_01_post

Revision ID: 813e4b7357fd
Revises: cf2a46e0195f
Create Date: 2024-07-15 14:27:41.954787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '813e4b7357fd'
down_revision: Union[str, None] = 'cf2a46e0195f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sc_01_post', sa.Column('uom', sa.Integer(), nullable=True))
    op.add_column('sc_01_post', sa.Column('category', sa.Integer(), nullable=True))
    op.add_column('sc_01_post', sa.Column('subcategory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sc_01_post', 'subcategory')
    op.drop_column('sc_01_post', 'category')
    op.drop_column('sc_01_post', 'uom')
    # ### end Alembic commands ###
