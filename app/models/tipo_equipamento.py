from peewee import CharField, IntegrityError
from app.models.base import TimestampModel

class TipoEquipamento(TimestampModel):
    nome = CharField(max_length=100, unique=True)

    class Meta:
        table_name = 'tipos_equipamento'

    @classmethod
    def criar_tipo(cls, nome):
        try:
            return cls.create(nome=nome)
        except IntegrityError:
            raise ValueError(f"Já existe um tipo de equipamento com o nome '{nome}'") 