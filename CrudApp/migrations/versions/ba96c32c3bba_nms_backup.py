"""nms_backup

Revision ID: ba96c32c3bba
Revises: b5c610ad3633
Create Date: 2024-06-13 16:40:31.570204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba96c32c3bba'
down_revision: Union[str, None] = 'b5c610ad3633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nms_backup', sa.Column('prev_backup_time', sa.Time(), nullable=True))
    op.add_column('nms_backup', sa.Column('host_name', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('db_engine', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('db_name', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('backup_file_name', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('backup_file_size', sa.Integer(), nullable=True))
    op.add_column('nms_backup', sa.Column('backup_file_loca', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('backup_status', sa.String(), nullable=True))
    op.add_column('nms_backup', sa.Column('next_backup_time', sa.Time(), nullable=True))
    op.add_column('nms_backup', sa.Column('app_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nms_backup', 'app_name')
    op.drop_column('nms_backup', 'next_backup_time')
    op.drop_column('nms_backup', 'backup_status')
    op.drop_column('nms_backup', 'backup_file_loca')
    op.drop_column('nms_backup', 'backup_file_size')
    op.drop_column('nms_backup', 'backup_file_name')
    op.drop_column('nms_backup', 'db_name')
    op.drop_column('nms_backup', 'db_engine')
    op.drop_column('nms_backup', 'host_name')
    op.drop_column('nms_backup', 'prev_backup_time')
    # ### end Alembic commands ###