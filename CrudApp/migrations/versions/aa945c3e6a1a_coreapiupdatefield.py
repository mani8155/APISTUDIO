"""coreapiupdatefield

Revision ID: aa945c3e6a1a
Revises: 9554d19453ba
Create Date: 2024-03-16 15:54:41.774171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa945c3e6a1a'
down_revision: Union[str, None] = '9554d19453ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_fields', sa.Column('old_field_property', sa.Text(), nullable=True))
    op.add_column('api_fields', sa.Column('field_rule', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_fields', 'field_rule')
    op.drop_column('api_fields', 'old_field_property')
    # ### end Alembic commands ###
