from marshmallow import Schema, fields, validate
from app.schemas.base import BaseSchema

class LocalizacaoBaseSchema(Schema):
    nome = fields.Str(required=True)
    estoque_id = fields.Int(required=True)

class LocalizacaoCreateSchema(LocalizacaoBaseSchema):
    pass

class LocalizacaoSchema(LocalizacaoBaseSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class LocalizacaoUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=3, max=100))
    estoque_id = fields.Int()

class LocalizacaoResponseSchema(BaseSchema):
    nome = fields.Str()
    estoque_id = fields.Int()

# Instâncias dos schemas
localizacao_create_schema = LocalizacaoCreateSchema()
localizacao_schema = LocalizacaoSchema() 