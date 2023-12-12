import calendar
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
import datetime
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from rest_framework import generics
from django.shortcuts import render
from accounts.models import Material
from course.helper import getchoicefromlist
from permissions.permissions import AdminAndRoleOrFacultyPermission, AdminAndRolePermission, AdminOrFaculty, FacultyPermission, NonePermission, OrPermission,AdminAndRolePermissionCopy
from .models import Batch, Branch, Course, Subject, Module, Topic, SubTopic
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets, filters
from rest_framework.decorators import api_view
from accounts.models import Faculty, User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from collections import defaultdict
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import pandas as pd
from .serializers import *

from accounts.api.serializers import MaterialSerializer, FacultyTopicsView, FacultySerializer, facultyprofileserializer, FacultyEditProfileSerializer, FacultySerializerforisverifiedandNOT, facultyviewDetails, facultyviewDetailsMaterial, facultyviewDetailsProfile
from accounts.api.serializers import FacultySerializer, facultyprofileserializer, FacultyEditProfileSerializer, FacultySerializerforisverifiedandNOT, facultyviewDetails


from accounts.api.authhandle import AuthHandlerIns
from rest_framework.views import APIView
from .serializers import Approvalserializers, CategorySerializer, TimeTableSerializer
from accounts.models import FacultyCourseAddition
from django.core.mail import EmailMessage
# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from accounts.models import Role


