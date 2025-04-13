from marshmallow import Schema, fields, validate
from app.schemas.base import BaseSchema

class TipoEquipamentoSchema(BaseSchema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))

class TipoEquipamentoCreateSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))

class TipoEquipamentoUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=3, max=100))

class TipoEquipamentoResponseSchema(BaseSchema):
    nome = fields.Str() 