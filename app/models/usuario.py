from werkzeug.security import generate_password_hash, check_password_hash
from peewee import CharField, BooleanField
from app.models.base import TimestampModel

class Usuario(TimestampModel):
    nome = CharField(max_length=100)
    email = CharField(max_length=120, unique=True)
    senha_hash = CharField(max_length=255, null=False)
    ativo = BooleanField(default=True)
    papel = CharField(max_length=20, default='operador')  # 'admin' ou 'operador'

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_admin(self):
        return self.papel == 'admin'

    class Meta:
        table_name = 'usuarios' 