from flask_restful import Resource, reqparse
from app.models import Produto, Leilao, TipoProduto
from app.schemas import ProdutoSchema
from app.db import db
from sqlalchemy import and_
from datetime import datetime

produto_schema = ProdutoSchema()

class ProdutoResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('marca', type=str, required=True, help='Marca do produto não informado')
        self.reqparse.add_argument('modelo', type=str, required=True, help='Modelo do produto não informado')
        self.reqparse.add_argument('descricao', type=str, required=True, help='Descrição do produto não informado')
        self.reqparse.add_argument('lance_inicial', type=float, required=True, help='Lance inicial do produto não informado')
        # ! Não é obrigatório
        self.reqparse.add_argument('leilao_id', type=int, required=True, help='Leilão do produto não informado')
        self.reqparse.add_argument('lance_adicional', type=float, required=True, help='Lance inicial do produto não informado')
        self.reqparse.add_argument('vendido', type=bool, default=False)
        self.reqparse.add_argument('leilao_id', type=int, required=True, help='ID do Leilão não informado')
        self.reqparse.add_argument('tipo_produto_id', type=int, required=True, help='ID do tipo do produto não informado')
        super(ProdutoResource, self).__init__()
    
    def get(self, id):
        produto = Produto.query.get_or_404(id)
        leilao = Leilao.query.get_or_404(produto.leilao_id)
        tipo_produto = TipoProduto.query.get_or_404(produto.tipo_produto_id)
        return {
            'id':produto.id,
            'marca':produto.marca,
            'modelo':produto.modelo,
            'descricao':produto.descricao,
            'lance_inicial':produto.lance_inicial,
            'lance_adicional':produto.lance_adicional,
            'vendido':produto.vendido,
            'leilao_data':datetime.isoformat(leilao.data_futura),
            'leilao_detalhes':leilao.detalhes,
            'leilao_status':leilao.status,
            'tipo_produto_info':tipo_produto.eletronico_veiculo,
            'tipo_produto_descricao':tipo_produto.descricao
        }
    
    def post(self):
        args = self.reqparse.parse_args()
        erros = produto_schema.validate(args)

        if erros:
            return erros, 400
        
        produto = Produto(**args)
        db.session.add(produto)
        db.session.commit()
        response_data = produto_schema.dump(produto)
        
        return response_data, 201
    
    def put(self, id):
        produto = Produto.query.get_or_404(id)
        args = self.reqparse.parse_args()
        erros = produto_schema.validate(args)

        if erros:
            return erros, 400
        
        for key, value in args.items():
            setattr(produto, key, value)

        db.session.commit()
        response_data = produto_schema.dump(produto)

        return response_data, 200

    def delete(self, id):
        produto = Produto.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        
        return {'message': 'Produto deletado com sucesso'}, 200
    
class ProdutoResourceLista(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('min', type=int)
        self.reqparse.add_argument('max', type=int)
        self.reqparse.add_argument('leilaoid', type=int)
        self.reqparse.add_argument('tipoproduto', type=str)
        self.reqparse.add_argument('nome', type=str)
        super(ProdutoResourceLista).__init__()
        
    def get(self):
        args = self.reqparse.parse_args()
        
        filters_list = []
        for key, value in args.items():
            if value is not None:
                match(key):
                    case 'min':
                        filters_list.append(Produto.lance_inicial >= value)
                    case 'max':
                        filters_list.append(Produto.lance_inicial <= value)
                    case 'leilaoid':
                        filters_list.append(Produto.leilao_id == value)
                    case 'tipoproduto':
                        tipoproduto: TipoProduto = TipoProduto.query.filter_by(eletronico_veiculo=value).first()
                        filters_list.append(Produto.tipo_produto_id == tipoproduto.id)
                    case 'nome':
                        filters_list.append(Produto.descricao.like(f'%{value}%'))
                
        ProdutosFiltrados = Produto.query.filter(and_(*filters_list))
        ProdutoRetorno = []
        
        for produto in ProdutosFiltrados:
            leilao = Leilao.query.get_or_404(produto.leilao_id)
            tipo_produto = TipoProduto.query.get_or_404(produto.tipo_produto_id)
            ProdutoRetorno.append({
                'id':produto.id,
                'marca':produto.marca,
                'modelo':produto.modelo,
                'descricao':produto.descricao,
                'lance_inicial':produto.lance_inicial,
                'lance_adicional':produto.lance_adicional,
                'vendido':produto.vendido,
                'leilao_data':datetime.isoformat(leilao.data_futura),
                'leilao_detalhes':leilao.detalhes,
                'leilao_status':leilao.status,
                'tipo_produto_info':tipo_produto.eletronico_veiculo,
                'tipo_produto_descricao':tipo_produto.descricao
            })
    
        return ProdutoRetorno