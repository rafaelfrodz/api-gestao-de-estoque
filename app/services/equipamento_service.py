from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento
from app.utils.errors import NotFoundError, ValidationError

class EquipamentoService:
    @staticmethod
    def criar_equipamento(data):
        erros = {}
        # Validação de estoque
        try:
            estoque = Estoque.get_by_id(data['estoque_id'])
        except Estoque.DoesNotExist:
            erros['estoque_id'] = "Estoque não encontrado"
            estoque = None
        
        # Validação de localização
        try:
            localizacao = Localizacao.get_by_id(data['localizacao_id'])
        except Localizacao.DoesNotExist:
            erros['localizacao_id'] = "Localização não encontrada"
            localizacao = None
        
        # Validação de tipo
        try:
            tipo = TipoEquipamento.get_by_id(data['tipo_id'])
        except TipoEquipamento.DoesNotExist:
            erros['tipo_id'] = "Tipo de equipamento não encontrado"
            tipo = None
        
        if erros:
            raise ValidationError(erros)
        # Verifica se a localização pertence ao estoque
        if localizacao.estoque_id != estoque.id:
            raise ValidationError("A localização não pertence ao estoque selecionado")
        
        equipamento = Equipamento.create(
            nome=data['nome'],
            estoque=estoque,
            localizacao=localizacao,
            tipo=tipo,
            status=data.get('status', 'ativo')
        )
        return EquipamentoService.to_dict(equipamento)

    @staticmethod
    def desativar_equipamento(equipamento_id):
        try:
            equipamento = Equipamento.get_by_id(equipamento_id)
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        equipamento.status = 'inativo'
        equipamento.save()
        return EquipamentoService.to_dict(equipamento)

    @staticmethod
    def ativar_equipamento(equipamento_id):
        try:
            equipamento = Equipamento.get_by_id(equipamento_id)
        except Equipamento.DoesNotExist:
            raise NotFoundError("Equipamento não encontrado")
        equipamento.status = 'ativo'
        equipamento.save()
        return EquipamentoService.to_dict(equipamento)

    @staticmethod
    def listar_ativos():
        Equipamento.select().where(Equipamento.status == 'ativo')
        equipamentos = Equipamento.select().where(Equipamento.status == 'ativo')
        return [EquipamentoService.to_dict(equipamento) for equipamento in equipamentos]
    
    @staticmethod
    def buscar_por_id(equipamento_id):
        equipamento = Equipamento.get_by_id(equipamento_id)
        return EquipamentoService.to_dict(equipamento)

    @staticmethod
    def to_dict(equipamento):
        return {
            'id': equipamento.id,
            'nome': equipamento.nome,
            'status': equipamento.status,
            'estoque_id': equipamento.estoque.id,
            'localizacao_id': equipamento.localizacao.id,
            'tipo_id': equipamento.tipo.id,
            'created_at': equipamento.created_at,
            'updated_at': equipamento.updated_at
        }