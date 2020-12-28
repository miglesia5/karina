"""Add category_name to Item

Revision ID: 9df9d64124e8
Revises: 2d6f4372c210
Create Date: 2020-10-06 08:43:11.402960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9df9d64124e8'
down_revision = '2d6f4372c210'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('category_name', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'category_name')
    # ### end Alembic commands ###