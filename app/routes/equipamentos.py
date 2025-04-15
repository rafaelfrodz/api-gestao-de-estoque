from flask import Blueprint, request, jsonify
from app.models import equipamento
from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento
from app.schemas.equipamento_schema import (
    EquipamentoCreateSchema, EquipamentoUpdateSchema,
    EquipamentoResponseSchema
)
from marshmallow import ValidationError  # Add this import
from app.utils.auth import require_auth
from app.utils.responses import success_response, error_response  # Add this import
from peewee import DoesNotExist
from app.utils.redis_cache import redis_client
import json
from flask_jwt_extended import jwt_required

bp = Blueprint('equipamentos', __name__, url_prefix='/api/equipamentos')

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_equipamentos():
    # Verifica se os equipamentos estão no cache
    equipamentos_cache = redis_client.get('equipamentos')
    if equipamentos_cache:
        return jsonify(json.loads(equipamentos_cache)), 200

    # Filtra apenas os equipamentos com status ativo
    equipamentos = Equipamento.select().where(Equipamento.status == 'ativo')
    equipamentos_data = EquipamentoResponseSchema(many=True).dump([e.to_dict() for e in equipamentos])
    
    # Armazena os dados no cache
    redis_client.set('equipamentos', json.dumps(equipamentos_data), ex=60)  # Cache por 60 segundos
    return jsonify(equipamentos_data), 200

@bp.route('/<int:id>', methods=['GET'])
@require_auth
def obter_equipamento(id):
    try:
        equipamento = Equipamento.get_by_id(id)
        schema = EquipamentoResponseSchema()
        return jsonify(schema.dump(equipamento.to_dict())), 200
    except DoesNotExist:
        return jsonify({"error": "Equipamento não encontrado"}), 404

@bp.route('/', methods=['POST'])
@require_auth
def criar_equipamento():
    try:
        schema = EquipamentoCreateSchema()
        data = schema.load(request.get_json())
        
        # Validar existência das entidades relacionadas
        try:
            Estoque.get_by_id(data['estoque_id'])
            Localizacao.get_by_id(data['localizacao_id'])
            TipoEquipamento.get_by_id(data['tipo_id'])
        except DoesNotExist as e:
            return jsonify({'error': 'Entidade relacionada não encontrada'}), 404
        
        equipamento = Equipamento.create(**data)
        
        # Atualiza o cache após a criação
        redis_client.delete('equipamentos')  # Invalida o cache
        return jsonify(EquipamentoResponseSchema().dump(equipamento.to_dict())), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

@bp.route('/<int:id>/desativar', methods=['PATCH'])
@require_auth
def desativar_equipamento(id):
    try:
        equipamento = Equipamento.get_by_id(id)
        equipamento.desativar()
        
        # Invalida o cache após a atualização
        redis_client.delete('equipamentos')
        redis_client.delete(f'equipamentos:{id}')
        
        return success_response(
            EquipamentoResponseSchema().dump(equipamento.to_dict()), 
            "Equipamento desativado com sucesso"
        )
    except Equipamento.DoesNotExist:  
        return error_response("Equipamento não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)
