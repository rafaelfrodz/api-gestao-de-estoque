from app.models.movimentacao import Movimentacao
from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.utils.errors import ValidationError, NotFoundError

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
        
        # Validar estoque de origem
        try:
            estoque_origem = Estoque.get_by_id(data['estoque_origem_id'])
        except Estoque.DoesNotExist:
            raise NotFoundError("Estoque de origem não encontrado")
        
        # Validar estoque de destino
        try:
            estoque_destino = Estoque.get_by_id(data['estoque_destino_id'])
        except Estoque.DoesNotExist:
            raise NotFoundError("Estoque de destino não encontrado")
        
        # Validar localização de origem
        try:
            localizacao_origem = Localizacao.get_by_id(data['localizacao_origem_id'])
        except Localizacao.DoesNotExist:
            raise NotFoundError("Localização de origem não encontrada")
        
        # Validar localização de destino
        try:
            localizacao_destino = Localizacao.get_by_id(data['localizacao_destino_id'])
        except Localizacao.DoesNotExist:
            raise NotFoundError("Localização de destino não encontrada")
        
        # Verificar se o equipamento está no estoque de origem
        if equipamento.estoque_id != estoque_origem.id:
            raise ValidationError("Equipamento não está no estoque de origem")
        
        # Verificar se o equipamento está na localização de origem
        if equipamento.localizacao_id != localizacao_origem.id:
            raise ValidationError("Equipamento não está na localização de origem")
        
        # Criar a movimentação
        movimentacao = Movimentacao.create(
            equipamento=equipamento,
            estoque_origem=estoque_origem,
            estoque_destino=estoque_destino,
            localizacao_origem=localizacao_origem,
            localizacao_destino=localizacao_destino,
            usuario=usuario,
            status='pendente',
            observacao=data.get('observacao', '')
        )
        
        return movimentacao
    
    def confirmar_movimentacao(self, movimentacao_id, usuario):
        """
        Confirma uma movimentação pendente
        """
        try:
            movimentacao = Movimentacao.get_by_id(movimentacao_id)
        except Movimentacao.DoesNotExist:
            raise NotFoundError("Movimentação não encontrada")
        
        if movimentacao.status != 'pendente':
            raise ValidationError("Apenas movimentações pendentes podem ser confirmadas")
        
        # Atualizar o equipamento
        equipamento = movimentacao.equipamento
        equipamento.estoque = movimentacao.estoque_destino
        equipamento.localizacao = movimentacao.localizacao_destino
        equipamento.save()
        
        # Atualizar a movimentação
        movimentacao.status = 'confirmada'
        movimentacao.usuario_confirmacao = usuario
        movimentacao.save()
        
        return movimentacao
    
    def cancelar_movimentacao(self, movimentacao_id, usuario):
        """
        Cancela uma movimentação pendente
        """
        try:
            movimentacao = Movimentacao.get_by_id(movimentacao_id)
        except Movimentacao.DoesNotExist:
            raise NotFoundError("Movimentação não encontrada")
        
        if movimentacao.status != 'pendente':
            raise ValidationError("Apenas movimentações pendentes podem ser canceladas")
        
        # Atualizar a movimentação
        movimentacao.status = 'cancelada'
        movimentacao.usuario_cancelamento = usuario
        movimentacao.save()
        
        return movimentacao 