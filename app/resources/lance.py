from flask_restful import Resource, reqparse
from app.models import Lance
from app.schemas import LanceSchema
from flask_jwt_extended import jwt_required, create_access_token
from app.db import db
from datetime import datetime

class LanceResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data', type=str, required=False, help='Data não informada')
        self.reqparse.add_argument('valor', type=str, required=True, help='Valor não informado')
        self.reqparse.add_argument('cliente_id', type=int, required=True, help='Cliente id não informado')
        self.reqparse.add_argument('leilao_id', type=int, required=True, help='Leilão não informado')
        self.reqparse.add_argument('produto_id', type=int, required=True, help='Produto não informado')
        super(LanceResource, self).__init__()
    
    def get(self, id):
        lance = Lance.query.get_or_404(id, description='Lance não encontrado')
        lance_schema = LanceSchema()
        return lance_schema.dump(lance)
    
    def post(self):
        args = self.reqparse.parse_args()
        lance_schema = LanceSchema()
        erros = lance_schema.validate(args)
        if erros:
            return erros, 400
        lance = Lance(**args)
        lance.data = datetime.strptime(args['data'], '%Y-%m-%dT%H:%M:%S')
        db.session.add(lance)
        db.session.commit()
        response_data = lance_schema.dump(lance)
        
        return response_data, 201
    
    
    def put(self, id):
        lance = Lance.query.get_or_404(id, description='Lance não encontrado')
        args = self.reqparse.parse_args()
        lance.data = args['data']
        lance.valor = args['valor']
        lance.cliente_id = args['cliente_id']
        lance.leilao_id = args['leilao_id']
        lance.produto_id = args['produto_id']
        lance.data = datetime.strptime(args['data'], '%Y-%m-%dT%H:%M:%S')
        db.session.add(lance)
        db.session.commit()
        lance_schema = LanceSchema()
        response_data = lance_schema.dump(lance)
        return response_data, 200
    
    def delete(self, id):
        lance = Lance.query.get_or_404(id, description='Cliente não encontrado')
        db.session.delete(lance)
        db.session.commit()
        return None, 204