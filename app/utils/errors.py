class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(APIError):
    def __init__(self, message="Recurso não encontrado"):
        super().__init__(message, status_code=404)

class ValidationError(APIError):
    def __init__(self, message="Erro de validação"):
        super().__init__(message, status_code=400)

class AuthenticationError(APIError):
    def __init__(self, message="Erro de autenticação"):
        super().__init__(message, status_code=401) 