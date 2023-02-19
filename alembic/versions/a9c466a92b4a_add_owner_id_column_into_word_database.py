"""add owner_id column into word_database

Revision ID: a9c466a92b4a
Revises: 1ba463a38221
Create Date: 2023-02-12 16:50:22.923493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9c466a92b4a'
down_revision = '1ba463a38221'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("word_database", sa.Column(
        "owner_id", sa.Integer(), nullable=False))

    op.create_foreign_key("user_word_fk", source_table="word_database", referent_table="user_database", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint(constraint_name="user_word_fk",table_name="word_database")
    op.drop_column(column_name="owner_id",table_name="word_database")
    pass
