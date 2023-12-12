

from accounts.api.authhandle import AuthHandlerIns
from accounts.models import User


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Replace this line to get the User object as needed
        try:
            user = User.objects.get(id=AuthHandlerIns.get_id(request=request))
            request.user = user
            print(request.user)
            # request._cached_user = user
        except:
            user=None

        # Set the user to the request

        response = self.get_response(request)
        return response

from django.http import QueryDict

class CustomUserMiddlewarebody:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.body,"11111111111")
        mutable_form_data = request.POST.copy()

        # You can now access and manipulate form data as needed
        # For example, you can modify a specific field's value
        mutable_form_data['email'] = 'new_value'

        # Update the request's POST attribute with the modified form data
        request.POST = mutable_form_data

        response = self.get_response(request)
        return response






    
class CustomUserMiddlewarebody2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Replace this line to get the User object as needed
        print(request.body,"2222222222")

        # Set the user to the request

        response = self.get_response(request)
        return response