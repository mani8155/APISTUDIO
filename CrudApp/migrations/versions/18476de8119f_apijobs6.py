"""apijobs6

Revision ID: 18476de8119f
Revises: 9daaf78899e7
Create Date: 2025-01-09 11:44:33.819011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '18476de8119f'
down_revision: Union[str, None] = '9daaf78899e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_jobs', 'timer_scheduler')
    op.drop_column('api_jobs', 'db_connection_name')
    op.drop_column('api_jobs', 'db_connection')
    op.drop_column('api_jobs', 'task_start_end')
    op.drop_column('api_jobs', 'api_base_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_jobs', sa.Column('api_base_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('api_jobs', sa.Column('task_start_end', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('api_jobs', sa.Column('db_connection', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('api_jobs', sa.Column('db_connection_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('api_jobs', sa.Column('timer_scheduler', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###