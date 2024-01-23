from flask_restful import Resource, reqparse
from app.models import Conta, Financeiro
from app.schemas import ContaSchema
from app.db import db

class ContaResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('agencia', type=str, required=True, help='Agência da conta não informada')
        self.reqparse.add_argument('conta_corrente', type=str, required=True, help='Número da conta não informado')
        self.reqparse.add_argument('financeiro_id', type=int, required=True, help='ID da conta não informado')
        super(ContaResource, self).__init__()

    def get(self, id):
        conta = Conta.query.get_or_404(id)
        financeiro = Financeiro.query.get_or_404(conta.financeiro_id)
        return {
            'id':conta.id,
            'agencia':conta.agencia,
            'conta_corrente':conta.conta_corrente,
            'financeiro_id':financeiro.banco
        }
    
    def post(self):
        args = self.reqparse.parse_args()
        conta_schema = ContaSchema()
        erros = conta_schema.validate(args)

        if erros:
            return erros, 400
        
        conta = Conta(**args)
        db.session.add(conta)
        db.session.commit()
        response_data = conta_schema.dump(conta)
        
        return response_data, 201

    def put(self, id):
        conta = Conta.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for key, value in args.items():
            setattr(conta, key, value)
        db.session.commit()
        return {'message': 'Conta atualizada com sucesso'}

    def delete(self, id):
        conta = Conta.query.get_or_404(id)
        db.session.delete(conta)
        db.session.commit()
        return {'message': 'Conta deletada com sucesso'}