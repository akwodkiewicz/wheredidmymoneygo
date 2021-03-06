"""empty message

Revision ID: 240c341734db
Revises: 898ffbf30e52
Create Date: 2017-10-07 22:06:45.614197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240c341734db'
down_revision = '898ffbf30e52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_index('ix_categories_name', table_name='categories')
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)
    op.drop_column('categories', 'user_id')
    # ### end Alembic commands ###
