"""am

Revision ID: 0e0791841117
Revises: 8490e2b9f335
Create Date: 2024-09-10 15:33:13.887225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e0791841117'
down_revision: Union[str, None] = '8490e2b9f335'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('am', sa.Column('a3', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('am', 'a3')
    # ### end Alembic commands ###
