"""am

Revision ID: 9a4d6a65a03e
Revises: 1c5022868398
Create Date: 2024-09-10 12:40:20.223187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4d6a65a03e'
down_revision: Union[str, None] = '1c5022868398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('am', sa.Column('a2', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('am', 'a2')
    # ### end Alembic commands ###