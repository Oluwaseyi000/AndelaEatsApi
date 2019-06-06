"""empty message

Revision ID: 8dff842c714a
Revises: 459d3bb06df4
Create Date: 2019-05-20 14:42:35.293970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dff842c714a'
down_revision = '459d3bb06df4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meal_items', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meal_items', sa.Column('description', sa.VARCHAR(length=1000), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
