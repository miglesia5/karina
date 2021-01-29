"""Added taller and anillos tables

Revision ID: 17f503fb479d
Revises: 9df9d64124e8
Create Date: 2021-01-09 12:48:03.731322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f503fb479d'
down_revision = '9df9d64124e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anillos_compromiso',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anillo_compromiso_name', sa.String(length=100), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taller',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('taller_name', sa.String(length=100), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('taller')
    op.drop_table('anillos_compromiso')
    # ### end Alembic commands ###
