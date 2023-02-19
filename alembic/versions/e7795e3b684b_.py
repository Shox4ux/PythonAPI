"""

Revision ID: e7795e3b684b
Revises: 764fb3920def
Create Date: 2023-02-11 08:51:06.516865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7795e3b684b'
down_revision = '764fb3920def'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("word_database", sa.Column(
        "transcription", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("word_database", "transcription")
    pass
 