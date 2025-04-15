from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.estoque import Estoque
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.estoque_schema import EstoqueSchema, EstoqueCreateSchema
from app.utils.redis_cache import redis_client
import json
from app.models.localizacao import Localizacao
from app.models.equipamento import Equipamento
from app.models.tipo_equipamento import TipoEquipamento  # Add this import
from app.schemas.localizacao_schema import LocalizacaoResponseSchema
from app.schemas.equipamento_schema import EquipamentoResponseSchema, EquipamentoEstoqueResponseSchema

bp = Blueprint('estoques', __name__, url_prefix='/api/estoques')
estoque_schema = EstoqueSchema()
estoques_schema = EstoqueSchema(many=True)
estoque_create_schema = EstoqueCreateSchema()

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_estoques():
    # Verifica se os estoques estão no cache
    estoques = redis_client.get('estoques')
    if estoques:
        return success_response(json.loads(estoques))

    # Se não estiver no cache, busca no banco de dados
    estoques = Estoque.select()
    # Serializa os dados
    estoques_data = estoques_schema.dump(list(estoques))
    
    # Armazena os dados no cache
    redis_client.set('estoques', json.dumps(estoques_data), ex=60)  # Cache por 60 segundos
    return success_response(estoques_data)

@bp.route('/<int:id>/localizacoes', methods=['GET'])
@jwt_required()
@require_auth
def listar_localizacoes_estoque(id):
    try:
        # Verifica se o estoque existe
        estoque = Estoque.get_by_id(id)
        
        # Verifica cache
        cache_key = f'estoque:{id}:localizacoes'
        localizacoes_cache = redis_client.get(cache_key)
        if localizacoes_cache:
            return success_response(json.loads(localizacoes_cache))
        
        # Busca localizações do estoque
        localizacoes = Localizacao.get_by_estoque(id)
        schema = LocalizacaoResponseSchema(many=True)
        localizacoes_data = schema.dump(list(localizacoes))
        
        return success_response(localizacoes_data)
        
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404)

@bp.route('/<int:id>/equipamentos', methods=['GET'])
@jwt_required()
@require_auth
def listar_equipamentos_estoque(id):
    try:
        # Verifica se o estoque existe
        estoque = Estoque.get_by_id(id)
        
        # Obtém parâmetros de filtro
        tipo_id = request.args.get('tipo_id', None)
        status = request.args.get('status', 'ativo')  # Default é 'ativo'
        localizacao_id = request.args.get('localizacao_id', None)
        
        # Verifica cache com os parâmetros
        cache_key = f'estoque:{id}:equipamentos:{tipo_id}:{status}:{localizacao_id}'
        equipamentos_cache = redis_client.get(cache_key)
        if equipamentos_cache:
            return success_response(json.loads(equipamentos_cache))
        
        # Constrói a query base com joins para obter dados relacionados
        query = (Equipamento
                .select(Equipamento, TipoEquipamento, Localizacao)
                .join(TipoEquipamento)
                .switch(Equipamento)
                .join(Localizacao)
                .where(Equipamento.estoque_id == id))
        
        # Aplica filtros
        if status:
            query = query.where(Equipamento.status == status)
        if tipo_id:
            query = query.where(Equipamento.tipo_id == tipo_id)
        if localizacao_id:
            query = query.where(Equipamento.localizacao_id == localizacao_id)
        
        # Executa a query e serializa
        equipamentos = list(query)
        schema = EquipamentoEstoqueResponseSchema(many=True)
        equipamentos_data = schema.dump(equipamentos)
        
        return success_response(equipamentos_data)
        
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404)

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_estoque(id):
    # Verifica se o estoque está no cache
    estoque_cache = redis_client.get(f'estoque:{id}')
    if estoque_cache:
        return success_response(json.loads(estoque_cache))

    # Se não estiver no cache, busca no banco de dados
    try:
        estoque = Estoque.get_by_id(id)
        # Serializa os dados
        estoque_data = estoque_schema.dump(estoque)
        
        # Armazena os dados no cache
        redis_client.set(f'estoque:{id}', json.dumps(estoque_data), ex=60)  # Cache por 60 segundos
        return success_response(estoque_data)
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404)

@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_estoque():
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        # Validar e carregar os dados
        estoque_data = estoque_create_schema.load(data)
        
        # Criar o estoque usando o novo método
        estoque = Estoque.criar_estoque(estoque_data['nome'])
        
        # Invalida o cache após a criação
        redis_client.delete('estoques')
        
        return success_response(estoque_schema.dump(estoque), "Estoque criado com sucesso", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>/desativar', methods=['PATCH'])
@jwt_required()
@require_auth
def desativar_estoque(id):
    try:
        estoque = Estoque.get_by_id(id)
        estoque.desativar()
        
        # Invalida o cache após a atualização
        redis_client.delete('estoques')
        redis_client.delete(f'estoque:{id}')
        
        return success_response(estoque_schema.dump(estoque), "Estoque desativado com sucesso")
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)

