from flask import jsonify

def success_response(data=None, message="Operação realizada com sucesso", status_code=200):
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="Erro na operação", status_code=400):
    response = {
        "success": False,
        "message": message
    }
    return jsonify(response), status_code 