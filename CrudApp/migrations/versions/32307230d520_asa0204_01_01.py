"""asa0204_01_01

Revision ID: 32307230d520
Revises: 8b663af6977c
Create Date: 2024-03-28 17:35:35.004309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32307230d520'
down_revision: Union[str, None] = '8b663af6977c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asa0204_01_01', sa.Column('user_roles', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asa0204_01_01', 'user_roles')
    # ### end Alembic commands ###
