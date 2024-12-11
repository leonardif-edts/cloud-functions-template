from typing import Callable, Optional
from functools import wraps

from pydantic import SecretStr
from flask import Request, jsonify
from flask.typing import ResponseReturnValue

from core.schemas import InvalidRequestException


def cors_handler(func: Callable[[Request], ResponseReturnValue]):
    """
    CORS Handler

    Handling CORS for Server-to-Server Requests
    See: https://cloud.google.com/functions/docs/writing/write-http-functions#cors
    """
    @wraps(func)
    def wrapper(request: Request):
        if request.method == "Options":
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "3600",
            }
            return ("", 204, headers)
        
        response = func(request)
        return response
    return wrapper


def authentication(is_set: bool = True, key: Optional[SecretStr] = None):
    """
    Authentiation

    Setup API key Authentication methods. Set is_set to False for no Auth.
    API Key are set using Bearer Token.

    params:
        - is_set: bool (default: True). Set authentication to active.
        - key: Optional[SecretStr] (default: None). API Key for authentication.
    """
    def factory(func: Callable[[Request], ResponseReturnValue]):
        @wraps(func)
        def wrapper(request: Request):
            if (is_set):
                pass
            
            response = func(request)
            return response
        return wrapper
    return factory


def error_handler(func: Callable[[Request], ResponseReturnValue]):
    """
    Error Handler

    Handling Error response cycle.
    """
    @wraps(func)
    def wrapper(request: Request):
        try:
            response = func(request)
            return response
        except Exception as err:
            if isinstance(err, InvalidRequestException):
                return jsonify(err.to_json()), err.code
            else:
                return jsonify({"message": str(err)}), 500
    return wrapper