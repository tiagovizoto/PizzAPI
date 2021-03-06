"""empty message

Revision ID: a12a46fd3c57
Revises: 
Create Date: 2017-03-29 04:32:07.227878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a12a46fd3c57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=225), nullable=True),
    sa.Column('telefone', sa.String(length=24), nullable=True),
    sa.Column('email', sa.String(length=225), nullable=True),
    sa.Column('pontos', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('estoque',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('quantidade_atual', sa.Float(), nullable=True),
    sa.Column('quantidade_minima', sa.Float(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pedido',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_pedido', sa.DateTime(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('endereco', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('endereco_cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_cliente', sa.Integer(), nullable=True),
    sa.Column('logradouro', sa.String(length=225), nullable=True),
    sa.Column('uf', sa.String(length=3), nullable=True),
    sa.Column('cidade', sa.String(length=120), nullable=True),
    sa.Column('numero', sa.String(length=45), nullable=True),
    sa.Column('cep', sa.Integer(), nullable=True),
    sa.Column('bairro', sa.String(length=140), nullable=True),
    sa.Column('completemento', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['fk_cliente'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_pedido',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantidade', sa.Float(), nullable=True),
    sa.Column('fk_pedido', sa.Integer(), nullable=True),
    sa.Column('fk_produto', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_pedido'], ['pedido.id'], ),
    sa.ForeignKeyConstraint(['fk_produto'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produto_ingrediente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_produto', sa.Integer(), nullable=True),
    sa.Column('fk_estoque', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_estoque'], ['estoque.id'], ),
    sa.ForeignKeyConstraint(['fk_produto'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cliente_pedido',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_endereco_cliente', sa.Integer(), nullable=True),
    sa.Column('fk_pedido', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_endereco_cliente'], ['endereco_cliente.id'], ),
    sa.ForeignKeyConstraint(['fk_pedido'], ['pedido.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cliente_pedido')
    op.drop_table('produto_ingrediente')
    op.drop_table('item_pedido')
    op.drop_table('endereco_cliente')
    op.drop_table('produto')
    op.drop_table('pedido')
    op.drop_table('estoque')
    op.drop_table('cliente')
    # ### end Alembic commands ###
