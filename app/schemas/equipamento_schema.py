from marshmallow import Schema, fields, validate
from app.schemas.estoque_schema import EstoqueSchema
from app.schemas.localizacao_schema import LocalizacaoSchema
from app.schemas.tipo_equipamento_schema import TipoEquipamentoSchema

class EquipamentoBaseSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=1, max=100))
    status = fields.String(required=True, validate=validate.OneOf(['ativo', 'inativo']))
    estoque_id = fields.Integer(required=True)
    localizacao_id = fields.Integer(required=True)
    tipo_id = fields.Integer(required=True)

class EquipamentoCreateSchema(EquipamentoBaseSchema):
    pass

class EquipamentoUpdateSchema(EquipamentoBaseSchema):
    nome = fields.String(validate=validate.Length(min=1, max=100))
    status = fields.String(validate=validate.OneOf(['ativo', 'inativo']))
    estoque_id = fields.Integer()
    localizacao_id = fields.Integer()
    tipo_id = fields.Integer()

class EquipamentoSchema(EquipamentoBaseSchema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class EquipamentoResponseSchema(EquipamentoSchema):
    estoque = fields.Nested(EstoqueSchema, dump_only=True)
    localizacao = fields.Nested(LocalizacaoSchema, dump_only=True)
    tipo = fields.Nested(TipoEquipamentoSchema, dump_only=True) 