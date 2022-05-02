"""create posts table

Revision ID: 97cc80c16cda
Revises: 
Create Date: 2022-04-30 12:47:25.206730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97cc80c16cda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('Posts')
    pass
