"""am

Revision ID: 8233dbea564b
Revises: f38ea5b1c184
Create Date: 2024-09-10 15:48:31.801594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8233dbea564b'
down_revision: Union[str, None] = 'f38ea5b1c184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('am', sa.Column('a4', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('am', 'a4')
    # ### end Alembic commands ###
