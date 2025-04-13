from marshmallow import Schema, fields, validate
from app.schemas.base import BaseSchema
from app.schemas.equipamento_schema import EquipamentoResponseSchema
from app.schemas.usuario_schema import UsuarioResponseSchema
from app.schemas.estoque_schema import EstoqueResponseSchema
from app.schemas.localizacao_schema import LocalizacaoResponseSchema
from app.models.movimentacao import Movimentacao

class MovimentacaoSchema(Schema):
    id = fields.Int()
    equipamento_id = fields.Int()
    usuario_id = fields.Int()
    tipo_movimentacao = fields.Str(required=True, validate=validate.OneOf(["entrada", "saida", "transferencia"]))
    data_hora = fields.DateTime()
    localizacao_destino_id = fields.Int()

class MovimentacaoCreateSchema(Schema):
    equipamento_id = fields.Int(required=True)
    tipo_movimentacao = fields.Str(required=True, validate=validate.OneOf(["entrada", "saida", "transferencia"]))
    localizacao_id = fields.Int(required=True)

class MovimentacaoResponseSchema(BaseSchema):
    id = fields.Int()
    equipamento = fields.Nested(EquipamentoResponseSchema)
    estoque_origem = fields.Nested(EstoqueResponseSchema)
    estoque_destino = fields.Nested(EstoqueResponseSchema)
    localizacao_origem = fields.Nested(LocalizacaoResponseSchema)
    localizacao_destino = fields.Nested(LocalizacaoResponseSchema)
    usuario = fields.Nested(UsuarioResponseSchema)
    status = fields.Str()
    observacao = fields.Str(allow_none=True)
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime(allow_none=True) 