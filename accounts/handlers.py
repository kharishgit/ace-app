from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler to override the status code for PermissionDenied exceptions.
    """
    if isinstance(exc, PermissionDenied):
        data = {
            "message": "You do not have permission to access this resource.",
            "status_code": 401
        }
        return Response(data, status=401)

    # Call the default exception handler for other exceptions
    response = exception_handler(exc, context)
    return response