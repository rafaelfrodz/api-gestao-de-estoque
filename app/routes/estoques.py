from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.estoque import Estoque
from app.utils.responses import success_response, error_response
from app.utils.auth import require_auth
from app.schemas.estoque_schema import EstoqueSchema, EstoqueCreateSchema

bp = Blueprint('estoques', __name__, url_prefix='/api/estoques')
estoque_schema = EstoqueSchema()
estoques_schema = EstoqueSchema(many=True)
estoque_create_schema = EstoqueCreateSchema()

@bp.route('/', methods=['GET'])
@jwt_required()
@require_auth
def listar_estoques():
    estoques = Estoque.select()
    return success_response(estoques_schema.dump(list(estoques)))

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@require_auth
def obter_estoque(id):
    try:
        estoque = Estoque.get_by_id(id)
        return success_response(estoque_schema.dump(estoque))
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
        
        return success_response(estoque_schema.dump(estoque), "Estoque criado com sucesso", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@require_auth
def atualizar_estoque(id):
    try:
        estoque = Estoque.get_by_id(id)
        data = request.get_json()
        
        if not data:
            return error_response("Dados inválidos", 400)
        
        estoque_data = estoque_schema.load(data, partial=True)
        for key, value in estoque_data.items():
            setattr(estoque, key, value)
        estoque.save()
        
        return success_response(estoque_schema.dump(estoque), "Estoque atualizado com sucesso")
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404)
    except Exception as e:
        return error_response(str(e), 400)

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_auth
def deletar_estoque(id):
    try:
        estoque = Estoque.get_by_id(id)
        estoque.delete_instance()
        return success_response(None, "Estoque deletado com sucesso")
    except Estoque.DoesNotExist:
        return error_response("Estoque não encontrado", 404) 