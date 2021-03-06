"""empty message

Revision ID: 3598df50da33
Revises: 6c8a2f2d23a8
Create Date: 2018-02-17 11:57:57.339428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3598df50da33'
down_revision = '6c8a2f2d23a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
