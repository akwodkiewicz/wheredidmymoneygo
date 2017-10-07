"""empty message

Revision ID: 69f955da12a3
Revises: 19570dccff9b
Create Date: 2017-10-07 23:10:31.830920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69f955da12a3'
down_revision = '19570dccff9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_category_for_user_uc', 'categories', ['name', 'user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_category_for_user_uc', 'categories', type_='unique')
    # ### end Alembic commands ###