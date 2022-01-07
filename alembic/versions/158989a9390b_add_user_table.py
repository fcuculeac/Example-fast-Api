"""add user table

Revision ID: 158989a9390b
Revises: 0177e62f3d68
Create Date: 2022-01-06 08:18:38.456230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '158989a9390b'
down_revision = '0177e62f3d68'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("NOW()"))
                    )


def downgrade():
    op.drop_table("users")
