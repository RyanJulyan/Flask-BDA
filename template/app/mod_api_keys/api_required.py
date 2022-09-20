from enum import Enum
import functools
from hmac import compare_digest
from datetime import datetime

from flask import request

# JWT for API
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.mod_api_keys.models import Api_keys


def is_valid(api_key):
    # datetime object containing current date and time
    now = datetime.now()
    valid_key = False
    key = Api_keys.find_by_api_key(api_key)

    if not key:
        return valid_key

    if now <= key.valid_from or now >= key.valid_to:
        return valid_key

    if compare_digest(key.api_key, api_key):
        valid_key = True

    return valid_key


def api_key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json:
            api_key = request.json.get("ApiKey")
        elif request.headers.get("ApiKey"):
            api_key = request.headers.get("ApiKey")
        else:
            raise NoAuthorizationError('Please provide an API key')
        
        # Check if API key is correct and valid
        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            raise NoAuthorizationError('The provided API key is not valid')

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
    json_payload = {}
    if request.json:
        json_payload = dict(request.json)
    if "Authorization" in headers:
        return jwt_func(func, *args, **kwargs)
    elif ("ApiKey" in json_payload) or ("ApiKey" in headers):
        return api_key_func(func, *args, **kwargs)
    return api_key_func(func, *args, **kwargs)  # Force Failure


class CheckType(Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    BOTH = "both"
    EITHER = "either"
    NONE = "none"


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
            elif checktype.value == "none":
                return func(*args, **kwargs)
            raise NoAuthorizationError('Invalid Input for checktype')

        return wrapper

    return decorator
