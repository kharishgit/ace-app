from django.utils.deprecation import MiddlewareMixin
from simple_history.models import HistoricalRecords
from accounts.api.authhandle import AuthHandlerIns
from accounts.models import User


class HistoryMixin:
    # def process_request(self, request):
        
    #     HistoricalRecords.context.request = request

    # def process_response(self, request, response):
    #     if hasattr(HistoricalRecords.context, "request"):
    #         del HistoricalRecords.context.request
    #     return response 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Replace this line to get the User object as needed
        try:
            HistoricalRecords.context.request = request
            print(HistoricalRecords.context.request,"ABCDEF")
            user = User.objects.get(id=AuthHandlerIns.get_id(request=request))
            request.user = user
        except:
            user=None

        # Set the user to the request

        response = self.get_response(request)
        return response