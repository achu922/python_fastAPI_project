"""add last few columns to post

Revision ID: d8fa1eadfecd
Revises: 7641f0186f3f
Create Date: 2022-04-30 15:23:00.524040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8fa1eadfecd'
down_revision = '7641f0186f3f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('Posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    pass
