from flask_restful import Resource, reqparse
from app.models import Cliente
from app.schemas import ClienteSchema
from flask_jwt_extended import jwt_required, create_access_token
from app.db import db

class ClienteResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nome', type=str, required=True, help='Nome do cliente não informado')
        self.reqparse.add_argument('email', type=str, required=True, help='Email do cliente não informado')
        self.reqparse.add_argument('senha', type=str, required=True, help='Senha do cliente não informada')
        self.reqparse.add_argument('telefone', type=str, required=True, help='Telefone do cliente não informado')
        self.reqparse.add_argument('cpf', type=str, required=True, help='CPF do cliente não informado')
        super(ClienteResource, self).__init__()
    
    def get(self, id):
        cliente = Cliente.query.get_or_404(id, description='Cliente não encontrado')
        schema = ClienteSchema()
        return schema.dump(cliente)
    
    def post(self):
        args = self.reqparse.parse_args()
        cliente_schema = ClienteSchema()
        erros = cliente_schema.validate(args)
        if erros:
            return erros, 400
        cliente = Cliente(**args)
        db.session.add(cliente)
        db.session.commit()
        response_data = cliente_schema.dump(cliente)
        
        return response_data, 201
    
    @jwt_required()
    def put(self, id):
        cliente = Cliente.query.get_or_404(id, description='Cliente não encontrado')
        args = self.reqparse.parse_args()
        cliente.nome = args['nome']
        cliente.email = args['email']
        cliente.senha = args['senha']
        cliente.telefone = args['telefone']
        cliente.cpf = args['cpf']
        db.session.add(cliente)
        db.session.commit()
        cliente_schema = ClienteSchema()
        response_data = cliente_schema.dump(cliente)
        return response_data, 200
    
    @jwt_required()
    def delete(self, id):
        cliente = Cliente.query.get_or_404(id, description='Cliente não encontrado')
        db.session.delete(cliente)
        db.session.commit()
        return None, 204
    
class ClienteLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='Email do cliente não informado')
        self.reqparse.add_argument('senha', type=str, required=True, help='Senha do cliente não informada')
        super(ClienteLogin, self).__init__()
    
    def post(self):
        args = self.reqparse.parse_args()
        cliente = Cliente.query.filter_by(email=args['email']).first()
        if cliente and cliente.verificar_senha(args['senha']):
            access_token = create_access_token(identity=cliente.id)
            return {'access_token': access_token}, 200
        return {'message': 'Email ou senha inválidos'}, 401