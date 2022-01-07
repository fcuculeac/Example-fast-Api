"""create post table

Revision ID: 413756eeb9d9
Revises: 
Create Date: 2022-01-06 07:53:19.643519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '413756eeb9d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
