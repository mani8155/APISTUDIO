"""country

Revision ID: 40a3741b49b2
Revises: 07831f1dc9ba
Create Date: 2024-04-02 20:30:00.149805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a3741b49b2'
down_revision: Union[str, None] = '07831f1dc9ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('country', sa.Column('language', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('country', 'language')
    # ### end Alembic commands ###