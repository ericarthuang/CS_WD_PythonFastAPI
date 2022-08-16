"""add content column to the posts table

Revision ID: cfbd170bf84f
Revises: 7506d4c94b6c
Create Date: 2022-08-16 16:10:51.130880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfbd170bf84f'
down_revision = '7506d4c94b6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column('content', sa.String(), nullable=False),

    )


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content',
    )
