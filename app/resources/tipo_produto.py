from flask import request
from flask_restful import Resource, reqparse
from app.models import db, TipoProduto
from app.schemas import TipoProdutoSchema

tipo_produto_schema = TipoProdutoSchema()
tipo_produtos_schema = TipoProdutoSchema(many=True)

class TipoProdutoResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('descricao', type=str, required=True, help='Descrição do produto não informada')
        self.reqparse.add_argument('eletronico_veiculo', type=str, required=True, help='Tipo do produto não informado')
        super(TipoProdutoResource, self).__init__()


    def get(self, id):
        tipo_produto = TipoProduto.query.get_or_404(id)
        return tipo_produto_schema.dump(tipo_produto)

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        tipo_produto_schema = TipoProdutoSchema()
        erros = tipo_produto_schema.validate(args)
        if erros:
            return erros, 400
        tipo_produto = TipoProduto(**args)
        db.session.add(tipo_produto)
        db.session.commit()
        return tipo_produto_schema.dump(tipo_produto)
        
        # json_data = request.get_json()
        # tipo_produto = tipo_produto_schema.load(json_data)
        
        # db.session.add(tipo_produto)
        # db.session.commit()

        # return tipo_produto_schema.dump(tipo_produto), 201

    def put(self, id):
        tipo_produto = TipoProduto.query.get_or_404(id)
        json_data = request.get_json()
        
        tipo_produto.eletronico_veiculo = json_data['eletronico_veiculo']
        tipo_produto.descricao = json_data['descricao']

        db.session.commit()

        return tipo_produto_schema.dump(tipo_produto)

    def delete(self, id):
        tipo_produto = TipoProduto.query.get_or_404(id)
        db.session.delete(tipo_produto)
        db.session.commit()

        return {'message': 'Tipo de Produto deletado com sucesso'}, 204
