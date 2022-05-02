"""add foreign key to post table

Revision ID: 7641f0186f3f
Revises: ee67a5b5a2de
Create Date: 2022-04-30 15:16:32.404873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7641f0186f3f'
down_revision = 'ee67a5b5a2de'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="Posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="Posts")
    op.drop_column('Posts', 'owner_id')
    pass
