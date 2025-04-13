from peewee import CharField, ForeignKeyField, IntegrityError
from app.models.base import TimestampModel
from app.models.estoque import Estoque

class Localizacao(TimestampModel):
    nome = CharField(max_length=100)
    estoque = ForeignKeyField(Estoque, backref='localizacoes')

    class Meta:
        table_name = 'localizacoes'

    @classmethod
    def get_by_estoque(cls, estoque_id):
        return cls.select().where(cls.estoque_id == estoque_id)

    @classmethod
    def criar_localizacao(cls, nome, estoque_id):
        try:
            estoque = Estoque.get_by_id(estoque_id)
            return cls.create(nome=nome, estoque=estoque)
        except Estoque.DoesNotExist:
            raise ValueError(f"Estoque com ID {estoque_id} não encontrado")
        except IntegrityError:
            raise ValueError(f"Já existe uma localização com o nome '{nome}' neste estoque") 