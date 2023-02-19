 
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '764fb3920def'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("word_database", sa.Column("id", sa.Integer(
    ), nullable=False, primary_key=True), sa.Column("word", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("word_database")
    pass
