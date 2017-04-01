from flask_restful import Resource, reqparse, abort
from flask import g, url_for
from app.common.db.tables import Cliente as User
from app import auth, db


parser = reqparse.RequestParser()
parser.add_argument('nome', required=True, help="Não pode ficar em branco!!")
parser.add_argument('telefone',required=True, help="Não pode ficar em branco!!")
parser.add_argument('email',required=True, help="Não pode ficar em branco!!")
#parser.add_argument('data_nascimento',required=True, help="Não pode ficar em branco!!")
parser.add_argument('senha',required=True, help="Não pode ficar em branco!!")
parser_email = reqparse.RequestParser()
parser_email.add_argument('email')

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class ClienteNew(Resource):

    def post(self):
        args = parser.parse_args()
        nome_usuario = args['nome']
        telefone = args['telefone']
        email = args['email']
        #data_nascimento = args['data_nascimento']
        senha = args['senha']

        if nome_usuario is None or senha is None:
            abort(400)

        if User.query.filter_by(email=email).first() is not None:
            abort(400)

        user = User(nome_usuario,telefone,email)
        user.hash_password(senha)
        db.session.add(user)
        db.session.commit()

        return {'nome':user.nome,'pass':user.senha_hash}

class Token(Resource):

    decorators = [
        auth.login_required
    ]
    def get(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}


class Cliente(Resource):

    decorators = [
        auth.login_required
    ]
    def get(self):
        args = parser_email.parse_args()
        email = args['email']
        dados = User.query.filter_by(email=email).first()
        return {'nome': dados.nome, 'email':dados.email, 'data_cadastro':str(dados.data_cadastro)}

    def put(self):



#curl -u teste@teste.com:abc -i -X GET http://127.0.0.1:5000/api/cliente/ -H "Content-Type: application/json" -d '{"email":"teste@teste.com"}'


