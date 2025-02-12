"""sc_01_post

Revision ID: bee0c2b13a47
Revises: cee79a84783d
Create Date: 2024-07-16 17:09:33.354618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bee0c2b13a47'
down_revision: Union[str, None] = 'cee79a84783d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sc_01_post', sa.Column('post_qty', sa.Integer(), nullable=True))
    op.add_column('sc_01_post', sa.Column('post_price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sc_01_post', 'post_price')
    op.drop_column('sc_01_post', 'post_qty')
    # ### end Alembic commands ###
