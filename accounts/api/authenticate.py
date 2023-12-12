# import jwt
# from datetime import datetime,timedelta
# from rest_framework.authentication import get_authorization_header,BaseAuthentication
# from rest_framework import exceptions

# class JWTTutorAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth = get_authorization_header(request).split()
#         print(auth)
#         if auth and len(auth) == 2:
#             token = auth[1].decode('utf-8')
#             print(token)
#             id = decode_access_token(token)

#             roleusers = RoleUsers.objects.get(pk=id)
#             return (roleusers, None)
#         raise exceptions.AuthenticationFailed('Anauthenticated')


# # def create_access_token(id):

# #     return jwt.encode({
# #         'id':id,
# #         'is_edit':roleusers.role.can_edit,
# #         'is_delete':roleusers.role.can_delete,
# #         'is_create':roleusers.role.can_create,
# #         'is_view':roleusers.role.can_view,
# #         'exp':datetime.utcnow()+timedelta(days=30),
# #         'iat':datetime.utcnow(),
        
        
# #     },'access_secret',algorithm='HS256')
    
    
# # def decode_access_token(token):
# #     try:
# #         payload = jwt.decode(token,'access_secret',algorithms='HS256')
# #         return payload['id','is_edit','is_view','is_delete','is_create']
# #     except Exception as e:
# #         print(e)
# #         raise exceptions.AuthenticationFailed('Bunauthenticated')


  
# # def create_refresh_token(id):
# #     return jwt.encode({
# #         'user_id':id,
# #         'exp':datetime.utcnow()+timedelta(days=30),
# #         'iat':datetime.utcnow()
        
# #     },'refresh_secret',algorithm='HS256')
    
    
# def decode_refresh_token(token):
#     try:
#         payload = jwt.decode(token,'refresh_secret',algorithms='HS256')
#         return payload['roleusers_id']
#     except:
#         raise exceptions.AuthenticationFailed('Cunauthenticated')