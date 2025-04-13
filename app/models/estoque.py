from peewee import CharField, BooleanField, IntegrityError
from app.models.base import TimestampModel

class Estoque(TimestampModel):
    nome = CharField(max_length=100, unique=True)
    status = BooleanField(default=True)  # True = ativo, False = inativo

    class Meta:
        table_name = 'estoques'

    def desativar(self):
        self.status = False
        return self.save()

    def ativar(self):
        self.status = True
        return self.save()

    @classmethod
    def criar_estoque(cls, nome):
        try:
            return cls.create(nome=nome)
        except IntegrityError:
            raise ValueError(f"Já existe um estoque com o nome '{nome}'") 