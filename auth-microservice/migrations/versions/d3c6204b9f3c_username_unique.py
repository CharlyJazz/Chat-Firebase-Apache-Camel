"""username unique

Revision ID: d3c6204b9f3c
Revises: fe1a63894533
Create Date: 2022-03-03 21:50:37.874584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c6204b9f3c'
down_revision = 'fe1a63894533'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_username', table_name='user')
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    # ### end Alembic commands ###
