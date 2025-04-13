from datetime import datetime
from peewee import AutoField, ForeignKeyField, DateTimeField, CharField
from app.models.base import TimestampModel
from app.models.equipamento import Equipamento
from app.models.usuario import Usuario
from app.models.localizacao import Localizacao
from app.database import db

class Movimentacao(TimestampModel):
    id = AutoField()  # Gera automaticamente um ID único
    equipamento = ForeignKeyField(Equipamento, backref='movimentacoes', on_delete='CASCADE')
    usuario = ForeignKeyField(Usuario, backref='movimentacoes', on_delete='CASCADE')
    tipo_movimentacao = CharField(max_length=20, choices=["entrada", "saida", "transferencia"])  # Tipo de movimentação
    data_hora = DateTimeField(default=datetime.now)  # Data e hora da movimentação
    localizacao_destino = ForeignKeyField(Localizacao, backref='movimentacoes', null=True, on_delete='SET NULL')  # Localização de destino

    def to_dict(self):
        return {
            'id': self.id,
            'equipamento_id': self.equipamento.id,
            'usuario_id': self.usuario.id,
            'tipo_movimentacao': self.tipo_movimentacao,
            'data_hora': self.data_hora.isoformat(),
            'localizacao_destino_id': self.localizacao_destino.id if self.localizacao_destino else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    class Meta:
        database = db

    @classmethod
    def criar_movimentacao(cls, equipamento_id, usuario_id, tipo, localizacao_id):
        from app.utils.database import db
        
        with db.atomic() as transaction:
            try:
                equipamento = Equipamento.get_by_id(equipamento_id)
                usuario = Usuario.get_by_id(usuario_id)
                localizacao = Localizacao.get_by_id(localizacao_id)

                if tipo not in cls.TIPOS_MOVIMENTACAO:
                    raise ValueError(f"Tipo de movimentação inválido. Deve ser um dos seguintes: {', '.join(cls.TIPOS_MOVIMENTACAO)}")

                movimentacao = cls.create(
                    equipamento=equipamento,
                    usuario=usuario,
                    tipo_movimentacao=tipo,
                    data_hora=datetime.now(),
                    localizacao_destino=localizacao
                )

                # Atualiza a localização do equipamento
                equipamento.localizacao = localizacao
                equipamento.save()

                return movimentacao
            except Exception as e:
                transaction.rollback()
                raise e 