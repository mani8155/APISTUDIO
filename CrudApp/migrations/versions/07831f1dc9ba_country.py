"""country

Revision ID: 07831f1dc9ba
Revises: 376bce88f497
Create Date: 2024-04-02 20:27:07.964035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07831f1dc9ba'
down_revision: Union[str, None] = '376bce88f497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('asa0202_01_01', 'menu_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('asa0202_01_01', 'menu_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('asa0204_01_01', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('asa0204_01_01_username_key', 'asa0204_01_01', type_='unique')
    op.add_column('country', sa.Column('region', sa.Text(), nullable=True))
    op.drop_constraint('gmc1202_01_01_username_key', 'gmc1202_01_01', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('gmc1202_01_01_username_key', 'gmc1202_01_01', ['username'])
    op.drop_column('country', 'region')
    op.create_unique_constraint('asa0204_01_01_username_key', 'asa0204_01_01', ['username'])
    op.alter_column('asa0204_01_01', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('asa0202_01_01', 'menu_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('asa0202_01_01', 'menu_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
