from datetime import datetime
from peewee import CharField, ForeignKeyField, DateTimeField, TextField
from app.models.base import TimestampModel
from app.models.equipamento import Equipamento
from app.models.usuario import Usuario
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.database import db

STATUS_PENDENTE = 'pendente'
STATUS_CONFIRMADO = 'confirmado'
STATUS_CANCELADO = 'cancelado'

class Movimentacao(TimestampModel):
    tipo = CharField(max_length=20)  # 'entrada' ou 'saida'
    equipamento = ForeignKeyField(Equipamento, backref='movimentacoes')
    usuario = ForeignKeyField(Usuario, backref='movimentacoes')
    usuario_confirmacao = ForeignKeyField(Usuario, backref='movimentacoes_confirmadas', null=True)
    usuario_cancelamento = ForeignKeyField(Usuario, backref='movimentacoes_canceladas', null=True)
    estoque_origem = ForeignKeyField(Estoque, backref='movimentacoes_saida', null=True)
    estoque_destino = ForeignKeyField(Estoque, backref='movimentacoes_entrada', null=True)
    localizacao_origem = ForeignKeyField(Localizacao, backref='movimentacoes_saida', null=True)
    localizacao_destino = ForeignKeyField(Localizacao, backref='movimentacoes_entrada', null=True)
    status = CharField(max_length=20, default=STATUS_PENDENTE)
    data_movimentacao = DateTimeField(default=datetime.now)
    observacao = TextField(null=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'status': self.status,
            'equipamento_id': self.equipamento.id,
            'usuario_id': self.usuario.id,
            'usuario_confirmacao_id': self.usuario_confirmacao.id if self.usuario_confirmacao else None,
            'usuario_cancelamento_id': self.usuario_cancelamento.id if self.usuario_cancelamento else None,
            'estoque_origem_id': self.estoque_origem.id if self.estoque_origem else None,
            'estoque_destino_id': self.estoque_destino.id if self.estoque_destino else None,
            'localizacao_origem_id': self.localizacao_origem.id if self.localizacao_origem else None,
            'localizacao_destino_id': self.localizacao_destino.id if self.localizacao_destino else None,
            'data_movimentacao': self.data_movimentacao.isoformat() if self.data_movimentacao else None,
            'observacao': self.observacao,
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
                    localizacao=localizacao
                )

                # Atualiza a localização do equipamento
                equipamento.localizacao = localizacao
                equipamento.save()

                return movimentacao
            except Exception as e:
                transaction.rollback()
                raise e 