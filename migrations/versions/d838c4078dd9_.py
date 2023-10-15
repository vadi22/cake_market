"""empty message

Revision ID: d838c4078dd9
Revises: c2a1880a9d6c
Create Date: 2023-10-14 10:39:06.177785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd838c4078dd9'
down_revision = 'c2a1880a9d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_adress', schema=None) as batch_op:
        batch_op.drop_column('submit')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_adress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('submit', sa.VARCHAR(length=120), autoincrement=False, nullable=True))

    # ### end Alembic commands ###