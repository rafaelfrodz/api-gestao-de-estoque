from app.models.movimentacao import Movimentacao
from app.models.equipamento import Equipamento
from app.models.localizacao import Localizacao
from app.utils.errors import ValidationError, NotFoundError
from datetime import datetime

class MovimentacaoService:
    def criar_movimentacao(self, data, usuario):
        """
        Cria uma nova movimentação de equipamento
        """
        # Validar equipamento
        try:
            equipamento = Equipamento.get_by_id(data['equipamento_id'])
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        
        # Validar localização de destino
        try:
            localizacao_destino = Localizacao.get_by_id(data['localizacao_id'])
        except Localizacao.DoesNotExist:
            raise NotFoundError("Localização de destino não encontrada")
        
        # Criar a movimentação
        movimentacao = Movimentacao.create(
            equipamento=equipamento,
            usuario=usuario,
            tipo_movimentacao=data['tipo_movimentacao'],
            data_hora=datetime.now(),
            localizacao_destino=localizacao_destino
        )
        
        # Atualizar a localização do equipamento
        equipamento.localizacao = localizacao_destino
        equipamento.save()

        return movimentacao
