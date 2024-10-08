"""empty message

Revision ID: 6bc53255a1a1
Revises: a16bc46876ef
Create Date: 2023-11-06 19:09:55.035486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bc53255a1a1'
down_revision = 'a16bc46876ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_review_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_review_user_id'))

    op.drop_table('review')
    # ### end Alembic commands ###
