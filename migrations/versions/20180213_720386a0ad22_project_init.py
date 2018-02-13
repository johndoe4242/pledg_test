"""Project init

Revision ID: 720386a0ad22
Revises: 
Create Date: 2018-02-13 23:34:15.588975

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from app.models import constants

# revision identifiers, used by Alembic.
revision = '720386a0ad22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pledger',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(constants.STATES), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('leader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['leader_id'], ['pledger.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('purchase_pledgers',
    sa.Column('pledger_id', sa.Integer(), nullable=False),
    sa.Column('purchase_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pledger_id'], ['pledger.id'], ),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchase.id'], ),
    sa.PrimaryKeyConstraint('pledger_id', 'purchase_id')
    )
    op.create_table('share',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('pledger_id', sa.Integer(), nullable=False),
    sa.Column('purchase_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['pledger_id'], ['pledger.id'], ),
    sa.ForeignKeyConstraint(['purchase_id'], ['purchase.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('share')
    op.drop_table('purchase_pledgers')
    op.drop_table('purchase')
    op.drop_table('pledger')
    # ### end Alembic commands ###