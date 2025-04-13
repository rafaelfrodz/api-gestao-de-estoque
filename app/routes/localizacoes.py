from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.localizacao import Localizacao
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.localizacao_schema import LocalizacaoSchema, localizacao_create_schema

bp = Blueprint('localizacoes', __name__, url_prefix='/api/localizacoes')
localizacao_schema = LocalizacaoSchema()
localizacoes_schema = LocalizacaoSchema(many=True)

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_localizacoes():
    localizacoes = Localizacao.select()
    return success_response(localizacoes_schema.dump(list(localizacoes)))

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_localizacao(id):
    try:
        localizacao = Localizacao.get_by_id(id)
        return success_response(localizacao_schema.dump(localizacao))
    except Localizacao.DoesNotExist:
        return error_response("Localização não encontrada", 404)

@bp.route('/', methods=['POST'])
@jwt_required()
@require_auth
def criar_localizacao():
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        # Validar e carregar os dados
        localizacao_data = localizacao_create_schema.load(data)
        
        # Criar a localização usando o novo método
        localizacao = Localizacao.criar_localizacao(
            nome=localizacao_data['nome'],
            estoque_id=localizacao_data['estoque_id']
        )
        
        return success_response(localizacao_schema.dump(localizacao), "Localização criada com sucesso", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_auth
def atualizar_localizacao(id):
    try:
        localizacao = Localizacao.get_by_id(id)
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        localizacao_data = localizacao_schema.load(data, partial=True)
        for key, value in localizacao_data.items():
            setattr(localizacao, key, value)
        localizacao.save()
        
        return success_response(localizacao_schema.dump(localizacao), "Localização atualizada com sucesso")
    except Localizacao.DoesNotExist:
        return error_response("Localização não encontrada", 404)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_auth
def deletar_localizacao(id):
    try:
        localizacao = Localizacao.get_by_id(id)
        localizacao.delete_instance()
        return success_response(None, "Localização deletada com sucesso")
    except Localizacao.DoesNotExist:
        return error_response("Localização não encontrada", 404) 