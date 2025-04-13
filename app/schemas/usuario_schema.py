from marshmallow import Schema, fields, validate, ValidationError
from app.schemas.base import BaseSchema

class UsuarioSchema(BaseSchema):
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    email = fields.Email(required=True)
    senha_hash = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))  # Alterado de senha para senha_hash
    cargo = fields.Str(validate=validate.OneOf(['admin', 'operador']), default='operador')  # Campo cargo

    def validate_cargo(self, value):
        if value not in ['admin', 'operador']:
            raise ValidationError('Cargo deve ser "admin" ou "operador"')
        return value

class UsuarioLoginSchema(Schema):
    email = fields.Email(required=True)
    senha_hash = fields.Str(required=True, load_only=True)  # Alterado de senha para senha_hash

class UsuarioResponseSchema(BaseSchema):
    nome = fields.Str()
    email = fields.Email()
    cargo = fields.Str()  # Campo cargo