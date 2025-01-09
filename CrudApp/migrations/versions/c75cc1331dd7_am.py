"""am

Revision ID: c75cc1331dd7
Revises: 4bac0e27a5e8
Create Date: 2024-09-10 12:15:47.102409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c75cc1331dd7'
down_revision: Union[str, None] = '4bac0e27a5e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('am', sa.Column('demo', sa.String(), nullable=True))
    op.add_column('am', sa.Column('demo1', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('am', 'demo1')
    op.drop_column('am', 'demo')
    # ### end Alembic commands ###
