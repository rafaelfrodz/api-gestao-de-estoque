from marshmallow import Schema, fields, validate
from app.schemas.base import BaseSchema

class EstoqueSchema(BaseSchema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    status = fields.Bool(dump_only=True)

class EstoqueCreateSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))

class EstoqueUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=3, max=100))
    status = fields.Bool()

class EstoqueResponseSchema(BaseSchema):
    nome = fields.Str()
    status = fields.Bool() 