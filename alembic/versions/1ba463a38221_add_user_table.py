"""add user table

Revision ID: 1ba463a38221
Revises: e7795e3b684b
Create Date: 2023-02-11 09:00:16.195057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ba463a38221'
down_revision = 'e7795e3b684b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_database",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("passord", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("user_database")
    pass
