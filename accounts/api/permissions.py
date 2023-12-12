##
from rest_framework import permissions
import jwt
from accounts.api.authhandle import AuthHandlerIns
from django.conf import settings
# from aceapp.settings import SECRET_KEY
# class ViewPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user_roles = RoleUsers.objects.filter(email=request.user)
#
#         print(user_roles)
#         for role in user_roles:
#             print(role.role.can_view,"VIW")
#             if role.role.can_view:
#                 return True
#         return False
#
# class CreatePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user_roles = RoleUsers.objects.filter(email=request.user)
#         for role in user_roles:
#             if role.role.can_create:
#                 return True
#         return False

# class EditPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # print(request.user)
#         # print(request.user.is_staff)
#
#         user_roles = RoleUsers.objects.filter(email=request.user)
#         for role in user_roles:
#             print(role.role.can_edit,"EDIT")
#
#             if role.role.can_edit:
#                 return True
#         return False

# class DeletePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user_roles = RoleUsers.objects.filter(email=request.user)
#         print(user_roles)
#
#         for role in user_roles:
#             if role.role.can_delete:
#                 return True
#         return False


class EditPermission(permissions.BasePermission):
    print("Edit")
    def has_permission(self, request,view):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        print("From put")
        # print(newarg.headers.get('Authorization'))
        # auth_header = request.headers.get('Authorization')
        # print(request.headers)
        # print(auth_header)
        # if auth_header is None:
        #     return False
        token = auth_header.split()[1]
        print(token,"TOKEN")
        # print(SECRET_KEY,"Secret")
        try:
            # decoded_token = AuthHandlerIns.decode_token(token=token)
            # print(decoded_token)
            decoded_token = jwt.decode(token,settings.SECRET_KEY, algorithms='HS256')
            # print(decoded_token)
            user_email = decoded_token['email']
        except Exception as e :
            print(e)
            print("Except")
            return False
            # Check if user has permission to create
        user_roles = RoleUsers.objects.filter(email=user_email)
        for role in user_roles:
            if role.role.can_edit:
                return True
        return False


class DeletePermission(permissions.BasePermission):
    print("Delete")
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        token = auth_header.split()[1]
        print(token)

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print (settings.SECRET_KEY)
            # print(decoded_token)
            user_email = decoded_token['email']
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False
            # Check if user has permission to create
        user_roles = RoleUsers.objects.filter(email=user_email)
        for role in user_roles:
            if role.role.can_delete:
                return True
        return False

class ViewPermission(permissions.BasePermission):
    print("Edit Permission")
    def has_permission(self, request, view):
        print("From HasPermission")
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        token = auth_header.split()[1]

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_email = decoded_token['email']
            print(user_email)
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False
            # Check if user has permission to create
        user_roles = RoleUsers.objects.filter(email=user_email)
        for role in user_roles:
            if role.role.can_view:
                return True
        return False



class CreatePermission(permissions.BasePermission):
    print("Edit")
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        token = auth_header.split()[1]

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_email = decoded_token['email']
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False
            # Check if user has permission to create
        user_roles = RoleUsers.objects.filter(email=user_email)
        for role in user_roles:
            if role.role.can_create:
                return True
        return False
