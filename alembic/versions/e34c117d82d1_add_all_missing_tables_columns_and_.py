"""add all missing tables, columns and constraints

Revision ID: e34c117d82d1
Revises: a9c466a92b4a
Create Date: 2023-02-12 17:15:50.391522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e34c117d82d1'
down_revision = 'a9c466a92b4a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote_database',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_database.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_id'], ['word_database.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'word_id')
    )
    op.add_column('user_database', sa.Column('password', sa.String(), nullable=False))
    op.add_column('user_database', sa.Column('is_active', sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('user_database', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_constraint('user_database_email_key', 'user_database', type_='unique')
    op.drop_column('user_database', 'passord')
    op.add_column('word_database', sa.Column('definition', sa.String(), nullable=False))
    op.add_column('word_database', sa.Column('example', sa.String(), nullable=False))
    op.add_column('word_database', sa.Column('level', sa.String(), nullable=False))
    op.add_column('word_database', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('word_database', 'created_at')
    op.drop_column('word_database', 'level')
    op.drop_column('word_database', 'example')
    op.drop_column('word_database', 'definition')
    op.add_column('user_database', sa.Column('passord', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_database_email_key', 'user_database', ['email'])
    op.drop_column('user_database', 'created_at')
    op.drop_column('user_database', 'is_active')
    op.drop_column('user_database', 'password')
    op.drop_table('vote_database')
    # ### end Alembic commands ###
