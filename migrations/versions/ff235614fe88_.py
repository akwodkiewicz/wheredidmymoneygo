"""empty message

Revision ID: ff235614fe88
Revises: 240c341734db
Create Date: 2017-10-07 22:22:42.562885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff235614fe88'
down_revision = '240c341734db'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('transactions', 'amount', type_=sa.Numeric(precision=10, scale=2))


def downgrade():
    op.alter_column('transactions', 'amount', type_=sa.Numeric())
