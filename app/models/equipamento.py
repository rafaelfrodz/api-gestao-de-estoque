from datetime import datetime
from peewee import CharField, ForeignKeyField, BooleanField, DateTimeField
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
    
    @classmethod
    def get_ativos(cls):
        return cls.select().where(cls.status == 'ativo')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'status': self.status,
            'estoque_id': self.estoque.id,
            'localizacao_id': self.localizacao.id,
            'tipo_id': self.tipo.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 