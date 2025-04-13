from marshmallow import Schema, fields

class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    criado_em = fields.DateTime(dump_only=True)
    atualizado_em = fields.DateTime(dump_only=True) 