from app.routes.auth import bp as auth_bp
from app.routes.estoques import bp as estoques_bp
from app.routes.equipamentos import bp as equipamentos_bp
from app.routes.localizacoes import bp as localizacoes_bp
from app.routes.movimentacoes import bp as movimentacoes_bp
from app.routes.tipos_equipamento import bp as tipos_equipamento_bp
import logging

logger = logging.getLogger(__name__)

# Verifica se o módulo foi importado corretamente
logger.debug("Importando blueprints...")
logger.debug(f"tipos_equipamento_bp: {tipos_equipamento_bp}")

__all__ = [
    'auth_bp',
    'estoques_bp',
    'equipamentos_bp',
    'localizacoes_bp',
    'movimentacoes_bp',
    'tipos_equipamento_bp'
] 