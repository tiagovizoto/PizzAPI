from app import db, app
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Estoque(db.Model):

    #__tablename__ = "estoque"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    quantidade_atual = db.Column(db.Float)
    quantidade_minima = db.Column(db.Float)
    preco = db.Column(db.Float)



    def __init__(self, descricao, quantidade_atual,quantidade_minima):
        self.descricao = descricao
        self.quantidade_atual = quantidade_atual
        self.quantidade_minima = quantidade_minima

    def __repr__(self):
        return "<Estoque> %s" % self.descricao



class Produto(db.Model):

    #__tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    preco = db.Column(db.Float)



    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def __repr__(self):
        return "<Produto> %s" % self.nome


class ProdutoIngrediente(db.Model):

    #__tablename__ = "produto_ingrediente"
    id = db.Column(db.Integer, primary_key=True)
    fk_produto = db.Column(db.Integer, db.ForeignKey("produto.id"))
    fk_estoque = db.Column(db.Integer,db.ForeignKey("estoque.id"))
    produto = db.relationship("Produto", foreign_keys=fk_produto)
    estoque = db.relationship("Estoque", foreign_keys=fk_estoque)



    def __init__(self, fk_estoque, fk_produto):
        self.fk_estoque = fk_estoque
        self.fk_produto = fk_produto

    def __repr__(self):
        return '<ProdutoIngrediente> %i' % self.id

class Pedido(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.DateTime)
    total = db.Column(db.Float)
    endereco = db.Column(db.Text)

    def __init__(self, total, endereco, data_pedido = None):
        self.total = total
        self.endereco = endereco

        if data_pedido == None:
            self.data_pedido = datetime.utcnow()
        else:
            self.data_pedido = data_pedido

    def __repr__(self):
        return '<Pedido> %i' % self.id

class ItemPedido(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Float)
    fk_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    fk_produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    pedido = db.relationship("Pedido", foreign_keys=fk_pedido)
    produto = db.relationship("Produto", foreign_keys=fk_produto)


    def __init__(self, quantidade, fk_pedido, fk_produto):
        self.quantidade = quantidade
        self.fk_produto = fk_produto
        self.fk_pedido = fk_pedido

    def __repr__(self):
        return '<ItemPedido> %i' % self.id


class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(225), nullable=False )
    telefone = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(225),unique=True ,nullable=False)
    pontos = db.Column(db.Integer())
    data_cadastro = db.Column(db.DateTime, nullable=False)
    senha_hash = db.Column(db.String(129), nullable=False)
    is_confidential = db.Column(db.Boolean)

    def __init__(self, nome, telefone, email, pontos=None):

        self.nome = nome
        self.email = email

        if pontos is not None:
            self.pontos = pontos
        self.data_cadastro = datetime.utcnow()
        self.telefone = telefone

    def __repr__(self):
        return "<Cliente> %s" % self.nome

    def hash_password(self, password):
         self.senha_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.senha_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = Cliente.query.get(data['id'])
        return user


class EnderecoCliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fk_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    logradouro = db.Column(db.String(225))
    uf = db.Column(db.String(3))
    cidade = db.Column(db.String(120))
    numero = db.Column(db.String(45))
    cep = db.Column(db.Integer)
    bairro = db.Column(db.String(140))
    completemento = db.Column(db.Text)

    cliente = db.relationship("Cliente", foreign_keys=fk_cliente)


    def __init__(self, fk_cliente, lograduro, numero, uf, cidade, bairro, cep, complemento):
        self.fk_cliente = fk_cliente
        self.logradouro =lograduro
        self.numero = numero
        self.uf = uf
        self.cidade = cidade
        self.bairro = bairro
        self.cep = cep
        self.completemento = complemento

    def __repr__(self):
        return "<Endereco> %s %i" %(self.logradouro, self.numero)


class ClientePedido(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fk_endereco_cliente = db.Column(db.Integer, db.ForeignKey("endereco_cliente.id"))
    fk_pedido = db.Column(db.Integer, db.ForeignKey("pedido.id"))
    endereco_cliente = db.relationship("EnderecoCliente", foreign_keys=fk_endereco_cliente)
    pedido = db.relationship("Pedido", foreign_keys=fk_pedido)


    def __init__(self, fk_endereco, fk_pedido):
        self.fk_endereco = fk_endereco
        self.fk_pedido = fk_pedido

    def __repr__(self):
        return "<ClientePedido> %i" % self.id