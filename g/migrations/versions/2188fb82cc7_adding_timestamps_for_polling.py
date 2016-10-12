"""Adding timestamps for polling

Revision ID: 2188fb82cc7
Revises: 2f4bbdf6293
Create Date: 2016-10-11 17:03:27.159326

"""

# revision identifiers, used by Alembic.
revision = '2188fb82cc7'
down_revision = '2f4bbdf6293'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_created_timestamp'), 'user', ['created_timestamp'], unique=False)
    op.add_column('user_language', sa.Column('created_timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_language_created_timestamp'), 'user_language', ['created_timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_language_created_timestamp'), table_name='user_language')
    op.drop_column('user_language', 'created_timestamp')
    op.drop_index(op.f('ix_user_created_timestamp'), table_name='user')
    op.drop_column('user', 'created_timestamp')
    ### end Alembic commands ###
