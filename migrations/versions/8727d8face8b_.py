"""empty message

Revision ID: 8727d8face8b
Revises: d838c4078dd9
Create Date: 2023-10-25 21:28:19.745471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8727d8face8b'
down_revision = 'd838c4078dd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('component__image', schema=None) as batch_op:
        batch_op.alter_column('component_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'component', ['component_id'], ['id'])
        batch_op.create_foreign_key(None, 'image', ['image_id'], ['id'])

    with op.batch_alter_table('price', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'component', ['component_id'], ['id'])

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_labor_id'), ['labor_id'], unique=False)
        batch_op.create_foreign_key(None, 'labor', ['labor_id'], ['id'])

    with op.batch_alter_table('product__component', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('component_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'component', ['component_id'], ['id'])
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'])

    with op.batch_alter_table('product__image', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'image', ['image_id'], ['id'])
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product__image', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('product__component', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('component_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_product_labor_id'))

    with op.batch_alter_table('price', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('component__image', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('component_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
