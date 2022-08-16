"""create posts table

Revision ID: 7506d4c94b6c
Revises: 
Create Date: 2022-08-16 15:52:01.979243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7506d4c94b6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )
    


def downgrade() -> None:
    op.drop_table('posts')
