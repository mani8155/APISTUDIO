""""country"

Revision ID: cc652cbded25
Revises: 989a34b0dc0b
Create Date: 2024-02-12 16:32:11.593320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc652cbded25'
down_revision: Union[str, None] = '989a34b0dc0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country_post',
    sa.Column('psk_id', sa.Integer(), nullable=False),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('parent_psk_id', sa.Integer(), nullable=True),
    sa.Column('row_order', sa.Integer(), nullable=True),
    sa.Column('post_comment', sa.String(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('cancel_by', sa.String(), nullable=True),
    sa.Column('cancel_on', sa.DateTime(), nullable=True),
    sa.Column('cancel_status', sa.String(), nullable=True),
    sa.Column('cancel_remarks', sa.String(), nullable=True),
    sa.Column('gis_latitude', sa.Float(), nullable=True),
    sa.Column('gis_longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['parent_psk_id'], ['country.psk_id'], ),
    sa.PrimaryKeyConstraint('psk_id')
    )
    op.create_index(op.f('ix_country_post_psk_id'), 'country_post', ['psk_id'], unique=False)
    op.create_table('country_post_reaction',
    sa.Column('psk_id', sa.Integer(), nullable=False),
    sa.Column('psk_uid', sa.String(), nullable=True),
    sa.Column('parent_psk_id', sa.Integer(), nullable=True),
    sa.Column('row_order', sa.Integer(), nullable=True),
    sa.Column('reaction', sa.String(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('cancel_by', sa.String(), nullable=True),
    sa.Column('cancel_on', sa.DateTime(), nullable=True),
    sa.Column('cancel_status', sa.String(), nullable=True),
    sa.Column('cancel_remarks', sa.String(), nullable=True),
    sa.Column('gis_latitude', sa.Float(), nullable=True),
    sa.Column('gis_longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['parent_psk_id'], ['country.psk_id'], ),
    sa.PrimaryKeyConstraint('psk_id')
    )
    op.create_index(op.f('ix_country_post_reaction_psk_id'), 'country_post_reaction', ['psk_id'], unique=False)
    op.add_column('api_studio_app_group', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('api_studio_app_group', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('api_studio_app_group', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('api_studio_app_group', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('api_studio_app_name', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('api_studio_app_name', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('api_studio_app_name', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('api_studio_app_name', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('assignmenu_roleprivilege', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('assignmenu_roleprivilege', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('assignmenu_roleprivilege', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('assignmenu_roleprivilege', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('country', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('country', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('country', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('country', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('country_media', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('country_media', sa.Column('parent_psk_id', sa.Integer(), nullable=True))
    op.drop_constraint('country_media_parent_fkey', 'country_media', type_='foreignkey')
    op.create_foreign_key(None, 'country_media', 'country', ['parent_psk_id'], ['psk_id'])
    op.drop_column('country_media', 'parent')
    op.add_column('gmc1201_01_01', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('gmc1201_01_01', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('gmc1201_01_01', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('gmc1201_01_01', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('gmc1202_01_01', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('gmc1202_01_01', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('gmc1202_01_01', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('gmc1202_01_01', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('gmc1203_01_01', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('gmc1203_01_01', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('gmc1203_01_01', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('gmc1203_01_01', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('gmc1204_01_01', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('gmc1204_01_01', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('gmc1204_01_01', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('gmc1204_01_01', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('gmc1208_01_01', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('gmc1208_01_01', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('gmc1208_01_01', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('gmc1208_01_01', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('kommunityapi', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('kommunityapi', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('kommunityapi', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('kommunityapi', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('menus', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('menus', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('menus', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('menus', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('menus_history', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('menus_history', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('menus_history', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('menus_history', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('name', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('name', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('name', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('name', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('product', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('product', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('product', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('product', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('roleprivileges', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('roleprivileges', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('roleprivileges', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('roleprivileges', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('roles', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('roles', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('roles', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('roles', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('saas_application', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('saas_application', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('saas_application', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('saas_application', sa.Column('psk_uid', sa.String(), nullable=True))
    op.add_column('users', sa.Column('transaction_remarks', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('app_psk_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('app_uid', sa.String(), nullable=True))
    op.add_column('users', sa.Column('psk_uid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'psk_uid')
    op.drop_column('users', 'app_uid')
    op.drop_column('users', 'app_psk_id')
    op.drop_column('users', 'transaction_remarks')
    op.drop_column('saas_application', 'psk_uid')
    op.drop_column('saas_application', 'app_uid')
    op.drop_column('saas_application', 'app_psk_id')
    op.drop_column('saas_application', 'transaction_remarks')
    op.drop_column('roles', 'psk_uid')
    op.drop_column('roles', 'app_uid')
    op.drop_column('roles', 'app_psk_id')
    op.drop_column('roles', 'transaction_remarks')
    op.drop_column('roleprivileges', 'psk_uid')
    op.drop_column('roleprivileges', 'app_uid')
    op.drop_column('roleprivileges', 'app_psk_id')
    op.drop_column('roleprivileges', 'transaction_remarks')
    op.drop_column('product', 'psk_uid')
    op.drop_column('product', 'app_uid')
    op.drop_column('product', 'app_psk_id')
    op.drop_column('product', 'transaction_remarks')
    op.drop_column('name', 'psk_uid')
    op.drop_column('name', 'app_uid')
    op.drop_column('name', 'app_psk_id')
    op.drop_column('name', 'transaction_remarks')
    op.drop_column('menus_history', 'psk_uid')
    op.drop_column('menus_history', 'app_uid')
    op.drop_column('menus_history', 'app_psk_id')
    op.drop_column('menus_history', 'transaction_remarks')
    op.drop_column('menus', 'psk_uid')
    op.drop_column('menus', 'app_uid')
    op.drop_column('menus', 'app_psk_id')
    op.drop_column('menus', 'transaction_remarks')
    op.drop_column('kommunityapi', 'psk_uid')
    op.drop_column('kommunityapi', 'app_uid')
    op.drop_column('kommunityapi', 'app_psk_id')
    op.drop_column('kommunityapi', 'transaction_remarks')
    op.drop_column('gmc1208_01_01', 'psk_uid')
    op.drop_column('gmc1208_01_01', 'app_uid')
    op.drop_column('gmc1208_01_01', 'app_psk_id')
    op.drop_column('gmc1208_01_01', 'transaction_remarks')
    op.drop_column('gmc1204_01_01', 'psk_uid')
    op.drop_column('gmc1204_01_01', 'app_uid')
    op.drop_column('gmc1204_01_01', 'app_psk_id')
    op.drop_column('gmc1204_01_01', 'transaction_remarks')
    op.drop_column('gmc1203_01_01', 'psk_uid')
    op.drop_column('gmc1203_01_01', 'app_uid')
    op.drop_column('gmc1203_01_01', 'app_psk_id')
    op.drop_column('gmc1203_01_01', 'transaction_remarks')
    op.drop_column('gmc1202_01_01', 'psk_uid')
    op.drop_column('gmc1202_01_01', 'app_uid')
    op.drop_column('gmc1202_01_01', 'app_psk_id')
    op.drop_column('gmc1202_01_01', 'transaction_remarks')
    op.drop_column('gmc1201_01_01', 'psk_uid')
    op.drop_column('gmc1201_01_01', 'app_uid')
    op.drop_column('gmc1201_01_01', 'app_psk_id')
    op.drop_column('gmc1201_01_01', 'transaction_remarks')
    op.add_column('country_media', sa.Column('parent', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'country_media', type_='foreignkey')
    op.create_foreign_key('country_media_parent_fkey', 'country_media', 'country', ['parent'], ['psk_id'])
    op.drop_column('country_media', 'parent_psk_id')
    op.drop_column('country_media', 'psk_uid')
    op.drop_column('country', 'psk_uid')
    op.drop_column('country', 'app_uid')
    op.drop_column('country', 'app_psk_id')
    op.drop_column('country', 'transaction_remarks')
    op.drop_column('assignmenu_roleprivilege', 'psk_uid')
    op.drop_column('assignmenu_roleprivilege', 'app_uid')
    op.drop_column('assignmenu_roleprivilege', 'app_psk_id')
    op.drop_column('assignmenu_roleprivilege', 'transaction_remarks')
    op.drop_column('api_studio_app_name', 'psk_uid')
    op.drop_column('api_studio_app_name', 'app_uid')
    op.drop_column('api_studio_app_name', 'app_psk_id')
    op.drop_column('api_studio_app_name', 'transaction_remarks')
    op.drop_column('api_studio_app_group', 'psk_uid')
    op.drop_column('api_studio_app_group', 'app_uid')
    op.drop_column('api_studio_app_group', 'app_psk_id')
    op.drop_column('api_studio_app_group', 'transaction_remarks')
    op.drop_index(op.f('ix_country_post_reaction_psk_id'), table_name='country_post_reaction')
    op.drop_table('country_post_reaction')
    op.drop_index(op.f('ix_country_post_psk_id'), table_name='country_post')
    op.drop_table('country_post')
    # ### end Alembic commands ###