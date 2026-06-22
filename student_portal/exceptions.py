from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def _flatten_errors(data):
    if isinstance(data, dict):
        flattened = {}
        for key, value in data.items():
            flattened[key] = _flatten_errors(value)
        return flattened
    if isinstance(data, list):
        if len(data) == 1:
            return _flatten_errors(data[0])
        return [_flatten_errors(item) for item in data]
    return data


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            {
                "success": False,
                "message": "An unexpected server error occurred.",
                "errors": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = "Request failed."
    if isinstance(response.data, dict):
        if "detail" in response.data:
            message = str(response.data["detail"])
        elif "non_field_errors" in response.data:
            message = " ".join(map(str, response.data["non_field_errors"]))
        else:
            message = "Validation error."
    elif isinstance(response.data, list):
        message = "Validation error."

    return Response(
        {
            "success": False,
            "message": message,
            "errors": _flatten_errors(response.data),
        },
        status=response.status_code,
    )
