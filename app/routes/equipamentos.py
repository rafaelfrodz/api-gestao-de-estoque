from flask import Blueprint, request, jsonify
from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.localizacao import Localizacao
from app.models.tipo_equipamento import TipoEquipamento
from app.schemas.equipamento_schema import (
    EquipamentoCreateSchema, EquipamentoUpdateSchema,
    EquipamentoResponseSchema
)
from app.utils.auth import require_auth
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

@bp.route('/<int:id>', methods=['PUT'])
@require_auth
def atualizar_equipamento(id):
    try:
        equipamento = Equipamento.get_by_id(id)
        schema = EquipamentoUpdateSchema()
        data = schema.load(request.get_json())
        
        # Validar existência das entidades relacionadas se fornecidas
        if 'estoque_id' in data:
            Estoque.get_by_id(data['estoque_id'])
        if 'localizacao_id' in data:
            Localizacao.get_by_id(data['localizacao_id'])
        if 'tipo_id' in data:
            TipoEquipamento.get_by_id(data['tipo_id'])
        
        for key, value in data.items():
            setattr(equipamento, key, value)
        
        equipamento.save()
        
        # Atualiza o cache após a atualização
        redis_client.delete('equipamentos')  # Invalida o cache
        return jsonify(EquipamentoResponseSchema().dump(equipamento.to_dict())), 200
    except DoesNotExist:
        return jsonify({"error": "Equipamento não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
@require_auth
def deletar_equipamento(id):
    try:
        equipamento = Equipamento.get_by_id(id)
        equipamento.delete_instance()
        
        # Atualiza o cache após a exclusão
        redis_client.delete('equipamentos')  # Invalida o cache
        return jsonify({"message": "Equipamento deletado com sucesso"}), 200
    except DoesNotExist:
        return jsonify({"error": "Equipamento não encontrado"}), 404 