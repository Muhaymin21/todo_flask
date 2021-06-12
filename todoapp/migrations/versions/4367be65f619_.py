"""empty message

Revision ID: 4367be65f619
Revises: f5886da3cf6d
Create Date: 2021-06-10 18:08:20.169537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4367be65f619'
down_revision = 'f5886da3cf6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
