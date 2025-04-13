from marshmallow import Schema, fields

class TipoEquipamentoBaseSchema(Schema):
    nome = fields.Str(required=True)

class TipoEquipamentoCreateSchema(TipoEquipamentoBaseSchema):
    pass

class TipoEquipamentoSchema(TipoEquipamentoBaseSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Instâncias dos schemas
tipo_create_schema = TipoEquipamentoCreateSchema()
tipo_schema = TipoEquipamentoSchema() 