"""asa0203_01_01

Revision ID: 0111e3f3edbc
Revises: 6169d135e9f2
Create Date: 2024-04-04 10:50:36.101278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0111e3f3edbc'
down_revision: Union[str, None] = '6169d135e9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asa0203_01_01', 'menu_privilege_grouping')
    op.drop_column('asa0203_01_01', 'menu_privilege_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asa0203_01_01', sa.Column('menu_privilege_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('asa0203_01_01', sa.Column('menu_privilege_grouping', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
