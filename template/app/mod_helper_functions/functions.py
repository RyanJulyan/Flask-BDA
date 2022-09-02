
from flask import jsonify

from datetime import datetime
import json

# Import the app module
from app import app

# Async Requests
import aiohttp
from asyncio import ensure_future, gather
import asyncio

# API Requests
import requests

# Import web_hooks module models 
from app.mod_web_hooks.models import Web_hooks

list_separator = app.config['LIST_SEPARATOR']

date_format = app.config['DATE_FORMAT']
time_format = app.config['TIME_FORMAT']
datetime_format = date_format + ' ' + time_format

def process_webhook(module_name, run_type, data, convert_sqlalchemy_to_json=True):

    run_types = {
        "before_insert": Web_hooks.run_before_insert,
        "after_insert": Web_hooks.run_after_insert,
        "before_update": Web_hooks.run_before_update,
        "after_update": Web_hooks.run_after_update,
        "before_delete": Web_hooks.run_before_delete,
        "after_delete": Web_hooks.run_after_delete,
    }

    web_hooks = (
                    Web_hooks.query
                    .filter(Web_hooks.run_in_module_name == module_name)
                    .filter(run_types[run_type] == 1)
                    .all()
                )

    if convert_sqlalchemy_to_json:
        data = jsonify(data.as_dict())
    
    status_code = 'No Webhook Run'
        
    for web_hook in web_hooks:

        method = web_hook.method
        data_type = web_hook.data_type

        api_headers = web_hook.api_headers
        params = web_hook.api_params

        api_endpoint = web_hook.api_endpoint

        if(method == 'get'):

            url = api_endpoint

            if data_type != 'json':
                x = requests.get(url, params = params, headers = api_headers, data = data)
            else:
                x = requests.get(url, params = params, headers = api_headers, json = data)

            status_code = x.status_code

            try:
                data = json.loads(x.content)
            except Exception:
                data = convert_to_python_data_type('str')(x.content)

        if(method == 'post'):

            url = api_endpoint

            if data_type != 'json':
                x = requests.post(url, params = params, headers = api_headers, data = data)
            else:
                x = requests.post(url, params = params, headers = api_headers, json = data)

            status_code = x.status_code

            try:
                data = json.loads(x.content)
            except Exception:
                data = convert_to_python_data_type('str')(x.content)

        if(method == 'put'):

            url = api_endpoint

            if data_type != 'json':
                x = requests.put(url, params = params, headers = api_headers, data = data)
            else:
                x = requests.put(url, params = params, headers = api_headers, json = data)

            status_code = x.status_code

            try:
                data = json.loads(x.content)
            except Exception:
                data = convert_to_python_data_type('str')(x.content)

        if(method == 'delete'):

            url = api_endpoint

            if data_type != 'json':
                x = requests.put(url, params = params, headers = api_headers, data = data)
            else:
                x = requests.put(url, params = params, headers = api_headers, json = data)

            status_code = x.status_code

            try:
                data = json.loads(x.content)
            except Exception:
                data = convert_to_python_data_type('str')(x.content)
    
    data = {
        "status_code":status_code,
        "data":data,
    }
    
    return data


def path_level(path, delimiter='/'):
    """
        path level will return the remaining chartars of a string excluding a specific delimiter string.

        Example:
        path = '/1/2/3/'
        delimiter='/'

        level = path_level(path,delimiter)

        print("level:", level) 
        ## level: 3

    """
    return len(path) - path.count(delimiter)


def convert_str_to_int(string):
    return int(float(string))


def convert_str_to_list(string, list_separator = list_separator):
    lst = string.split(list_separator)
    lst = [x.replace('\n', ' ').replace('\r', '').replace(' ','') for x in lst]
    return lst


def convert_str_to_date(string, date_format = date_format):
    string = string[:10]
    return datetime.strptime(string, date_format)


def convert_str_to_datetime(string, datetime_format = datetime_format):
    return datetime.strptime(string, datetime_format)


def convert_to_python_data_type(data_type_string):
    data_type_string = data_type_string.lower()

    data_types_func = {
        'string': str,
        'str': str,
        'integer': convert_str_to_int,
        'float': float,
        'number': float,
        'double': float,
        'date': convert_str_to_date,
        'datetime': convert_str_to_datetime,
        'boolean': bool,
        'dict_to_json': json.dumps,
        'json_to_dict': json.loads,
        'list': convert_str_to_list
    }

    try:
        fn = data_types_func[data_type_string]
    except Exception:
        fn = data_types_func['string']

    return fn


async def get_request_worker(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_request_controller(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [ensure_future(get_request_worker(session, url)) for url in urls]
        results = await gather(*tasks)
    return results


def multi_async_get_requests(urls):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(get_request_controller(urls))

    return results
