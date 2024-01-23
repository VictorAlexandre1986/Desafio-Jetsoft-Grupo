from flask_restful import Resource, reqparse
from app.models import Financeiro
from app.schemas import FinanceiroSchema
from app.db import db

class FinanceiroResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('banco', type=str, required=True, help='Banco do financeiro não informado')
        super(FinanceiroResource, self).__init__()

    def get(self, id):
        financeiro = Financeiro.query.get_or_404(id)
        financeiro_schema = FinanceiroSchema()
        return financeiro_schema.dump(financeiro)

    
    def post(self):
        args = self.reqparse.parse_args()
        financeiro_schema = FinanceiroSchema()
        erros = financeiro_schema.validate(args)

        if erros:
            return erros, 400
        
        financeiro = Financeiro(**args)
        db.session.add(financeiro)
        db.session.commit()
        response_data = financeiro_schema.dump(financeiro)
        
        return response_data, 201


    def put(self, id):
        financeiro = Financeiro.query.get_or_404(id)
        args = self.reqparse.parse_args()

        for key, value in args.items():
            setattr(financeiro, key, value)
        db.session.commit()

        return {'message': 'Financeiro atualizado com sucesso'}

    def delete(self, id):
        financeiro = Financeiro.query.get_or_404(id)
        db.session.delete(financeiro)
        db.session.commit()
        return {'message': 'Financeiro deletado com sucesso'}