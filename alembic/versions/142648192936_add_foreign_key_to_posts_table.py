"""add foreign-key to posts table

Revision ID: 142648192936
Revises: 28a823bcbe44
Create Date: 2022-08-16 17:03:15.775489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '142648192936'
down_revision = '28a823bcbe44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column(
            'owner_id', 
            sa.Integer(),
            nullable=False,
        )
    )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table="users",
        local_cols=['owner_id'], remote_cols=['id'],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
