from datetime import datetime
from peewee import CharField, ForeignKeyField, DateTimeField
from app.models.base import TimestampModel
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento

class Equipamento(TimestampModel):
    nome = CharField(max_length=100)
    status = CharField(default='ativo')
    estoque = ForeignKeyField(Estoque, backref='equipamentos', field='id')
    localizacao = ForeignKeyField(Localizacao, backref='equipamentos', field='id')
    tipo = ForeignKeyField(TipoEquipamento, backref='equipamentos', field='id')
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
  