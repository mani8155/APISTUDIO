"""country

Revision ID: 0e40a9a138ae
Revises: 3820021aa1a4
Create Date: 2024-06-12 12:38:16.863989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e40a9a138ae'
down_revision: Union[str, None] = '3820021aa1a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('country', sa.Column('demo5', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('country', 'demo5')
    # ### end Alembic commands ###
