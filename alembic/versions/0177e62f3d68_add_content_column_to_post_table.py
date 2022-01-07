"""add content column to post table

Revision ID: 0177e62f3d68
Revises: 413756eeb9d9
Create Date: 2022-01-06 08:08:13.418920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0177e62f3d68'
down_revision = '413756eeb9d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
