"""Adding timestamps

Revision ID: 22ba47e67cc
Revises: 2188fb82cc7
Create Date: 2016-10-12 11:12:33.257733

"""

# revision identifiers, used by Alembic.
revision = '22ba47e67cc'
down_revision = '2188fb82cc7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_user_google_id'), 'user', ['google_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_google_id'), table_name='user')
    ### end Alembic commands ###
