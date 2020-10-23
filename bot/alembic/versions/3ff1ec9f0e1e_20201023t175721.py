"""20201023t175721

Revision ID: 3ff1ec9f0e1e
Revises: 
Create Date: 2020-10-23 17:57:21.395678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ff1ec9f0e1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('botovod_followers',
    sa.Column('chat', sa.Unicode(length=64), nullable=False),
    sa.Column('bot', sa.Unicode(length=64), nullable=False),
    sa.Column('dialog', sa.Unicode(length=64), nullable=True),
    sa.Column('next_step', sa.Unicode(length=64), nullable=True),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_botovod_followers_id'), 'botovod_followers', ['id'], unique=True)
    op.create_table('follower_states',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['botovod_followers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_follower_states_follower_id'), 'follower_states', ['follower_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_follower_states_follower_id'), table_name='follower_states')
    op.drop_table('follower_states')
    op.drop_index(op.f('ix_botovod_followers_id'), table_name='botovod_followers')
    op.drop_table('botovod_followers')
    # ### end Alembic commands ###
