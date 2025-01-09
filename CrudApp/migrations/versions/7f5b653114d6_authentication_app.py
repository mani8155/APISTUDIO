"""Authentication app

Revision ID: 7f5b653114d6
Revises: effa5218f0b0
Create Date: 2024-02-27 17:12:27.955288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7f5b653114d6'
down_revision: Union[str, None] = 'effa5218f0b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_auth_token_generator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('token_type', sa.String(), nullable=True),
    sa.Column('app_id', sa.String(), nullable=True),
    sa.Column('source_key', sa.String(), nullable=True),
    sa.Column('secret_key', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('expiry_period', sa.String(), nullable=True),
    sa.Column('expiry_datetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_auth_token_generator_id'), 'api_auth_token_generator', ['id'], unique=False)
    op.create_table('api_auth_token_generator_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('log', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['api_auth_token_generator.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_auth_token_generator_logs_id'), 'api_auth_token_generator_logs', ['id'], unique=False)
    op.create_table('api_auth_token_generator_migrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.Column('token_type', sa.String(), nullable=True),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('app_id', sa.String(), nullable=True),
    sa.Column('source_key', sa.String(), nullable=True),
    sa.Column('secret_key', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('expiry_period', sa.String(), nullable=True),
    sa.Column('expiry_datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['api_auth_token_generator.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_auth_token_generator_migrations_id'), 'api_auth_token_generator_migrations', ['id'], unique=False)
    op.create_table('api_models_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('log', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['api_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_models_logs_id'), 'api_models_logs', ['id'], unique=False)
    op.create_table('api_models_migrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('table_name', sa.String(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('migration_name', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('fields_list', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['api_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_models_migrations_id'), 'api_models_migrations', ['id'], unique=False)
    op.drop_index('ix_api_model_logs_id', table_name='api_model_logs')
    op.drop_table('api_model_logs')
    op.drop_index('ix_api_model_migrations_id', table_name='api_model_migrations')
    op.drop_table('api_model_migrations')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_model_migrations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('table_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('table_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('migration_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('uid', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fields_list', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['api_models.id'], name='api_model_migrations_table_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='api_model_migrations_pkey')
    )
    op.create_index('ix_api_model_migrations_id', 'api_model_migrations', ['id'], unique=False)
    op.create_table('api_model_logs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('table_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('log', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['api_models.id'], name='api_model_logs_table_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='api_model_logs_pkey')
    )
    op.create_index('ix_api_model_logs_id', 'api_model_logs', ['id'], unique=False)
    op.drop_index(op.f('ix_api_models_migrations_id'), table_name='api_models_migrations')
    op.drop_table('api_models_migrations')
    op.drop_index(op.f('ix_api_models_logs_id'), table_name='api_models_logs')
    op.drop_table('api_models_logs')
    op.drop_index(op.f('ix_api_auth_token_generator_migrations_id'), table_name='api_auth_token_generator_migrations')
    op.drop_table('api_auth_token_generator_migrations')
    op.drop_index(op.f('ix_api_auth_token_generator_logs_id'), table_name='api_auth_token_generator_logs')
    op.drop_table('api_auth_token_generator_logs')
    op.drop_index(op.f('ix_api_auth_token_generator_id'), table_name='api_auth_token_generator')
    op.drop_table('api_auth_token_generator')
    # ### end Alembic commands ###
