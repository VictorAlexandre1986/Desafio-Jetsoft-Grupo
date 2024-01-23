from app.db import db
from flask_migrate import Migrate
from flask import Flask
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app.resources.produto import ProdutoResource, ProdutoResourceLista
from app.resources.financeiro import FinanceiroResource
from app.resources.conta import ContaResource
from app.resources.cliente import ClienteResource, ClienteLogin
from app.resources.leilao import LeilaoResource, LeilaoResourceLista
from app.resources.leilao_financeiro import LeilaoFinanceiroResource
from app.resources.tipo_produto import TipoProdutoResource
from app.models import Leilao
from app.scheduler import scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    JWTManager(app)
    Migrate(app, db)
    db.init_app(app)
    
    api = Api(app)
    api.add_resource(ClienteResource, '/clientes', '/clientes/<int:id>')
    api.add_resource(ProdutoResource, '/produtos', '/produtos/<int:id>')
    api.add_resource(FinanceiroResource, '/financeiro', '/financeiro/<int:id>')
    api.add_resource(ContaResource, '/conta', '/conta/<int:id>')
    api.add_resource(ClienteLogin, '/login')
    api.add_resource(LeilaoResource, '/leilao', '/leilao/<int:id>')
    api.add_resource(LeilaoResourceLista, '/listaleilao')
    api.add_resource(LeilaoFinanceiroResource, '/leilao-financeiro', '/leilao-financeiro/<int:id>')
    api.add_resource(TipoProdutoResource, '/tipo-produto', '/tipo-produto/<int:id>')
    
    scheduler.init_app(app)

    def report_leilao():
        with app.app_context():
            info_leilao = Leilao.detalhes_leilao(self=Leilao)
            print(info_leilao)
            


    report_leilao()
    scheduler.start()
    
    return app  