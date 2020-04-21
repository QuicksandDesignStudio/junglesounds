"""empty message

Revision ID: 6c77bb651826
Revises: 2e3b18750365
Create Date: 2020-04-21 18:08:09.817601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c77bb651826'
down_revision = '2e3b18750365'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('approved', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.drop_column('user', 'approved')
    # ### end Alembic commands ###
