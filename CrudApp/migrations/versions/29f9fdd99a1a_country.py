""""country"

Revision ID: 29f9fdd99a1a
Revises: fa1cf20c17f9
Create Date: 2024-01-08 15:54:20.921320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29f9fdd99a1a'
down_revision: Union[str, None] = 'fa1cf20c17f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('country', sa.Column('Demo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('country', 'Demo')
    # ### end Alembic commands ###
