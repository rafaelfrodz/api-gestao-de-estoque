from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento
from app.utils.errors import NotFoundError, ValidationError

class EquipamentoService:
    def criar_equipamento(self, data):
        """
        Cria um novo equipamento
        """
        # Validar estoque
        try:
            estoque = Estoque.get_by_id(data['estoque_id'])
        except Estoque.DoesNotExist:
            raise NotFoundError("Estoque não encontrado")
        
        # Validar localização
        try:
            localizacao = Localizacao.get_by_id(data['localizacao_id'])
        except Localizacao.DoesNotExist:
            raise NotFoundError("Localização não encontrada")
        
        # Validar tipo
        try:
            tipo = TipoEquipamento.get_by_id(data['tipo_id'])
        except TipoEquipamento.DoesNotExist:
            raise NotFoundError("Tipo de equipamento não encontrado")
        
        # Verificar se a localização pertence ao estoque
        if localizacao.estoque_id != estoque.id:
            raise ValidationError("A localização não pertence ao estoque selecionado")
        
        # Criar o equipamento
        equipamento = Equipamento.create(
            nome=data['nome'],
            estoque=estoque,
            localizacao=localizacao,
            tipo=tipo
        )
        
        return equipamento
    
    def atualizar_equipamento(self, equipamento_id, data):
        """
        Atualiza um equipamento existente
        """
        try:
            equipamento = Equipamento.get_by_id(equipamento_id)
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        
        # Validar estoque se fornecido
        if 'estoque_id' in data:
            try:
                estoque = Estoque.get_by_id(data['estoque_id'])
                equipamento.estoque = estoque
            except Estoque.DoesNotExist:
                raise NotFoundError("Estoque não encontrado")
        
        # Validar localização se fornecida
        if 'localizacao_id' in data:
            try:
                localizacao = Localizacao.get_by_id(data['localizacao_id'])
                equipamento.localizacao = localizacao
            except Localizacao.DoesNotExist:
                raise NotFoundError("Localização não encontrada")
        
        # Validar tipo se fornecido
        if 'tipo_id' in data:
            try:
                tipo = TipoEquipamento.get_by_id(data['tipo_id'])
                equipamento.tipo = tipo
            except TipoEquipamento.DoesNotExist:
                raise NotFoundError("Tipo de equipamento não encontrado")
        
        # Atualizar nome se fornecido
        if 'nome' in data:
            equipamento.nome = data['nome']
        
        # Atualizar status se fornecido
        if 'status' in data:
            equipamento.status = data['status']
        
        # Verificar se a localização pertence ao estoque
        if equipamento.localizacao.estoque_id != equipamento.estoque.id:
            raise ValidationError("A localização não pertence ao estoque selecionado")
        
        # Salvar as alterações
        equipamento.save()
        
        return equipamento
    
    def desativar_equipamento(self, equipamento_id):
        """
        Desativa um equipamento
        """
        try:
            equipamento = Equipamento.get_by_id(equipamento_id)
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        
        equipamento.status = 'inativo'
        equipamento.save()
        return equipamento
    
    def ativar_equipamento(self, equipamento_id):
        """
        Ativa um equipamento
        """
        try:
            equipamento = Equipamento.get_by_id(equipamento_id)
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        
        equipamento.status = 'ativo'
        equipamento.save()
        return equipamento 