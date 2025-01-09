"""deepakupdate

Revision ID: 7d7da47bddeb
Revises: 8363f4fa6b40
Create Date: 2024-04-04 17:44:09.658892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d7da47bddeb'
down_revision: Union[str, None] = '8363f4fa6b40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_fields', sa.Column('field_select', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_fields', 'field_select')
    # ### end Alembic commands ###