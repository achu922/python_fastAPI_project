"""add content column to posts table

Revision ID: 1e7137819222
Revises: 97cc80c16cda
Create Date: 2022-04-30 12:59:29.379247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e7137819222'
down_revision = '97cc80c16cda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('Posts', 'content')
    pass
