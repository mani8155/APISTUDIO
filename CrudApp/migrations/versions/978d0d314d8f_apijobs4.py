"""apijobs4

Revision ID: 978d0d314d8f
Revises: 24555663b0e5
Create Date: 2024-12-31 16:33:43.752499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '978d0d314d8f'
down_revision: Union[str, None] = '24555663b0e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_jobs', sa.Column('core_api_secrete_key', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_jobs', 'core_api_secrete_key')
    # ### end Alembic commands ###
