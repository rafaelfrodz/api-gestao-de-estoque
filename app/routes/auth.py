from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.usuario import Usuario
from app.utils.responses import success_response, error_response
from app.utils.errors import AuthenticationError
from werkzeug.security import generate_password_hash
import logging
import traceback

# Configuração de logging
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.debug(f"Dados recebidos: {data}")
        
        if not data:
            logger.warning("Nenhum dado recebido na requisição")
            return error_response("Dados inválidos", 400)
            
        if not data.get('email') or not data.get('senha'):
            logger.warning("Email ou senha não fornecidos")
            return error_response("Email e senha são obrigatórios", 400)
        
        try:
            usuario = Usuario.get(Usuario.email == data['email'])
            logger.debug(f"Usuário encontrado: {usuario.email}")
        except Usuario.DoesNotExist:
            logger.warning(f"Usuário não encontrado para o email: {data['email']}")
            return error_response("Email ou senha inválidos", 401)
        
        if not usuario.check_senha(data['senha']):
            logger.warning(f"Senha incorreta para o usuário: {usuario.email}")
            return error_response("Email ou senha inválidos", 401)
        
        if not usuario.ativo:
            logger.warning(f"Usuário inativo tentou fazer login: {usuario.email}")
            return error_response("Usuário inativo", 401)
        
        # Criar claims do usuário
        claims = {
            'id': usuario.id,
            'email': usuario.email,
            'nome': usuario.nome,
            'papel': usuario.papel
        }
        
        # Criar tokens com as claims
        access_token = create_access_token(identity=str(usuario.id), additional_claims=claims)
        refresh_token = create_refresh_token(identity=str(usuario.id), additional_claims=claims)
        
        logger.info(f"Login bem-sucedido para o usuário: {usuario.email}")
        
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            }
        }
        
        logger.debug(f"Resposta de sucesso: {response_data}")
        return success_response(response_data)
        
    except Exception as e:
        logger.error(f"Erro durante o login: {str(e)}")
        logger.error(traceback.format_exc())
        return error_response("Erro interno do servidor", 500)

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return success_response({'access_token': access_token})

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('nome') or not data.get('email') or not data.get('senha'):
        return error_response("Nome, email e senha são obrigatórios", 400)
    
    if Usuario.select().where(Usuario.email == data['email']).exists():
        return error_response("Email já cadastrado", 400)
    
    senha_hash = generate_password_hash(data['senha'])
    usuario = Usuario.create(
        nome=data['nome'],
        email=data['email'],
        senha_hash=senha_hash
    )
    
    return success_response({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email
    }, "Usuário criado com sucesso", 201) 