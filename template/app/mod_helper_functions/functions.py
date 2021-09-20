
from datetime import datetime
import json

# Import the app module
from app import app

list_separator = app.config['LIST_SEPARATOR']

date_format = app.config['DATE_FORMAT']
time_format = app.config['TIME_FORMAT']
datetime_format = date_format + ' ' + time_format


def path_level(path,delimiter='/'):
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
    return datetime.strptime(string, date_format)


def convert_str_to_datetime(string, datetime_format = datetime_format):
    return datetime.strptime(string, datetime_format)


def convert_to_python_data_type(data_type_string):
    data_type_string = data_type_string.lower()

    data_types_func = {
        'string':str,
        'str':str,
        'integer':convert_str_to_int,
        'float':float,
        'number':float,
        'double':float,
        'date':convert_str_to_date,
        'datetime':convert_str_to_datetime,
        'boolean':bool,
        'dict_to_json':json.dumps,
        'json_to_dict':json.loads,
        'list':convert_str_to_list
    }

    try:
        fn = data_types_func[data_type_string]
    except:
        fn = data_types_func['string']

    return fn

