from marshmallow import Schema, fields

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)
    telefone = fields.Str(required=True)
    cpf = fields.Str(required=True)


class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    marca = fields.Str(required=True)
    modelo = fields.Str(required=True)
    descricao = fields.Str(required=True)
    lance_inicial = fields.Float(required=True)
    lance_adicional = fields.Float(required=True)
    vendido = fields.Bool(default=False, required=False)
    leilao_id = fields.Int(required=True)
    tipo_produto_id = fields.Int(required=True)

class FinanceiroSchema(Schema):
    id = fields.Int(dump_only=True)
    banco = fields.Str(required=True)

class ContaSchema(Schema):
    id = fields.Int(dump_only=True)
    agencia = fields.Str(required=True)
    conta_corrente = fields.Str(required=True)
    financeiro_id = fields.Int(required=True)

    
class VeiculoSchema(Schema):
    id = fields.Int(dump_only=True)
    placa = fields.Str(required=True)
    ano = fields.Str(required=True)
    qtd_portas = fields.Str(required=True)

class EletronicoSchema(Schema):
    id = fields.Int(dump_only=True)
    
class LeilaoSchema(Schema):
    id = fields.Int(dump_only=True)
    data_futura = fields.DateTime(required=True)
    data_visitacao = fields.DateTime(required=True)
    detalhes = fields.Str(required=True)
    qtd_produtos = fields.Int(required=False, default=0)

    status = fields.Str(required=False, default="EM ABERTO")

class LanceSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.DateTime(required=True)
    valor = fields.Float(required=True)
    cliente_id = fields.Int(required=True)
    leilao_id = fields.Int(required=True)
    produto_id = fields.Int(required=True)

class LeilaoFinanceiroSchema(Schema):
    id = fields.Int(dump_only=True)
    conta_id = fields.Int(required=True)
    leilao_id = fields.Int(required=True)

class TipoProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    eletronico_veiculo = fields.Str(required=True)
    descricao = fields.Str(required=True)

