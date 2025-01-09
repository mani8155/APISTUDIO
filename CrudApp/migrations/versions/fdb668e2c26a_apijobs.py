"""apijobs

Revision ID: fdb668e2c26a
Revises: e7adda125b9d
Create Date: 2024-12-31 10:28:47.436795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdb668e2c26a'
down_revision: Union[str, None] = 'e7adda125b9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_jobs',
    sa.Column('psk_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('created_by', sa.String(length=255), nullable=True),
    sa.Column('updated_by', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('uid', sa.String(length=255), nullable=True),
    sa.Column('api_name', sa.String(length=255), nullable=True),
    sa.Column('api_type', sa.String(length=255), nullable=True),
    sa.Column('api_method', sa.String(length=10), nullable=True),
    sa.Column('api_source', sa.String(length=255), nullable=True),
    sa.Column('db_connection', sa.Integer(), nullable=True),
    sa.Column('db_connection_name', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('document_url', sa.String(length=255), nullable=True),
    sa.Column('core_api', sa.String(length=255), nullable=True),
    sa.Column('core_api_url', sa.String(length=255), nullable=True),
    sa.Column('timer_interval', sa.Integer(), nullable=True),
    sa.Column('timer_options', sa.String(length=255), nullable=True),
    sa.Column('timer_scheduler', sa.Text(), nullable=True),
    sa.Column('task_start', sa.DateTime(), nullable=True),
    sa.Column('task_end', sa.DateTime(), nullable=True),
    sa.Column('task_start_time', sa.Time(), nullable=True),
    sa.Column('task_start_end', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('psk_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_jobs')
    # ### end Alembic commands ###
