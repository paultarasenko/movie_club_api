"""initial migration

Revision ID: 91867619950f
Revises:
Create Date: 2026-11-09 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91867619950f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'opinion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('source', sa.String(length=256), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('added_by', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('text'),
    )
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_opinion_timestamp'), ['timestamp'], unique=False
        )


def downgrade():
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_opinion_timestamp'))

    op.drop_table('opinion')
