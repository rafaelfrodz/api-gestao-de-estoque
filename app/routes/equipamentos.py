from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request
from peewee import DoesNotExist
from app.services.equipamento_service import EquipamentoService
from app.schemas.equipamento_schema import (
    EquipamentoCreateSchema,
    EquipamentoResponseSchema
)
from app.utils.redis_cache import redis_client
from app.utils.responses import success_response, error_response 
from app.utils.errors import NotFoundError, ValidationError
from marshmallow import ValidationError as MarshmallowValidationError
import json

bp = Blueprint('equipamentos', __name__, url_prefix='/api/equipamentos')

@bp.before_request
def before_request_callback():
    verify_jwt_in_request()

@bp.route('/', methods=['GET'])
def listar_equipamentos():
    # Verifica se os equipamentos estão no cache
    equipamentos_cache = redis_client.get('equipamentos')
    if equipamentos_cache:
        return jsonify(json.loads(equipamentos_cache)), 200

    # Filtra apenas os equipamentos com status ativo
    equipamentos = EquipamentoService.listar_ativos()
    equipamentos_data = EquipamentoResponseSchema(many=True).dump(equipamentos)
    
    # Armazena os dados no cache
    redis_client.set('equipamentos', json.dumps(equipamentos_data), ex=60)  # Cache por 60 segundos
    return jsonify(equipamentos_data), 200

@bp.route('/<int:id>', methods=['GET'])
def obter_equipamento(id):
    try:
        equipamento = EquipamentoService.buscar_por_id(id)
        schema = EquipamentoResponseSchema()
        return jsonify(schema.dump(equipamento)), 200
    except DoesNotExist:
        return jsonify({"error": "Equipamento não encontrado"}), 404

@bp.route('/', methods=['POST'])
def criar_equipamento():
    try:
        schema = EquipamentoCreateSchema()
        data = schema.load(request.get_json())
        
        # Validar existência das entidades relacionadas
        try:
            equipamento = EquipamentoService.criar_equipamento(data)
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return error_response(e.args[0], 400)

        # Atualiza o cache após a criação
        redis_client.delete('equipamentos')  # Invalida o cache
        return jsonify(EquipamentoResponseSchema().dump(equipamento)), 201
    except MarshmallowValidationError as err:
        return error_response(err.messages, 400)
@bp.route('/<int:id>/<string:acao>', methods=['PATCH'])
def desativar_equipamento(id, acao):
    try:
        # Realiza a ação de desativação ou ativação
        if acao == 'desativar':
            equipamento = EquipamentoService.desativar_equipamento(id)
            message = "Equipamento desativado com sucesso"
        elif acao == 'ativar':
            equipamento = EquipamentoService.ativar_equipamento(id)
            message = "Equipamento ativado com sucesso"
        else:
            return error_response("Ação inválida", 400)
        # Invalida o cache após a atualização
        redis_client.delete('equipamentos')
        
        return success_response(
            EquipamentoResponseSchema().dump(equipamento), 
            message
        )
    except DoesNotExist:  
        return error_response("Equipamento não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)
    