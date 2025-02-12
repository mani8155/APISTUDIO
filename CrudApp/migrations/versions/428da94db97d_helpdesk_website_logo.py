"""helpdesk_website_logo

Revision ID: 428da94db97d
Revises: 372a505325ca
Create Date: 2024-05-31 09:12:42.832844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '428da94db97d'
down_revision: Union[str, None] = '372a505325ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('helpdesk_website_logo', sa.Column('website_name', sa.String(), nullable=True))
    op.add_column('helpdesk_website_logo', sa.Column('website_domain', sa.String(), nullable=True))
    op.add_column('helpdesk_website_logo', sa.Column('google_analytics_key', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('helpdesk_website_logo', 'google_analytics_key')
    op.drop_column('helpdesk_website_logo', 'website_domain')
    op.drop_column('helpdesk_website_logo', 'website_name')
    # ### end Alembic commands ###
