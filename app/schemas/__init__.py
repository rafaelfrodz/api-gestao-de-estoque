# Schemas do projeto
from app.schemas.equipamento_schema import EquipamentoSchema, EquipamentoCreateSchema, EquipamentoUpdateSchema, EquipamentoResponseSchema
from app.schemas.estoque_schema import EstoqueSchema, EstoqueCreateSchema, EstoqueUpdateSchema, EstoqueResponseSchema
from app.schemas.localizacao_schema import LocalizacaoSchema, LocalizacaoCreateSchema, LocalizacaoUpdateSchema, LocalizacaoResponseSchema
from app.schemas.movimentacao_schema import MovimentacaoSchema, MovimentacaoCreateSchema, MovimentacaoResponseSchema
from app.schemas.tipo_equipamento_schema import TipoEquipamentoSchema, TipoEquipamentoCreateSchema, TipoEquipamentoUpdateSchema, TipoEquipamentoResponseSchema
from app.schemas.usuario_schema import UsuarioSchema, UsuarioLoginSchema, UsuarioResponseSchema

__all__ = [
    'EquipamentoSchema',
    'EquipamentoCreateSchema',
    'EquipamentoUpdateSchema',
    'EquipamentoResponseSchema',
    'EstoqueSchema',
    'EstoqueCreateSchema',
    'EstoqueUpdateSchema',
    'EstoqueResponseSchema',
    'LocalizacaoSchema',
    'LocalizacaoCreateSchema',
    'LocalizacaoUpdateSchema',
    'LocalizacaoResponseSchema',
    'MovimentacaoSchema',
    'MovimentacaoCreateSchema',
    'MovimentacaoResponseSchema',
    'TipoEquipamentoSchema',
    'TipoEquipamentoCreateSchema',
    'TipoEquipamentoUpdateSchema',
    'TipoEquipamentoResponseSchema',
    'UsuarioSchema',
    'UsuarioLoginSchema',
    'UsuarioResponseSchema'
] 