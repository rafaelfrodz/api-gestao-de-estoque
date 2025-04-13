from marshmallow import Schema, fields, validate, ValidationError
from app.schemas.base import BaseSchema
from app.schemas.equipamento_schema import EquipamentoResponseSchema
from app.schemas.usuario_schema import UsuarioResponseSchema
from app.schemas.estoque_schema import EstoqueResponseSchema
from app.schemas.localizacao_schema import LocalizacaoResponseSchema
from app.models.movimentacao import Movimentacao

class MovimentacaoSchema(BaseSchema):
    equipamento_id = fields.Int(required=True)
    estoque_origem_id = fields.Int(required=True)
    estoque_destino_id = fields.Int(required=True)
    localizacao_origem_id = fields.Int(required=True)
    localizacao_destino_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    observacao = fields.Str(allow_none=True)

class MovimentacaoCreateSchema(Schema):
    equipamento_id = fields.Int(required=True)
    estoque_origem_id = fields.Int(required=True)
    estoque_destino_id = fields.Int(required=True)
    localizacao_origem_id = fields.Int(required=True)
    localizacao_destino_id = fields.Int(required=True)
    observacao = fields.Str(allow_none=True)

class MovimentacaoResponseSchema(BaseSchema):
    id = fields.Int()
    equipamento = fields.Nested(EquipamentoResponseSchema)
    estoque_origem = fields.Nested(EstoqueResponseSchema)
    estoque_destino = fields.Nested(EstoqueResponseSchema)
    localizacao_origem = fields.Nested(LocalizacaoResponseSchema)
    localizacao_destino = fields.Nested(LocalizacaoResponseSchema)
    usuario = fields.Nested(UsuarioResponseSchema)
    usuario_confirmacao = fields.Nested(UsuarioResponseSchema, allow_none=True)
    usuario_cancelamento = fields.Nested(UsuarioResponseSchema, allow_none=True)
    status = fields.Str()
    observacao = fields.Str(allow_none=True)
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime(allow_none=True) 