"""add phone number

Revision ID: 82756016de80
Revises: c437fbace5f3
Create Date: 2022-08-16 20:57:02.787402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82756016de80'
down_revision = 'c437fbace5f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ### 
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number') 
    # ### end Alembic commands ###
