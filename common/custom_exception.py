from rest_framework.views import exception_handler
from rest_framework.response import Response


def get_error_msg(data, key):
    if isinstance(data, str):
        return f"{key}: {data.lower()}"
    elif isinstance(data, dict):
        key = list(data.keys())[0]
        data = data[key]
        if isinstance(data, list):
            if isinstance(data, str):
                return f"{key}: {data.lower()}"
            else:
                return f"{key}: {data[0]}"
    elif isinstance(data, list):
            if isinstance(data, str):
                return f"{key}: {data.lower()}"
            else:
                return f"{key}: {data[0]}"
    return get_error_msg(data, key)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    return _handle_generic_error(exc, context, response)


def _handle_generic_error(exc, context, response):

    data = {'data': [], 'status': False}

    if response is not None:
        if isinstance(response.data, list):
            if isinstance(response.data, str):
                data['message'] = f"{response.data.lower()}"
                response.data = data
                
            else:
                data['message'] = f"{response.data[0]}"
                response.data = data
        else:
            key = list(response.data.keys())[0]
            value = response.data[key]
            data['message'] = get_error_msg(value, key)
            response.data = data
    # else:
    #     data['message'] = f"{exc.__class__.__name__}: {exc} {context}"
    #     return Response(data)

    return response