"""am

Revision ID: c187a6ed9a44
Revises: 9a4d6a65a03e
Create Date: 2024-09-10 12:40:58.211111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c187a6ed9a44'
down_revision: Union[str, None] = '9a4d6a65a03e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('am', 'a1',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('am', 'a1',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###