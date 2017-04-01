from app import api
from app.resources.cliente import ClienteNew, Token,Cliente


api.add_resource(ClienteNew, '/api/cliente_novo')
api.add_resource(Token,'/api/token')
api.add_resource(Cliente,'/api/cliente/')
