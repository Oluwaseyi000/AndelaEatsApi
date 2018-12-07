"""empty message

Revision ID: f1e897fca46d
Revises: b15ee05052f7
Create Date: 2018-11-29 14:42:22.851622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1e897fca46d'
down_revision = 'caa3c018a501'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('locations', 
               sa.Column('zone', sa.VARCHAR(10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('locations', 'zone')
    # ### end Alembic commands ###