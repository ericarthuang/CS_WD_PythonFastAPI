"""add few columns to table posts

Revision ID: 652052436586
Revises: 142648192936
Create Date: 2022-08-16 17:18:07.287379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '652052436586'
down_revision = '142648192936'
branch_labels = None
depends_on = None


def upgrade() -> None:
   op.add_column(
    'posts',
    sa.Column(
        'published',
        sa.Boolean(),
        nullable=False,
        server_default="TRUE",
    )
   )
   op.add_column(
    'posts',
    sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.text('now()')
    )
   )

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
