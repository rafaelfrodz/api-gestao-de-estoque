from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.models.tipo_equipamento import TipoEquipamento
from app.utils.errors import NotFoundError, ValidationError
import logging
from app.schemas.tipo_equipamento_schema import tipo_create_schema, tipo_schema

logger = logging.getLogger(__name__)

# Cria o blueprint
bp = Blueprint('tipos_equipamento', __name__, url_prefix='/api/tipos_equipamento')
logger.debug(f"Criando blueprint tipos_equipamento com url_prefix: {bp.url_prefix}")

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_tipos_equipamento():
    logger.debug("Listando tipos de equipamento")
    tipos = TipoEquipamento.select()
    return success_response([tipo.to_dict() for tipo in tipos])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_tipo_equipamento(id):
    try:
        tipo = TipoEquipamento.get_by_id(id)
        return success_response(tipo.to_dict())
    except TipoEquipamento.DoesNotExist:
        return error_response("Tipo de equipamento não encontrado", 404)

@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_tipo_equipamento():
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        # Validar e carregar os dados
        tipo_data = tipo_create_schema.load(data)
        
        # Criar o tipo usando o novo método
        tipo = TipoEquipamento.criar_tipo(tipo_data['nome'])
        
        return success_response(tipo_schema.dump(tipo), "Tipo de equipamento criado com sucesso", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_auth
def atualizar_tipo_equipamento(id):
    try:
        tipo = TipoEquipamento.get_by_id(id)
        data = request.get_json()
        
        if not data.get('nome'):
            raise ValidationError("O nome é obrigatório")
        
        tipo.nome = data['nome']
        tipo.save()
        return success_response(tipo.to_dict(), "Tipo de equipamento atualizado com sucesso")
    except TipoEquipamento.DoesNotExist:
        return error_response("Tipo de equipamento não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_auth
def deletar_tipo_equipamento(id):
    try:
        tipo = TipoEquipamento.get_by_id(id)
        tipo.delete_instance()
        return success_response(None, "Tipo de equipamento deletado com sucesso")
    except TipoEquipamento.DoesNotExist:
        return error_response("Tipo de equipamento não encontrado", 404) 