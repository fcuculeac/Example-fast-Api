"""add foreign-key to post table

Revision ID: 4259e4c06bd4
Revises: 158989a9390b
Create Date: 2022-01-06 08:32:39.453448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4259e4c06bd4'
down_revision = '158989a9390b'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="True"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text("NOW()")))
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts-userid-fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("posts-userid-fk", "posts")
    op.drop_column("posts", "owner_id")
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
