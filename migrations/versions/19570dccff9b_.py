"""empty message

Revision ID: 19570dccff9b
Revises: ff235614fe88
Create Date: 2017-10-07 22:57:14.070744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19570dccff9b'
down_revision = 'ff235614fe88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_word_in_category_uc', 'keywords', ['word', 'category_id'])
    op.drop_index('ix_keywords_word', table_name='keywords')
    op.create_index(op.f('ix_keywords_word'), 'keywords', ['word'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_keywords_word'), table_name='keywords')
    op.create_index('ix_keywords_word', 'keywords', ['word'], unique=True)
    op.drop_constraint('_word_in_category_uc', 'keywords', type_='unique')
    # ### end Alembic commands ###
