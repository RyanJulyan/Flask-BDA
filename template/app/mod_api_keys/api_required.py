from enum import Enum
import functools
from hmac import compare_digest
from datetime import date

from flask import request

# JWT for API
from flask_jwt_extended import jwt_required

from app.mod_api_keys.models import Api_keys


def is_valid(api_key):
    today = date.today()
    valid_key = False
    key = Api_keys.find_by_api_key(api_key)

    if key and compare_digest(key.api_key, api_key):
        valid_key = True
    if key.valid_from <= today or key.valid_to >= today:
        valid_key = False

    return valid_key


def api_key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json:
            api_key = request.json.get("api_key")
        elif request.headers:
            api_key = request.headers.get("api_key")
        else:
            return {"message": "Please provide an API key"}, 400

        # Check if API key is correct and valid
        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403

    return decorator


@jwt_required
def jwt_func(func, *args, **kwargs):
    return func(*args, **kwargs)


@api_key_required
def api_key_func(func, *args, **kwargs):
    return func(*args, **kwargs)


@jwt_required
@api_key_required
def jwt_and_api_key_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def jwt_or_api_key_func(func, *args, **kwargs):
    headers = dict(request.headers)
    json_payload = dict(request.json)
    if "Authorization" in headers:
        return jwt_func(func, *args, **kwargs)
    elif ("api_key" in json_payload) or ("api_key" in headers):
        return api_key_func(func, *args, **kwargs)
    return {"message": "Please provide an API key or a JWT token"}, 400


class CheckType(Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    BOTH = "both"
    EITHER = "either"


def jwt_or_api_key_required(checktype: CheckType = CheckType.EITHER):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if checktype.value == "api_key":
                return api_key_func(func, *args, **kwargs)
            elif checktype.value == "jwt":
                return jwt_func(func, *args, **kwargs)
            elif checktype.value == "both":
                return jwt_and_api_key_func(func, *args, **kwargs)
            elif checktype.value == "either":
                return jwt_or_api_key_func(func, *args, **kwargs)
            return "Invalid Input"

        return wrapper

    return decorator
