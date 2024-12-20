"""Initial migration

Revision ID: 2becb868bdd6
Revises: 
Create Date: 2024-12-19 00:38:28.896578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2becb868bdd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=80), nullable=False),
    sa.Column('lastName', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('photo', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('check_in_time', sa.Time(), nullable=True),
    sa.Column('check_out_time', sa.Time(), nullable=True),
    sa.Column('status', sa.String(20), nullable=False), 
    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('users')
    # ### end Alembic commands ###
