"""empty message

Revision ID: 6f45d3c92000
Revises: d1d790441f19
Create Date: 2023-11-06 11:43:12.083466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f45d3c92000'
down_revision = 'd1d790441f19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_comment_product_id'), ['product_id'], unique=False)
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_comment_product_id'))
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###