from flask import request
from flask_restful import Resource
from app.models import db, LeilaoFinanceiro
from app.schemas import LeilaoFinanceiroSchema

leilao_financeiro_schema = LeilaoFinanceiroSchema()
leilao_financeiros_schema = LeilaoFinanceiroSchema(many=True)

class LeilaoFinanceiroResource(Resource):
    def __init__(self):
        self.reqparse.add_argument('conta_id', type=int, required=True, help='ID da conta não informado')
        self.reqparse.add_argument('leilao_id', type=int, required=True, help='ID do leilão não informado')
        super(LeilaoFinanceiroResource, self).__init__()

    def get(self, id):
        leilao_financeiro = LeilaoFinanceiro.query.get_or_404(id)
        return leilao_financeiro_schema.dump(leilao_financeiro)

    def post(self):
        json_data = request.get_json()
        leilao_financeiro = leilao_financeiro_schema.load(json_data)
        
        db.session.add(leilao_financeiro)
        db.session.commit()

        return leilao_financeiro_schema.dump(leilao_financeiro), 201

    def put(self, id):
        leilao_financeiro = LeilaoFinanceiro.query.get_or_404(id)
        json_data = request.get_json()
        
        leilao_financeiro.conta_id = json_data['conta_id']
        leilao_financeiro.leilao_id = json_data['leilao_id']

        db.session.commit()

        return leilao_financeiro_schema.dump(leilao_financeiro)

    def delete(self, id):
        leilao_financeiro = LeilaoFinanceiro.query.get_or_404(id)
        db.session.delete(leilao_financeiro)
        db.session.commit()

        return {'message': 'Leilão Financeiro deletado com sucesso'}, 204
