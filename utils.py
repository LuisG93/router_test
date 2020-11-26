from cerberus import Validator, errors
from flask import Flask, jsonify, make_response, request
from functools import wraps

def validate_request(schema):
    """
    Decorador para validar un el request
    - schema: diccionario con el schema que debe cumplir la petición
    Por default los campos son requeridos
    """
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validate_data = request.json.copy() if request.json else {}
            if not isinstance(schema, dict):
                raise TypeError('The schema should be a dict')
            v = Validator(schema, error_handler=CustomErrorHandler)
            v.allow_unknown = True
            if not v.validate(validate_data):
                response = make_response(jsonify(v.errors), 422)
            else:
                response = f(*args, **kwargs)
            return response
        return wrapper
    return inner_function

class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = 'required field not found'