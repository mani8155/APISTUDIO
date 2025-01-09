"""“tracesql”

Revision ID: 22314a449dfa
Revises: 431ba5f14019
Create Date: 2024-10-01 14:37:13.115336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22314a449dfa'
down_revision: Union[str, None] = '431ba5f14019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_sql_trace',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('api_request_payload', sa.Text(), nullable=True),
    sa.Column('api_response_payload', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['api_sql.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_sql_trace_id'), 'api_sql_trace', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_api_sql_trace_id'), table_name='api_sql_trace')
    op.drop_table('api_sql_trace')
    # ### end Alembic commands ###
