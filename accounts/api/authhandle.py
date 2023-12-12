from passlib.context import CryptContext
import jwt
from aceapp.settings.base import SECRET_KEY
from datetime import datetime, timedelta
# from accounts.models import RoleUsers
from django.http import HttpResponse
from accounts.models import User, get_default
from rest_framework.exceptions import PermissionDenied


class AuthHandler():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = SECRET_KEY

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # def get_token(self, payload):
    #     return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')
    def get_token(self, payload):
        now = datetime.now()
        # email = request.data.get("email")
        # user = RoleUsers.objects.filter(email=email).first()

        # payload['is_edit'] = user.role.can_edit
        now = datetime.utcnow()
        # user_id = str(request.user.id)
        # user_email = request.user.email
        payload['iat'] = now
        payload['exp'] = now + timedelta(days=10)
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def get_refersh_token(self, payload):
        now = datetime.now()
        # email = request.data.get("email")
        # user = RoleUsers.objects.filter(email=email).first()

        # payload['is_edit'] = user.role.can_edit
        now = datetime.utcnow()
        # user_id = str(request.user.id)
        # user_email = request.user.email
        payload['iat'] = now
        payload['exp'] = now + timedelta(days=10)
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def refresh_token(self, token):
        try:
            decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
            user=User.objects.filter(id=decoded['id']).values().first()
            payload = {'id': user['id'], 'username': user['username'], 'email': user['email'],
                       'admin': user['is_superuser'], 'role': user['is_roleuser'], 'faculty': user['is_faculty'],'student':user['is_student']}
            token = self.get_token(payload=payload)
            return token
        except jwt.ExpiredSignatureError:
            # handle expired token error
            print("Decode")
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except jwt.InvalidTokenError:
            # handle invalid token error
            print("Decode except")
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})

    def decode_token(self, token):
        try:
            decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            # handle expired token error
            print("Decode")
        except jwt.InvalidTokenError:
            # handle invalid token error
            print("Decode except")

    def is_staff(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            payload = self.decode_token(token)
            print('jjj')

        except:
            return False

        try:

            return payload['admin']
            print('jjj')
        except:
            return False

    def is_role(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            payload = self.decode_token(token)
            print('jjj')

        except:
            return False

        try:

            return payload['role']
            print('jjj')
        except:
            return False

    def is_faculty(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            print("hi")
            token = auth_header.split()[1]
            payload = self.decode_token(token)

        except:
            return False

        try:

            return payload['faculty']
            print('jjj')
        except:
            return False

    def get_permissions(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split()[1]

            payload = self.decode_token(token)
            permissions = payload['permission']
            return permissions
        except:
            return get_default


    def get_mail(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            payload = self.decode_token(token)
        except:
            return False
        return payload['email']

    def get_id(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            payload = self.decode_token(token)
        except:
            return False
        return payload['id']
    
    def is_student(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            print("hi")
            token = auth_header.split()[1]
            payload = self.decode_token(token)

        except:
            return False

        try:

            return payload['student']
            print('jjj')
        except:
            return False



AuthHandlerIns = AuthHandler()



class AttendanceHandler():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = SECRET_KEY

    # def get_password_hash(self, password):
    #     return self.pwd_context.hash(password)

    # def verify_password(self, plain_password, hashed_password):
    #     return self.pwd_context.verify(plain_password, hashed_password)

    # def get_token(self, payload):
    #     return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')
    def get_token(self, payload):
        now = datetime.now()
        # email = request.data.get("email")
        # user = RoleUsers.objects.filter(email=email).first()

        # payload['is_edit'] = user.role.can_edit
        now = datetime.utcnow()
        # user_id = str(request.user.id)
        # user_email = request.user.email
        payload['iat'] = now
        payload['exp'] = now + timedelta(seconds=15)
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def decode_token(self, token):
        try:
            decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            # handle expired token error
            print("Decode")
        except jwt.InvalidTokenError:
            # handle invalid token error
            print("Decode except")                                                                                    


attendanceIns = AttendanceHandler()