def set_history_user(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        user = AuthHandlerIns.get_id(request=request)
        user_who_made_change = User.objects.get(id=user)
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        response = view_func(self, request, *args, **kwargs)
        # Assuming you have access to the instance here, set the history_user
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        instance = self.get_object() if hasattr(self, 'get_object') else None
        print(instance,"instancekkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        if instance and hasattr(instance, 'history'):
            history_instance = instance.history.first()
            if history_instance:
                history_instance.history_user = user_who_made_change
                history_instance.save()

        return response
    return wrapped_view


def set_history_user_delete(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        user = AuthHandlerIns.get_id(request=request)
        user_who_made_change = User.objects.get(id=user)
        instance = self.get_object() if hasattr(self, 'get_object') else None
        history_instance = instance.history.first()
        if history_instance:
            history_instance.history_user = user_who_made_change
            history_instance.save()
        response = view_func(self, request, *args, **kwargs)
        ins=instance._meta.model.newobjects.get(id = instance.id ).history.first()
        ins.history_user=user_who_made_change
        ins.save()


        return response
    return wrapped_view

def create_history_user__decorator(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        user = AuthHandlerIns.get_id(request=request)
        print("pipipipipipipipipippipipipipi",user)
        user_who_made_change = User.objects.get(id=user)
        print(hasattr(self, 'get_object'),"9999999999999")
        # history_instance = instance.history.first()
        # if history_instance:
        #     history_instance.history_user = user_who_made_change
        #     history_instance.save()
        response = view_func(self, request, *args, **kwargs)
        print(response)
        print(response.data,"66666666666666666")
        # ins=instance._meta.model.newobjects.get(id = instance.id ).history.first()
        instance = get_object_or_404(self.queryset.model,pk=response.data['id']) 
        history_instance = instance.history.first()
        if history_instance:
            history_instance.history_user = user_who_made_change
            history_instance.save()
        # ins.history_user=user_who_made_change
        # ins.save()


        return response
    return wrapped_view


def create_history_user(instance,user):
    instance = instance
    if instance and hasattr(instance, 'history'):
        history_instance = instance.history.first()
        if history_instance:
            history_instance.history_user = user
            history_instance.save()

# def confirm_delete(request, *args, **kwargs):
#     password = request.data.get('password')
#     user = request.user

#     # Verify the password is correct
#     if not check_password(password, user.password):
#         return Response({"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

    



# class Batch(models.Model):
#     WEEKDAYS_CHOICES = (
#         ('Sun', 'Sunday'),
#         ('Mon', 'Monday'),
#         ('Tue', 'Tuesday'),
#         ('Wed', 'Wednesday'),
#         ('Thu', 'Thursday'),
#         ('Fri', 'Friday'),
#         ('Sat', 'Saturday'),
#     )

#     name = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     start_time = models.TimeField()

#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     description = models.TextField(null=True, blank=True)
#     strength = models.IntegerField(default=0)
#     active = models.BooleanField(default=True)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     photo = models.ImageField(null=True, blank=True)
#     working_days = MultiSelectField(choices=WEEKDAYS_CHOICES, default=[
#                                     'Mon'], max_choices=7, validators=[MaxValueValidator(7)])
#     exam_days = MultiSelectField(choices=WEEKDAYS_CHOICES, default=[
#                                  'Mon'], max_choices=7, validators=[MaxValueValidator(7)])


class CategoryViewset(viewsets.ModelViewSet):
    """
        Category CRUD.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Category"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list']:
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Category"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    





    

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Category"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list']:
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Category"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Category"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class HistoryUserMixin:
    def set_history_user(self, instance):
        print("hii")
        email = AuthHandlerIns.get_mail(request=self.request)
        user = User.objects.get(email=email)
        instance._history_user = user

from functools import wraps
# from django.contrib.auth import get_user_model
# User = get_user_model()




from simple_history.utils import update_change_reason
from django.db import transaction

class BranchListCreateView(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchCreateSerializer1

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Branch"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list']:
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Branch"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        print(self.queryset.model)
        return super().get_queryset()
    


    
    # @set_history_user
    def create(self, request, *args, **kwargs):
        try:
        
            email = AuthHandlerIns.get_mail(request=request)
            user = User.objects.get(email=email)
            
            


            try:
                b = None
                try:
                    b = Branch.objects.create(

                        name=request.data['name'], location=request.data['location'])
                    create_history_user(b,user)
                    
                except Exception as e:
                    print(e,"EX")
                    return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                for i in request.data['courses']:
                    course = Course.objects.filter(id=i)
                    Branch_courses.objects.create(course=course[0], branch=b)

                # serializer = BranchCreateSerializer1(b)

                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e,"NEEX")

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # @set_history_user
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    


class BranchRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTTutorAuthentication]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get(self, request, *args, **kwargs):
        # if not ViewPermission().has_permission(request, self):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        # if not EditPermission().has_permission(request, self):
        if not AuthHandlerIns.is_staff(request=request):

            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # if not DeletePermission().has_permission(request, self):
        if not AuthHandlerIns.is_staff(request=request):

            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # if not CreatePermission().has_permission(request, self):4
        if not AuthHandlerIns.is_staff(request=request):

            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Category"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class LevelListCreateView(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Level"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class LevelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class CreateClassLevelView(generics.CreateAPIView):
    queryset = ClassLevel.objects.all()
    serializer_class = ClassLevelSerializer

    # def post(self, request, *args, **kwargs):
    #     if not AuthHandlerIns.is_staff(request):
    #         return Response({"message": "Only admin can create a ClassLevel"}, status=status.HTTP_401_UNAUTHORIZED)

    #     return super().post(request, *args, **kwargs)


class ClassLevelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassLevel.objects.all()
    serializer_class = ClassLevelSerializer


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        # print(AuthHandlerIns.get_permissions(request=request)['course'],'jjjjjjjjjjjjjjjjjjjjj')
        if not AuthHandlerIns.is_staff(request):
            print('hiiiiii')
            return Response({"message": "Only admin can create a course"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)
    

class CourseCreateModelView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all() 
    permission_classes = [AdminAndRolePermission]  

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'create']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Course"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list']:
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Course"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @set_history_user
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)     


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTTutorAuthentication]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request) or AuthHandlerIns.get_permissions(request=request)['course']['post'] == 'true':
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        userid = AuthHandlerIns.get_id(request)
        user = User.objects.get(id=userid)

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"},
                            status=status.HTTP_401_UNAUTHORIZED)
        # Get the password from the request data
        # password = request.data.get('password')
        # # Verify the password is correct
        # if not check_password(password, user.password):
        #     return Response({"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class BatchCreateView(generics.CreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Batch"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class BatchRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTTutorAuthentication]
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class SubjectCreateView(generics.CreateAPIView):
    # authentication_classes = [IsAdminUser]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def post(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Subject"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)

class SubjectCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)  

class SubtopicCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)  

class ModuleCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 

class TopicCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 


class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminUser]

    # authentication_classes = [JWTTutorAuthentication]

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class ModuleCreateView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Module"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class ModuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTTutorAuthentication]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)
##### MODULE CRUD OPERATIONS ENDS #########


class TopicCreateView(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Topic"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class TopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    # authentication_classes = [JWTTutorAuthentication]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class SubTopicCreateView(generics.CreateAPIView):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Topic"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class SubTopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTTutorAuthentication]
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer

    def get(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to edit the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to delete the data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to create new data"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class ExamScheduleListCreateView(generics.ListCreateAPIView):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer


class ExamScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer


@api_view(['GET'])
def getcourse_batch(request, id):
    # print(id,'lllllll',pk)
    ans = []
    course = Course_batch.objects.filter(batch=id).values()
    print(course)
    for i in course:
        subject = Subject_batch.objects.filter(course=i['id']).values()
        for j in subject:
            module = Module_batch.objects.filter(subject=j['id']).values()
            for k in module:
                topic = Topic_batch.objects.filter(module=k['id']).values()

                for st in topic:

                    subtopic = Subtopic_batch.objects.filter(
                        topic=st['id']).values()

                    if st['status'] == 'P':
                        # st['topics'] = topic
                        # st.update({"name": "hi"})
                        print('yesssssssssssss')

                    elif st['status'] == 'S':
                        print('ji')
                        st['details'] = [Timetableserializersdate(TimeTable.objects.filter(
                            topic=st['id']).first()).data, {'length': len(Approvals.objects.filter(timetable=TimeTable.objects.get(
                                topic=st['id'])))}, Timetableserializers(TimeTable.objects.filter(topic=st['id'], batch=id).first()).data]

                    elif st['status'] == 'B':
                        st['details'] = [Timetableserializersdate(TimeTable.objects.filter(
                            topic=st['id']).first()).data, {'length': len(Approvals.objects.filter(timetable=TimeTable.objects.get(
                                topic=st['id'])))}, {'id': Timetableserializers(TimeTable.objects.filter(
                                    topic=st['id']).first()).data}]

                    else:
                        print('jiii')
                        # st.update({"name": "hi"})

                        k['topics'] = topic

                        print('nooooooooooo')
                    subtopic = Subtopic_batch.objects.filter(
                        topic=st['id']).values()

                    st['subtopic'] = subtopic

                k['topics'] = topic
            j['modules'] = module

        i['subject'] = subject

        ans.append(i)

    print(ans)
    return Response({"data": ans})


@api_view(['GET'])
def getall(request, id):
    ans = []
    c = Course.objects.filter(id=id).values()
    print(c)
    for i in c:
        s = Subject.objects.filter(
            course=i['id']).values().order_by('priority')
        for j in s:
            m = Module.objects.filter(
                subject=j['id']).values().order_by('priority')
            for k in m:
                t = Topic.objects.filter(
                    module=k['id']).values().order_by('priority')
                for st in t:
                    su = SubTopic.objects.filter(
                        topic=st['id']).values().order_by('priority')
                    st['subtopic'] = su

                k['topics'] = t
            j['modules'] = m

        i['subject'] = s

        ans.append(i)

    print(ans)
    return Response({"data": ans})


@api_view(['GET'])
def getallNew(request, id):
    if AuthHandlerIns.is_role(request):
        course = Course_branch.objects.filter(branch=id)
        print(course, "kjksjdks")
        return Response({"data": CourseBranchNewDragSerializer(course, many=True).data})
    course = Course.objects.filter(id=id)
    print(course, "kjksjdks")
    return Response({"data": CourseNewDragSerializer(course, many=True).data})


@api_view(['GET'])
def getallNewBatch(request, id):
    if AuthHandlerIns.is_role(request):
        course = Course_batch.objects.filter(branch=id)
        print(course, "kjksjdks")
        return Response({"data": CourseBatchNewDragSerializer(course, many=True).data})
    course = Course_batch.objects.filter(id=id)
    print(course, "kjksjdks")
    return Response({"data": CourseBatchNewDragSerializer(course, many=True).data})

@api_view(['GET'])
def getsubtopic(request):
    sub_topic = SubTopic.objects.all()
    serializer = SubTopicSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def gettopic(request):
    sub_topic = Topic.objects.all()
    serializer = TopicSerializer(sub_topic, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gettopic(request,id):
    sub_topic = Topic.objects.filter(id=id)
    serializer = TopicSerializer(sub_topic, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def getsubtopic(request,id):
    sub_topic = SubTopic.objects.filter(id=id)
    serializer = SubTopicSerializerforexcel(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getmodule(request):
    sub_topic = Module.objects.all()
    serializer = ModuleSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getcourse(request):
    print("From getcourse")
    if AuthHandlerIns.is_role(request=request):
        branch = Branch.objects.filter(user=AuthHandlerIns.get_id(request=request)).values('id')
        branch_course = Branch_courses.objects.filter(branch__in=branch).values('course')
        course = Course.objects.filter(id__in=branch_course).order_by('created_at')
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)
    sub_topic = Course.objects.all().order_by('created_at')
    serializer = CourseSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getbranch(request):
    if AuthHandlerIns.is_role(request):
        branch = Branch.objects.filter(user=AuthHandlerIns.get_id(request=request))
        # batch = Batch.objects.filter(branch__in=branch)
        serializer = BranchCreateSerializer(branch, many=True)
        return Response(serializer.data)
    sub_topic = Branch.objects.all().order_by('created_at')

    serializer = BranchCreateSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getsubject(request):
    sub_topic = Subject.objects.all()
    serializer = SubjectSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getbatch(request):
    sub_topic = Batch.objects.all()
    serializer = BatchSerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getcategory(request):
    sub_topic = Category.objects.all()
    serializer = CategorySerializer(sub_topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getlevel(request):
    sub_topic = Level.objects.all()
    serializer = LevelSerializer(sub_topic, many=True)
    return Response(serializer.data)


class TimeTable_C(generics.ListCreateAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = TimeTable.objects.all().order_by('date')
    serializer_class = Timetableserializers

    def post(self, request, *args, **kwargs):
        print("jjdksjdsj",request.data)
        if request.data['is_combined']:
            timetable = TimeTable.objects.filter(batch__in=request.data['combined_batch'],date=request.data['date'])
            faculty = timetable.values('faculty')
            print(faculty.exists(),"fac")
            for tt in timetable:
                tt.is_combined = True
                tt.combined_batch.set(request.data['combined_batch'] + [request.data['batch']])
                tt.save()
            if len(faculty.exclude(faculty=None))>0:
                request.data['faculty']=timetable.exclude(faculty=None).first().faculty.pk
                return self.create(request, *args, **kwargs)
            return self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

 
    def get(self, request, *args, **kwargs):
        if AuthHandlerIns.is_faculty(request):
            approve = self.request.query_params.get('approve',None)
            faculty_course= FacultyCourseAddition.objects.filter(user=AuthHandlerIns.get_id(request=request),status="approved").values('topic')
            print(faculty_course,"sss")
            a = False
            s= Topic_branch.objects.filter(topic__in=faculty_course).values('id')
            print(s,"sss")
            faculty_course= Topic_batch.objects.filter(topic__in=s).values('id')
            print(faculty_course,"fac")
            
            app = Approvals.objects.filter(user__id=AuthHandlerIns.get_id(request=request)).values('timetable')
            if approve:
                q = TimeTable.objects.filter(id__in=app).order_by('-date').exclude(date__lte=datetime.date.today(),id__in=app)
            else:
                q = TimeTable.objects.filter(topic__in=faculty_course,faculty__isnull=True).order_by('-date').exclude(date__lte=datetime.date.today(),id__in=app)
            # q = TimeTable.objects.filter(faculty__isnull=True)
            print(q, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            t = Timetableserializersnew(
                q, many=True, context={'request': request})
            if a:
                return Response({"Time_Table": t.data})
            else:
                return Response({"Time_Table": t.data})

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"}, status=status.HTTP_401_UNAUTHORIZED)
        return self.list(request, *args, **kwargs)


@api_view(['GET'])
def getbatch(request):
    if AuthHandlerIns.is_role(request):
        branch = Branch.objects.filter(user=AuthHandlerIns.get_id(request=request)).values('id')
        batch = Batch.objects.filter(branch__in=branch)
        serializer = BatchSerializer(batch, many=True)
        return Response(serializer.data)
    sub_topic = Batch.objects.all()
    serializer = BatchSerializer(sub_topic, many=True)
    return Response(serializer.data)


########## Approvals##########

class Approvals_c(generics.ListCreateAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Approvals.objects.all()
    serializer_class = Approvalserializerspost

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


class Approval_c_p(generics.ListCreateAPIView, mixins.UpdateModelMixin):
    queryset = Approvals.objects.all()
    serializer_class = Approvalserializers_get

    def put(self, request, *args, **kwargs):
        try:
            approval = Approvals.objects.get(id=kwargs['id'])
            approval.status = True
            approval.save()
            timetable = approval.timetable
            # faculty_id = request.data.get('faculty')
            faculty = User.objects.get(id=approval.faculty.pk)
            timetable.faculty = faculty
            timetable.save(update_fields=['faculty'])
            return Response({"message": "Faculty assigned"}, status=status.HTTP_202_ACCEPTED)
        except Approvals.DoesNotExist:
            return Response({"message": "Approval not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_course_by_branch(request, branch_id):
    print(branch_id)
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    courses = branch.courses.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


class TimeTableList(generics.ListAPIView):
    serializer_class = TimeTableSearchSerializer

    def get_queryset(self):
        faculty_id = self.request.query_params.get('faculty_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        queryset = TimeTable.objects.filter(
            date__range=[start_date, end_date], faculty__isnull=True)
        if faculty_id:
            faculty = Faculty.objects.get(id=faculty_id)
            print(faculty_id)
            # queryset = queryset.filter(faculty=faculty, topic__in=faculty.topics.all())
            # topic_batch = Topic_batch.objects.filter(topic__in=Faculty.objects.get(
            #     id=faculty_id).topic.all()).values('topic').distinct()
            topic_batch = Topic_batch.objects.filter(topic__in=Faculty.objects.get(
                id=faculty_id).topic.all())

            print(queryset)
            queryset = queryset.filter(topic__in=topic_batch)
            print(queryset)

            return queryset


# @api_view(['GET'])
# def get_subtopic_by_topic(request, topic_id):
#     try:
#         topic = Topic.objects.get(id=topic_id)
#     except Topic.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     subtopic = topic.subtopic.all()
#     serializer = SubTopicSerializer(subtopic, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def get_subtopic_by_topic(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    subtopics = SubTopic.objects.filter(topic=topic)
    serializer = SubTopicSerializer(subtopics, many=True)
    return Response(serializer.data)


# sh get time table list based on class
@api_view(['GET'])
def get_faculty_timetablelist_by_each_class(request, timetable_id):
    try:
        aproval = Approvals.objects.filter(timetable=timetable_id)
    except Approvals.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # aproval=Approvals.objects.filter(id=timetable_id)
    aproval = Approvals.objects.filter(timetable=timetable_id)
    serializer = Approvalserializers(aproval, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_timetable_by_batch(request, batch_id):
    try:
        batch = Batch.objects.get(id=batch_id)
    except Batch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    timetable = TimeTable.objects.filter(batch=batch)
    serializer = Timetableserializers(timetable, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_batch_in_branch(request, branch_id):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    batch = Batch.objects.filter(branch=branch)
    serializer = BatchSerializer(batch, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
def change_order(request):
    course_id = request.query_params.get('c')
    subject_id = request.query_params.get('s')
    module_id = request.query_params.get('m')
    topic_id = request.query_params.get('t')
    if course_id:
        if subject_id:
            if module_id:
                if topic_id:
                    for i in range(0, len(request.data)):
                        SubTopic.objects.filter(
                            id=request.data[i]['id_obj']).update(priority=i)

                else:
                    for i in range(0, len(request.data)):
                        Topic.objects.filter(
                            id=request.data[i]['id_obj']).update(priority=i)
                    pass
            else:
                for i in range(0, len(request.data)):
                    Module.objects.filter(
                        id=request.data[i]['id_obj']).update(priority=i)
                pass
        else:
            # subject = Subject.objects.filter(course=course_id).values()
            for i in range(0, len(request.data)):
                Subject.objects.filter(
                    id=request.data[i]['id_obj']).update(priority=i)

    else:
        pass
    return Response(status=status.HTTP_200_OK) 

    # print(post_id, post_id1)


# list all faculty list


# class FacultyList(generics.ListAPIView):

#     queryset = Faculty.objects.filter(is_verified=True)
#     serializer_class = FacultySerializerforisverifiedandNOT


# class FacultyList(generics.ListAPIView):
#     serializer_class = FacultySerializerforisverifiedandNOT

#     def get_queryset(self):
#         queryset = Faculty.objects.filter(is_verified=True)

#         # Apply search filter
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(user__username__icontains=search_query) |
#                                        Q(user__email__icontains=search_query) |
#                                        Q(user__mobile__icontains=search_query) |
#                                        Q(course__name__icontains=search_query) |
#                                        Q(subject__name__icontains=search_query) |
#                                        Q(module__name__icontains=search_query) |
#                                        Q(topic__name__icontains=search_query)).distinct()

#         # Apply filter fields
#         course = self.request.query_params.get('course', None)
#         if course:
#             queryset = queryset.filter(course__name=course)

#         subject_name = self.request.query_params.get('subject__name', None)
#         if subject_name:
#             queryset = queryset.filter(subject__name=subject_name)

#         module_name = self.request.query_params.get('module__name', None)
#         if module_name:
#             queryset = queryset.filter(module__name=module_name)

#         topic_name = self.request.query_params.get('topic__name', None)
#         if topic_name:
#             queryset = queryset.filter(topic__name=topic_name)

#         return queryset
# class FacultyList(generics.ListAPIView):
#     serializer_class = facultyviewDetails

#     def get_queryset(self):
#         queryset = Faculty.objects.filter(is_verified=True)

#         # Apply search filter
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(user__username__icontains=search_query) |
#                                        Q(user__email__icontains=search_query) |
#                                        Q(user__mobile__icontains=search_query)).distinct()

#         # Apply filter fields
#         course = self.request.query_params.get('course', None)
#         if course:
#             queryset = queryset.filter(course__name=course)

#         subject_name = self.request.query_params.get('subject__name', None)
#         if subject_name:
#             queryset = queryset.filter(subject__name=subject_name)

#         module_name = self.request.query_params.get('module__name', None)
#         if module_name:
#             queryset = queryset.filter(module__name=module_name)

#         topic_name = self.request.query_params.get('topic__name', None)
#         if topic_name:
#             queryset = queryset.filter(topic__name=topic_name)

#         return queryset
from rest_framework.pagination import PageNumberPagination

class SinglePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'pagesize'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and 'http://' in next_url:
            next_url = next_url.replace('http://', 'https://')
        if previous_url is not None and 'http://' in previous_url:
            previous_url = previous_url.replace('http://', 'https://')

        return Response({
            'count': self.page.paginator.count,
            'next': next_url,
            'previous': previous_url,
            'current' : self.page.number,
            'results': data
        })

    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0 and (self.max_page_size is None or page_size <= self.max_page_size):
                    return page_size
            except ValueError:
                pass
        return self.page_size

from django.db.models import OuterRef, Subquery,Max
from searchall.utils import generate_pdf,get_queryset_headers_data
class FacultyList(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class = SinglePagination
    
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
            is_verified=True, is_blocked=False, is_rejected=False).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query) |
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            # queryset = FacultyCourseAddition.objects.filter(category__name__icontains=category).order_by('  created_at')
            # queryset=FacultyCourseAddition.objects.filter(user__in=usersid,category__name__icontains=category).distinct('user')
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
      



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response
        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Verifed Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp


        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class FacultyList(generics.ListAPIView):
#     serializer_class = facultyviewDetails
#     pagination_class = SinglePagination

#     def get_queryset(self):
    
#         queryset = Faculty.objects.filter(
#             is_verified=True, is_blocked=False, is_rejected=False)
#         usersid=[]
#         for x in queryset:
#             usersid.append(x.user.pk)
#         # Apply search filter
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(user__username__icontains=search_query) |
#                                        Q(user__email__icontains=search_query) |
#                                        Q(district__icontains=search_query)|
#                                        Q(user__mobile__icontains=search_query)).distinct()
#         category=self.request.query_params.get('category',None)
#         if category:
#             queryset=FacultyCourseAddition.objects.filter(user__in=usersid,category__name__icontains=category).values('id')
#             # queryset = Faculty.objects.filter(
#             # is_verified=True, is_blocked=False, is_rejected=False,id__in=queryset)
            

#         levels=self.request.query_params.get('levels',None)
#         if levels:
#             queryset=FacultyCourseAddition.objects.filter(user__in=usersid,level__name__icontains=levels)
#         # Apply filter fields
#         course = self.request.query_params.get('course', None)
#         if course:
#             queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid,course__name__icontains=course))
    

#         subject_name = self.request.query_params.get('subject', None)
#         if subject_name:
#             queryset = FacultyCourseAddition.objects.filter(user__in=usersid,subject__name__icontains=subject_name)

#         module_name = self.request.query_params.get('module', None)

#         if module_name:
#             queryset = FacultyCourseAddition.objects.filter(user__in=usersid,module__name__icontains=module_name)
#         topic_name = self.request.query_params.get('topic', None)
#         if topic_name:
#             queryset = FacultyCourseAddition.objects.filter(user__in=usersid,topic__name__icontains=topic_name)
#         if any([ category, levels, course, subject_name, module_name, topic_name]):
#                 queryset = queryset
#                 print(queryset.model,'************')

#         return queryset
        # return queryset.distinct('user')

    # def get_queryset(self):

    #     queryset = Faculty.objects.filter(
    #         is_verified=True, is_blocked=False, is_rejected=False).order_by('-joined_date')

    #     # Apply search filter
    #     search_query = self.request.query_params.get('search', None)
    #     if search_query:
    #         queryset = queryset.filter(Q(user__username__icontains=search_query) |
    #                                    Q(user__email__icontains=search_query) |
    #                                    Q(user__mobile__icontains=search_query)).distinct()

    #     # Apply filter fields
    #     course = self.request.query_params.get('course', None)
    #     if course:
    #         queryset = FacultyCourseAddition.objects.filter(
    #             course__name=course)

    #     subject_name = self.request.query_params.get('subject', None)
    #     if subject_name:
    #         queryset = FacultyCourseAddition.objects.filter(
    #             subject__name=subject_name)

    #     module_name = self.request.query_params.get('module', None)
    #     module_name = self.request.query_params.get('module', None)
    #     if module_name:
    #         queryset = FacultyCourseAddition.objects.filter(
    #             module__name=module_name)
    #     topic_name = self.request.query_params.get('topic', None)
    #     if topic_name:
    #         queryset = FacultyCourseAddition.objects.filter(
    #             topic__name=topic_name)

    #     return queryset

# not verified teacher
# class FacultyListNotVerified(generics.ListAPIView):

#     queryset = Faculty.objects.filter(is_verified=False)
#     serializer_class = FacultySerializerforisverifiedandNOT
# class FacultyListNotVerified(generics.ListAPIView):
#     queryset = Faculty.objects.filter(is_verified=False)
#     serializer_class = FacultySerializerforisverifiedandNOT

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         # Apply search filter
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(user__username__icontains=search_query) |
#                                        Q(user__email__icontains=search_query) |
#                                        Q(user__mobile__icontains=search_query) |
#                                        Q(course__name__icontains=search_query) |
#                                        Q(subject__name__icontains=search_query) |
#                                        Q(module__name__icontains=search_query) |
#                                        Q(topic__name__icontains=search_query)).distinct()

#         # Apply filter fields
#         course = self.request.query_params.get('course', None)
#         if course:
#             queryset = queryset.filter(course__name=course)

#         subject_name = self.request.query_params.get('subject__name', None)
#         if subject_name:
#             queryset = queryset.filter(subject__name=subject_name)

#         module_name = self.request.query_params.get('module__name', None)
#         if module_name:
#             queryset = queryset.filter(module__name=module_name)

#         topic_name = self.request.query_params.get('topic__name', None)
#         if topic_name:
#             queryset = queryset.filter(topic__name=topic_name)

#         return queryset


# class FacultyListNotVerified(generics.ListAPIView):

#     queryset = Faculty.objects.filter(
#         is_verified=False, is_rejected=False, is_blocked=False).order_by('-joined_date')
#     serializer_class = facultyviewDetails
#     pagination_class = SinglePagination

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         # Apply search filter
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(user__username__icontains=search_query) |
#                                        Q(user__email__icontains=search_query) |
#                                        Q(user__mobile__icontains=search_query) |
#                                        Q(course__name__icontains=search_query) |
#                                        Q(subject__name__icontains=search_query) |
#                                        Q(module__name__icontains=search_query) |
#                                        Q(topic__name__icontains=search_query)).distinct()

#         # Apply filter fields
#         course = self.request.query_params.get('course', None)
#         if course:
#             queryset = queryset.filter(course__name=course)

#         subject_name = self.request.query_params.get('subject__name', None)
#         if subject_name:
#             queryset = queryset.filter(subject__name=subject_name)

#         module_name = self.request.query_params.get('module__name', None)
#         if module_name:
#             queryset = queryset.filter(module__name=module_name)

#         topic_name = self.request.query_params.get('topic__name', None)
#         if topic_name:
#             queryset = queryset.filter(topic__name=topic_name)

#         return queryset


class FacultyListNotVerified(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class =SinglePagination
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
          is_verified=False, is_rejected=False, is_blocked=False).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query)|
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
            



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')
            

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        print(queryset.model,'************')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response

        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Not Verifed Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class facultyprofile(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = facultyviewDetailsProfile
    def get_permissions(self):
        print(self.action,"hhhhhhhhhh")
        self.permission = "Faculty"
        if self.action =='list':
            self.feature="list"
            self.permission_classes = [AdminAndRolePermission]
        elif self.action == 'list':
            self.permission_classes = [AdminAndRolePermission]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        print(request,'ddd')
        if AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_role(request=request):
            # try:
            queryset =Faculty.objects.get(id=self.kwargs['pk'])
            serilizer = facultyviewDetailsProfile(queryset)
            return Response(serilizer.data)
            
        elif AuthHandlerIns.is_faculty(request=request):
            print("***********")
            queryset =Faculty.objects.get(user__id=AuthHandlerIns.get_id(request))
            serilizer = facultyviewDetailsProfile(queryset)
            return Response(serilizer.data)
            return self.queryset.get(user__id=AuthHandlerIns.get_id(request))
        else:
            return Response({"message": "You don't have permission to get data"}, status=403)


class facultyupdateprofile(APIView):
    def put(self, request, pk):
        try:
            student = Faculty.objects.get(pk=pk)
            print(student)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FacultyEditProfileSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyAppliedList(APIView):
    def get(self, request, faculty_id):
        try:
            approvals = Approvals.objects.filter(
                faculty__id=faculty_id, status=False)
            serializer = Approvalserializers(approvals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Approvals.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Facultyallbookingdetils(APIView):
    def get(self, request, faculty_id):
        try:
            approvals = Approvals.objects.filter(
                faculty__id=faculty_id, status=True)
            serializer = Approvalserializers(approvals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Approvals.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_batch_in_branch(request, branch_id):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    batch = Batch.objects.filter(branch=branch)
    serializer = BatchSerializer(batch, many=True)
    return Response(serializer.data)


############# FACULTY ATTENDENCE  #########
class FacultyAttendenceListCreateView(generics.ListCreateAPIView):
    queryset = FacultyAttendence.objects.filter(timetable__in=TimeTable.objects.filter(faculty__isnull=False).values('id'))
    
    serializer_class = FacultyAttendenceSerializer

    # def perform_create(self, serializer):
    #     serializer.save(

    #         # created_by=self.request.user,
    #         # updated_by=self.request.user,
    #         created_at=timezone.now(),
    #         updated_at=timezone.now(),
    #     )


class FacultyAttendenceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacultyAttendence.objects.all()
    # queryset = FacultyAttendence.objects.filter(timetable__in=TimeTable.objects.filter(faculty__isnull=False).values('id'))

    serializer_class = FacultyAttendenceSerializer

    # def perform_update(self, serializer):
    #     serializer.save(
    #         updated_by=self.request.user,
    #         updated_at=timezone.now(),
    #         request_type=self.request.method
    #     )

    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.request_type = self.request.method
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


############# FACULTY ATTENDENCE ENDS #########
############# LOG CREATION #########

# class BranchHistoryView(APIView):
#     def get(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id)
#         history = branch.history.all()
#         history_data = []
#         for h in history:
#             # Get the original Branch instance from the historical record
#             original_branch = h.instance

#             if isinstance(original_branch, Branch):
#                 # Only compare to non-historical Branch instances
#                 # history_changes = h.diff_against(original_branch)
#                 history_data.append({
#                     'id': h.id,
#                     'timestamp': h.history_date.isoformat(),
#                     'action': h.history_type,
#                     'Changes': h.history_change_reason,
#                     'User': h.history_user_id,
#                     # 'changes': self.get_changes(original_branch, h),
#                 })
#         data = {'branch': {'id': branch.id, 'name': branch.name},
#                 'history': history_data}
#         return Response(data)

class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'pagesize'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and 'http://' in next_url:
            next_url = next_url.replace('http://', 'https://')
        if previous_url is not None and 'http://' in previous_url:
            previous_url = previous_url.replace('http://', 'https://')

        return Response({
            'count': self.page.paginator.count,
            'next': next_url,
            'previous': previous_url,
            'current': self.page.number,
            'results': data
        })

    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0 and (self.max_page_size is None or page_size <= self.max_page_size):
                    return page_size
            except ValueError:
                pass
        return self.page_size

# class BranchHistoryView(APIView):
#     pagination_class =CustomPagination
#     def get(self, request, branch_id):
#         bexists = Branch.objects.get(id=branch_id)
#         if bexists:
#             print("Hii")
#             branch= Branch.history.filter(id=branch_id)

        
#         else:
#             print("HELLO")
#             branch = Branch.history.all().order_by('-history_date')
        # paginator = self.pagination_class()
        # serializer = HistorySerializer(branch,many=True)
        # page = paginator.paginate_queryset(serializer.data, request)
        # return paginator.get_paginated_response(page)

class BranchHistoryView(viewsets.ModelViewSet):
    queryset = Branch.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Branch.history.filter(id=branch_id)
        else:
            queryset= Branch.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset
        
    

# class BranchHistoryView(APIView):
#     pagination_class = CustomPagination

#     def get(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id)  
        
        
#         if hasattr(branch, 'history'):
#             branch_history = branch.history.all().order_by('-history_date')
#         else:
#             branch_history = []
        
#         paginator = self.pagination_class()
#         serializer = HistorySerializer(branch_history, many=True)
#         page = paginator.paginate_queryset(serializer.data, request)
#         return paginator.get_paginated_response(page)
class CourseHistory(viewsets.ModelViewSet):
    queryset = Course.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Course.history.filter(id=branch_id)
        else:
            queryset= Course.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset

class ModuleHistory(viewsets.ModelViewSet):
    queryset = Module.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Module.history.filter(id=branch_id)
        else:
            queryset= Module.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset

class FacultyHistory(viewsets.ModelViewSet):
    queryset = Faculty.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Faculty.history.filter(id=branch_id)
        else:
            queryset= Faculty.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset
    
    


class TopicHistory(viewsets.ModelViewSet):
    queryset = Topic.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Topic.history.filter(id=branch_id)
        else:
            queryset= Topic.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset
    
    


class SubtopicHistory(viewsets.ModelViewSet):
    queryset = SubTopic.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= SubTopic.history.filter(id=branch_id)
        else:
            queryset= SubTopic.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset
    
    

class SubjectHistory(viewsets.ModelViewSet):
    queryset = Subject.history.all().order_by('-history_date')
    serializer_class = HistorySerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Subject.history.filter(id=branch_id)
        else:
            queryset= Subject.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

        # history_user = self.request.query_params.get('history_user', None)
        # if history_user:
        #     history_user=User.objects.get(email=history_user)
        #     history_user = User.objects.get(email__icontains=history_user)
        #     queryset = queryset.filter(history_user__id__icontains=history_user.id)
            
        history_user_email = self.request.query_params.get('history_user', None)
        if history_user_email:
            queryset = queryset.filter(history_user__email__icontains=history_user_email)
        
        
        branch_name = self.request.query_params.get('branch_name', None)
        if branch_name:
            queryset = queryset.filter(name__icontains=branch_name)

        
        
        ids = self.request.query_params.get('ids', None)
        if ids:
            queryset = queryset.filter(id__contains=ids)
        
        return queryset
    
    
    
class CourseHistoryView(APIView):
    pagination_class =CustomPagination
    def get(self, request, id):
        branch = Course.newobjects.get(id=id)
        history = branch.history.all()
        paginator = self.pagination_class()
        history_data = []
        for h in history:
            action = self.get_action(h)
            user = self.get_user(h)
            changes = self.get_changes(h)
            if 'is_deleted' in changes and changes['is_deleted']:
                action = 'Delete'
            
            history_data.append({
                'id': h.id,
                'timestamp': h.history_date.isoformat(),
                'action': action,
                'changes': changes,
                'user': user,
                
            })
        
        
        
        
        page = paginator.paginate_queryset(history_data, request)
        return paginator.get_paginated_response(page)
    
    def get_action(self, history_record):
        if history_record.history_type == '+':
            return 'Create'
        elif history_record.history_type == '-':
            return 'Delete'
        elif history_record.history_type == '~':
            return 'Update'
        return 'Unknown'

    def get_user(self, history_record):
        user_id = history_record.history_user_id
        print(history_record.history_user_id)
        if user_id:
            user = User.objects.get(id=user_id)
            return f'{user.username}'
        return 'Unknown'

    
        
    #     return changes
    def get_changes(self, history_record):
        changes = {}

        if history_record.history_type == '~':
            prev_records = history_record.instance.history.filter(history_date__lt=history_record.history_date)
            if prev_records.exists():
                prev_record = prev_records.latest('history_date')
                original_instance = prev_record.instance
                for field in original_instance._meta.fields:
                    old_value = getattr(prev_record, field.attname)
                    new_value = getattr(history_record, field.attname)
                    if old_value != new_value:
                        changes[field.verbose_name] = {
                            'old': old_value,
                            'new': new_value,
                        }
                if 'is delete' in changes and changes['is delete']['new'] == True:
                    return {'is_deleted': True, 'id': history_record.instance.id}
        
        
        return changes




@api_view(['GET'])
def get_examschedule_by_batch(request, batch_id):
    try:
        batch = Batch.objects.get(id=batch_id)
    except Batch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    examshedule = ExamSchedule.objects.filter(batch=batch)
    serializer = ExamScheduleSerializer(examshedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_examschedule_by_batch_and_branch(request, batch_id, branch_id):
    try:
        batch = Batch.objects.get(id=batch_id)
        branch = Branch.objects.get(id=branch_id)
    except (Batch.DoesNotExist, Branch.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    examshedule = ExamSchedule.objects.filter(batch=batch, branch=branch)
    serializer = ExamScheduleSerializer(examshedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getwhatyouwant(request):
    category_id = request.query_params.get('cat')
    level_id = request.query_params.get('lev')

    course_id = request.query_params.get('c')
    subject_id = request.query_params.get('s')
    module_id = request.query_params.get('m')
    topic_id = request.query_params.get('t')
    
    if category_id:
        queryset = Level.objects.filter(category=category_id)
        serializer = LevelSerializer(queryset, many=True)
    if level_id:
        queryset = Course.objects.filter(level=level_id)
        serializer = CourseSerializer(queryset, many=True)

    if course_id:
        queryset = Subject.objects.filter(course=course_id)
        serializer = SubjectSerializer(queryset, many=True)
    if subject_id:
        queryset = Module.objects.filter(subject=subject_id)
        serializer = ModuleSerializer(queryset, many=True)

    if module_id:
        queryset = Topic.objects.filter(module=module_id)
        serializer = TopicSerializer(queryset, many=True)

    if topic_id:
        queryset = SubTopic.objects.filter(topic=topic_id)
        serializer = SubTopicSerializer(queryset, many=True)

    return Response(serializer.data)


class CreateHolidays(APIView):
    def post(self, request, format=None):
        serializer = holidaysserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        holiday = Holidays.objects.order_by('date')
        serializers = holidaysserializer(holiday, many=True)
        return Response(serializers.data)

    def delete(self, request, pk):
        holiday = get_object_or_404(Holidays, pk=pk)
        holiday.delete()

        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        holiday = get_object_or_404(Holidays, pk=pk)
        serializer = holidaysserializer(
            holiday, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListByCategory(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategorySummaryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySummarySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)


@api_view(['GET'])
def get_course_by_level(request, level_id):
    print(level_id)
    try:
        level = Level.objects.get(id=level_id)
        print(level)
    except Level.DoesNotExist:
        return Response([])

    courses = Course.objects.filter(level=level)
    print(courses)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_level_by_category(request, category_id):
    try:
        return Response(LevelSerializer(Level.objects.filter(category=category_id), many=True).data)
    except Exception as e:
        return Response(e)


@api_view(['GET'])
def get_course_by_category(request, category_id):
    try:
        level = Level.objects.filter(category=category_id)
        course = Course.objects.filter(level__in=level)
        cs = CourseSerializer(course, many=True)
        return Response(cs.data)
        # return Response(Co(Level.objects.filter(category=category_id),many=True).data)
    except Exception as e:
        return Response(e)
    
class CourseByCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AdminAndRolePermission]  
    pagination_class =SinglePagination

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'create']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Course"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list','retrieve']:
            self.feature = self.action
            self.permission = "Course"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Course"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            level = Level.objects.filter(category=kwargs['pk'])
            course = Course.objects.filter(level__in=level)
            cs = CourseSerializer(course, many=True)
            return Response(cs.data)
        except Exception as e:
            return Response(e)
        
        



@api_view(['GET'])
def getclasslevel(request):
    # print("From getcourse")
    classlevel = ClassLevel.objects.all().order_by('-id')
    serializer = ClassLevelSerializer(classlevel, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def subjectbycourse(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    subject = Subject.objects.filter(course=course)
    serializer = SubjectSerializer(subject, many=True)
    return Response(serializer.data)

# from django.db.models import Sum, Value
# from django.db.models.functions import Coalesce
# class FacultyHistoryView(APIView):
#     def get(self, request, faculty_id):
#         print(faculty_id)
        
#         # faculty_history = defaultdict(list)
#         faculty_history = []

#         attendances = FacultyAttendence.objects.filter(name=faculty_id)
#         print("ATD", attendances)
#         if not attendances:
#             return Response({'error': 'No attendance records found for the specified faculty ID.'}, status=status.HTTP_404_NOT_FOUND)
#         # total_paid_amount = attendances.aggregate(total_paid_amount=Coalesce(Sum('paid_amount'), Value(0)))['total_paid_amount']
#         total_amount = 0
#         for attendance in attendances:
            
#             timetable = attendance.timetable
#             print(timetable, "TIM")

#             # Retrieve necessary details from the timetable instance
#             date = timetable.date
#             branch = timetable.branch.name
#             batch = timetable.batch.name
#             course = timetable.course.name
#             topic = timetable.topic.name
#             payment = attendance.payment_done
#             time_from = attendance.start_time
#             time_to = attendance.end_time
#             hours = attendance.hours
#             subtopics_covered = [
#                 str(subtopic) for subtopic in attendance.subtopics_covered.all()]

#             payed_amnt = attendance.paid_amount
#             total_amount = total_amount + int(payed_amnt)
#             payment_method = attendance.payment_method
#             # Retrieve faculty name
#             faculty_name = attendance.name.name
#             print(faculty_name)
#             # Store details for each faculty
#             # faculty_history[faculty_name].append({
#             faculty_history.append({

#                 'date': date,
#                 'time_from': time_from,
#                 'time_to': time_to,
#                 'hours': hours,
#                 'subtopics_covered': subtopics_covered,
#                 'branch': branch,
#                 'batch': batch,
#                 'course': course,
#                 'topic': topic,
#                 'payment': payment,
#                 'paidamount': payed_amnt,
#                 'payment_method':payment_method,
#                 'faculty_name':faculty_name,
#                 'total_amount': total_amount,

#             })
#             # Add total paid amount to response

#         faculty_fixed_salary = Faculty_Salary.objects.filter(faculty = faculty_id)
#         for x in faculty_fixed_salary:
#             faculty_history.append({x.level.name:x.fixed_salary.salaryscale})

#         # faculty_history.append({'total_paid_amount': total_amount})

#         return Response(faculty_history)

# class CustomPagination(PageNumberPagination):
#     page_size = 8
#     page_size_query_param = 'pagesize'
#     max_page_size = 100

#     def get_paginated_response(self, data):
#         next_url = self.get_next_link()
#         previous_url = self.get_previous_link()

#         if next_url is not None and 'http://' in next_url:
#             next_url = next_url.replace('http://', 'https://')
#         if previous_url is not None and 'http://' in previous_url:
#             previous_url = previous_url.replace('http://', 'https://')

#         return Response({
#             'count': self.page.paginator.count,
#             'next': next_url,
#             'previous': previous_url,
#             'current': self.page.number,
#             'results': data
#         })


class FacultyHistoryView(APIView):
    pagination_class =SinglePagination

    def get(self, request, faculty_id):
        faculty_history = []

        attendances = FacultyAttendence.objects.filter(name=faculty_id)
        if not attendances:
            return Response({'error': 'No attendance records found for the specified faculty ID.'})

        total_amount = 0
        for attendance in attendances:
            timetable = attendance.timetable

            # Retrieve necessary details from the timetable instance
            date = timetable.date
            branch = timetable.branch.name
            batch = timetable.batch.name
            course = timetable.course.name
            level_id = timetable.course.course.course.level.id
            level = timetable.course.course.course.level.name
            topic = timetable.topic.name
            payment = attendance.payment_done
            time_from = attendance.start_time
            time_to = attendance.end_time
            hours = attendance.hours
            subtopics_covered = [
                str(subtopic) for subtopic in attendance.subtopics_covered.all()]

            payed_amnt = attendance.paid_amount
            total_amount = total_amount + payed_amnt
            payment_method = attendance.payment_method
            fixed_salary = Faculty_Salary.objects.filter(faculty = faculty_id,level = level_id)

            for salary in fixed_salary:
                faculty_fixed_salary = salary.fixed_salary
            fixed_sal = faculty_fixed_salary
            if fixed_sal==None:
                return Response([])
            # Retrieve faculty name
            faculty_name = attendance.name.name
            
            
            

            # Store details for each attendance record
            faculty_history.append({
                'date': date,
                'time_from': time_from,
                'time_to': time_to,
                'hours': hours,
                'subtopics_covered': subtopics_covered,
                'branch': branch,
                'batch': batch,
                'level': level,
                'course': course,
                'topic': topic,
                'payment': payment,
                'paidamount': payed_amnt,
                'payment_method':payment_method,
                'faculty_name':faculty_name,
                'total_amount': total_amount,
                'fixed_salary': fixed_sal.salaryscale,

            })

        

        # return Response(faculty_history)
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(faculty_history, request)
        
        return paginator.get_paginated_response(paginated_data)
        




    
class FacultyHistoryAllView(APIView):
    def get(self, request):
        
        # faculty_history = defaultdict(list)
        faculty_history = []
    
        attendances = FacultyAttendence.objects.filter()
        print("ATD", attendances)
        if not attendances:
            return Response({'error': 'No attendance records found for the specified faculty ID.'})
        total_amount = 0

        for attendance in attendances:
            timetable = attendance.timetable
            print(timetable, "TIM")
            try:
                # Retrieve faculty id
                faculty_id = attendance.name.id
            except:
                faculty_id = None
            
            # Retrieve necessary details from the timetable instance
            date = timetable.date
            branch = timetable.branch.name
            batch = timetable.batch.name
            course = timetable.course.name
            level_id = timetable.course.course.course.level.id
            level = timetable.course.course.course.level.name
            topic = timetable.topic.name
            payment = attendance.payment_done
            time_from = attendance.start_time
            time_to = attendance.end_time
            hours = attendance.hours
            # subtopics_covered = attendance.subtopics_covered
            # subtopics_covered = [
            #     str(subtopic) for subtopic in attendance.subtopics_covered.all()]

            payed_amnt = attendance.paid_amount
            total_amount = total_amount + payed_amnt
            payment_method = attendance.payment_method

            fixed_salary = Faculty_Salary.objects.filter(level = level_id ,faculty = faculty_id)
            for salary in fixed_salary:
                faculty_fixed_salary = salary.fixed_salary
            fixed_sal = faculty_fixed_salary
            try:
                # Retrieve faculty name
                faculty_name = attendance.name.user.username
            except:
                faculty_name = None

            try:
                # Retrieve faculty Mobile
                faculty_mobile = attendance.name.user.mobile
            except:
                faculty_mobile = None
            
            # Store details for each faculty
            # faculty_history[faculty_name].append({
            faculty_history.append({

                'date': date,
                'time_from': time_from,
                'time_to': time_to,
                'hours': hours,
                # 'subtopics_covered': subtopics_covered,
                'branch': branch,
                'batch': batch,
                'course': course,
                'level': level,
                'topic': topic,
                'payment': payment,
                'paidamount': payed_amnt,
                'payment_method':payment_method,
                'total_amount': total_amount,
                'faculty_name':faculty_name,
                'faculty_mobile':faculty_mobile,
                'fixed_salary': str(fixed_sal),


            })
            # Add total paid amount to response

        # faculty_fixed_salary = Faculty_Salary.objects.filter(faculty = faculty_id)
        # for x in faculty_fixed_salary:
        #     faculty_history.append({x.level.name:x.fixed_salary.salaryscale})

        # faculty_history.append({'total_paid_amount': total_amount})
        return Response(faculty_history)
        

# from django.db.models import Sum, Value
# from django.db.models.functions import Cast

# class FacultyHistoryView(APIView):
#     def get(self, request, faculty_id):
#         print(faculty_id)
#         faculty_history = []

#         attendances = FacultyAttendence.objects.filter(name=faculty_id)
#         print("ATD", attendances)
#         if not attendances:
#             return Response({'error': 'No attendance records found for the specified faculty ID.'}, status=status.HTTP_404_NOT_FOUND)

#         # Calculate total paid amount
#         total_paid_amount = attendances.annotate(
#     paid_amount_numeric=Cast('paid_amount', output_field=models.DecimalField())
# ).aggregate(Sum('paid_amount_numeric'))['paid_amount_numeric__sum'] or 0

#         for attendance in attendances:
#             timetable = attendance.timetable
#             print(timetable, "TIM")

#             # Retrieve necessary details from the timetable instance
#             date = timetable.date
#             branch = timetable.branch.name
#             batch = timetable.batch.name
#             course = timetable.course.name
#             topic = timetable.topic.name
#             payment = attendance.payment_done
#             time_from = attendance.start_time
#             time_to = attendance.end_time
#             hours = attendance.hours
#             subtopics_covered = [
#                 str(subtopic) for subtopic in attendance.subtopics_covered.all()]

#             payed_amnt = attendance.paid_amount
#             payment_method = attendance.payment_method
#             # Retrieve faculty name
#             faculty_name = attendance.name
#             print(faculty_name)

#             # Store details for each faculty
#             faculty_history.append({
#                 'date': date,
#                 'time_from': time_from,
#                 'time_to': time_to,
#                 'hours': hours,
#                 'subtopics_covered': subtopics_covered,
#                 'branch': branch,
#                 'batch': batch,
#                 'course': course,
#                 'topic': topic,
#                 'payment': payment,
#                 'paidamount': payed_amnt,
#                 'payment_method': payment_method,
#             })

#         # Add total paid amount to response
#         faculty_history.append({'total_paid_amount': total_paid_amount})

#         return Response(faculty_history)


# ################################  WITH DATE #################################
@api_view(['POST'])
def FacultyHistoryViewWithDate(request, faculty_id):
    start_date_str = request.data.get('start_date', None)
    end_date_str = request.data.get('end_date', None)
        

    if start_date_str and end_date_str:
        # start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        # end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        start_date = start_date_str
        end_date = end_date_str
        attendances = FacultyAttendence.objects.filter(name=faculty_id, created_date__gte=start_date, created_date__lte=end_date)
    else:
        attendances = FacultyAttendence.objects.filter(name=faculty_id)

    faculty_history = []
    total_paid_amount = 0

    if not attendances:
        return Response('No attendance records found for the specified faculty ID.')

    for attendance in attendances:
        timetable = attendance.timetable

        # Retrieve necessary details from the timetable instance
        date = timetable.date
        branch = timetable.branch.name
        batch = timetable.batch.name
        course = timetable.course.name
        level_id = timetable.course.course.course.level.id
        level = timetable.course.course.course.level.name

        topic = timetable.topic.name
        payment = attendance.payment_done
        time_from = attendance.start_time
        time_to = attendance.end_time
        hours = attendance.hours
        # subtopics_covered = [
        #     str(subtopic) for subtopic in attendance.subtopics_covered.all()]

        payed_amnt = attendance.paid_amount
        payment_method = attendance.payment_method
        fixed_salary = Faculty_Salary.objects.filter(faculty = faculty_id,level = level_id,is_online=False)
        faculty_fixed_salary = 0
        if fixed_salary.exists():
            for salary in fixed_salary:
                faculty_fixed_salary = salary.fixed_salary
        
        fixed_sal = faculty_fixed_salary
        
        

        total_paid_amount += float(payed_amnt)


        try:
            # Retrieve faculty name
            faculty_name = attendance.name.user.username
        except:
            faculty_name = None

        try:
            # Retrieve faculty Mobile
            faculty_mobile = attendance.name.user.mobile
        except:
            faculty_mobile = None

        # Store details for each faculty
        faculty_history.append({
            'date': date,
            'time_from': time_from,
            'time_to': time_to,
            'hours': hours,
            # 'subtopics_covered': subtopics_covered,
            'faculty_name' : faculty_name,
            'faculty_mobile':faculty_mobile,
            'branch': branch,
            'batch': batch,
            'course': course,
            'level': level,
            'topic': topic,
            'payment': payment,
            'paidamount': payed_amnt,
            'payment_method': payment_method,
            'total_paid_amount': total_paid_amount,
            'fixed_salary': str(fixed_sal),

        })
    # print(level)
    # response_data = ( faculty_history,)
        # 'total_paid_amount': total_paid_amount
    

    return Response( faculty_history,)
################################  WITH DATE ENDS #################################


@api_view(['GET'])
def modulesbysubject(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    module = Module.objects.filter(subject=subject)
    serializer = ModuleSerializer(module, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topicsbymodule(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    topics = Topic.objects.filter(module=module)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


class AllSubTopicsView(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        serialized_data = []

        for topic in topics:
            serializer = SubTopicSerializer(
                topic.subtopic_set.all(), many=True)
            serialized_data.append({
                'topic': topic.name,
                'subtopics': serializer.data
            })

        return Response(serialized_data)


@api_view(['GET'])
def getclasslevel(request):
    # print("From getcourse")
    classlevel = ClassLevel.objects.all().order_by('-id')
    serializer = ClassLevelSerializer(classlevel, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def statuschangecourse(request, id):
    if AuthHandlerIns.is_staff(request=request):
        Course.objects.filter(id=id).update(
            active=not Course.objects.get(id=id).active)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def statuschangesubject(request, id):
    if AuthHandlerIns.is_staff(request=request):
        Subject.objects.filter(id=id).update(
            active=not Subject.objects.get(id=id).active)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def statuschangemodule(request, id):
    if AuthHandlerIns.is_staff(request=request):
        Module.objects.filter(id=id).update(
            active=not Module.objects.get(id=id).active)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def statuschangetopic(request, id):
    if AuthHandlerIns.is_staff(request=request):
        Topic.objects.filter(id=id).update(
            active=not Topic.objects.get(id=id).active)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def statuschangesubtopic(request, id):
    if AuthHandlerIns.is_staff(request=request):
        SubTopic.objects.filter(id=id).update(
            active=not SubTopic.objects.get(id=id).active)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

import datetime

@api_view(['POST'])
def batchcreate(request):
    if AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_role(request=request):
        try:
            branch = Branch.objects.get(id=request.data['branch'])
            course = Course_branch.objects.get(
                course=request.data['course'], branch=branch.pk)
            batchexist = Batch.objects.filter(name=request.data['name'])
            if batchexist.exists():
                return Response({"message": "Name Already Taken"}, status=status.HTTP_409_CONFLICT)
            batch = Batch.objects.create(name=request.data['name'], start_date=request.data['start_date'], end_date=request.data['end_date'],
                                         course=course, strength=request.data['strength'],fees=request.data['fees'],installment_count=request.data['installment_count'],
                                         branch=branch, working_days=getchoicefromlist(request.data['working_days']), exam_days=getchoicefromlist(request.data['exam_days']))

            # serializer = BatchSerializer(data=batch)
            # serializer.is_valid(raise_exception=True)
            if request.data['autotime']:
                print(request.data['auto_start_date'], type(
                    request.data['auto_start_date']), "kklksalksa")
                # print(request.data['facultylist'][0]['user']['id'], "newwww")
                createautomaticTimetable(
                    batch.id, request.data['autofaculty'], request.data['auto_start_date'], request.data['auto_end_date'], request.data['facultylist'] if request.data['autofaculty'] else [])
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def getweekdayarray(arr):
    ans = []
    for i in arr:
        if i == 'Mon':
            ans.append(0)
        elif i == 'Tue':
            ans.append(1)
        elif i == 'Wed':
            ans.append(2)
        elif i == 'Thu':
            ans.append(3)
        elif i == 'Fri':
            ans.append(4)
        elif i == 'Sat':
            ans.append(5)
        elif i == 'Sun':
            ans.append(6)

    return ans


def createautomaticTimetable(batch_id, faculty=False, autostartdate=None, autoenddate=None, facultylist=[]):
    batch = Batch.objects.filter(id=batch_id).values()
    batch_ins = Batch.objects.get(id=batch_id)
    holiday = SpecialHoliday.objects.filter(Q(batches__in=[batch_ins]) | Q(branches__in=[batch_ins.branch]) | Q(levels__in=[batch_ins.course.course.level]) |  Q(batches=None, branches=None, levels=None)).values('date')
    holidays = [datetime.datetime.combine(i["date"], datetime.time.min) for i in holiday]

    batch_weekdays = getweekdayarray(batch[0]["working_days"])
    dates = []
    timetablelist = []

    start_date = datetime.datetime.strptime(autostartdate, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(autoenddate, '%Y-%m-%d')
    crnt_date = start_date
    topics_batch = Topic_batch.objects.filter(
        batch=batch[0]["id"], status="P").order_by('order')

    i = 0

    while crnt_date <= end_date and i <= len(topics_batch):
       
        if crnt_date.weekday() in batch_weekdays and  crnt_date not in holidays:
            # if autoenddate and autoenddate <= crnt_date:
            #     return
        

            try:

                timetable = TimeTable.objects.create(date=crnt_date, branch=Branch.objects.get(
                    id=batch[0]['branch_id']), batch=Batch.objects.get(id=batch[0]['id']), topic=topics_batch[i], course=Course_batch.objects.get(course=batch[0]['course_id'], batch=batch[0]['id']))
                i += 1
                timetablelist.append(timetable)

            except Exception as e:
                print(e, "jjj")

            # print(crnt_date)

        crnt_date = crnt_date + datetime.timedelta(days=1)
    print(faculty)
    if faculty:
        facultyid = [x['user']['id'] for x in facultylist]
        topicid = [x.topic.topic.topic.id for x in timetablelist]
        print("hhhhhhsahshashahsa")
        print(topicid)
        for i in timetablelist:
            time = TimeTable.objects.get(id=i.id)
            faccourse = FacultyCourseAddition.objects.filter(
                user__in=facultyid, topic=time.topic.topic.topic.id)
            if faccourse.exists():
                # TimeTable.objects.filter(id=i.id).update(faculty=faccourse[0].user)
                time.faculty = faccourse[0].user
                time.save()

    pass


# class MaterialCreateAPIView(generics.CreateAPIView):
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def perform_create(self, serializer):
#         serializer.save(file=self.request.data.get('file'))

# class MaterialDetailView(generics.RetrieveAPIView):
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer

#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


class facultyblockedlist(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class =SinglePagination
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
           is_blocked=True, is_verified=True, is_rejected=False).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query)|
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
            



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')
            

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        print(queryset.model,'************')
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response

        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Blocked Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def get(self, requeust):
    #     blockedllist = Faculty.objects.filter(
    #         is_blocked=True, is_verified=True, is_rejected=False)

    #     print(blockedllist)
    #     serializer = facultyviewDetails(blockedllist, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

# class FacultyTopics(RetrieveAPIView):
#     queryset = Faculty.objects.all()
#     serializer_class = FacultyTopicsView

#     def get_object(self):
#         return self.queryset.get(id=self.kwargs['id'])


class FacultyTopics(APIView):
    def get(self, request, id):
        # Fetch faculty data using faculty id
        faculty = Faculty.objects.get(id=id)

        # Serialize faculty data with topics
        faculty_serializer = FacultyTopicsView(faculty)

        # Fetch all materials related to the faculty
        materials = Material.objects.filter(faculty=faculty)

        # Serialize materials
        material_serializer = MaterialSerializer(materials, many=True)

        # Combine faculty data with materials
        data = {
            "faculty": faculty_serializer.data,
            "materials": material_serializer.data
        }

        return Response(data)

# block faculty with reason

@api_view(['POST'])
def faculyblockewdwithreason(request, id):
    if AuthHandlerIns.is_staff(request=request):
        faculty = Faculty.objects.get(id=id)
        try:

            if faculty.is_blocked == False:
                blockreason = request.data['blockreason']
                faculty.is_blocked = True
                faculty.blockreason = blockreason
                faculty.save()
                history_withoutdecorator(request,faculty)
                serializer = facultyblockwithreson(faculty)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                faculty.is_blocked = False
                faculty.blockreason = None
                faculty.save()
                history_withoutdecorator(request,faculty)
                serializer = facultyblockwithreson(faculty)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Please give the reason of rejection"}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response({"message": "You have not perimission to block faculty"}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# def faculyrejectwithreason(request, id):
#     if AuthHandlerIns.is_staff(request=request):

#         faculty = Faculty.objects.get(id=id)
#         try:
#             if faculty.is_rejected == False:
#                 print("***********")
#                 rejectreason = request.data['rejectreason']
#                 faculty.is_rejected = True
#                 email = faculty.user.email
#                 faculty.rejectreason = rejectreason
#                 faculty.save()

#                 # send an email to the faculty after registration
#                 subject = f'{faculty.user.username}, Your Registration has been Rejected'
#                 print("hhhhhhhhhhh")
#                 body = f'Your registration with ACE EDUCATION CENTER has been rejected for the following reason: {rejectreason}. Please contact us for more information.'
#                 from_email = settings.EMAIL_HOST_USER
#                 to_email = [email]
#                 print("KKKKKKKKKK")
#                 send_mail(
#                     subject=subject,
#                     message=body,
#                     from_email=from_email,
#                     recipient_list=to_email,
#                     fail_silently=False
#                 )
#                 print("PPPPPPPPPPPPPPP")
#                 serializer = facultyrejectwithreson(faculty)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             faculty.is_rejected = False
#             faculty.rejectreason = None
#             faculty.save()
#             serializer = facultyrejectwithreson(faculty)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response({"message": "Please give the reason of rejection"}, status=status.HTTP_401_UNAUTHORIZED)

#     else:
#         return Response({"message": "You do not have permission to reject faculty"}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# def faculyrejectwithreason(request, id):
#     if AuthHandlerIns.is_staff(request=request):
#         faculty = Faculty.objects.get(id=id)
#         try:
#             if faculty.is_rejected == False:
#                 rejectreason = request.data['rejectreason']
#                 faculty.is_rejected = True
#                 email = faculty.user.email
#                 print("email",email)
#                 faculty.rejectreason = rejectreason
#                 faculty.save()

#                 # send an email to the faculty after registration
#                 mail_subject = f'{faculty.user.username}, Your Registration has been Rejected'
#                 body = f'Your registration with ACE EDUCATION CENTER has been rejected for the following reason: {rejectreason}. Please contact us for more information.'
#                 print("OOOOOOOOOOOO")
#                 # from_email = settings.EMAIL_HOST_USER
#                 # print("OOOOOOOOddddddddOOOO",from_email)
#                 to_email = [email]
#                 print(to_email,'tomaail')
#                 send_email = EmailMessage(mail_subject, body, to=[to_email])
#                 print(send_email,'dddddddd')
#                 send_email.send()
#                 print("sendddd")
#                 # send_mail(
#                 #     subject=subject,
#                 #     message=body,
#                 #     # from_email=from_email,
#                 #     recipient_list=to_email,
#                 #     fail_silently=False
#                 # )
#                 serializer = facultyrejectwithreson(faculty)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             faculty.is_rejected = False
#             faculty.rejectreason = None
#             faculty.save()
#             serializer = facultyrejectwithreson(faculty)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except KeyError as e:
#             return Response({"message": f"Please provide the {e} field in the request data."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(e)
#             return Response({"message": "An error occurred while rejecting the faculty."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     else:
#         return Response({"message": "You do not have permission to reject faculty"}, status=status.HTTP_401_UNAUTHORIZED)
# new func fac reject
def history_withoutdecorator(request,instance):
    user = AuthHandlerIns.get_id(request=request)
    user_who_made_change = User.objects.get(id=user)
    history_instance = instance.history.first()
    print("historyyyyyyyyyyyyyy",history_instance)
    if history_instance:
        history_instance.history_user = user_who_made_change
        history_instance.save()
    ins=instance._meta.model.newobjects.get(id = instance.id ).history.first()
    print("issssssssssssssssssssssss",ins)
    ins.history_user=user_who_made_change
    ins.save()
@api_view(['POST'])
def faculyrejectwithreason(request, id):
    if AuthHandlerIns.is_staff(request=request):

        faculty = Faculty.objects.get(id=id)
        try:
            if faculty.is_rejected == False:
                rejectreason = request.data['rejectreason']
                faculty.is_rejected = True
                email = faculty.user.email
                faculty.rejectreason = rejectreason
                faculty.save()

                # send an email to the faculty after registration
                subject = f'{faculty.user.username}, Your Registration has been Rejected'
                body = f'Your registration with ACE EDUCATION CENTER has been rejected for the following reason:\n {rejectreason}.\nPlease contact us for more information.\n\n\nACE EDUCATION CENTER,Manjeri'
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=from_email,
                    recipient_list=to_email,
                    fail_silently=False
                )
                try:
                    print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                    history_withoutdecorator(request,faculty)
                    print("printtttttttttttttttttttttttttttt")
                except Exception as e:
                    print(e,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                    pass
                serializer = facultyrejectwithreson(faculty)
                return Response(serializer.data, status=status.HTTP_200_OK)
            faculty.is_rejected = False
            faculty.rejectreason = None
            faculty.save()
            try:
                print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
                history_withoutdecorator(request,faculty)
                print("printtttttttttttttttttttttttttttt")
            except Exception as e:
                print(e,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                pass
            serializer = facultyrejectwithreson(faculty)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e,"4444444444444444444")
            return Response({"message": "Please give the reason of rejection"}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response({"message": "You do not have permission to reject faculty"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def timetable_by_batch(request, id):
    print(id, "hhhhhhhhhhhh")
    if AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_role(request=request):
        q = TimeTable.objects.filter(batch=id)
        t = Timetableserializers(
            q, many=True, context={'request': request})
        return Response({"timetable": t.data})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

from searchall.views import queryset_to_excel, queryset_to_excel_data, queryset_to_pdf, get_table_data
from django.http import FileResponse
from searchall.utils import generate_pdf_new

class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    pagination_class = SinglePagination
    queryset = Course.objects.filter()
    # permission_classes=[AdminAndRolePermission]

    def get_queryset(self):
        queryset = Course.objects.all()
        search_query = self.request.query_params.get('search', None)
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)
        name = self.request.query_params.get('name', None)
        level_name = self.request.query_params.get('level_name', None)
        category_name = self.request.query_params.get('category_name', None)
        year = self.request.query_params.get('year', None)
        id = self.request.query_params.get('id', None)
        category = self.request.query_params.get('category', None)
        level = self.request.query_params.get('level', None)
        batch = self.request.query_params.get('batch_name', None)

        if search_query:
            queryset = queryset.filter(Q(level__category__name__icontains=search_query) |
                                       Q(level__name__icontains=search_query) |
                                       Q(name__icontains=search_query) |
                                       Q(year__icontains=search_query)|
                                       Q(id__icontains=search_query)|
                                       Q(batch_type__name__icontains=search_query)).distinct()
        if id:
            queryset=queryset.filter(id__startswith=id)
        if year:
            queryset=queryset.filter(year__startswith=year)

        if category_name:
            queryset=queryset.filter(level__category__name__icontains=category_name)
        
        if level_name:
            queryset=queryset.filter(level__name__icontains=level_name)
        if name:
            queryset=queryset.filter(name__icontains=name)
        if level:
            queryset=queryset.filter(level__id=level)
            
        if category:
            queryset=queryset.filter(level__category__id=category)
        if batch:
            queryset=queryset.filter(batch_type__name__icontains=batch)
            
        
        return queryset

    def list(self, request, *args, **kwargs):
        print("hellos")
        queryset = self.get_queryset()
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            fields = ['name','description','batch_type__name','is_online','active','year','created_at']
            response = queryset_to_excel_data(queryset,[field for field in fields],
                                         {
                            # 'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'}
                            'is_online': {True: 'Yes', False: 'No'},
                            'active': {True: 'Yes', False: 'No'},
                            # 'idverified': {'True': 'Yes', 'False': 'No'}
                            })
            print(response)
            return response
        if pdf_query:
            fields = ['name', 'level__name','level__category__name', 'batch_type__name', 'year']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            print(headers,'dddd')
            modified_headers = []

            modified_headers.append(headers[0].replace('Name', 'Course Name'))
            modified_headers.append(headers[1].replace('Name', 'Course Category Name'))
            modified_headers.append(headers[2].replace('Name', 'Category Name'))
            modified_headers.append(headers[3].replace('Name', 'Category Name'))
            modified_headers.append(headers[4].replace('Name', 'Batch Name'))
            print(modified_headers, 'modified headers')
                    
            nameheading = 'Course'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def retrieve(self, request, *args, **kwargs):
        print("helkpppppppppppppp")
        course = Course.objects.filter(id= kwargs['pk'])
        coser= CourseSerializer(course, many=True)
        subject = Subject.objects.filter(course=kwargs['pk'])
        print(subject)
        print(")))))")
        subser= SubjectSerializer(subject, many=True)
        module = Module.objects.filter(subject__course=kwargs['pk'])
        moser=ModuleSerializer(module, many =True)
        topic = Topic.objects.filter(module__subject__course=kwargs['pk'])
        toser = TopicSerializer(topic, many=True)
        return Response({"course":coser.data,"subject":subser.data,"module":moser.data,"topic":toser.data})
        
        





class facultyrejecteddlist(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class =SinglePagination
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
          is_blocked=False, is_verified=False, is_rejected=True).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query)|
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
            



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')
            

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        # if pdf_query:
            # pdf_buffer = queryset_to_pdf(queryset, ['name','id'])
            # queryset = User.objects.all()
            # pdf_buffer = queryset_to_pdf(queryset, ['email', 'id'])

            # # Prepare the file response for downloading
            # response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename=output.pdf'

            # # Write the PDF buffer to the response
            # response.write(pdf_buffer.getvalue())
            # queryset= User.objects.all()
            # resp = generate_pdf('coursepdf.html',
            #                     {
            #                         # 'headers': headers,
            #                         'data': queryset,
            #                         'current_datetime': 111,
            #                         'model':"faculty"
            #                     }, 'courselist.pdf')
            # return resp

            
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response

        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Rejected Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # def get(self, requeust):
    #     rejectedllist = Faculty.objects.filter(
    #         is_blocked=False, is_verified=False, is_rejected=True)
    #     serializer = facultyviewDetails(rejectedllist, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class facultyonlinelist(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class =SinglePagination
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
          is_blocked=False, is_verified=True, is_rejected=False,modeofclasschoice__in=[2,3]).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid') 
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                           Q(user__mobile__icontains=search_query)|
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
            



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')
            

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        print(queryset.model,'************')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response

        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Online Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp



        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class facultyofflinelist(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class =SinglePagination
    #####add permissions
    def get_permissions(self):
        print("PPPP")
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Faculty"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Faculty"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
          is_blocked=False, is_verified=True, is_rejected=False,modeofclasschoice__in=[1,3]).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query)|
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
            



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')
            

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        print(queryset.model,'************')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response

        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Offline Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





@api_view(['PUT'])
def approve_faculty_timetable(request, id):
    if not AuthHandlerIns.is_staff(request=request):
        return Response({"message": "only admin can approve"})
    approvals = Approvals.objects.get(id=id)
    timetable = TimeTable.objects.get(id=approvals.timetable.pk)
    exist = TimeTable.objects.filter(
        date=timetable.date, faculty=approvals.faculty)

    if len(exist) != 0:
        return Response({"message": "faculty is not available"})

    approvals.status = True
    approvals.save()
    timetable.faculty = approvals.faculty

    timetable.save()

    return Response({"done": "done"})


@api_view(['PUT'])
def add_faculty_timetable(request, id, pk):
    if  AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_role(request=request):

        timetable = TimeTable.objects.get(id=id)
        faculty = User.objects.get(id=pk)
        exist = TimeTable.objects.filter(date=timetable.date, faculty=faculty)
        if timetable.is_combined:
            
            time=TimeTable.objects.filter(date=timetable.date, batch__in=timetable.combined_batch.values('id'))
            for i in time:
                i.faculty = faculty
                i.save()

        elif len(exist) != 0:
            
            time=Timetableserializersnew(exist, many=True , context={'request': request})
            
            return Response({"message": "faculty is not available","TimeTable":time.data})

        # approvals.status=True
        # approvals.save()
        timetable.faculty = faculty

        timetable.save()
    

        return Response({"done": "done"})
    else:
        return Response({"message": "only admin can approve"},status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def get_subject_batch(request, id):
    subject = Subject_batch.objects.filter(batch=id)
    subjects = Subject_batchSerializer(subject, many=True)
    return Response(subjects.data)


@api_view(['GET'])
def get_bat_batch(request, id):
    subject = Subject_batch.objects.filter(batch=id)
    subjects = Subject_batchSerializer(subject, many=True)
    return Response(subjects.data)


class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



class RatingOnFacultyViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = AuthHandlerIns.get_id(request=request)
            user = User.objects.get(id=user_id)
            rating_id = request.data['rating_on']
            rating_on = TimeTable.objects.get(id=rating_id)
            choice = request.data['choice']
            tt = TimeTable.objects.get(id=rating_id)
            
            #############CHECK CLASS FINISHED? #############
            if tt.topic.status != 'F':
                raise ValidationError('The Class Is Not Completed.')
            faculty = Faculty.objects.get(user=tt.faculty.id)
            queryset = Rating.objects.filter(user=user,rating_on=rating_on)
            if queryset.exists():
                raise ValidationError('A rating by this user for this TimeTable already exists.')
            
            else:
                rating = Rating.objects.create(
                    user=user,
                    rating_on=rating_on,
                    choice=choice,
                    rate_fac=faculty
                )

                serializer = self.serializer_class(rating)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        except TimeTable.DoesNotExist:
            return Response({"error": "TimeTable does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Faculty.DoesNotExist:
            return Response({"error": "Faculty does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    


class RatingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class FacultyRatingView(APIView):
    def get(self, request, faculty_id):
        # print(faculty_id)

        faculty = get_object_or_404(Faculty, id=faculty_id)
        timetables = TimeTable.objects.filter(faculty=faculty.user.id)
        timetable_ratings = []
        for timetable in timetables:
            rating = Rating.objects.filter(
                rating_on=timetable).aggregate(Avg('choice'))
            

            timetable_ratings.append({
                'timetable': timetable,
                'rating': rating['choice__avg'] if rating['choice__avg'] is not None else 0
            })
        
        faculty_rating = sum([tr['rating'] for tr in timetable_ratings]) / \
            len(timetable_ratings) if len(timetable_ratings) > 0 else 0
        return Response({'faculty': faculty.name, 'rating': faculty_rating})


class BatchTypeCreateView(generics.CreateAPIView):
    queryset = BatchType.objects.all()
    serializer_class = BatchTypeSerializer

    def post(self, request, *args, **kwargs):

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Batch Type"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)


class BatchTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BatchType.objects.all()
    serializer_class = BatchTypeSerializer


@api_view(['GET'])
def batch_type_list(request):
    batch_types = BatchType.objects.all()
    serializer = BatchTypeSerializer(batch_types, many=True)
    return Response(serializer.data)


class TopicOrderGet(viewsets.ViewSet):
    def list(self, request, pk):
        subject = Subject.objects.filter(course=pk).values('id')
        module = Module.objects.filter(subject__in=subject).values('id')
        topics = Topic.objects.filter(module__in=module, order__isnull=True)
        highest_order = Topic.objects.filter(module__in=module).aggregate(
            models.Max('order')
        )['order__max']
        if len(topics) != 0:
            if highest_order == None:
                highest_order = 0
            for topic in topics:
                topic.order = highest_order + 1
                highest_order += 1
                topic.save()
        topics = Topic.objects.filter(module__in=module).order_by('order')
        return Response(TopicSerializer(topics, many=True).data)

    def edit(self, request, pk):
        print("hellooooo", AuthHandlerIns.is_staff(request))
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can change order"}, status=status.HTTP_401_UNAUTHORIZED)
        for i in range(0, len(request.data)):
            Topic.objects.filter(id=request.data[i]['id_obj']).update(order=i)
        return Response({"done": "ok"})
    
    def create(self, request, pk):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can change order"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            topic_id = int(request.data['topic'])
            new_order = int(request.data['order'])
        except (KeyError, ValueError):
            return Response({"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.get(id=pk)
        subject = Subject.objects.filter(course=course)
        module = Module.objects.filter(subject__in=subject)
        topc_tochange = Topic.objects.get(id=topic_id)

        # if new_order == topc_tochange.order:
        #     return Response({"message": "Topic order already set to the requested value"})
        print(topc_tochange.name , topc_tochange.order,new_order,"ABhis")
        with transaction.atomic():
            if new_order <= topc_tochange.order:
                print("great")
                new_order-=1
                topics_to_update = Topic.objects.filter(
                    module__in=module,
                    order__lt=topc_tochange.order,
                    order__gte=new_order,
                ).exclude(id=topic_id).order_by('-order')

                for topic in topics_to_update:
                    topic.order += 1
                    topic.save()

            elif new_order > topc_tochange.order:
                print("less")
                new_order-=1
                topics_to_update = Topic.objects.filter(
                    module__in=module, 
                    order__gt=topc_tochange.order,
                    order__lte=new_order,
                ).exclude(id=topic_id).order_by('order')

                for topic in topics_to_update:
                    topic.order -= 1
                    topic.save()

            topc_tochange.order = new_order
            topc_tochange.save()

        return Response({"message": "Topic order updated successfully"})

class BranchCourseView(viewsets.ModelViewSet):
    queryset = Branch_courses.objects.all()
    serializer_class = Branch_coursesSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name')
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self, queryset):
        branch = self.request.query_params.get('branch')
        if branch:
            queryset = queryset.filter(branch=branch)
        return queryset


class BranchCoursesView(viewsets.ViewSet):
    def list(self, request, pk):
        branchCourse = Branch_courses.objects.filter(branch=pk)
        return Response(Branch_coursesSerializer(branchCourse, many=True).data)


class BatchTopicListView(viewsets.ViewSet):
    def list(self, request, pk):
        batchCourse = Topic_batch.objects.filter(batch=pk)
        return Response(TopicBatchSerializer(batchCourse, many=True).data)

import datetime
class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Get the related topic instance
        with transaction.atomic():
            if instance.is_combined:
                print("here")
                timetables = TimeTable.objects.filter(date=instance.date,batch__in=instance.combined_batch.values('id'))
                for timetable in timetables:
                    timetable.combined_batch.remove(instance.batch.id)
                    if timetable.combined_batch.count()<=1:
                        print("here1")
                        timetable.is_combined=False
                    timetable.save()
        topic = instance.topic
        instance.faculty = None
        # Update the status of the topic instance
        topic.status = 'P'
        topic.save()
        # Delete the timetable instance
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, *args, **kwargs):
        print("yesssssssssss",request.data['faculty']=='null')
        if AuthHandlerIns.is_staff(request=request):
            return super().partial_update(request, *args, **kwargs)
        if 'faculty' in request.data and request.data['faculty']=='null':
            time =TimeTable.objects.get(id=kwargs['pk'])
            current_date = datetime.datetime.now().date()
            timetable_date = time.date

            # Calculate the difference between the timetable date and current date
            date_difference = timetable_date - current_date

            # Check if the date difference is at least 1 day
            if date_difference >= timedelta(days=1):
                return super().partial_update(request, *args, **kwargs)
            else:
                return Response({"message":"Too Late Cancel kindly Contact Admin"},status=status.HTTP_304_NOT_MODIFIED)
            print("yesssss")
        else:
            return super().partial_update(request, *args, **kwargs)



class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchViewsetSerializer


class BranchCourseViewSet(viewsets.ModelViewSet):
    queryset = Branch_courses.objects.all()
    serializer_class = BranchCourseSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def crud_course_branch(request, branch_id, course_id):
    try:
        if request.method == 'DELETE':
            branch = Branch_courses.objects.filter(
                branch=branch_id, course=course_id)
            print(branch_id, "COU", course_id)
            # branch.delete()
            if branch:
                branch.delete()
                return Response({'Status': 'Success'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'status': 'fail', 'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PATCH':
            try:
                branch = Branch_courses.objects.get(
                    branch=branch_id, course=course_id)

            except Branch_courses.DoesNotExist:
                raise NotFound()
            serializer = BranchCourseSerializer(
                instance=branch, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CourseBranchViewSet(viewsets.ViewSet):

#     def destroy(self, request, branch_id, course_id):
#         branch = Branch_courses.objects.filter(branch=branch_id, course=course_id)
#         if branch:
#             branch.delete()
#             return Response({'Status': 'Success'}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'status': 'fail', 'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)

#     def partial_update(self, request, branch_id, course_id):
#         try:
#             branch = Branch_courses.objects.get(branch=branch_id, course=course_id)
#         except Branch_courses.DoesNotExist:
#             raise NotFound()
#         serializer = BranchCourseSerializer(instance=branch, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

class CourseBranchViewSet(viewsets.ViewSet):

    def destroy(self, request, branch_id, course_id):
        branch = Branch_courses.objects.filter(
            branch=branch_id, course=course_id)
        if branch:
            branch.delete()
            return Response({'Status': 'Success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 'fail', 'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, branch_id):
        courses = request.data.get('courses', [])
        branch_courses = []
        for course_id in courses:
            try:
                branch_course = Branch_courses.objects.get(
                    branch=branch_id, course=course_id)
                serializer = BranchCourseAdditionalSerializer(
                    instance=branch_course, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                branch_courses.append(serializer.data)
            except Branch_courses.DoesNotExist:
                serializer = BranchCourseAdditionalSerializer(
                    data={'branch': branch_id, 'course': course_id})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                branch_courses.append(serializer.data)
        print(branch_courses,"jjjjjjjjjjjjjjjjjjjjjjjjjjj")
        branchCourses(request,branch_courses)
        return Response(branch_courses, status=status.HTTP_200_OK)
    
def branchCourses(request,branch_courses):
    print("okkokkoookookookokokokokokokoko")

    return 



class TopicScheduleGet(viewsets.ViewSet):
    def list(self, request, pk):
        subject = Subject_batch.objects.filter(batch=pk).values('id')
        module = Module_batch.objects.filter(subject__in=subject).values('id')
        topics = Topic_batch.objects.filter(module__in=module, status="P").order_by('order')
        return Response(TopicBatchSerializerNew(topics, many=True).data)


class FacultyAvailablity(viewsets.ViewSet):
    def list(self, request, pk, date):
        timetable = TimeTable.objects.filter(faculty=pk, date=date)
        if timetable.exists():
            return Response({'is_available': False})
        return Response({'is_available': True})


class AutoTimeSchedule(viewsets.ViewSet):
    def create(self, request, batch_id):
        try:
            autostartdate = request.data['autostartdate']
        except:
            autostartdate = None
            return Response({"message": "autostartdate not found"})
        try:

            autoenddate = request.data['autoenddate']
        except:
            autoenddate = None
            return Response({"message": "autoenddate not found"})
        try:

            facultylist = request.data['facultylist']
        except:
            facultylist = []
        try:
            faculty = request.data['faculty']
        except:
            faculty = None
        try:
            createautomaticTimetable(batch_id, faculty=faculty, autostartdate=autostartdate,
                                     autoenddate=autoenddate, facultylist=facultylist)
            return Response({"message": "Success"})
        except:
            return Response({"message": "Fail"})


class ReviewQuestionsViewSet(viewsets.ModelViewSet):
    queryset = ReviewQuestions.objects.all()
    serializer_class = ReviewQuestionsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer





class ReviewQuestionsGetViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewQuestionsSerializer
    queryset = ReviewQuestions.objects.all()

    def retrieve(self, request,pk=None, *args, **kwargs):
        questions = ReviewQuestions.objects.filter(choice=pk)
        serilizer = ReviewQuestionsSerializer(questions,many = True)
        return Response(serilizer.data)

    

class TimeTableReViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def retrieve(self, request,pk=None, *args, **kwargs):
        reviews = Review.objects.filter(review_on=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    


class FacultyAttendanceViewSet(viewsets.ModelViewSet):
    queryset = FacultyAttendence.objects.all()
    serializer_class = FacultyAttendenceSerializer

    def list(self, request):
        timetable_id = request.query_params.get('timetable_id')
        if not timetable_id:
            return Response({'error': 'timetable_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset.filter(timetable__id=timetable_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
def sutopic_based_on_timetable(request, timetable_id):
    timetable = TimeTable.objects.get(id=timetable_id)
    topic = timetable.topic.topic.topic
    subtopic = SubTopic.objects.filter(topic=topic)
    subtopicid = []
    for id in subtopic:
        subtopicid.append(id.id)
    # print(subtopicid)
    facattendence = FacultyAttendence.objects.get(timetable=timetable_id)
    print(facattendence.subtopics_covered)
    # for subtop in facattendence:
    #     print(subtop.subtopics_covered)

    # print (facattendence.subtopics_covered.id)

    serializer = SubTopicSerializer(subtopic, many=True)
    return Response(serializer.data)


# class TimeTableAttendanceViewSet(viewsets.ModelViewSet):
#     queryset = TimeTable.objects.all()
#     serializer_class = TimetableAttendanceSerializer

#     def retrieve(self, request, pk):
#         timetable = TimeTable.objects.filter(date=pk)
#         serializer = self.serializer_class(timetable, many=True)
#         return Response({"date": serializer.data})
    
class FacultySalaryViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimetableAttendanceSerializer

    def retrieve(self, request, pk):
        timetable = TimeTable.objects.filter(faculty=pk)
        serializer = self.serializer_class(timetable, many=True)
        return Response({"date": serializer.data})
    
class FacultyAttendenceSubtopicBatchViewSet(viewsets.ModelViewSet):
    queryset = Subtopic_batch.objects.all()
    serializer_class = FacultyAttendenceSubtopicBatchSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view(('POST',))
def branchAdminSignup(request):
    print(request.data)
    try:
        branch = request.data['branch']
    except:
        branch = None

    try:
        mobile = request.data['mobile']
    except:
        mobile = None
    
    try:
        username = request.data['username']
    except:
        username = None
    
    try:
        email = request.data['email']
    except:
        email = None
    
    try:
        password = request.data['password']
    except:
        password = None

    if branch:
        try:
            user = User.objects.create_roleuser(email=email,password=password,mobile=mobile,username=username)
            print(user,"jjjj")
        except Exception as e:
            return Response({"message":str(e)})
        branch_ins = Branch.objects.get(id=branch[0])
        branch_ins.user.set([user])
        branch_ins.save()
        return Response({"message":"done"})

    else:
        return Response({"message":"Assign Branch"})


class TimeTableForBooked(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = Timetableserializers
    pagination_class = SinglePagination

    def get_queryset(self):
        queryset = TimeTable.objects.all()
        date = self.request.query_params.get('date')
        topic = self.request.query_params.get('topic_name')
        subtopic = self.request.query_params.get('subtopic')
        course = self.request.query_params.get('course_name')
        faculty = self.request.query_params.get('faculty_name')
        branch = self.request.query_params.get('branch_name')
        batch = self.request.query_params.get('batch_name')
        completed = self.request.query_params.get('completed')
        notcomplete = self.request.query_params.get('notcomplete')
        notassigned =self.request.query_params.get('notassigned')
        id =self.request.query_params.get('id')
        # facultyassigned =self.request.query_params.get('facultyassigned')
        if completed:
            queryset= queryset.filter(topic__status="F")
        if notcomplete:
            queryset = queryset.filter(faculty__isnull=False,topic__status="B")
        if notassigned:
            print("hello",len(queryset))

            queryset = queryset.filter(faculty__isnull=True)
            print("hello",len(queryset))
        # if facultyassigned:
        #     queryset = queryset.filter(topic__status='S',faculty__isnull=False)
        if date:
            queryset=queryset.filter(date__icontains=date)
        if topic:
            queryset=queryset.filter(topic__name__icontains=topic)
        if course:
            queryset=queryset.filter(course__name__icontains=course)
        if branch:
            queryset=queryset.filter(branch__name__icontains=branch)
        if batch:
            queryset=queryset.filter(batch__name__icontains=batch)
        if faculty:
            # user = queryset.values('faculty')
            fac = Faculty.objects.filter(name__icontains=faculty).values('user')

            queryset = queryset.filter(faculty__in=fac)
        if id:
            queryset=queryset.filter(id=id)



        return queryset.order_by('date')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
#             response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
#     'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
#     'photoverified': {'True': 'Yes', 'False': 'No'},
#     'resumeverified': {'True': 'Yes', 'False': 'No'},
#     'idverified': {'True': 'Yes', 'False': 'No'}
# })
            response = queryset_to_excel(queryset,['batch','branch','faculty','date'],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response
        if pdf_query:
            fields = ['date','batch__name','branch__name','faculty__username']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Name', 'Batch-Name')
                                    
                                for header in headers]
            modified_headers = [header.replace('Name', 'Branch-Name')
                                    
                                for header in modified_headers]
            modified_headers=['Date','Batch','Branch','UserName']
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Verifed Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp


        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        timetable = TimeTable.objects.filter(faculty=pk).order_by('date')
        serializer = self.serializer_class(timetable, many=True)
        return Response({"date": serializer.data})

# class CategoryCheckListView(generics.ListAPIView):
#     serializer_class = CategorySerializer

#     def get_queryset(self):
#         # Get all the non-empty levels
#         non_empty_levels = Level.objects.exclude(id='')

#         # Get the categories for the non-empty levels
#         categories = Category.objects.filter(level__in=non_empty_levels).distinct()

#         return categories
    
class CategoryCheckViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.filter(is_delete=False)
    serializer_class = LevelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        levels_with_courses = []
        for level in queryset:
            if level.course_set.filter(is_delete=False).exists():
                levels_with_courses.append(level)
        serializer = self.get_serializer(levels_with_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseCheckViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_delete=False)
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        courses_with_subjects = []
        for course in queryset:
            if course.subject_set.filter(is_delete=False).exists():
                courses_with_subjects.append(course)
        serializer = self.get_serializer(courses_with_subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubjectCheckViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(is_delete=False)
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        subjects_with_modules = []
        for subject in queryset:
            if subject.module_set.filter(is_delete=False).exists():
                subjects_with_modules.append(subject)
        serializer = self.get_serializer(subjects_with_modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CourseTopicExist(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('id')
        return Course.objects.annotate(num_topics=Count('subject__module__topic')).filter(level=course_id, num_topics__gt=0).exclude(active=False)  

class CategoryTopicExist(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.annotate(num_topics=Count('level__course__subject__module__topic')).filter(num_topics__gt=0).exclude(active=False)  

class SubjectTopicExist(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        subject_id = self.kwargs.get('id')

        return Subject.objects.annotate(num_topics=Count('module__topic')).filter(course=subject_id, num_topics__gt=0).exclude(active=False)  

class ModuleTopicExist(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    
    def get_queryset(self):
        module_id = self.kwargs.get('id')

        return Module.objects.annotate(num_topics=Count('topic')).filter(subject=module_id, num_topics__gt=0).exclude(active=False)  

class LevelTopicExist(viewsets.ModelViewSet):
    serializer_class = LevelSerializer
    
    def get_queryset(self):
        level_id = self.kwargs.get('id')
        return Level.objects.annotate(num_topics=Count('course__subject__module__topic')).filter(category=level_id, num_topics__gt=0).exclude(active=False)  

class HollidayForBatch(viewsets.ModelViewSet):
    serializer_class = Batchholidaysserializer

    def retrieve(self, request, pk):
        batch = Batch.objects.get(id=pk)
        ids = SpecialHoliday.objects.filter(Q(batches=batch)| Q(branches=batch.branch) | Q(levels=batch.course.course.level)).values('id')
        id = SpecialHoliday.objects.filter(Q(batches__isnull=True)| Q(branches__isnull=True) | Q(levels__isnull=True)).values('id')
        ik=[i['id'] for i in ids ]
        ip = [i['id'] for i in id]
        holidays = SpecialHoliday.objects.filter(id__in=ik+ip)
        serializer = self.serializer_class(holidays, many=True)
        return Response({"date": serializer.data})
    
    
# class CategoryIdTopicExist(viewsets.ModelViewSet):
#     serializer_class = CategorySerializer
    
#     def get_queryset(self):
#         category_id = self.kwargs.get('id')
#         return Level.objects.annotate(num_topics=Count('level__course__subject__module__topic')).filter(id=category_id, num_topics__gt=0)



class TimeTableMultipleDelete(viewsets.ModelViewSet):
    serializer_class = TimeTableUpdateSerializer
    queryset = TimeTable.objects.all()

    def create(self, request, *args, **kwargs):
        id = request.data['id']
        timetable =TimeTable.objects.filter(id__in=id)
        for timetable in timetable:
            # Get the related topic instance
            topic = timetable.topic
            timetable.faculty = None
            # Update the status of the topic instance
            topic.status = 'P'
            topic.save()
            timetable.delete()
            # Delete the timetable instance
            
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseViewSetNew(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    pagination_class = SinglePagination

    def get_queryset(self):
        
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        queryset = Course.objects.all()
        if search_query:
            queryset = queryset.filter(Q(level__category__name__icontains=search_query) |
                                       Q(level__name__icontains=search_query) |
                                       Q(batch_type__name__icontains=search_query) |
                                       Q(year__icontains=search_query) |
                                       Q(name__icontains=search_query)).distinct()
            
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level__name__icontains=level)
        
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(level__category__name__icontains=category)
        
        batch_type = self.request.query_params.get('batch_type', None)
        if batch_type:
            queryset = queryset.filter(batch_type__name__icontains=batch_type)
        
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year__icontains=year)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    
})
            return response





class TimeTableByDateOfBranch(viewsets.ModelViewSet):
    serializer_class =Timetableserializers
    def get_queryset(self):
        branch_id = self.request.query_params.get('id')
        date = self.request.query_params.get('date')
        return TimeTable.objects.filter(branch=branch_id,date=date)
    

class CombinedBatchPercentage(viewsets.ModelViewSet):
    serializer_class =TimetableCombinedPercentageSerializers

    def get_queryset(self):
        timetable_id = self.request.query_params.get('id')
        timetable = TimeTable.objects.get(id=timetable_id)
        ids = timetable.combined_batch.values('id')
        print(ids,"idsss",(timetable.combined_batch) )
        timetable_ids=TimeTable.objects.filter(date=timetable.date,batch__in=ids).values('id')
        print(timetable_ids,"ti")
        if timetable.is_combined:
            return TimeTable.objects.filter(branch = timetable.branch,date=timetable.date).exclude(id__in=timetable_ids).exclude(id=timetable_id)
        return TimeTable.objects.filter(branch = timetable.branch,date=timetable.date).exclude(id=timetable_id)
        
        
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add any additional context data here
        timetable_id = self.request.query_params.get('id')
        context['timetable'] = TimeTable.objects.get(id=timetable_id)
        return context

    def partial_update(self, request, *args, **kwargs):
        timetable1= TimeTable.objects.get(id=kwargs['pk'])
        timetable_id = self.request.query_params.get('id')
        timetable2= TimeTable.objects.get(id=timetable_id)
        print(timetable2.faculty!=None,"faculty",timetable2.faculty)
        # print(if( timetable1.faculty or timetable2.faculty),"jjjjjjjjjjjjjjjjjjj")
        if not (timetable1.faculty and timetable2.faculty):
            print("hellooooooo")
            timetable1.is_combined=True
            timetable1.combined_batch.set([timetable2.batch])
            timetable2.is_combined=True
            timetable2.combined_batch.set([timetable1.batch])
            timetable1.save() , timetable2.save()
        if (timetable1.faculty and timetable2.faculty):
            return Response({"message":"You Have to Choose One Faculty From Two"})
        if (timetable1.faculty!= None):
            print("hhhhhhh1234")
            faculty=timetable1.faculty
            faculty= timetable1.faculty if timetable1.faculty else timetable2.faculty
            print(faculty,"faculty")
            timetable2.faculty = faculty 
            timetable1.faculty = faculty 
            timetable1.is_combined=True
            timetable1.combined_batch.set([timetable2.batch])
            timetable2.is_combined=True
            timetable2.combined_batch.set([timetable1.batch])
            timetable1.save() , timetable2.save()   
        if timetable2.faculty !=None:
            print('shamil')
            faculty=timetable2.faculty
            timetable2.faculty = faculty 
            timetable1.faculty = faculty 
            timetable1.is_combined=True
            timetable1.combined_batch.set([timetable2.batch])
            timetable2.is_combined=True
            timetable2.combined_batch.set([timetable1.batch])
            timetable1.save() , timetable2.save()

        else:
            print("here")




        return Response({"message":"Success"}) 




class BatchTopicOrderChange(viewsets.ModelViewSet):
    serializer_class = BatchTopicSerializer
    permission_classes =[AdminAndRolePermission]
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create','list']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Course"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Course"
            print(self.request.data,"dadadd")
            self.feature = "Order_change"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()

    def get_queryset(self):
        course_id = self.request.query_params.get('id')
        subject = Subject_batch.objects.filter(course=course_id).values('id')
        module =Module_batch.objects.filter(subject__in=subject).values('id')
        topics =Topic_batch.objects.filter(module__in=module,order__isnull=True)
        highest_order = Topic_batch.objects.filter(module__in=module).aggregate(
            models.Max('order')
        )['order__max']
        if len(topics) != 0:
            if highest_order == None:
                highest_order = 0
            for topic in topics:
                topic.order = highest_order + 1
                highest_order += 1
                topic.save()
        topics =Topic_batch.objects.filter(module__in=module).order_by('order')
        return topics
    

    def partial_update(self, request, *args, **kwargs):
        for i in range(0, len(request.data)):
            Topic_batch.objects.filter(id=request.data[i]['id_obj']).update(order=i)
        return Response({"done": "ok"})
    
    def update(self, request, pk):

        try:
            topic_id = int(request.data['topic'])
            new_order = int(request.data['order'])
        except (KeyError, ValueError):
            return Response({"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

        course = Course_batch.objects.get(id=pk)
        subject = Subject_batch.objects.filter(course=course)
        module = Module_batch.objects.filter(subject__in=subject)
        topc_tochange = Topic_batch.objects.get(id=topic_id)

        # if new_order == topc_tochange.order:
        #     return Response({"message": "Topic order already set to the requested value"})
        print(topc_tochange.name , topc_tochange.order,new_order,"ABhis")
        with transaction.atomic():
            if new_order <= topc_tochange.order:
                print("great")
                new_order-=1
                topics_to_update = Topic_batch.objects.filter(
                    module__in=module,
                    order__lt=topc_tochange.order,
                    order__gte=new_order,
                ).exclude(id=topic_id).order_by('-order')

                for topic in topics_to_update:
                    topic.order += 1
                    topic.save()

            elif new_order > topc_tochange.order:
                print("less")
                new_order-=1
                topics_to_update = Topic_batch.objects.filter(
                    module__in=module, 
                    order__gt=topc_tochange.order,
                    order__lte=new_order,
                ).exclude(id=topic_id).order_by('order')

                for topic in topics_to_update:
                    topic.order -= 1
                    topic.save()

            topc_tochange.order = new_order
            topc_tochange.save()

        return Response({"message": "Topic order updated successfully"})
        

import pandas as pd

class CourseExcelAdd(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def create(self, request, *args, **kwargs):
        print("hello")
        file = request.FILES['excel']  # Assuming the file is uploaded using the 'file' field in the request
        df = pd.read_excel(file)  # Read the Excel file using pandas
    
        for _, row in df.iterrows():
            print(row,"rowww")
            batch_type, _ = BatchType.objects.get_or_create(name=row.batchtype)
            category, _ =Category.objects.get_or_create(name=row.Category)
            level, _ = Level.objects.get_or_create(name=row.Level,category=category)
            course, _ = Course.objects.get_or_create(name=row.Course, year=row.year, batch_type=batch_type,level=level)
            subject, _ = Subject.objects.get_or_create(name=row.Subject, course=course)
            module, _ = Module.objects.get_or_create(name=row.Module, subject=subject)
            topic, _ = Topic.objects.get_or_create(name=row.Topic, module=module)
            subtopic, _ = SubTopic.objects.get_or_create(name=row.Subtopic, topic=topic,time_needed=row.Time)

        return Response({"ok": "Ok"})
    

@api_view(['GET'])
def deletebugfix(request):
    non_unique_timetables = TimeTable.objects.values('batch', 'date').annotate(count=Count('id')).filter(count__gt=1)

    if non_unique_timetables:
        for timetable in non_unique_timetables:
            TimeTable.objects.filter(batch=timetable['batch'], date=timetable['date']).delete()

        return JsonResponse({'message': 'Non-unique rows deleted successfully.'})
    else:
        return JsonResponse({'message': 'No non-unique rows found.'})
    
@api_view(['GET'])
def deletebugfix2(request):
    non_unique_timetables = TimeTable.objects.values('batch', 'date').annotate(count=Count('id')).filter(count__gt=1)

    if non_unique_timetables:
        for timetable in non_unique_timetables:
            TimeTable.objects.filter(batch=timetable['batch'], date=timetable['date'],is_delete=True).delete()

        return JsonResponse({'message': 'Non-unique rows deleted successfully.'})
    else:
        return JsonResponse({'message': 'No non-unique rows found.'})
    

class BranchCourseList(viewsets.ModelViewSet):
    serializer_class = CourseBranchSerilizer

    def get_queryset(self):
        queryset = Course_branch.objects.filter(branch__user__id=AuthHandlerIns.get_id(request=self.request))
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        queryset = Course_branch.objects.filter(id=kwargs['pk'])
        serializer = CourseBranchNewDragSerializer(queryset, many= True)
        return Response ({"data":serializer.data})
        # return super().retrieve(request, *args, **kwargs)
    

class BranchCourseListByLevel(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseBranchSerilizer

    def get_queryset(self):

        queryset = Course_branch.objects.filter(branch__user__id=AuthHandlerIns.get_id(request=self.request))
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        queryset = Course_branch.objects.filter(branch__user__id=AuthHandlerIns.get_id(request=self.request),course__level__id=kwargs['pk'])
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


class BranchCourseListByCategory(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseBranchSerilizer

    def get_queryset(self):

        queryset = Course_branch.objects.filter(branch__user__id=AuthHandlerIns.get_id(request=self.request))
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        queryset = Course_branch.objects.filter(branch__user__id=AuthHandlerIns.get_id(request=self.request),course__level__category__id=kwargs['pk'])
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class SubtopicBatchViewset(viewsets.ModelViewSet):
    serializer_class = Subtopic_batchSerializer
    queryset = Subtopic_batch.objects.all()

class OrderChangeBranch(viewsets.ModelViewSet):
    serializer_class= BranchSerializer
    queryset = Branch.objects.all()

    def partial_update(self, request, *args, **kwargs):
        course_id = request.query_params.get('c')
        subject_id = request.query_params.get('s')
        module_id = request.query_params.get('m')
        topic_id = request.query_params.get('t')
        if course_id:
            if subject_id:
                if module_id:
                    if topic_id:
                        for i in range(0, len(request.data)):
                            Subtopic_branch.objects.filter(
                                id=request.data[i]['id_obj']).update(priority=i)

                    else:
                        for i in range(0, len(request.data)):
                            Topic_branch.objects.filter(
                                id=request.data[i]['id_obj']).update(priority=i)
                        pass
                else:
                    for i in range(0, len(request.data)):
                        Module_branch.objects.filter(
                            id=request.data[i]['id_obj']).update(priority=i)
                    pass
            else:
                # subject = Subject.objects.filter(course=course_id).values()
                for i in range(0, len(request.data)):
                    Subject_branch.objects.filter(
                        id=request.data[i]['id_obj']).update(priority=i)

        else:
            pass
        return Response(status=status.HTTP_200_OK) 
    



class BranchTopicOrderChange(viewsets.ModelViewSet):
    serializer_class = BranchTopicSerializer
    permission_classes = [AdminAndRolePermission]

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create','list']:
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Course"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Course"
            print(self.request.data,"dadadd")
            self.feature = "Order_change"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()

    def get_queryset(self):
        course_id = self.request.query_params.get('id')
        subject = Subject_branch.objects.filter(course=course_id).values('id')
        module =Module_branch.objects.filter(subject__in=subject).values('id')
        topics =Topic_branch.objects.filter(module__in=module,order__isnull=True)
        highest_order = Topic_branch.objects.filter(module__in=module).aggregate(
            models.Max('order')
        )['order__max']
        if len(topics) != 0:
            if highest_order == None:
                highest_order = 0
            for topic in topics:
                topic.order = highest_order + 1
                highest_order += 1
                topic.save()
        topics =Topic_branch.objects.filter(module__in=module).order_by('order')
        return topics
    

    def partial_update(self, request, *args, **kwargs):
        # if not AuthHandlerIns.is_staff(request):
        #     return Response({"message": "Only admin can change order"}, status=status.HTTP_401_UNAUTHORIZED)
        for i in range(0, len(request.data)):
            Topic_branch.objects.filter(id=request.data[i]['id_obj']).update(order=i)
        return Response({"done": "ok"})
    
    def update(self, request, pk):
        # if not AuthHandlerIns.is_staff(request):
        #     return Response({"message": "Only admin can change order"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            topic_id = int(request.data['topic'])
            new_order = int(request.data['order'])
        except (KeyError, ValueError):
            return Response({"message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

        course = Course_branch.objects.get(id=pk)
        subject = Subject_branch.objects.filter(course=course)
        module = Module_branch.objects.filter(subject__in=subject)
        topc_tochange = Topic_branch.objects.get(id=topic_id)

        # if new_order == topc_tochange.order:
        #     return Response({"message": "Topic order already set to the requested value"})
        print(topc_tochange.name , topc_tochange.order,new_order,"ABhis")
        with transaction.atomic():
            if new_order <= topc_tochange.order:
                print("great")
                new_order-=1
                topics_to_update = Topic_branch.objects.filter(
                    module__in=module,
                    order__lt=topc_tochange.order,
                    order__gte=new_order,
                ).exclude(id=topic_id).order_by('-order')

                for topic in topics_to_update:
                    topic.order += 1
                    topic.save()

            elif new_order > topc_tochange.order:
                print("less")
                new_order-=1
                topics_to_update = Topic_branch.objects.filter(
                    module__in=module, 
                    order__gt=topc_tochange.order,
                    order__lte=new_order,
                ).exclude(id=topic_id).order_by('order')

                for topic in topics_to_update:
                    topic.order -= 1
                    topic.save()

            topc_tochange.order = new_order
            topc_tochange.save()

        return Response({"message": "Topic order updated successfully"})
        
class ReviewListOfStudentBasedFaculty(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        faculty_id = self.request.query_params.get('faculty_id', None)
        queryset = Review.objects.filter(user_id=user_id, review_on__faculty_id=faculty_id)
        return queryset

class OnlineCategoryVIewset(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = OnlineCategorySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            'data': serializer.data
        }
        return Response(data)


class OnlineLevelVIewset(viewsets.ReadOnlyModelViewSet):
    queryset = Level.objects.all()
    serializer_class = OnlineLevelSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = Level.objects.filter(category=kwargs['pk'])
        serializer = OnlineLevelSerializer(queryset, many=True)
        return Response({"data":serializer.data}) 
    
class OnlineCourseVIewset(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_online=True)
    serializer_class = CourseOnlineSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = Course.objects.filter(level=kwargs['pk'],is_online=True)
        serializer = CourseOnlineSerializer(queryset, many=True)
        return Response({"data":serializer.data}) 

class RatingQuestionsByChoice(viewsets.ModelViewSet):
    queryset = ReviewQuestions.objects.all()
    serializer_class = ReviewQuestionsSerializer

    
    
    def get_queryset(self):
        choice = self.request.query_params.get('choice')
        print(choice)
        queryset = self.queryset.filter(choice=choice)
        return queryset

class TimeTableModelViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AdminAndRoleOrFacultyPermission]
    serializer_class=Timetableserializersnew
    pagination_class = SinglePagination

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Add custom value to the context
        context['request'] = self.request
        faculty_course= FacultyCourseAddition.objects.filter(user=AuthHandlerIns.get_id(request=self.request),status="approved").values('topic')
        a = False
        s= Topic_branch.objects.filter(topic__in=faculty_course).values('id')
        user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
        q = (
                FacultyLimitaion.objects
                .filter(faculty=user)
                .order_by('-is_admin', 'branch_id')
                .distinct()
            )
        fac_limit = q.all()
        bid=[]
        print(fac_limit,"faccccccccccccccccccc",user.id)
        for i in fac_limit:
            print("hellooooo")
            end_date = datetime.datetime.now().date()
            # end_date = datetime.now().date()  # Current date
            start_date = end_date - timedelta(days=i.current_count)
            print(start_date,end_date,"dateeeeeeeeeeeeeeeeeeeeeeeee")
            time = TimeTable.objects.filter(faculty__id=AuthHandlerIns.get_id(request=self.request),branch__id=i.branch.id,date__range=(start_date,end_date)).values('date')
            print(time,"timeeeeeeeeeeeeeeeeeeeee",len(time))
            if len(time) >= i.max_class:
                bid.append(i.branch.id)
        user_id=AuthHandlerIns.get_id(request=self.request)
        faculty_course= Topic_batch.objects.filter(topic__in=s).values('id')
        app = Approvals.objects.filter(faculty__id=user_id).values('timetable')
        context['available'] = TimeTable.objects.filter(topic__in=faculty_course,faculty__isnull=True).order_by('date').exclude(date__lte=datetime.date.today()).exclude(id__in=app).exclude(branch__id__in=bid).values_list('id',flat=True)
        context['approvals'] = TimeTable.objects.filter(id__in=app).order_by('date').exclude(date__lte=datetime.date.today()).exclude(faculty__id=user_id).values_list('id',flat=True)
        context['history'] = TimeTable.objects.filter(topic__status="F",faculty__id=AuthHandlerIns.get_id(request=self.request)).order_by('-date').values_list('id',flat=True)
        context['booked'] = TimeTable.objects.filter(faculty=user_id).order_by('date').exclude(date__lte=timezone.now().date() - timedelta(days=1)).values_list('id',flat=True)
        return context
    
    def get_queryset(self):
        if AuthHandlerIns.is_faculty(self.request):
            faculty_course= FacultyCourseAddition.objects.filter(user=AuthHandlerIns.get_id(request=self.request),status="approved").values('topic')
            a = False
            s= Topic_branch.objects.filter(topic__in=faculty_course).values('id')
            user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
            q = (
                    FacultyLimitaion.objects
                    .filter(faculty=user)
                    .order_by('-is_admin', 'branch_id')
                    .distinct()
                )
            fac_limit = q.all()
            bid=[]
            print(fac_limit,"faccccccccccccccccccc",user.id)
            for i in fac_limit:
                print("hellooooo")
                end_date = datetime.datetime.now().date()
                # end_date = datetime.now().date()  # Current date
                start_date = end_date - timedelta(days=i.current_count)
                print(start_date,end_date,"dateeeeeeeeeeeeeeeeeeeeeeeee")
                time = TimeTable.objects.filter(faculty__id=AuthHandlerIns.get_id(request=self.request),branch__id=i.branch.id,date__range=(start_date,end_date)).values('date')
                print(time,"timeeeeeeeeeeeeeeeeeeeee",len(time))
                if len(time) >= i.max_class:
                    bid.append(i.branch.id)

            faculty_course= Topic_batch.objects.filter(topic__in=s).values('id')
            approve = self.request.query_params.get('applied', None)
            availabe = self.request.query_params.get('available', None)
            history = self.request.query_params.get('history', None)
            booked = self.request.query_params.get('booked', None)
            user_id=AuthHandlerIns.get_id(request=self.request)
            app = Approvals.objects.filter(faculty__id=user_id).values('timetable')
            month = self.request.query_params.get('month', None)
            year = self.request.query_params.get('year', None)
            start_date_filter = self.request.query_params.get('start', None)
            end_date_filter = self.request.query_params.get('end', None)
            search = self.request.query_params.get('search', None)
            if approve:
                print(app,"available")
                queryset = TimeTable.objects.filter(id__in=app).order_by('date').exclude(date__lte=datetime.date.today()).exclude(faculty__id=user_id)
            elif availabe:
                print(app,"available")
                queryset = TimeTable.objects.filter(topic__in=faculty_course,faculty__isnull=True).order_by('date').exclude(date__lte=datetime.date.today()).exclude(id__in=app).exclude(branch__id__in=bid)
            # q = TimeTable.objects.filter(faculty__isnull=True)
            elif history:
                 queryset = TimeTable.objects.filter(topic__status="F",faculty__id=AuthHandlerIns.get_id(request=self.request)).order_by('-date')

            elif booked:
                 queryset = TimeTable.objects.filter(faculty=user_id).order_by('date').exclude(date__lte=timezone.now().date() - timedelta(days=1))


            else:
                queryset = TimeTable.objects.filter(topic__in=faculty_course,faculty__isnull=True).order_by('date').exclude(date__lte=datetime.date.today())
            date = self.request.query_params.get('date', None)
            if date:
                print("HELLO",date, type(date),date.split(','))
                date=date.split(',')
                queryset = queryset.filter(date__in=[date] if not type(date)==list else date)

            branch = self.request.query_params.get('branch', None)
            if branch:
                queryset = queryset.filter(branch__name__icontains=branch)
            batch = self.request.query_params.get('batch', None)
            if batch:
                queryset = queryset.filter(batch__name__icontains=batch)
            course = self.request.query_params.get('course', None)
            if course:
                queryset = queryset.filter(course__name__icontains=course)
            topic = self.request.query_params.get('topic', None)
            if topic:
                queryset = queryset.filter(topic__name__icontains=topic)
            faculty = self.request.query_params.get('faculty', None)
            if faculty:
                queryset = queryset.filter(faculty__username__icontains=faculty)   
            subtopic = self.request.query_params.get('subtopic', None)
            if subtopic:
                topic=Subtopic_batch.objects.filter(name__icontains=subtopic).values('topic')
                queryset = queryset.filter(topic__in=topic)   
            id = self.request.query_params.get('id', None)
            if id:
                queryset = queryset.filter(pk__icontains=id)
            if year and month:
                queryset=queryset.filter(date__year=year,date__month=month)
            if start_date_filter and end_date_filter:
                queryset=queryset.filter(date__range=(start_date_filter, end_date_filter))
            if search:
                topic=Subtopic_batch.objects.filter(name__icontains=search).values('topic')
                queryset=queryset.filter(Q(branch__name__icontains=search)|Q(batch__name__icontains=search)|Q(course__name__icontains=search)|Q(topic__name__icontains=search)|Q(topic__in=topic))
            return queryset
        elif AuthHandlerIns.is_staff(request=self.request):
            queryset = TimeTable.objects.filter().order_by('-date').exclude(date__lte=datetime.date.today())
            date = self.request.query_params.get('date', None)
            if date:
                print("HELLO",date, type(date),date.split(','))
                date=date.split(',')
                queryset = queryset.filter(date__in=[date] if not type(date)==list else date)

            branch = self.request.query_params.get('branch', None)
            if branch:
                queryset = queryset.filter(branch__name__icontains=branch)
            batch = self.request.query_params.get('batch', None)
            if batch:
                queryset = queryset.filter(batch__name__icontains=batch)
            course = self.request.query_params.get('course', None)
            if course:
                queryset = queryset.filter(course__name__icontains=course)
            topic = self.request.query_params.get('topic', None)
            if topic:
                queryset = queryset.filter(topic__name__icontains=topic)
            faculty = self.request.query_params.get('faculty', None)
            if faculty:
                queryset = queryset.filter(faculty__username__icontains=faculty)   
            subtopic = self.request.query_params.get('subtopic', None)
            if subtopic:
                topic=Subtopic_batch.objects.filter(name__icontains=subtopic).values('topic')
                queryset = queryset.filter(topic__in=topic)   
            id = self.request.query_params.get('id', None)
            if id:
                queryset = queryset.filter(pk__icontains=id) 
            if year and date:
                queryset=queryset.filter(date__year=year,date__month=month)  
            return queryset
        



        
class facultyCategorylist(viewsets.ReadOnlyModelViewSet):
    serializer_class =CategorySerializer
    queryset = Category.objects.all().exclude(active=False)

class facultyCourseCategorylist(viewsets.ReadOnlyModelViewSet):
    serializer_class =LevelSerializer
    queryset = Level.objects.all().exclude(active=False)    

class facultyCourselist(viewsets.ReadOnlyModelViewSet):
    serializer_class =CourseSerializer
    queryset = Course.objects.all().exclude(active=False)     

class facultySubjectlist(viewsets.ReadOnlyModelViewSet):
    serializer_class =SubjectSerializer
    queryset = Subject.objects.all().exclude(active=False)  

class facultyModulelist(viewsets.ReadOnlyModelViewSet):
    serializer_class =ModuleSerializer
    queryset = Module.objects.all().exclude(active=False)  

class facultyTopiclist(viewsets.ReadOnlyModelViewSet):
    serializer_class =TopicSerializer
    queryset = Topic.objects.all().exclude(active=False)    
        


class MaterialNewCoureselist(viewsets.ReadOnlyModelViewSet):
    serializer_class =CourseNewMaterialSerializer
    queryset = Course.objects.all()
    def get_queryset(self):

        ##### Not Working #############
        faculty = self.request.query_params.get('faculty',None)
        course = self.request.query_params.get('course',None)
        print(faculty,course)
        cou = Course.objects.filter(id=course)
        fac= FacultyCourseAddition.objects.filter(course=course,user__id=faculty).values('course','subject','module','topic')
        fd={

        }
        cous=[]
        subj=[]
        modl=[]
        topi=[]
        for i in fac:
            print(i['course'])
            cous.append(i['course'])
            subj.append(i['subject'])
            modl.append(i['module'])
            topi.append(i['topic'])


        fd={
            "course":cous,
            "subject":subj,
            "module":modl,
            "topic":topi

        }
        # print(fd,"kkkkkkkkkk")
        # return
        ser=CourseNewMaterialSerializer(cou ,many=True,context={"fac":fd})
        return Response({"data":ser.data}) 
        return super().get_queryset()
    

@api_view(['GET'])
def getallNewMaterial(request):

    if AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_role(request=request):
        if AuthHandlerIns.is_role(request=request):
            s=AuthHandlerIns.is_role(request=request)
            l=AuthHandlerIns.get_id(request=request)
            print(l,'pppp')
            print(s,'kkk')
            print("PPPP")
            role = Role.objects.get(user=AuthHandlerIns.get_id(request=request))
            print(role,'ssss')
            r = role.permissions.permissions
            # print(r,' rrrr')
            print(r["Material"]["list"],'ppp')
            if not r["Material"]["list"]:
                return Response({"message":"you dont have permission to view the data"})
        faculty = request.query_params.get('faculty',None)
        course = request.query_params.get('course',None)
        print(faculty,course)
        cou = Course.objects.filter(id=course)
        fac= FacultyCourseAddition.objects.filter(course=course,user__id=faculty,status="approved").values('course','subject','module','topic')
        fd={

        }
        cous=[]
        subj=[]
        modl=[]
        topi=[]
        for i in fac:
            print(i['course'])
            cous.append(i['course'])
            subj.append(i['subject'])
            modl.append(i['module'])
            topi.append(i['topic'])


        fd={
            "course":cous,
            "subject":subj,
            "module":modl,
            "topic":topi

        }
        # print(fd,"kkkkkkkkkk")
        # return
        ser=CourseNewMaterialAdminSerializer(cou ,many=True,context={"fac":fd})
        return Response({"data":ser.data}) 

    faculty = request.query_params.get('faculty',None)
    course = request.query_params.get('course',None)
    print(faculty,course)
    cou = Course.objects.filter(id=course)
    fac= FacultyCourseAddition.objects.filter(course=course,user__id=faculty,status="approved").values('course','subject','module','topic')
    fd={

    }
    cous=[]
    subj=[]
    modl=[]
    topi=[]
    for i in fac:
        print(i['course'])
        cous.append(i['course'])
        subj.append(i['subject'])
        modl.append(i['module'])
        topi.append(i['topic'])


    fd={
        "course":cous,
        "subject":subj,
        "module":modl,
        "topic":topi

    }
    # print(fd,"kkkkkkkkkk")
    # return
    ser=CourseNewMaterialSerializer(cou ,many=True,context={"fac":fd})
    return Response({"data":ser.data}) 


class BatchModelVieset(viewsets.ReadOnlyModelViewSet):
    pagination_class= SinglePagination
    serializer_class = BatchSerializer

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create','list']:
            pdf_query = self.request.query_params.get('pdf', None)
            excel_query = self.request.query_params.get('excel', None)
            if pdf_query or excel_query:
                self.feature='PDF'
            else:
                self.feature = self.action
            self.permission = "Batch"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Batch"
            self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    

    def get_queryset(self):
        name = self.request.query_params.get('name')
        branch = self.request.query_params.get('Branch_name')
        course = self.request.query_params.get('course_name')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if AuthHandlerIns.is_role(self.request):
            branchs = Branch.objects.filter(user=AuthHandlerIns.get_id(request=self.request)).values('id')

            queryset = Batch.objects.filter(branch__in=[i['id'] for i in branchs])
       
            # serializer = BatchSerializer(batch, many=True)
            # return Response(serializer.data)
        elif AuthHandlerIns.is_staff(self.request):

            queryset = Batch.objects.all()
    
        if name:
            queryset= queryset.filter(name__icontains=name)
        if branch:
            queryset = queryset.filter(branch__name__icontains=branch)
        if course:
            queryset = queryset.filter(course__name__icontains=course)
        if start_date:
            queryset = queryset.filter(start_date__icontains=start_date)
        if end_date:
            queryset = queryset.filter(end_date__icontains=end_date)
        return queryset.order_by('-created_at')
        serializer = BatchSerializer(sub_topic, many=True)
        return Response(serializer.data)
        return super().get_queryset()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
  
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                            'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
                            'photoverified': {'True': 'Yes', 'False': 'No'},
                            'resumeverified': {'True': 'Yes', 'False': 'No'},
                            'idverified': {'True': 'Yes', 'False': 'No'}
                        })
            return response
        if pdf_query:
            fields = ['name', 'course__name', 'branch__name', 'start_date', 'end_date']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []
            modified_headers.append(headers[0].replace('Name', 'Name'))
            modified_headers.append(headers[1].replace('Name', 'Course Name'))
            modified_headers.append(headers[2].replace('Name', 'Branch Name'))
            modified_headers.append(headers[3].replace('Start_date', 'Start date'))
            modified_headers.append(headers[4].replace('End_date', 'End Name'))
            print(modified_headers, 'modified headers')
               
            nameheading = 'Batch'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class FacultyLimitaionModelViewset(viewsets.ModelViewSet):
    queryset = FacultyLimitaion.objects.all()
    serializer_class = FacultyLimitaionSerializer
    def get_permissions(self):
        self.permission_classes = [AdminAndRolePermission]
        return super().get_permissions()

    
    def get_queryset(self):
        queryset = FacultyLimitaion.objects.all()
        if AuthHandlerIns.is_staff(request=self.request):
            return queryset
        elif AuthHandlerIns.is_role(request=self.request):
            user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
            branch = Branch.objects.filter(user=user).values('id')
            queryset=queryset.filter(branch__in=branch)
            return queryset

        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            branch = Branch.objects.filter(id__in=request.data['branch_list'])
            fac= User.objects.get(id=request.data['faculty'])
            created_by= User.objects.get(id=AuthHandlerIns.get_id(request=request))
            for i in branch:
                fac_lim = FacultyLimitaion.objects.create(faculty=fac,created_by=created_by,max_class=request.data['max_class'],current_count=request.data['current_count'],is_admin=AuthHandlerIns.is_staff(request=request),branch=i)
        

            return Response(status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        queryset = FacultyLimitaion.objects.filter(faculty__id=kwargs['pk'])
        if AuthHandlerIns.is_staff(request=self.request):
            serializer = FacultyLimitaionSerializer(queryset, many=True)
    
            return Response(serializer.data)
        elif AuthHandlerIns.is_role(request=self.request):
            user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
            branch = Branch.objects.filter(user=user).values('id')
            queryset=queryset.filter(branch__in=branch)

            
            serializer = FacultyLimitaionSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class ReviewAnswersViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        review_on = self.request.query_params.get('review_on')

        counts = {
            'answer1': {},
            'answer2': {},
            'answer3': {},
            'answer4': {},
            'answer5': {},
        }

        # Count "YES" values
        yes_counts = self.queryset.filter(review_on=review_on, answer1='YES').values('answer1').annotate(count=Count('answer1'))
        counts['answer1']['YES'] = yes_counts[0]['count'] if yes_counts else 0

        # Count "NO" values
        no_counts = self.queryset.filter(review_on=review_on, answer1='NO').values('answer1').annotate(count=Count('answer1'))
        counts['answer1']['NO'] = no_counts[0]['count'] if no_counts else 0

        # Count null values
        null_counts = self.queryset.filter(review_on=review_on, answer2__isnull=True).values('answer1').annotate(count=Count('answer1'))
        counts['answer1'][None] = null_counts[0]['count'] if null_counts else 0

        
        # Count "YES" values

        yes_counts = self.queryset.filter(review_on=review_on, answer2='YES').values('answer2').annotate(count=Count('answer2'))
        counts['answer2']['YES'] = yes_counts[0]['count'] if yes_counts else 0

        # Count "NO" values
        no_counts = self.queryset.filter(review_on=review_on, answer2='NO').values('answer2').annotate(count=Count('answer2'))
        counts['answer2']['NO'] = no_counts[0]['count'] if no_counts else 0

        # Count null values
        null_counts = self.queryset.filter(review_on=review_on, answer2__isnull=True).values('answer2').annotate(count=Count('answer2'))
        counts['answer2'][None] = null_counts[0]['count'] if null_counts else 0

        
        # Count "YES" values

        yes_counts = self.queryset.filter(review_on=review_on, answer3='YES').values('answer3').annotate(count=Count('answer3'))
        counts['answer3']['YES'] = yes_counts[0]['count'] if yes_counts else 0

        # Count "NO" values
        no_counts = self.queryset.filter(review_on=review_on, answer3='NO').values('answer3').annotate(count=Count('answer3'))
        counts['answer3']['NO'] = no_counts[0]['count'] if no_counts else 0

        # Count null values
        null_counts = self.queryset.filter(review_on=review_on, answer3__isnull=True).values('answer3').annotate(count=Count('answer3'))
        counts['answer3'][None] = null_counts[0]['count'] if null_counts else 0


        # Count "YES" values

        yes_counts = self.queryset.filter(review_on=review_on, answer4='YES').values('answer4').annotate(count=Count('answer4'))
        counts['answer4']['YES'] = yes_counts[0]['count'] if yes_counts else 0

        # Count "NO" values
        no_counts = self.queryset.filter(review_on=review_on, answer4='NO').values('answer4').annotate(count=Count('answer4'))
        counts['answer4']['NO'] = no_counts[0]['count'] if no_counts else 0

        # Count null values
        null_counts = self.queryset.filter(review_on=review_on, answer4__isnull=True).values('answer4').annotate(count=Count('answer4'))
        counts['answer4'][None] = null_counts[0]['count'] if null_counts else 0




        yes_counts = self.queryset.filter(review_on=review_on, answer5='YES').values('answer5').annotate(count=Count('answer5'))
        counts['answer5']['YES'] = yes_counts[0]['count'] if yes_counts else 0

        # Count "NO" values
        no_counts = self.queryset.filter(review_on=review_on, answer5='NO').values('answer5').annotate(count=Count('answer5'))
        counts['answer5']['NO'] = no_counts[0]['count'] if no_counts else 0

        # Count null values
        null_counts = self.queryset.filter(review_on=review_on, answer5__isnull=True).values('answer5').annotate(count=Count('answer5'))
        counts['answer5'][None] = null_counts[0]['count'] if null_counts else 0

        # Repeat the above code for answer2, answer3, answer4, and answer5

        return Response((counts))
  

class ReviewAllTimeTableFacultyViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        if user_id is None:
            return Response({'error': 'user_id parameter is required.'}, status=400)

        timetables = TimeTable.objects.filter(faculty_id=user_id)
        result = {}

        for timetable in timetables:
            reviews = Review.objects.filter(review_on=timetable)

            counts = {
                'answer1': {
                    'YES': reviews.filter(answer1='YES').count(),
                    'NO': reviews.filter(answer1='NO').count(),
                },
                'answer2': {
                    'YES': reviews.filter(answer2='YES').count(),
                    'NO': reviews.filter(answer2='NO').count(),
                },
                'answer3': {
                    'YES': reviews.filter(answer3='YES').count(),
                    'NO': reviews.filter(answer3='NO').count(),
                },
                'answer4': {
                    'YES': reviews.filter(answer4='YES').count(),
                    'NO': reviews.filter(answer4='NO').count(),
                },
                'answer5': {
                    'YES': reviews.filter(answer5='YES').count(),
                    'NO': reviews.filter(answer5='NO').count(),
                },
            }

            timetable_info = [{
                'id': timetable.id,
                'date': timetable.date.strftime('%Y-%m-%d'),
                'branch': timetable.branch.name,
                'batch': timetable.batch.name,
                'topic': timetable.topic.name,
                'counts': counts,
            }]

            result[f'Timetable{timetable.id}'] = timetable_info


        return Response(result)
    

from django.db.models import Count, Case, When, Value, F, TextField

# class ReviewCountFacultyWiseViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     # permission_classes = [AdminOrFaculty]
#     pagination_class= CustomPagination

    
#     def get_queryset(self):
#             queryset = Review.objects.all()
#             self.faculty_id = self.request.query_params.get('user_id', None)
            
#             if self.faculty_id:
#                 queryset = queryset.filter(review_on__faculty_id=self.faculty_id)

#             return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
        
#         # Check if faculty_id is None and handle accordingly
#         if self.faculty_id is None:
#             timetables = TimeTable.objects.all().order_by('-date')
#         else:
#             timetables = TimeTable.objects.filter(faculty=self.faculty_id).order_by('-date')

#         response_data = []

#         for timetable in timetables:
#                 # Filter the reviews for each timetable
#                 faculty_name = timetable.faculty.id
#                 faculty = Faculty.objects.get(user_id=faculty_name)
#                 print(faculty.name,faculty.user)
#                 queryset = Review.objects.filter(review_on=timetable)
#                 subquery1 = ReviewQuestions.objects.filter(
#     choice=OuterRef('choice')
# ).values('question1')[:1]
#                 subquery2 = ReviewQuestions.objects.filter(
#     choice=OuterRef('choice')
# ).values('question2')[:1]
#                 subquery3 = ReviewQuestions.objects.filter(
#     choice=OuterRef('choice')
# ).values('question3')[:1]
#                 subquery4 = ReviewQuestions.objects.filter(
#     choice=OuterRef('choice')
# ).values('question4')[:1]
#                 subquery5 = ReviewQuestions.objects.filter(
#     choice=OuterRef('choice')
# ).values('question5')[:1]
#                 reviews = Review.objects.filter(review_on=timetable.id).order_by('review_on__date')

#                 # Create a list to store feedback and user pairs
#                 feedback_data = []

#                 for review in reviews:
#                     if review.feedback:
#                         # feedback_data.append([review.feedback,review.choice, review.user.username])
#                         feedback_obj = {
#                         'feedback': review.feedback,
#                         'rating': review.choice,
#                         'student_name': review.user.username
#                     }
#                     feedback_data.append(feedback_obj)

#                 # Perform the aggregation query for this timetable
#                 review_counts = queryset.values('choice').annotate(
#                     question1=Subquery(subquery1),
#                     answer1_yes_count=Count('id', filter=Q(answer1='YES')),
#                     answer1_no_count=Count('id', filter=Q(answer1='NO')),
#                     question2=Subquery(subquery2),

#                     answer2_yes_count=Count('id', filter=Q(answer2='YES')),
#                     answer2_no_count=Count('id', filter=Q(answer2='NO')),
#                     question3=Subquery(subquery3),

#                     answer3_yes_count=Count('id', filter=Q(answer3='YES')),
#                     answer3_no_count=Count('id', filter=Q(answer3='NO')),
#                     question4=Subquery(subquery4),

#                     answer4_yes_count=Count('id', filter=Q(answer4='YES')),
#                     answer4_no_count=Count('id', filter=Q(answer4='NO')),
#                     question5=Subquery(subquery5),

#                     answer5_yes_count=Count('id', filter=Q(answer5='YES')),
#                     answer5_no_count=Count('id', filter=Q(answer5='NO')),
                    
                    
                    
#                 )
                    

#                 # Prepare the response data for this timetable
#                 response_data.append({
#                     'timetable_id': timetable.id,
#                     'faculty': faculty.name,
#                     'date':timetable.date,
#                     'branch': timetable.branch.name,
#                     'batch': timetable.batch.name,
#                     'result': list(review_counts),
#                     # 'questions': ReviewQuestionsSerializer(review_questions, many=True).data,  # Serialize review questions
#                     'feedback': feedback_data,

#                 })

#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(response_data, request)
#         return paginator.get_paginated_response(page)



class ReviewCountFacultyWiseViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Review.objects.all()
        self.faculty_id = self.request.query_params.get('user_id', None)

        if self.faculty_id:
            queryset = queryset.filter(review_on__faculty_id=self.faculty_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Check if faculty_id is None and handle accordingly
        if self.faculty_id is None:
            # timetables = TimeTable.objects.all().order_by('-date')
            timetables = TimeTable.objects.filter(faculty__isnull=False).order_by('-date')

        else:
            timetables = TimeTable.objects.filter(faculty=self.faculty_id).order_by('-date')

        response_data = []
        
        for timetable in timetables:
            handle_exception = True
            # Filter the reviews for each timetable
            faculty_name = None
            try:
                faculty_name = timetable.faculty.id
                print(faculty_name)

                faculty = Faculty.objects.get(user_id=faculty_name)
                if not faculty:
                    handle_exception = False
                    continue
            except:
                pass
            #     print(faculty)
            # except Faculty.DoesNotExist:
            #     if handle_exception:
            #         error_message = f"Faculty information missing for timetable: {timetable.id,timetable.faculty.id}"
            #         return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
            # except AttributeError:
            #     if handle_exception:
            #         error_message = f"Faculty Information missing for timetable: {timetable.id}"
            #         return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

            queryset = Review.objects.filter(review_on=timetable)
            subquery1 = ReviewQuestions.objects.filter(
                choice=OuterRef('choice')
            ).values('question1')[:1]
            subquery2 = ReviewQuestions.objects.filter(
                choice=OuterRef('choice')
            ).values('question2')[:1]
            subquery3 = ReviewQuestions.objects.filter(
                choice=OuterRef('choice')
            ).values('question3')[:1]
            subquery4 = ReviewQuestions.objects.filter(
                choice=OuterRef('choice')
            ).values('question4')[:1]
            subquery5 = ReviewQuestions.objects.filter(
                choice=OuterRef('choice')
            ).values('question5')[:1]
            reviews = Review.objects.filter(review_on=timetable.id).order_by('review_on__date')

            # Create a list to store feedback and user pairs
            feedback_data = []

            for review in reviews:
                if review.feedback:
                    # feedback_data.append([review.feedback,review.choice, review.user.username])
                    feedback_obj = {
                        'feedback': review.feedback,
                        'rating': review.choice,
                        'student_name': review.user.username
                    }
                    feedback_data.append(feedback_obj)

            # Perform the aggregation query for this timetable
            review_counts = queryset.values('choice').annotate(
                question1=Subquery(subquery1),
                answer1_yes_count=Count('id', filter=Q(answer1='YES')),
                answer1_no_count=Count('id', filter=Q(answer1='NO')),
                question2=Subquery(subquery2),
                answer2_yes_count=Count('id', filter=Q(answer2='YES')),
                answer2_no_count=Count('id', filter=Q(answer2='NO')),
                question3=Subquery(subquery3),
                answer3_yes_count=Count('id', filter=Q(answer3='YES')),
                answer3_no_count=Count('id', filter=Q(answer3='NO')),
                question4=Subquery(subquery4),
                answer4_yes_count=Count('id', filter=Q(answer4='YES')),
                answer4_no_count=Count('id', filter=Q(answer4='NO')),
                question5=Subquery(subquery5),
                answer5_yes_count=Count('id', filter=Q(answer5='YES')),
                answer5_no_count=Count('id', filter=Q(answer5='NO')),
            )

            # Create a list to store the restructured result data
            result_data = []

            for result in review_counts:
                # Restructure the result data for each question
                question_data = {}
                for i in range(1, 6):  # Assuming you have 5 questions
                    question_key = f"question{i}"
                    question_value = result[question_key]
                    question_data[question_key] = {
                        f"answer{i}_yes_count": result[f"answer{i}_yes_count"],
                        f"answer{i}_no_count": result[f"answer{i}_no_count"],
                        "Question": question_value,  # Include the value here
                    }

                result_item = {
                    "choice": result["choice"],
                    **question_data,
                }

                result_data.append(result_item)

            # Prepare the response data for this timetable
            response_data.append({
                'timetable_id': timetable.id,
                'faculty': faculty.name,
                'date': timetable.date,
                'branch': timetable.branch.name,
                'batch': timetable.batch.name,
                'result': result_data,  # Use the restructured result_data
                'feedback': feedback_data,
            })

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(response_data, request)
        return paginator.get_paginated_response(page)
        

class BranchModelVieset(viewsets.ReadOnlyModelViewSet):
    pagination_class= SinglePagination
    serializer_class = BranchCreateSerializer
    

    def get_queryset(self):
        location = self.request.query_params.get('location')
        branchname = self.request.query_params.get('name')
        course = self.request.query_params.get('course')

        if AuthHandlerIns.is_role(self.request):
            branchs = Branch.objects.filter(user=AuthHandlerIns.get_id(request=self.request)).values('id')
            print(branchs,"branch")
            # queryset = Batch.objects.filter(branch__in=[i['id'] for i in branchs])
            # print(queryset,"firsts")
            # serializer = BatchSerializer(batch, many=True)
            # return Response(serializer.data)
        else:

            queryset = Branch.objects.all()
            print(queryset,'kkkk')

        if location:
            queryset= queryset.filter(location__icontains=location)
        if branchname:
            queryset = queryset.filter(name__icontains=branchname)
        if course:
            print("***********")
            print(queryset,'querysetqueryset')
            queryset = queryset.filter(id__in=Branch_courses.objects.filter(course__name__icontains=course))
            print(queryset.values(),'LLLL')
        print(queryset.values(),'LLL')
        return queryset.order_by('-created_at')
        serializer = BatchSerializer(sub_topic, many=True)
        return Response(serializer.data)
        return super().get_queryset()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
  
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                            'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
                            'photoverified': {'True': 'Yes', 'False': 'No'},
                            'resumeverified': {'True': 'Yes', 'False': 'No'},
                            'idverified': {'True': 'Yes', 'False': 'No'}
                        })
            return response
        if pdf_query:
            fields = ['name', 'location']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []
            modified_headers.append(headers[0].replace('name', 'Name'))
            modified_headers.append(headers[1].replace('location', 'Location'))

            print(modified_headers, 'modified headers')
               
            nameheading = 'Branch'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


class ApprovalModelviewset(viewsets.ModelViewSet):
    serializer_class = Approvalserializerspost
    queryset = Approvals.objects.all()
    permission_classes =[AdminOrFaculty]

    def destroy(self, request, *args, **kwargs):
        if AuthHandlerIns.is_faculty(request=request):
            app = Approvals.objects.filter(id=kwargs['pk'],faculty=AuthHandlerIns.get_id(request=request))
            if app:
                app.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return super().destroy(request, *args, **kwargs)
    

class BatchModelViesetpatch(viewsets.ModelViewSet):
    pagination_class= SinglePagination
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'create']:
            self.feature = self.action
            self.permission = "Batch"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['list']:
            self.feature = self.action
            self.permission = "Batch"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Batch"
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    

    def create(self, request, *args, **kwargs):
        try:
            branch = Branch.objects.get(id=request.data['branch'])
            course = Course_branch.objects.get(
                course=request.data['course'], branch=branch.pk)
            batchexist = Batch.objects.filter(name=request.data['name'])
            if batchexist.exists():
                return Response({"message": "Name Already Taken"}, status=status.HTTP_409_CONFLICT)
            is_account=User.objects.get(id=AuthHandlerIns.get_id(request=request)).is_account
            batch = Batch.objects.create(name=request.data['name'], start_date=request.data['start_date'], end_date=request.data['end_date'],is_account=is_account,
                                         course=course, strength=request.data['strength'],fees=request.data['fees'],installment_count=request.data['installment_count'],
                                         branch=branch, working_days=getchoicefromlist(request.data['working_days']), exam_days=getchoicefromlist(request.data['exam_days']))

            # serializer = BatchSerializer(data=batch)
            # serializer.is_valid(raise_exception=True)
            if request.data['autotime']:
                print(request.data['auto_start_date'], type(
                    request.data['auto_start_date']), "kklksalksa")
                # print(request.data['facultylist'][0]['user']['id'], "newwww")
                createautomaticTimetable(
                    batch.id, request.data['autofaculty'], request.data['auto_start_date'], request.data['auto_end_date'], request.data['facultylist'] if request.data['autofaculty'] else [])
            return Response({"message": "success","batch_name":batch.name,"id":batch.id,"fees":batch.fees}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    


class FacultyListMaterial(viewsets.ReadOnlyModelViewSet):
    serializer_class = facultyviewDetailsMaterial
    pagination_class = SinglePagination
            #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            self.permission = "Material"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
            is_verified=True, is_blocked=False, is_rejected=False).order_by('name')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query) |
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            # queryset = FacultyCourseAddition.objects.filter(category__name__icontains=category).order_by('  created_at')
            # queryset=FacultyCourseAddition.objects.filter(user__in=usersid,category__name__icontains=category).distinct('user')
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
      



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response
        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Verifed Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp


        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LevelListCreateViewsCopy(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
        #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Level"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Level"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Level"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermissionCopy, ]
        return super().get_permissions()


    def post(self, request, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "Only admin can create a Level"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)
    


class TopicCreateViewCopy(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

        #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Topic"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Topic"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Topic"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermissionCopy, ]
        return super().get_permissions()


class ModuleCreateViewCopy(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
        #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Topic"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Topic"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Topic"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermissionCopy, ]
        return super().get_permissions()




class MeterialVerifiedFacultylist(viewsets.ModelViewSet):
    serializer_class = facultyviewDetails
    pagination_class = SinglePagination
            #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Material"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Material"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Material"
            print(self.request.data,"dadadd")
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermissionCopy, ]
        return super().get_permissions()


    def get_queryset(self):
        queryset = Faculty.objects.filter(
            is_verified=True, is_blocked=False, is_rejected=False).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query) |
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            # queryset = FacultyCourseAddition.objects.filter(category__name__icontains=category).order_by('  created_at')
            # queryset=FacultyCourseAddition.objects.filter(user__in=usersid,category__name__icontains=category).distinct('user')
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
      



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        
        return queryset

from rest_framework import viewsets

class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all().order_by('date')
    serializer_class = Timetableserializers

    def create(self, request, *args, **kwargs):
        print("jjdksjdsj", request.data)
        if request.data['is_combined']:
            timetable = TimeTable.objects.filter(batch__in=request.data['combined_batch'], date=request.data['date'])
            faculty = timetable.values('faculty')
            print(faculty.exists(), "fac")
            for tt in timetable:
                tt.is_combined = True
                tt.combined_batch.set(request.data['combined_batch'] + [request.data['batch']])
                tt.save()
            if len(faculty.exclude(faculty=None)) > 0:
                request.data['faculty'] = timetable.exclude(faculty=None).first().faculty.pk
                return super().create(request, *args, **kwargs)
            return super().create(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if AuthHandlerIns.is_faculty(request):
            approve = self.request.query_params.get('approve', None)
            faculty_course = FacultyCourseAddition.objects.filter(user=AuthHandlerIns.get_id(request=request),
                                                                   status="approved").values('topic')
            print(faculty_course, "sss")
            a = False
            s = Topic_branch.objects.filter(topic__in=faculty_course).values('id')
            print(s, "sss")
            faculty_course = Topic_batch.objects.filter(topic__in=s).values('id')
            print(faculty_course, "fac")

            app = Approvals.objects.filter(user__id=AuthHandlerIns.get_id(request=request)).values('timetable')
            if approve:
                q = TimeTable.objects.filter(id__in=app).order_by('-date').exclude(date__lte=datetime.date.today(),
                                                                                    id__in=app)
            else:
                q = TimeTable.objects.filter(topic__in=faculty_course, faculty__isnull=True).order_by('-date').exclude(
                    date__lte=datetime.date.today(), id__in=app)
            print(q, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            t = Timetableserializersnew(
                q, many=True, context={'request': request})
            if a:
                return Response({"Time_Table": t.data})
            else:
                return Response({"Time_Table": t.data})

        if not AuthHandlerIns.is_staff(request):
            return Response({"message": "You don't have permission to view the data"},
                            status=status.HTTP_401_UNAUTHORIZED)

        return super().list(request, *args, **kwargs)
    

class FacultyHistoryPagination(PageNumberPagination):
    page_size = 8  # Adjust the page size according to your needs
    page_size_query_param = 'pagesize'
    max_page_size = 100

class FacultyHistoryViewSet(viewsets.ModelViewSet):
    pagination_class = SinglePagination
    # permission_classes = [AdminOrFaculty]
    serializer_class= FacultyHistorySerializer


    def list(self, request, *args, **kwargs):
        print("hiii")
        faculty_id = request.query_params.get('faculty_id')
        print(faculty_id)
        faculty_history = []
        ratings = Rating.objects.filter(rate_fac=faculty_id)
        if not ratings:
            average_rating = 0
        else:
            rating_sum = 0
            total_ratings = ratings.count()
            for rating_instance in ratings:
                rating_sum += rating_instance.choice
            average_rating = rating_sum / total_ratings

        queryset = Review.objects.all()
        if faculty_id:
            user_id = Faculty.objects.filter(id=faculty_id).first()
            print(user_id.user.id) 
            queryset = queryset.filter(review_on__faculty_id=user_id.user.id)

        # Perform the aggregation query
        review_counts = queryset.values('choice').annotate(
            answer1_yes_count=Count('id', filter=Q(answer1='YES')),
            answer1_no_count=Count('id', filter=Q(answer1='NO')),
            answer2_yes_count=Count('id', filter=Q(answer2='YES')),
            answer2_no_count=Count('id', filter=Q(answer2='NO')),
            answer3_yes_count=Count('id', filter=Q(answer3='YES')),
            answer3_no_count=Count('id', filter=Q(answer3='NO')),
            answer4_yes_count=Count('id', filter=Q(answer4='YES')),
            answer4_no_count=Count('id', filter=Q(answer4='NO')),
            answer5_yes_count=Count('id', filter=Q(answer5='YES')),
            answer5_no_count=Count('id', filter=Q(answer5='NO')),
            date=F('review_on__date'),  # Include the date field from TimeTable
            branch=F('review_on__branch__name'),
            batch=F('review_on__batch__name'),
        )

        

        attendances = FacultyAttendence.objects.filter(name=faculty_id)
        if not attendances:
            return Response({'error': 'No attendance records found for the specified faculty ID.'})

        total_amount = 0
        for attendance in attendances:
            timetable = attendance.timetable

            # Retrieve necessary details from the timetable instance
            date = timetable.date
            branch = timetable.branch.name
            batch = timetable.batch.name
            course = timetable.course.name
            level_id = timetable.course.course.course.level.id
            level = timetable.course.course.course.level.name
            topic = timetable.topic.name
            payment = attendance.payment_done
            time_from = attendance.start_time
            time_to = attendance.end_time
            hours = attendance.hours
            subtopics_covered = [
                str(subtopic) for subtopic in attendance.subtopics_covered.all()]

            payed_amnt = attendance.paid_amount
            total_amount = total_amount + payed_amnt
            payment_method = attendance.payment_method
            fixed_salary = Faculty_Salary.objects.filter(faculty=faculty_id, level=level_id)
            print(fixed_salary)
            faculty_fixed_salary = 0
            for salary in fixed_salary:
                faculty_fixed_salary = salary.fixed_salary

            fixed_sal = faculty_fixed_salary
            pending_salary = fixed_sal.salaryscale - payed_amnt
            if pending_salary <= 0:
                pending_salary = "Fully Paid"
            # Retrieve faculty name
            faculty_name = attendance.name.name

            # Store details for each attendance record
            faculty_history.append({
                'date': date,
                'time_from': time_from,
                'time_to': time_to,
                'hours': hours,
                # 'subtopics_covered': subtopics_covered,
                'branch': branch,
                'batch': batch,
                'level': level,
                'course': course,
                'topic': topic,
                'payment': payment,
                'paidamount': payed_amnt,
                'payment_method': payment_method,
                'faculty_name': faculty_name,
                'total_amount': total_amount,
                'fixed_salary': fixed_sal.salaryscale,
                'pending_salary': pending_salary,
                'average_rating': average_rating,
            })
        review_counts = {
            'average_rating': average_rating,
            'review_counts': list(review_counts),
        }
        
        # return Response(faculty_history)
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(faculty_history, request)
        serialized_data = self.serializer_class(paginated_data, many=True)
        response_data = {
            'results': serialized_data.data,
            'review&rating': review_counts
        }
        return paginator.get_paginated_response(response_data)


@api_view(['GET'])
def getcalender_batch(request, id,month,year):
    batch = Batch.objects.get(id=id)
    result_list = []
    num_days = calendar.monthrange(year, month)[1]  # Get the number of days in the month

    for day in range(1, num_days + 1):
        date = datetime.date(year, month, day)
        # date_object = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)")
        ids = SpecialHoliday.objects.filter(Q(batches=batch)| Q(branches=batch.branch) | Q(levels=batch.course.course.level),date=date).values('id')
        id = SpecialHoliday.objects.filter(Q(batches__isnull=True)| Q(branches__isnull=True) | Q(levels__isnull=True),date=date).values('id')
        ik=[i['id'] for i in ids ]
        ip = [i['id'] for i in id]
        holidays = SpecialHoliday.objects.filter(id__in=ik+ip,date=date)
        holiserializer = Batchholidaysserializer(holidays, many=True)
        
        try:
            time=TimeTable.objects.filter(date=date,batch=batch)
            if time.exists():
                ser=Timetableserializers(time,many=True,context={'request': request})
                result_list.append({"date":formatted_date,"obj":ser.data[0],"day":day,"dayName":date.strftime("%a"),"month": "07",
  "year": year,
  
  "holi": holiserializer.data[0] if len(holiserializer.data)>0 else {} })
            else:
                result_list.append({"date":formatted_date,"obj":{},"day":day,"dayName":date.strftime("%a"),"month": "07",
  "year": year,
  "holi": holiserializer.data[0] if len(holiserializer.data)>0 else {}})
        except Exception as e:
            print(e)
            result_list.append({"date":formatted_date,"obj":{},"day":day,"dayName":date.strftime("%a"),"month": "07",
  "year": year,
  "holi": holiserializer.data[0] if len(holiserializer.data)>0 else {}})

            
          # Append the object to the list along with the corresponding date

    return Response({"data":result_list})

    pass


class FacultyListQuestions(viewsets.ReadOnlyModelViewSet):
    serializer_class = facultyviewDetailsMaterial
    pagination_class = SinglePagination
            #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Faculty.objects.filter(
            is_verified=True, is_blocked=False, is_rejected=False).order_by('-joined_date')

        usersid = [x.user.pk for x in queryset]
        print(usersid,'userdid')
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(user__username__icontains=search_query) |
                                       Q(user__email__icontains=search_query) |
                                       Q(district__icontains=search_query) |
                                       Q(user__mobile__icontains=search_query) |
                                       Q(name__icontains=search_query)).distinct()

        category = self.request.query_params.get('category', None)
        if category:
            # queryset = FacultyCourseAddition.objects.filter(category__name__icontains=category).order_by('  created_at')
            # queryset=FacultyCourseAddition.objects.filter(user__in=usersid,category__name__icontains=category).distinct('user')
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, category__name__icontains=category).values('user')
      



        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, level__name__icontains=levels).values('user')

        course = self.request.query_params.get('course', None)
        if course:
            queryset = FacultyCourseAddition.objects.filter(Q(user__in=usersid, course__name__icontains=course)).values('user')

        subject_name = self.request.query_params.get('subject', None)
        if subject_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, subject__name__icontains=subject_name).values('user')

        module_name = self.request.query_params.get('module', None)
        if module_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, module__name__icontains=module_name).values('user')

        topic_name = self.request.query_params.get('topic', None)
        if topic_name:
            queryset = FacultyCourseAddition.objects.filter(user__in=usersid, topic__name__icontains=topic_name).values('user')

        if any([category, levels, course, subject_name, module_name, topic_name]):
            queryset = Faculty.objects.filter(user__in=queryset).distinct('id')
        #     queryset = queryset
        #     print(queryset.model,'************')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # Check if PDF download is requested
        pdf_query = self.request.query_params.get('pdf', None)
        excel_query = self.request.query_params.get('excel', None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
    'modeofclasschoice': {1: 'Offline', 2: 'Online', 3: 'Both'},
    'photoverified': {'True': 'Yes', 'False': 'No'},
    'resumeverified': {'True': 'Yes', 'False': 'No'},
    'idverified': {'True': 'Yes', 'False': 'No'}
})
            return response
        if pdf_query:
            fields = ['name', 'user__username', 'user__email', 'user__mobile', 'address', 'district', 'whatsapp_contact_number', 'qualification', 'modeofclasschoice']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []

            modified_headers = [header.replace('Whatsapp_c\nontact_number', 'Whatsapp Number')
                                    .replace('Modeofclas\nschoice', 'Mode of Class')
                                    .replace('Qualificat\nion', 'Qualification')
                                for header in headers]
            print(modified_headers, 'modified headers')
            for entry in data:
                mode_of_class_choice = entry[-1]
                if mode_of_class_choice == '1':
                    entry[-1] = 'Online'
                elif mode_of_class_choice == '2':
                    entry[-1] = 'Offline'
                elif mode_of_class_choice == '3':
                    entry[-1] = 'Both'           
            nameheading = 'Verifed Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'courselist.pdf')  
            return resp


        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TimeTableAttendanceViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimetableAttendanceSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create','list']:
            pdf_query = self.request.query_params.get('pdf', None)
            excel_query = self.request.query_params.get('excel', None)
            if pdf_query or excel_query:
                self.feature='PDF'
            else:
                self.feature = self.action
            self.permission = "Attendance"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Attendance"
            self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['retrieve']:
            print("TEst 12/12/23")
            self.permission = "Attendance"
            self.feature = "list"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    
    def get_queryset(self):
        if AuthHandlerIns.is_role(self.request):
            branches = Branch.objects.filter(user=AuthHandlerIns.get_id(request=self.request)).values('id')


            queryset = TimeTable.objects.filter(branch__in=branches)
            
        else:
            queryset = TimeTable.objects.filter()
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        if AuthHandlerIns.is_role(request):
            branches = Branch.objects.filter(user=AuthHandlerIns.get_id(request=request)).values('id')
            queryset = TimeTable.objects.filter(branch__in=branches, date=kwargs['pk'])
        else:
            queryset = TimeTable.objects.filter(date= kwargs['pk'])

        # instance = self.get_object(queryset)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)      


class SubTopicBatchViewsetDelete(viewsets.ModelViewSet):
    serializer_class=Subject_batchSerializer
    queryset=Subtopic_batch.objects.all()
    pagination_class=SinglePagination

    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = [AdminAndRolePermission, ]
        else:
            self.permission_classes = [NonePermission ]

        return super().get_permissions()


class ApprovalModelViewset(viewsets.ReadOnlyModelViewSet):
    queryset=Approvals.objects.all()
    pagination_class=SinglePagination
    permission_classes=[AdminAndRolePermission]
    serializer_class=ApprovalModelViewsetSerializer

    def get_queryset(self):
        queryset=Approvals.objects.all()
        queryset=queryset.filter(timetable__faculty__isnull=True)
        if AuthHandlerIns.is_staff(request=self.request):
            queryset=queryset.filter() 
        
        batch_name=self.request.query_params.get('batch_name', None)
        branch_name=self.request.query_params.get('branch_name', None)
        course_name=self.request.query_params.get('course_name', None)
        topic_name=self.request.query_params.get('topic_name', None)
        user_name=self.request.query_params.get('user_name', None)
        faculty_name=self.request.query_params.get('faculty_name', None)
        mobile=self.request.query_params.get('mobile', None)
        if batch_name:
            queryset=queryset.filter(timetable__batch__name__icontains=batch_name)
        if branch_name:
            queryset=queryset.filter(timetable__branch__name__icontains=branch_name)
        if course_name:
            queryset=queryset.filter(timetable__course__name__icontains=course_name)
        if topic_name:
            queryset=queryset.filter(timetable__topic__name__icontains=topic_name)
        if user_name:
            queryset=queryset.filter(timetable__faculty__username__icontains=user_name)
        if faculty_name:
            fac=Faculty.objects.filter(name__icontains=faculty_name).values_list('user__id',flat=True)
            queryset=queryset.filter(faculty__in=fac)
        if mobile:
            queryset=queryset.filter(faculty__mobile__startswith=mobile)

        return queryset
    
class LevelForSalaryViewset(viewsets.ReadOnlyModelViewSet):
    queryset=Level.objects.all()
    # pagination_class=SinglePagination
    permission_classes=[FacultyPermission]
    serializer_class=LevelSerializer

    def get_queryset(self):
        user=User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
        online=self.request.query_params.get('online', None)
        offline=self.request.query_params.get('offline', None)
        category=self.request.query_params.get('category', None)
        faculty=FacultyCourseAddition.objects.filter(user__id=user.id)
        fs=Faculty_Salary.objects.filter(faculty__id=Faculty.objects.get(user__id=user.id).id)
        print(fs.values_list('level',flat=True))
        if online:
            faculty=faculty.exclude(course__is_online=False)
        if offline:
            faculty=faculty.exclude(course__is_online=True)
        if online:
            fs=fs.filter(is_online=True).values_list('level',flat=True)
        if offline:
            fs=fs.filter(is_online=False).values_list('level',flat=True)
        

        print(Level.objects.filter(id__in=faculty.values_list('level',flat=True),category=category))
        
        level=Level.objects.filter(id__in=faculty.values_list('level',flat=True),category=category).exclude(id__in=fs)



        return level


# from .celery import scheduler

from student.models import StudentBatch
class ClassRoomViewsets(viewsets.ModelViewSet):
    queryset=ClassRooms.objects.all()
    serializer_class=ClassRoomSerializer
    permission_classes=[AdminAndRolePermission]
    pagination_class=SinglePagination



