from django.core.mail import EmailMessage
import string
import random
from decouple import config
import json
from django.shortcuts import render, get_object_or_404
import requests
from rest_framework import status
from dotenv import load_dotenv
import os
from rest_framework import serializers
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.forms.models import model_to_dict
# from webpush import send_user_notification
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from .serializers import AdminUserRegSerializer, UserSerializer, FacultyPhotoSerializer
from .serializers import BatchTypeSerializer, SalaryFixationSerializer, FacultySalarySerializer, FacultySerializer, FacultyCourseAdditionSerializer, UserSerializer, AdminFacultySerializer, MaterialSerializer, ExperienceSerializer, QuestionPoolSerializer, QuestionSerializer, FacultyList_AutoTimeTable_Topic_Serializer, FacultyList_AutoTimeTable_Course_Serializer
from accounts.models import SalaryFixation, Faculty_Salary, Material, Experience, User, Faculty, Role, FacultyCourseAddition, Permissions, get_default, Question, QuestionPool
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from .authhandle import AuthHandlerIns
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from course.models import *
from accounts.api.serializers import *
from .serializers import *
from rest_framework import viewsets
from django.db.models import Q 
from django.template.loader import render_to_string
from django.core.files import File
from django.core.files.base import ContentFile
import urllib.request
from django.db.models import Count
from permissions.permissions import *
from permissions.permissions import AdminAndRoleOrFacultyPermission, AdminAndRolePermission,AdminOrFaculty, FacultyPermission, NonePermission
from course.serializers import BranchSerializer
import requests
import re
from aceapp.settings.base import vimeo_access_token
from accounts.api.vimeo import upload_video_to_vimeo
from searchall.views import queryset_to_excel
from searchall.utils import get_queryset_headers_data,generate_pdf
from accounts.api.vimeo import SinglePagination
###################### PyJWT Authentication#########################

@api_view(['POST'])
def Login_single(request):

    try:
        username = request.data['email']

        print(username)

        password = request.data['password']
    except:
        return Response({'error': "credential missing"}, status=400)

    user = User.objects.filter(email=username).exists()
    if user:
        user = User.objects.filter(email=username).values().first()
        if user['is_faculty']:
            faculty = Faculty.objects.get(user=user['id'])
            print(faculty, 'faculty')
            if faculty.is_verified == False:
                return Response({'error': "Not verified"}, 401)

        if check_password(password, user['password']):
            payload = {'id': user['id'], 'username': user['username'], 'email': user['email'],
                       'admin': user['is_superuser'], 'role': user['is_roleuser'], 'faculty': user['is_faculty'],'student':user['is_student']}

            print(user['is_roleuser'], 'kkkkkkkkkkkkkkkkkkkkkk')

            if user['is_roleuser']:
                l = Role.objects.filter(user=user['id']).values(
                    'id')
                if not l:
                    l = get_default
                    payload["permission"] = get_default()

                else:
                    o = Permissions.objects.filter(
                        role__in=l).values('permissions')
                    o=get_permissions_login(o)
                    payload["permission"] = o
            # print(payload)

            p = AuthHandlerIns.get_token(payload=payload)
            r= AuthHandlerIns.get_refersh_token(payload={'id':user['id']})
            return Response({"access": p}, status=200)
        else:
            return Response({'error': "No User Found"}, status=404)

    else:
        return Response({'error': "No User Found"}, status=404)

    return Response({'error': "not valid"}, status=401)

def get_permissions_login(pay):
    p =pay
    # print(p)
    permission ={}
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    for i in p:
        # print(i['permissions'])
        for k in i['permissions'].keys():
            permission[k]={}
            print(k,"lkllllllllllllllllllllll")
            for ki in i['permissions'][k].keys():
                print(ki,"kiiiiiiiiiiiiiii")
                try:
                    if permission[k][ki]:
                        pass
                    else:
                        permission[k][ki]=i['permissions'][k][ki]
                except:
                    permission[k][ki]=i['permissions'][k][ki]

            # if permission[k]:
            #     if permission[k] ==v:
            #         pass
            #     else:
            #         pass
            # else:
            #     if permission[k] ==v:
            #         pass
            #     else:
            #         permission[k]=v

    print(permission)

        

    return permission

@api_view(['POST'])
def Refersh_token(request):
    token = request.data['refresh']
    access=AuthHandlerIns.refresh_token(token=token)
    return Response({
        "access":access
    })




@api_view(['POST'])
def Admin_signup(request):
    serializer = AdminUserRegSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_admin(
            email=request.data['email'], password=request.data['password'], mobile=request.data['mobile'], username=request.data['username'])
        s = UserSerializer(user)
        return Response({'yess': s.data})
    else:
        return Response({"error": "invalid"})


# @api_view(['POST'])
# def Faculty_signup(request):
#     print("***********")
#     try:
#         serializer = AdminUserRegSerializer(data=request.data)
#     except Exception as e:
#         return Response({"error":str(e)})
#     try:
#         ser = FacultySerializer(data=request.data)
#         print(ser.is_valid())
#     except Exception as e:
#         return Response({"error":str(e)})

#     if serializer.is_valid() and ser.is_valid():

#         print("ooo")
#         user=User.objects.create_faculty(email=request.data['email'],password=request.data['password'],mobile=request.data['mobile'],username=request.data['username'])
#         fac = ser.save()
#         Faculty.objects.filter(id=fac.id).update(user=user)

#         s=UserSerializer(user)

#         return Response({"messages":"Your registration is Pending,if you are select give a whatsapp message ace education center.",'user':s.data,'faculty':ser.data})
#     else:
#         print(ser.errors)
#         print(serializer.errors)
#         return Response({'error': serializer.errors or ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'error':"not valid"})


@api_view(['POST'])
def Faculty_signup(request):
    try:
        # Validate the request data using the serializer for AdminUser model
        print(request.data, "dataaaaaaaaaaaaaaaaaa")
        serializer = AdminUserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        name = request.data['name']

        # Validate the request data using the serializer for Faculty model
        faculty_serializer = FacultySerializer(data=request.data)
        faculty_serializer.is_valid(raise_exception=True)
        try:
            experiences = ExperienceSerializer(
                data=request.data['experiences'], many=True)
            experiences.is_valid(raise_exception=True)
            print(experiences.errors, "eorrrrrororororororo")
        except:
            pass
        print(faculty_serializer.errors, "facultyhjhswjshjw")
        print(serializer.errors, "user ser,mkdsjdksj")

        # Create a User object with the validated request data and "create_faculty" method
        user = serializer.save()
        # User.objects.create_faculty(
        #     email=serializer.validated_data['email'],
        #     password=serializer.validated_data['password'],
        #     mobile=serializer.validated_data['mobile'],
        #     username=serializer.validated_data['username']
        # )

        # Create a Faculty object with the validated request data
        faculty = faculty_serializer.save()

        # Create a Faculty_Salary object with the validated request data
        # faculty_salary_serializer = FacultySalarySerializer(data=request.data)
        # faculty_salary_serializer.is_valid(raise_exception=True)
        # faculty_salary = faculty_salary_serializer.save(faculty=faculty)

        # Update the "user" attribute of the Faculty object with the User object
        faculty.user = user
        faculty.save()
        try:
            experiences.faculty = faculty
            experiences.save()
        except:
            pass

        # Serialize and return the response data
        user_serializer = UserSerializer(user)
        faculty_serializer = FacultySerializer(faculty)
        # faculty_salary_serializer = FacultySalarySerializer(faculty_salary)

        # send a email to the faculty after registration
        mail_subject = f'Subject:{name} your booking is Pending'
        to_email = email
        body = "Your registration is pending... \nIf your selected we message confiramtion message to your whatsapp \nLogin Link: http://example.com/login \n\n\nACE EDUCATION CENTER"
        send_email = EmailMessage(mail_subject, body, to=[to_email])
        send_email.send()
        return Response({
            'message': 'Your registration is pending. If you are selected, we will send a WhatsApp message to Your Whatsapp number.',
            'user': user_serializer.data,
            'faculty': faculty_serializer.data,
            # 'faculty_salary': faculty_salary_serializer.data,

        })
    except serializers.ValidationError as e:
        print(e)
        # Return a 400 Bad Request response with the validation error details
        return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        # Return a 500 Internal Server Error response with the exception details
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# faculty signup update
# @api_view(['POST'])
# def Faculty_signup(request):
#     try:
#         # Validate the request data using the serializer for AdminUser model
#         print(request.data,"dataaaaaaaaaaaaaaaaaa")
#         serializer = AdminUserRegSerializer(data=request.data)
#         print(serializer,"this is serializer")
#         serializer.is_valid(raise_exception=True)
#         email=request.data['email']
#         name=request.data['name']


#         # Validate the request data using the serializer for Faculty model
#         faculty_serializer = FacultySerializer(data=request.data)
#         faculty_serializer.is_valid(raise_exception=True)
#         try:
#             experiences = ExperienceSerializer(data=request.data['experiences'], many=True)
#             experiences.is_valid(raise_exception=True)
#             print(experiences.errors,"eorrrrrororororororo")
#         except:
#             pass
#         print(faculty_serializer.errors,"facultyhjhswjshjw")
#         print(serializer.errors,"user ser,mkdsjdksj")


#         # Create a User object with the validated request data and "create_faculty" method
#         # user = serializer.save()
#         users=User.objects.create_faculty(
#             email=serializer.validated_data['email'],
#             password=serializer.validated_data['password'],
#             mobile=serializer.validated_data['mobile'],
#             username=serializer.validated_data['username']
#         )

#         # Create a Faculty object with the validated request data
#         faculty = faculty_serializer.save()


#         # Update the "user" attribute of the Faculty object with the User object
#         faculty.user = users
#         faculty.save()
#         try:
#             experiences.faculty = faculty
#             experiences.save()
#         except:
#             pass

#         # Serialize and return the response data
#         user_serializer = UserSerializer(users)
#         faculty_serializer = FacultySerializer(faculty)
#         # send a email to the faculty after registration
#         mail_subject = f'Subject:{name} your booking is Pending'
#         to_email = email
#         body = "Your registration is pending... \nIf your selected we message confiramtion message to your whatsapp \nLogin Link: http://example.com/login \n\n\nACE EDUCATION CENTER"
#         send_email = EmailMessage(mail_subject, body, to=[to_email])
#         send_email.send()
#         return Response({
#             'message': 'Your registration is pending. If you are selected, we will send a WhatsApp message to Your Whatsapp number.',
#             'user': user_serializer.data,
#             'faculty': faculty_serializer.data
#         })
#     except serializers.ValidationError as e:
#         print(e)
#         # Return a 400 Bad Request response with the validation error details
#         return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         print(e)
#         # Return a 500 Internal Server Error response with the exception details
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def Roleuser_signup(request):
    serializer = AdminUserRegSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_roleuser(
            email=request.data['email'], password=request.data['password'], mobile=request.data['mobile'], username=request.data['username'])
        s = UserSerializer(user)
        return Response({'yess': s.data})
    return Response({'error': 'not valid'})



from course.views import history_withoutdecorator

# 31-1-2023 vrification faculty is verified send to a whatsapp message
class adminfacultyverificationwithWhatsapp(APIView):

    def post(self, request, id):
        try:
            users = get_object_or_404(Faculty, id=id)
            faculty_email=users.user
            # course_approvals = FacultyCourseAddition.objects.filter(user=users.user.pk, status='approved').values('level').distinct()
            course_approvals = FacultyCourseAddition.objects.filter(user=users.user.pk, status='approved').values('category', 'level').distinct()
            print(course_approvals,'course_approvals')
            for approval in course_approvals:
                level=approval['level']
                cours_category=approval['category']
                level=Level.objects.get(id=level).name
                print(level,'name')
                category=Category.objects.get(id=cours_category).name
                print(category,'cat naem')
            
            
            try:
                # Get a list of level ids from course_approvals
                level_ids = course_approvals.values_list('level', flat=True)
                print(level_ids,'level id')

                # Filter faculty salary based on the level ids
                faculty_salary = Faculty_Salary.objects.filter(faculty=id, level__in=level_ids)
                print(faculty_salary,'faculty saaaaaaaaaaaaalary')

                # Loop through the faculty salaries and print the fixed salary
                for salary in faculty_salary:
                    print(salary.fixed_salary,'level wise salary')

            except:
                pass
            if course_approvals:
                assignedsalary=Faculty_Salary.objects.filter(faculty=id,fixed_salary__isnull=False,level__in=level_ids)
                print(assignedsalary,'assigned salary')
                if course_approvals.count() == assignedsalary.count():
                    phone = users.whatsapp_contact_number
                    if users.is_verified == False:
                        users.is_verified = True
                        data = request.data
                        # users.fixed_salary = data['fixed_salary']
                        users.save()
                        """send email also fucntion"""
                        try:
                            mail_subject = f'Subject:Your Course Verification Is Successful - ACE Education Center'
                            to_email = faculty_email
                            nameuser = (users.user.username)
                            body = f"Congratulations {nameuser}!\n\n Your course verification is successful.\n\n"

                            table_headers = ["Category", "Level", "Level-wise Salary"]
                            table_data = []
                            print(table_data,'dada')
                            for approval in course_approvals:
                                category = Category.objects.get(id=approval['category']).name
                                level = Level.objects.get(id=approval['level']).name
                                salary = Faculty_Salary.objects.get(faculty=id, level=approval['level']).fixed_salary
                                table_data.append([category, level, salary])
                            # Construct the HTML email body using the template and the course approval data
                            context = {
                                'name': users.user.username,
                                'table_data': table_data,
                                'login_url': 'https://v2.aceonline.app/login',
                            }
                            body = render_to_string('verification_email.html', context=context)

                            # Send the email
                            mail_subject = 'Subject:Your Course Verification Is Successful - ACE Education Center'
                            to_email = faculty_email
                            send_email = EmailMessage(mail_subject, body, to=[to_email])
                            send_email.content_subtype = 'html'
                            send_email.send()
                            return Response({'status': "True", 'message': 'you are verified'})
                            

                        except Exception as e:
                            return Response({'success': True}, status=status.HTTP_201_CREATED)

                        ##########whatsapp message#############
                        # load_dotenv()
                        # access_token = config('ACCESS_TOKEN')
                        # headers = {
                        #     'Authorization': f'Bearer {access_token}',
                        #     'Content-Type': 'application/json',
                        # }
                        # print("OOOOOOOOOOOOOOOO")
                        # payload = {
                        #     "messaging_product": "whatsapp",
                        #     "to": f'{phone}',
                        #     "type": "template",
                        #     "template": {
                        #         "name": "ace",
                        #         "language": {
                        #             "code": "en"
                        #         }
                        #     }
                        # }
                        # response = requests.post(
                        #     'https://graph.facebook.com/v15.0/113400621655857/messages',
                        #     headers=headers,
                        #     data=json.dumps(payload)
                        # )
                        # return Response({'status': response.status_code, 'message': 'you are verified'})
                    else:
                        return Response({'message': 'you are allready verified'})
                else:
                    return Response({"message": "approved courses are not assigned salary,please assign fixed salary"})
            else:
                return Response({"message":"please verify the course"})   
        except Exception as e:
            return Response({"message": "Something went wrong"})

# block a faculty


class adminfacultyblockforverifiedfaculty(APIView):
    def post(self, request, fid):
        facultys = get_object_or_404(Faculty, id=fid)

        if facultys.is_verified == True:
            if facultys.is_active == False:
                facultys.is_active = True
                facultys.save()
                return Response({'message': 'faculty is  blocked', 'status': status.HTTP_200_OK})
            if facultys.is_active == True:
                facultys.is_active = False
                facultys.save()
                return Response({'message': 'faculty is unblocked', 'status': status.HTTP_200_OK})
        else:
            pass


# forgot password of faculty


class facultyforgotpassword(APIView):
    def post(self, request):
        email = request.data.get("email")
        if email is None:
            return Response({'error': 'Please provide an email address'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # facultys = User.objects.filter(email=email).first()
                facultys = User.objects.filter(email=email).values()

                print(facultys, 'idddss')
                facultys_id = facultys[0]['id']
                if not facultys:
                    return Response({'error': 'The provided email address does not exist'},
                                    status=status.HTTP_404_NOT_FOUND)
                faculty = Faculty.objects.get(user=facultys_id)
                if faculty.is_verified == True:
                    new_password = ''.join(random.choice(
                        string.ascii_uppercase + string.digits) for _ in range(8))
                    print(new_password, 'new password')
                    faculty_get = User.objects.get(email=email)
                    faculty_get.set_password(new_password)
                    faculty_get.save()

                    mail_subject = 'Subject: Password reset for your account'
                    to_email = email
                    body = f"Your new password is: {new_password} \nPlease log in with this password and change it to a secure one.\n\n\nACE EDUCATION CENTER"
                    send_email = EmailMessage(mail_subject, body, to=[to_email])
                    send_email.send()
                    response = {
                        "messages": "A new password has been sent to your email.",
                    }
                    return Response(data=response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "messages": "You are not verified",
                    }
                    return Response(data=response, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({"message":"The provided email address does not exist or something went wrong"}, status=status.HTTP_404_NOT_FOUND)


# class FacultyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     # def get_object(self):
#     #     pk = self.kwargs.get('pk')
#     #     print("ID",pk)
#     queryset = Faculty.objects.filter(id=1)
#     print("queryset",queryset)
#     serializer_class = FacultySerializer
# #         # return get_object_or_404(self.queryset, pk=pk)
# #     # id = AuthHandlerIns.get_id(request=request)

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if serializer.initial_data != serializer.validated_data:
#             # check if course, subject, module, or topic fields have been updated
#             if 'course' in serializer.validated_data or \
#                'subject' in serializer.validated_data or \
#                'module' in serializer.validated_data or \
#                'topic' in serializer.validated_data:
#                 payload = {
#                     "head": "Notification",
#                     "body": "Your course, subject, module, or topic has been changed!",
#                     "icon": "/path/to/icon.png",
#                     "url": "/path/to/redirect",
#                 }
#                 send_user_notification(user=instance.user, payload=payload, ttl=1000)

# @receiver(m2m_changed, sender=Faculty.course.through)
# @receiver(m2m_changed, sender=Faculty.subject.through)
# @receiver(m2m_changed, sender=Faculty.module.through)
# @receiver(m2m_changed, sender=Faculty.topic.through)
# def send_notification_on_field_change(sender, instance, **kwargs):
#     if kwargs['action'] in ['post_add', 'post_remove', 'post_clear']:
#         payload = {
#             "head": "Notification",
#             "body": "Your course, subject, module, or topic has been changed!",
#             "icon": "/path/to/icon.png",
#             "url": "/path/to/redirect",
#         }
#         send_user_notification(user=instance.user, payload=payload, ttl=1000)


# end shamil code

# 20-2-23 admin add faculty end points

# @api_view(['POST'])
# def AdminFaculty_signup(request):
#     print("***********")
#     try:
#         serializer = AdminUserRegSerializer(data=request.data)
#         print(serializer,'iiiiiiiiiiiiiii')
#         print(request.data,'request')
#     except Exception as e:
#         return Response({"error": str(e),"hwkl":"sssss"})
#     try:
#         ser = AdminFacultySerializer(data=request.data)
#         print(ser.is_valid())
#     except Exception as e:
#         return Response({"error": str(e)})
#     try:
#         sal= NewFacultySalarySerializer(data=request.data)
#     except Exception as e:
#         return Response({"error": str(e)})

#     if serializer.is_valid() and ser.is_valid():

#         print("ooo")
#         user = User.objects.create_faculty(
#             email=request.data['email'], password=request.data['password'], mobile=request.data['mobile'], username=request.data['username'])
#         fac = ser.save()
#         Faculty.objects.filter(id=fac.id).update(user=user, is_verified=True)

#         s = UserSerializer(user)

#         return Response({"messages": "Your registration is Pending,if you are select give a whatsapp message ace education center.", 'user': s.data, 'faculty': ser.data})
#     else:
#         print(ser.errors)
#         print(serializer.errors)
#         return Response({'error': serializer.errors or ser.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def faculty_list(request):
    faculty = Faculty.objects.filter()
    f_ser = FacultySerializer(faculty, many=True)
    return Response({"data": f_ser.data})


# class MaterialCreateAPIView(generics.CreateAPIView):
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer

#     def create(self, request, *args, **kwargs):
#         print("Hiii!")
#         print(request.data['subtopic'])
#         val = request.data['subtopic'] 
#         lst = val[1:-1]
#         print(lst)
#         eng=[]
#         request.data.pop('subtopic')
#         print(request.data)
#         mat = Material.objects.create(faculty = Faculty.objects.get(id =request.data['faculty']) ,category =Category.objects.get(id=request.data['category']) ,level = Level.objects.get(id=request.data['level']),
#                        course = Course.objects.get(id =request.data['course']) ,subject = Subject.objects.get(id=request.data['subject']),module = Module.objects.get(id=request.data['module']),
#                        topic = Topic.objects.get(id=request.data['topic']),file = request.data['file'] )
#         for i in lst: 
#             if i not in ['[',',',']']:
#                 eng.append(SubTopic.objects.get(id=i).pk)
#         print(eng)
#         mat.subtopic.set(eng)
#         request.data['subtopic']=eng
#         print(request.data)

#         ser = self.serializer_class(mat)
#         return Response(ser.data)

class MaterialCreateAPIView(generics.CreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Hiii!")
            print(request.data['subtopic'])
            val = request.data['subtopic'] 
            lst = val[1:-1]
            print(lst)
            eng = []
            request.data.pop('subtopic')
            print(request.data)
            mat = Material.objects.create(faculty=Faculty.objects.get(id=request.data['faculty']),
                                          category=Category.objects.get(id=request.data['category']),
                                          level=Level.objects.get(id=request.data['level']),
                                          course=Course.objects.get(id=request.data['course']),
                                          subject=Subject.objects.get(id=request.data['subject']),
                                          module=Module.objects.get(id=request.data['module']),
                                          topic=Topic.objects.get(id=request.data['topic']),
                                          file=request.data['file'])
            for i in lst: 
                if i not in ['[', ',', ']']:
                    eng.append(SubTopic.objects.get(id=i).pk)
            print(eng)
            mat.subtopic.set(eng)
            request.data['subtopic'] = eng
            print(request.data)

            ser = self.serializer_class(mat)
            return Response(ser.data)
        except KeyError:
            return Response({'error': 'Invalid request data.'}, status=400)
        except (Material.DoesNotExist, Faculty.DoesNotExist, Category.DoesNotExist,
                Level.DoesNotExist, Course.DoesNotExist, Subject.DoesNotExist,
                Module.DoesNotExist, Topic.DoesNotExist, SubTopic.DoesNotExist):
            return Response({'error': 'Invalid data references.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# class MaterialCreateAPIView(APIView):
#     def post(self, request):
#         subtopics = request.data.get('subtopics', [])  # List of subtopic IDs
#         print(subtopics)
#         serializer = MaterialSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():

#             material = serializer.save()

#             # Assign material to each subtopic
#             for subtopic_id in subtopics:
#                 material.subtopic_id = subtopic_id
#                 material.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MaterialDetailView(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)







class ExperienceListCreateView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

# class FacultyCourseAdditionListCreateView(generics.ListCreateAPIView):
#     queryset = FacultyCourseAddition.objects.all()
#     serializer_class = FacultyCourseAdditionSerializer

# class FacultyCourseAdditionListCreateView(generics.ListCreateAPIView):
#     queryset = FacultyCourseAddition.objects.all()
#     serializer_class = FacultyCourseAdditionSerializer

from course.views import set_history_user_delete,create_history_user__decorator

class FacultyCourseAdditionListCreateView(generics.CreateAPIView):
    queryset = FacultyCourseAddition.objects.all()
    serializer_class = FacultyCourseAdditionSerializer
    def create(self, request, *args, **kwargs):
        # Check if the course key is present in the request data
        if 'course' not in request.data:
            return Response({'error': 'course key is missing'}, status=status.HTTP_400_BAD_REQUEST)

        courses = request.data['course']
        created_objects = []

        for course in courses:
            serializer = self.get_serializer(data=course)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            history_withoutdecorator(request,obj)
            created_objects.append(obj)

        return Response(FacultyCourseAdditionSerializer(created_objects, many=True).data, status=status.HTTP_201_CREATED)

class SalaryCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Faculty_Salary.objects.all()
    serializer_class = FacultySalarySerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    # @set_history_user_delete
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
class salaryfacultychanging(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Faculty_Salary.objects.all()

    serializer_class = FacultySalaryFixSerializer

    permission_classes = [AdminAndRolePermission]

   
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        
        return super().update(request, *args, **kwargs)
    
class ExperianceCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    permission_classes = [AdminAndRolePermission]

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @create_history_user__decorator
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
 
class InhouseFacultyCreation(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    permission_classes = [AdminAndRolePermission]

    # @set_history_user_delete
    def partial_update(self, request, *args, **kwargs):
        pk=kwargs['pk']
        print('rajjjjjjjjjjjjj')
        if AuthHandlerIns.is_staff(request=request):
            try:
                faculty = Faculty.objects.get(id=pk)
                if faculty.inhouse_fac == True:
                    faculty.inhouse_fac = False
                    history_withoutdecorator(request,faculty)
                    faculty.save()
                    return Response({'Message': 'Success', 'inhouse_fac': 'False'}, status=status.HTTP_200_OK)
                else:
                    faculty.inhouse_fac = True
                    history_withoutdecorator(request,faculty)
                    faculty.save()
                    return Response({'Message': 'Success', 'inhouse_fac': 'True'}, status=status.HTTP_200_OK)
            except Faculty.DoesNotExist:
                return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Only Admin Can Change'}, status=status.HTTP_401_UNAUTHORIZED)

    @create_history_user__decorator
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
  
    
class FacultyCourseDeletion(viewsets.ModelViewSet):
    # authentication_classes = [IsAdminUser]
    queryset = FacultyCourseAddition.objects.all()
    serializer_class = FacultyCourseAdditionSerializer

    permission_classes = [AdminAndRolePermission]

    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class FacultyCourseCreation(viewsets.ModelViewSet):
    
    queryset = FacultyCourseAddition.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= FacultyCourseAddition.history.filter(id=branch_id)
        else:
            queryset= FacultyCourseAddition.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

            
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
    
class FacultySalaryCreation(viewsets.ModelViewSet):
    
    queryset = Faculty_Salary.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Faculty_Salary.history.filter(id=branch_id)
        else:
            queryset= Faculty_Salary.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

            
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

    
class FacultyExperianceCreation(viewsets.ModelViewSet):
    
    queryset = Experience.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Experience.history.filter(id=branch_id)
        else:
            queryset= Experience.history.all().order_by('-history_date')
        
        history_type = self.request.query_params.get('history_type', None)
        if history_type:
            if history_type in ('+', '~', '-'):
                queryset = queryset.filter(Q(history_type=history_type))
                        

            
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

    
    


# class FacultyCourseAdditionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = FacultyCourseAddition.objects.all()
#     serializer_class = FacultyCourseAdditionSerializer
# class FacultyCourseAdditionRetrieveUpdateDestroyView(APIView):
#     def post(self, request,pk, *args, **kwargs):
#         if not AuthHandlerIns.is_staff(request=request):
#                 return Response({"message": "Only admin can varify facultu subject"}, status=status.HTTP_401_UNAUTHORIZED)
#         ids=request.data['faculty']
#         if not ids:
#                 return Response({"message": "Missing faculty ID"}, status=status.HTTP_400_BAD_REQUEST)
#         faccourse=FacultyCourseAddition.objects.get(id=pk,user=Faculty.objects.get(id=ids).user)
#         print(faccourse,'this is facoursedfsdf')
#         # if faccourse.status=='pending':
#         #     faccourse.status='approved'
#         #     faccourse.save()
#         # if faccourse.status=='approved' or 'pending':
#         #     faccourse.status='blocked'
#         #     faccourse.save()
#         # elif faccourse.status=='blocked' or 'pending':
#         #     faccourse.status='approved'
#         #     faccourse.save()
#         if faccourse.status == 'approved' or faccourse.status == 'pending':
#             faccourse.status = 'blocked'
#             faccourse.save()
#         elif faccourse.status == 'blocked' or faccourse.status == 'pending':
#             faccourse.status = 'approved'
#             faccourse.save()

#         serializer = FacultyCourseAdditionSerializer(faccourse)
#         return Response(serializer.data)

class FacultyCourseAdditionPendingtoapprove(APIView):
    def post(self, request, pk, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can varify facultu subject"}, status=status.HTTP_401_UNAUTHORIZED)
        ids = request.data['faculty']
        if not ids:
            return Response({"message": "Missing faculty ID"}, status=status.HTTP_400_BAD_REQUEST)
        faccourse = FacultyCourseAddition.objects.get(
            id=pk, user=Faculty.objects.get(id=ids).user)
        if faccourse.status == 'pending' or faccourse.status == 'blocked':
            faccourse.status = 'approved'
            faccourse.save()
        else:
            pass
        history_withoutdecorator(request,faccourse)
        serializer = FacultyCourseAdditionSerializer(faccourse)
        
        return Response(serializer.data)
    
    def patch(self, request, pk, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can varify facultu subject"}, status=status.HTTP_401_UNAUTHORIZED)
        course = FacultyCourseAddition.objects.filter(id__in=request.data['id']).update(status='approved')
        # serializer = FacultyCourseAdditionSerializer(course)

        for i in FacultyCourseAddition.objects.filter(id__in=request.data['id']):
            print("oooooooooo")
            i.status = 'approved'
            i.save()
            history_withoutdecorator(request,i)
        return Response({"status":True})



class FacultyCourseAdditionPendingtoBlock(APIView):
    def post(self, request, pk, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can varify facultu subject"}, status=status.HTTP_401_UNAUTHORIZED)
        ids = request.data['faculty']
        if not ids:
            return Response({"message": "Missing faculty ID"}, status=status.HTTP_400_BAD_REQUEST)
        faccourse = FacultyCourseAddition.objects.get(
            id=pk, user=Faculty.objects.get(id=ids).user)
        if faccourse.status == 'pending' or faccourse.status == 'approved':
            faccourse.status = 'blocked'
            faccourse.save()
        else:
            pass
        history_withoutdecorator(request,faccourse)
        serializer = FacultyCourseAdditionSerializer(faccourse)
        return Response(serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can varify facultu subject"},  status=status.HTTP_401_UNAUTHORIZED)
        print(request.data['id'],"333333333333333333333")
        course = FacultyCourseAddition.objects.filter(id__in=request.data['id'])
        # .update(status='blocked')
        print(course,'0000000000000000000000000')
        for i in FacultyCourseAddition.objects.filter(id__in=request.data['id']):
            print("oooooooooo")
            i.status = 'blocked'
            i.save()
            history_withoutdecorator(request,i)
        # serializer = FacultyCourseAdditionSerializer(course)
        return Response({"status":True})


@api_view(['POST'])
def update_faculty_photo(request, faculty_id):  # We are actually passing userid####
    print(faculty_id)
    try:
        faculty = Faculty.objects.get(user=faculty_id)
        serializer = FacultyPhotoSerializer(faculty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        faculty = Faculty.objects.get(user=faculty_id)
        print(faculty.user.id)
        user = User.objects.get(id=faculty.user.id)
        user.delete()
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getfacultyonuserid(request, user_id):
    print(user_id)
    faculty = Faculty.objects.get(user=user_id)
    faculty_id = faculty.id
    return Response({'Faculty id': faculty_id})


# class QuestionPoolCreateView(generics.CreateAPIView):
#     serializer_class = QuestionPoolSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data,status=201, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()


class QuestionPoolget(generics.ListCreateAPIView):
    queryset = QuestionPool.objects.all()
    serializer_class = QuestionPoolSerializer

# class QuestionPoolCreateView(generics.CreateAPIView):
#     serializer_class = QuestionPoolSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Save the question pool instance
#         self.perform_create(serializer)

#         # Get the list of questions from the request data
#         question_data = request.data.get('questions')

#         # Add the questions to the newly created question pool instance
#         question_pool = serializer.instance
#         for question in question_data:
#             question_obj = Question.objects.create(
#                 question_text=question.get('question_text'),
#                 option_1=question.get('option_1'),
#                 option_2=question.get('option_2'),
#                 option_3=question.get('option_3'),
#                 option_4=question.get('option_4'),
#                 option_5=question.get('option_5'),
#                 answer=question.get('answer')
#             )
#             question_pool.questions.add(question_obj)

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# @api_view(['POST'])
# def QuestionPoolCreateView(request):
#     if not AuthHandlerIns.is_faculty(request):
#         return Response({"message": "Only faculty can create a questions"}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         print(AuthHandlerIns.is_faculty(request),'kkkkkkkkkk')
#         print(AuthHandlerIns.get_mail(request))
#         s=AuthHandlerIns.get_mail(request)
#         facid=AuthHandlerIns.get_id(request)
#         print(facid,'facid')
#         print(s,"this is faculyt email")
#         # kk=Faculty.objects.get(user=User.objects.get(email=s))
#         # print(kk.expected_salary,'this is kk faculty')
#         kks=FacultyCourseAddition.objects.get(faculty=User.objects.get(email=s))
#         c=model_to_dict(kks)
#         print(c,"thsi is is")
#         print(c['category'][0].name,'FacultyCourseAddition')
#         print(kks,"this faculty cousre addition")
#         categories = [category.name for category in c['category']]
#         levels = [level.name for level in c['level']]
#         topics = [topic.name for topic in c['topic']]
#         print("**************")
#         faculty_course_addition_instance = FacultyCourseAddition.objects.get(id=2)
#         print(faculty_course_addition_instance,'ooo')
#         category_ids = faculty_course_addition_instance.category.values_list('id', flat=True)
#         print(category_ids)
#         print("::::::::::::::::")

#         faculty_course_addition_instance = FacultyCourseAddition.objects.get(faculty=User.objects.get(id=9))
#         print(faculty_course_addition_instance,"kkkk")
#         category_ids = faculty_course_addition_instance.category.values_list('id', flat=True)
#         if request.data['category'] in category_ids:
#             passSSSS
#         # do something
#         else:
#             pass
#         # do something else

#         print(categories)
#         print(levels)
#         print(topics)


#         serializer = QuestionPoolSerializer(data=request.data)
#         print(request.data['categorys'])
#         requestcat=request.data['categorys']
#         print(requestcat)
#         cat=Category.objects.filter(id=requestcat)
#         print(cat)
#         if serializer.is_valid():
#             # Save the question pool instance
#             serializer.save()

#             # Get the list of questions from the request data
#             question_data = request.data.get('questions', [])

#             # Add the questions to the newly created question pool instance
#             question_pool = serializer.instance
#             for question in question_data:
#                 question_obj = Question.objects.create(
#                     question_text=question.get('question_text'),
#                     option_1=question.get('option_1'),
#                     option_2=question.get('option_2'),
#                     option_3=question.get('option_3'),
#                     option_4=question.get('option_4'),
#                     option_5=question.get('option_5'),
#                     answer=question.get('answer')
#                 )
#                 question_pool.questions.add(question_obj)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response({"message":"not valid seriaizer","errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def QuestionPoolCreateView(request):
#     serializer = QuestionPoolSerializer(data=request.data)
#     if serializer.is_valid():
#         # Save the question pool instance
#         serializer.save()

#         # Get the list of questions from the request data
#         question_data = request.data.get('questions', [])

#         # Add the questions to the newly created question pool instance
#         question_pool = serializer.instance
#         for question in question_data:
#             question_obj = Question.objects.create(
#                 question_text=question.get('question_text'),
#                 option_1=question.get('option_1'),
#                 option_2=question.get('option_2'),
#                 option_3=question.get('option_3'),
#                 option_4=question.get('option_4'),
#                 option_5=question.get('option_5'),
#                 answer=question.get('answer')
#             )
#             question_pool.questions.add(question_obj)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response({"message":"not valid seriaizer","errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def QuestionPoolCreateView(request):
#     if not AuthHandlerIns.is_faculty(request):
#         return Response({"message": "Only faculty can create a questions"}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         facultyidintoken = AuthHandlerIns.get_id(request)
#         getfaculty = Faculty.objects.get(
#             user=User.objects.get(id=facultyidintoken))
#         data = request.data
#         data['facultys'] = getfaculty.id
#         serializer = QuestionPoolSerializer(data=request.data)

#         if serializer.is_valid():
#             # Save the question pool instance
#             serializer.save()

#             # Get the list of questions from the request data
#             question_data = request.data.get('questions', [])
#             print(question_data,'question data')
            
#             try:
#                 question=Question.objects.filter(question_text=)
#             except Exception as e:
#                 print(e)

#             # Add the questions to the newly created question pool instance
#             question_pool = serializer.instance
#             print(question_pool,'question pool')
#             for question in question_data:
#                 question_obj = Question.objects.create(
#                     question_text=question.get('question_text'),
#                     option_1=question.get('option_1'),
#                     option_2=question.get('option_2'),
#                     option_3=question.get('option_3'),
#                     option_4=question.get('option_4'),
#                     option_5=question.get('option_5'),
#                     answer=question.get('answer')
#                 )
#                 question_pool.questions.add(question_obj)

#             return Response({"message":"created successfully"}, status=status.HTTP_201_CREATED)

#         return Response({"message": "not valid seriaizer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def QuestionPoolCreateView(request):
    if not AuthHandlerIns.is_faculty(request):
        return Response({"message": "Only faculty can create a questions"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        facultyidintoken = AuthHandlerIns.get_id(request)
        getfaculty = Faculty.objects.get(
            user=User.objects.get(id=facultyidintoken))
        data = request.data
        topic_id=request.data['topic']
        type=request.data['type']
        data['facultys'] = getfaculty.id
        serializer = QuestionPoolSerializer(data=request.data)

        if serializer.is_valid():
            # Save the question pool instance
            serializer.save()

            # Get the list of questions from the request data
            question_data = request.data.get('questions', [])

            # Add the questions to the newly created question pool instance
            question_pool = serializer.instance
            
            for question in question_data:
                # Check if the question already exists in the Question model
                question_text = question.get('question_text')
                # matching_questions = Question.objects.filter(question_text=question_text)
                matching_questions = QuestionPool.objects.filter(questions__question_text=question_text, topic=topic_id,type=type)
                

                if matching_questions.exists():
                    #delete the question pool instance(question pool is created but question is not created)
                    question_pool.delete()
                    # Skip adding the question to the question pool
                    return Response({"message":"question is allready exist"},status=status.HTTP_400_BAD_REQUEST)

                # Create a new question object and add it to the question pool
                question_obj = Question.objects.create(
                    question_text=question_text,
                    option_1=question.get('option_1'),
                    option_2=question.get('option_2'),
                    option_3=question.get('option_3'),
                    option_4=question.get('option_4'),
                    option_5=question.get('option_5'),
                    answer=question.get('answer')
                )
                question_pool.questions.add(question_obj)

            return Response({"message":"created successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "not valid seriaizer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Questionget(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class FacultyCourseAdditionView(APIView):
    def get(self, request, user_id):
        try:
            faculty_course_addition = FacultyCourseAddition.objects.get(
                user=user_id)
        except FacultyCourseAddition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FacultyCourseAdditionSerializer(
            instance=faculty_course_addition)

        return Response(serializer.data)


class CheckEmailExists(APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'email_exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'email_exists': False}, status=status.HTTP_200_OK)


class CheckMobileExists(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        if User.objects.filter(mobile=mobile).exists():
            return Response({'mobile_exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'mobile_exists': False}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@csrf_exempt
def faculty_signup_and_experience(request):
    if request.method == 'POST':
        # Call Faculty_signup view
        try:
            serializer = AdminUserRegSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            faculty_serializer = FacultySerializer(data=request.data)
            faculty_serializer.is_valid(raise_exception=True)
            experiences = ExperienceSerializer(
                data=request.data['experiences'], many=True)
            experiences.is_valid(raise_exception=True)
            user = serializer.save()
            faculty = faculty_serializer.save()
            faculty.user = user
            faculty.save()
            experiences.faculty = faculty
            experiences.save()
            user_serializer = UserSerializer(user)
            faculty_serializer = FacultySerializer(faculty)
            return Response({
                'message': 'Your registration is pending. If you are selected, we will send a WhatsApp message to Your Whatsapp number.',
                'user': user_serializer.data,
                'faculty': faculty_serializer.data
            })
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        # Call ExperienceListCreateView view
        queryset = Experience.objects.all()
        serializer = ExperienceSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        queryset = FacultyCourseAddition.objects.all()
        serializer_class = FacultyCourseAdditionSerializer

        def create(self, request, *args, **kwargs):
            # Check if the course key is present in the request data
            if 'course' not in request.data:
                return Response({'error': 'course key is missing'}, status=status.HTTP_400_BAD_REQUEST)

            courses = request.data['course']
            created_objects = []

            for course in courses:
                serializer = self.get_serializer(data=course)
                serializer.is_valid(raise_exception=True)
                obj = serializer.save()
                created_objects.append(obj)

            return Response(FacultyCourseAdditionSerializer(created_objects, many=True).data, status=status.HTTP_201_CREATED)

    else:
        # Return a 405 Method Not Allowed response for any other HTTP method
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CheckWhatsappExists(APIView):
    def post(self, request):
        whatsapp_contact_number = request.data.get('whatsapp_contact_number')
        if Faculty.objects.filter(whatsapp_contact_number=whatsapp_contact_number).exists():
            return Response({'mobile_exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'mobile_exists': False}, status=status.HTTP_200_OK)


class SalaryListCreateView(generics.ListCreateAPIView):
    queryset = Faculty_Salary.objects.all()
    serializer_class = FacultySalarySerializer


class SalaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty_Salary.objects.all()
    serializer_class = FacultySalarySerializer


class SalaryFixDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty_Salary.objects.all()
    serializer_class = FacultySalaryFixSerializer


@api_view(['GET'])
def facultyList_AutoTimeTable_Course(request, pk):
    if not AuthHandlerIns.is_staff(request) and not AuthHandlerIns.is_role(request=request):
        return Response({"message": "Only admin can access this"}, status=status.HTTP_401_UNAUTHORIZED)

    topic = Topic.objects.filter(module__in=Module.objects.filter(
        subject__in=Subject.objects.filter(course=pk).values('id')).values('id')).values('id')

    faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
        topic__in=topic, status='approved').values('user')

    fac = Faculty.objects.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3]).values()
    course = Course.objects.get(id=pk)
    fac_ser = FacultyList_AutoTimeTable_Course_Serializer(
        list(fac), many=True, context={'level': course.level, 'course': course})

    return Response(fac_ser.data)


@api_view(['GET'])
def facultyList_AutoTimeTable_Topic(request, pk):
    if not AuthHandlerIns.is_staff(request) and not AuthHandlerIns.is_role(request=request):
        return Response({"message": "Only Admin can access this"}, status=status.HTTP_401_UNAUTHORIZED)

    # print(Subject.objects.filter(course=pk).values('id'))
    topic_batch = Topic_batch.objects.filter(id=pk).values('topic')
    print(topic_batch, "topicBatch")
    topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')
    print(topic, "hellooooo")

    faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
        topic__in=topic, status='approved').values('user')
    salary = Topic.objects.get(id__in=topic)
    level = salary.module.subject.course.level
    print(level, "hellllllll")

    fac = Faculty.objects.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3])
    faculty = FacultyList_AutoTimeTable_Topic_Serializer(fac, many=True,context={'level':level})

    return Response({"Facukty_List": faculty.data})


class SalaryFixationListCreateView(generics.ListCreateAPIView):
    queryset = SalaryFixation.objects.all()
    serializer_class = SalaryFixationSerializer


class SalaryFixationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryFixation.objects.all()
    serializer_class = SalaryFixationSerializer


class BatchTypeListCreateView(generics.ListCreateAPIView):
    queryset = BatchType.objects.all()
    serializer_class = BatchTypeSerializer


class BatchTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BatchType.objects.all()
    serializer_class = BatchTypeSerializer


class DeclarationCreation(APIView):
    def post(self, request):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can verify faculty subject"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if a declaration already exists
        if Declaration.objects.exists():
            return Response({"message": "A declaration already exists. Use PATCH method to update it."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            declaration = request.data['declaration']
        except Exception as e:
            return Response({'Message': 'Missing declaration '}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = DeclarationSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(slef, request):
        try:

            declaration = Declaration.objects.all()
            serializer = DeclarationSerializer(declaration, many=True)
            return Response(serializer.data)
        except:
            return Response({'message':'something went wrong'},status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk):
        # Check if the user is authenticated and has admin privileges
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can verify faculty subject"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the declaration object to update
        try:
            declaration = Declaration.objects.get(pk=pk)
        except Declaration.DoesNotExist:
            return Response({"message": "Declaration does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Update the declaration object with the request data
        serializer = DeclarationSerializer(
            instance=declaration, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def get_salarydetails_by_faculty(request, faculty_id):
    try:
        faculty = Faculty.objects.get(id=faculty_id)
    except Faculty.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    faculty_sal = Faculty_Salary.objects.filter(faculty=faculty)
    serializer = FacultySalarySerializer(faculty_sal, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def faculty_signup_new(request):
    user = None  # set a default value for the user variable
    try:
        user_serializer = AdminUserRegSerializer(data=request.data['user'])
        user_serializer.is_valid(raise_exception=True)
        # create faculty method for is_faculy is true is acive true
        user = User.objects.create_faculty(
            email=user_serializer.validated_data['email'],
            password=user_serializer.validated_data['password'],
            mobile=user_serializer.validated_data['mobile'],
            username=user_serializer.validated_data['username']
        )
        # crete faculty start
        faculty_data = request.data['faculty']
        faculty_data['user'] = user.pk
        faculty_serializer = FacultySerializerNew(data=faculty_data)
        faculty_serializer.is_valid(raise_exception=True)
        if not faculty_serializer.is_valid():
                user.delete()
                return Response({'success': False, 'message': str(faculty_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        faculty_serializer.save()
        # end the faculty model save
        # start the experianc model and experiance model is foriegn key of user model
        users = User.objects.get(email=user)
        faculty = Faculty.objects.get(user=users)
        experiences_data = request.data.get('experiences', [])
        if isinstance(experiences_data, list):
            users = User.objects.get(email=user)
            for experience in experiences_data:
                experience['name'] = faculty.id
                experiences_serializer = ExperienceSerializer(data=experience)
                if not experiences_serializer.is_valid():
                    error_message=dict(experiences_serializer.errors)
                    user.delete()
                    return Response({'status':"false",'message':error_message},status=status.HTTP_400_BAD_REQUEST)
                experiences_serializer.save()
        # start the course additon model and save couse on based this faculty
        courses = request.data['course']
        if isinstance(courses, list):
            for course in courses:
                course['user'] = user.pk
                course_serializer = FacultyCourseAdditionSerializer(
                    data=course)
                if not course_serializer.is_valid():
                    error_message=dict(course_serializer.errors)
                    user.delete()
                    return Response({"status":"false","message":error_message},status=status.HTTP_400_BAD_REQUEST)
                course_serializer.save()
        # start the level based salary and save that model
        salary = request.data.get('levelbysalary', [])
        if isinstance(salary, list):
            for sal in salary:
                # Assuming you have the faculty object defined earlier in your code
                sal['faculty'] = faculty.id
                salary_serializer = NewFacultySalarySerializer(data=sal)
                if not salary_serializer.is_valid():
                    user.delete()
                    error_message=dict(salary_serializer.errors)
                    return Response({"status":"false","message":error_message},status=status.HTTP_400_BAD_REQUEST)
                salary_serializer.save()
                
        # send a email to the faculty after registration
        try:
            mail_subject = f'Subject:Your Registration Successful - ACE Education Center'
            to_email = users.email
            nameuser = (user.username)
            body = f"Hi {nameuser},\n\n Thank you for registering with us.\n We will sent a confirmation message in Whatsapp and Email after verification.\n Then You can log in to your account using this link. \n\nLogin Link: https://v2.aceonline.app/login \n\n\nACE EDUCATION CENTER,Manjeri"

            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()
            return Response({
                'message': 'Your registration is pending. If you are selected, we will send a WhatsApp message to Your Whatsapp number.',
                'user': user_serializer.data,
                'faculty': faculty_serializer.data,
                # 'faculty_salary': faculty_salary_serializer.data,

            })
        except Exception as e:
            print(e)
            return Response({'success': True}, status=status.HTTP_201_CREATED)

        # return Response({'success': True}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # if user creating is not success then delete that user in user model('error':"user allready exist error")
        if user:
            user.delete()
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AdminFaculty_signup(request):
    user = None  # set a default value for the user variable
    try:
        user_serializer = AdminUserRegSerializer(data=request.data['user'])
        user_serializer.is_valid(raise_exception=True)
        # create faculty method for is_faculy is true is acive true
        user = User.objects.create_faculty(
            email=user_serializer.validated_data['email'],
            password=user_serializer.validated_data['password'],
            mobile=user_serializer.validated_data['mobile'],
            username=user_serializer.validated_data['username']
        )
        # crete faculty start
        faculty_data = request.data['faculty']
        faculty_data['user'] = user.pk
        faculty_serializer = AdminsideFacultySerializerNew(data=faculty_data)
        faculty_serializer.is_valid(raise_exception=True)

        faculty_serializer.save()
        # end the faculty model save
        # start the experianc model and experiance model is foriegn key of user model
        users = User.objects.get(email=user)
        faculty = Faculty.objects.get(user=users)
        faculty.is_verified = True
        faculty.inhouse_fac = True
        faculty.save()

        courses = request.data['course']
        if isinstance(courses, list):
            for course in courses:
                course['user'] = user.pk
                course_serializer = FacultyCourseAdditionSerializer(
                    data=course)
                course_serializer.is_valid()
                course_serializer.save()
        # start the level based salary and save that model
        salary = request.data.get('levelbysalary', [])
        if isinstance(salary, list):
            for sal in salary:
                # Assuming you have the faculty object defined earlier in your code
                sal['faculty'] = faculty.id
                salary_serializer = NewFacultySalarySerializer(data=sal)
                if salary_serializer.is_valid():
                    salary_serializer.save()
                else:
                    print(salary_serializer.errors)
        try:
            mail_subject = f'Subject:Your Registration Successful - ACE Education Center'
            to_email = users.email
            print(to_email, 'to email')
            body = "Your registration is succesfull \nIf your selected we send confirmtion message to your whatsapp \n\nLogin Link: http://example.com/login \n\n\nACE EDUCATION CENTER"
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()
            return Response({
                'message': 'Your registration is pending. If you are selected, we will send a WhatsApp message to Your Whatsapp number.',
                'user': user_serializer.data,
                'faculty': faculty_serializer.data,
                # 'faculty_salary': faculty_salary_serializer.data,

            })
        except:

            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': True}, status=status.HTTP_201_CREATED)

        # return Response({'success': True}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # if user creating is not success then delete that user in user model('error':"user allready exist error")
        if user:
            user.delete()
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def AdmincangefacPassword(request, pk):
    print("hello")
    if AuthHandlerIns.is_staff(request=request):
        facid = Faculty.objects.get(id=pk)
        user = User.objects.get(email=facid.user)
        password = request.data.get('password')
        print(password, 'ddddddd')
        try:
            user.password = password
            user.set_password(password)
            user.save()
        except Exception as e:
            pass
        return Response({'message': "changed faculty password"})
    else:
        return Response({'message': "only admin can change faculty password"})


@api_view(['GET'])
def get_salary_list(request):
    salary_types = SalaryFixation.objects.all()
    serializer = SalaryFixationSerializer(salary_types, many=True)
    return Response(serializer.data)


class FacultyViewSet(viewsets.ViewSet):
    def partial_update(self, request, pk):
        if AuthHandlerIns.is_staff(request=request):
            try:
                faculty = Faculty.objects.get(id=pk)
                if faculty.inhouse_fac == True:
                    faculty.inhouse_fac = False
                    faculty.save()
                    return Response({'Message': 'Success', 'inhouse_fac': 'False'}, status=status.HTTP_200_OK)
                else:
                    faculty.inhouse_fac = True
                    faculty.save()
                    return Response({'Message': 'Success', 'inhouse_fac': 'True'}, status=status.HTTP_200_OK)
            except Faculty.DoesNotExist:
                return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Only Admin Can Change'}, status=status.HTTP_401_UNAUTHORIZED)


class InternalFaculty(viewsets.ViewSet):
    def list(self, request):
        if not AuthHandlerIns.is_staff(request=request) and not AuthHandlerIns.is_role(request=request):
            return Response({"message": "Only admin can verify faculty subject"}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Faculty.objects.filter(inhouse_fac=True)
        serializer = FacultyList_AutoTimeTable_Topic_Serializer(
            queryset, many=True)
        return Response(serializer.data)


class InternalFacultyByTopic(viewsets.ViewSet):
    def retrieve(self, request, pk):
        if not AuthHandlerIns.is_staff(request=request) and not AuthHandlerIns.is_role(request=request):
            return Response({"message": "Only admin can verify faculty subject"}, status=status.HTTP_401_UNAUTHORIZED)
        topic_batch = Topic_batch.objects.filter(id=pk).values("topic")
        topic = Topic_branch.objects.filter(id__in=topic_batch).values("topic")
        facultywithcourse = FacultyCourseAddition.objects.filter(
            topic__in=topic, status="approved").values('user')
        queryset = Faculty.objects.filter(
            inhouse_fac=True, user__in=facultywithcourse)

        # salary =
        salary = Topic.objects.get(id__in=topic)
        level = salary.module.subject.course.level

        serializer = FacultyList_AutoTimeTable_Topic_Serializer(
            queryset, many=True,context={'level':level})
        return Response(serializer.data)

from rest_framework.decorators import action
class facultychangepassword(viewsets.ViewSet):
    @action(detail=True, methods=['patch'], url_path='updatepassword')
    def update_password(self, request):
        try:
            old_password = request.data.get('old password')
            new_password = request.data.get('new password')
            confirmnewpassword = request.data.get('confirm new password')
            try:
                facemail=AuthHandlerIns.get_mail(request=request)
                user=User.objects.get(email=facemail)
                if old_password is not None and check_password(old_password, user.password):
                    if new_password == confirmnewpassword and confirmnewpassword is not None:

                        # Set the new password
                        if new_password is not None:
                            user.password = new_password
                            user.set_password(new_password)
                            user.save()
                            return Response({'message': 'Password updated successfully','status':"True"})
                        else:
                            return Response({'message':"Please add the new and confirm password",'status':'False'})
                    else:
                        return Response({"message":"New password and confirm password are not equal",'status':'False'})
                else:
                    return Response({"message":"Old password is incorrect",'status':'False'})
        
            except Faculty.DoesNotExist:
                return Response({'errors': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# # Viewset
# class QuestionPoolViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for fetching questions based on faculty, course, and topic IDs.
#     """
#     def list(self, request):
#         faculty_id = request.query_params.get('faculty_id', None)
#         print(faculty_id, 'faculty_id')
#         course_id = request.query_params.get('course_id', None)
#         print(course_id, 'course_id')
#         topic_id = request.query_params.get('topic_id', None)
#         print(topic_id, 'topic_id')

#         questions = QuestionPool.get_questions(faculty_id, course_id, topic_id)
#         print(questions,'views')
#         # questions_list = list(questions.values())
#         # return Response(questions_list)
#         for i in questions:
#             print(i,'hh')

#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

class QuestionPoolViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for fetching and updating questions based on faculty, course, and topic IDs.
    """
    def list(self, request):
        faculty_id = request.query_params.get('faculty_id', None)
        category_id = request.query_params.get('category_id', None)
        level_id = request.query_params.get('level_id', None)
        course_id = request.query_params.get('course_id', None)
        subject_id=request.query_params.get('subject_id',None)
        topic_id = request.query_params.get('topic_id', None)
        type=request.query_params.get('type', None)

        questions = QuestionPool.get_questions(faculty_id, course_id,subject_id, topic_id,type,category_id,level_id)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'message': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mesage":"Question updated successfully","data":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'message': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response({"message":"Question deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class SpecialHolidayViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = SpecialHolidaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    def list(self,request):
        try:
            Specialholiday=SpecialHoliday.objects.all()
        except:
            return Response({"message":"Data not found"},status=status.HTTP_400_BAD_REQUEST)
        serializers=GetSpecialHoliday(Specialholiday,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
        
    def update(self,request,pk=None):
        try:
            specialholiday=SpecialHoliday.objects.get(id=pk)
        except:
            return Response({"message":"Data not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer=SpecialHolidaySerializer(specialholiday,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"update successfully"})
        else:
            return Response({"message":"not valid"})
        
    def destroy(self,request,pk=None):
        try:
            specialholidays=SpecialHoliday.objects.get(id=pk)
        except:
            return Response({"message":"Data not found"},status=status.HTTP_400_BAD_REQUEST)
        
        specialholidays.delete()
        return Response({"message":"Deleted succrssfully"},status=status.HTTP_200_OK)
    

class DeleteFacRejectApp(viewsets.ViewSet):
    def destroy(self,request,pk=None):
        try:
            user=User.objects.get(id=pk)
        except:
            return Response({"message":"Data not found"},status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"message":"Deleted succrssfully"},status=status.HTTP_200_OK)
    
    def patch(self,request,pk=None,*args,**kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can varify facultu subject"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            rejectapplication=User.objects.filter(id__in=request.data['id']).delete()        
            return Response({'status': True},status=status.HTTP_200_OK )
        except:
            return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)

class QuestionPoolSearch(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultyQuestionSerchserializer
    
    @action(detail=False, methods=['GET'])
    def search_by_username(self, request):
        query = request.GET.get('query')
        if not query:
            return Response([])
        faculties = Faculty.objects.filter(Q(name__icontains=query))
        serializer = self.get_serializer(faculties, many=True)
        return Response(serializer.data)
    

        
class CheckUsernameExistsViewSet(viewsets.ViewSet):
    serializer_class = UsercheckSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        exists = User.objects.filter(username=username).exists()
        return Response({'Username_exists': exists}, status=status.HTTP_200_OK)
    
# class MaterialViewSet(viewsets.ModelViewSet):
#     queryset = Material.objects.filter(is_delete=False)
#     serializer_class = MaterialSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         faculty_id = self.request.query_params.get('faculty_id')
#         topic_id = self.request.query_params.get('topic_id')
#         if faculty_id is not None and topic_id is not None:
#             queryset = queryset.filter(faculty_id=faculty_id, topic_id=topic_id)
#         return queryset

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         material = self.get_object()
#         # Check that the requesting user has permission to download the file, e.g. based on their role or ownership of related objects.
#         # ...
#         # Return the file as a response.
#         try:
#             response = FileResponse(material.file)
#         except FileNotFoundError:
#             return HttpResponseBadRequest("File not found.")
#         response['Content-Disposition'] = 'attachment; filename=%s' % material.file.name.split('/')[-1]
#         return response
    

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(is_delete=False)
    serializer_class = MaterialSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        faculty_id = self.request.query_params.get('faculty_id')
        topic_id = self.request.query_params.get('topic_id')
        print(faculty_id,"faculty_id",topic_id,"topic_id")
        if faculty_id is not None and topic_id is not None:
            queryset = queryset.filter(faculty_id=faculty_id, topic_id=topic_id)
        return queryset

    # @action(detail=True, methods=['get'])
    # def download(self, request, pk=None):
    #     faculty_id = self.request.query_params.get('faculty_id')
    #     topic_id = self.request.query_params.get('topic_id')
    #     queryset = Material.objects.filter(faculty_id=faculty_id, topic_id=topic_id, is_delete=False)
    #     material = get_object_or_404(queryset, pk=pk)
    #     # Check that the requesting user has permission to download the file, e.g. based on their role or ownership of related objects.
    #     # ...
    #     # Return the file as a response.
    #     try:
    #         response = FileResponse(material.file)
    #     except FileNotFoundError:
    #         return HttpResponseBadRequest("File not found.")
    #     response['Content-Disposition'] = 'attachment; filename=%s' % material.file.name.split('/')[-1]
    #     return response

    
class QuestionImageViewSet(viewsets.ModelViewSet):
    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer


class QuestionPoolCreateNew(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature = self.action
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        elif self.action in [ 'destroy']:
            self.feature = 'delete'
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        # elif self.action in ['list']:
        #     self.feature=self.action
        #     self.permission="QuestionPool"
        #     self.permission_classes=[AdminAndRoleOrFacultyPermission,]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "QuestionPool"
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                self.feature = "edit"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        return super().get_permissions()    

    def create(self,request,*args,**kwargs):
        print("hsahilllllllllllllllllllllllllll")
        try:
            if request.data['user'] != '' and (AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request)):
                useridintokens=AuthHandlerIns.get_id(request)
                request.data['add_user']=useridintokens
                request.data['publish']=True
                questionexist=NewQuestionPool.objects.filter(user=request.data['user'],question_text=request.data['question_text']).exists()
                if questionexist:
                    return Response({"error":"question allready added"},status=status.HTTP_409_CONFLICT)
                else:
                    serializer=QustionpoolNewone(data=request.data)
                    if serializer.is_valid():
                        print('serilizer')
                        serializer.save()
                        return Response({"message":"Question Created Successfully"},status=status.HTTP_201_CREATED)
                    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                print("faculty")
                useridintoken=AuthHandlerIns.get_id(request)
                if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
                     request.data['publish']=True
                else:
                    request.data['publish']=False
                getuser=User.objects.get(id=useridintoken)
                print(getuser)
                request.data['user']=useridintoken
                request.data['add_user']=useridintoken
                data=request.data
                print(data,'data')
                data['user']=useridintoken
                questionexist=NewQuestionPool.objects.filter(user=getuser,question_text=data['question_text']).exists()
                if questionexist:
                    return Response({"error":"question allready added"},status=status.HTTP_409_CONFLICT)
                else:
                    serializer=QustionpoolNewone(data=request.data)
                    if serializer.is_valid():
                        print('serilizer')
                        serializer.save()
                        return Response({"message":"Question created successfully"},status=status.HTTP_201_CREATED)
                    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error":"something went wrong","message":e},status=500)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        try:
            if request.data['user'] != '' and (AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request)):
                data = request.data.copy()  # Make a copy of the request data
                serializer = self.get_serializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                useridintoken = AuthHandlerIns.get_id(request)
                data = request.data.copy()  # Make a copy of the request data
                data['user'] = useridintoken  # Add the user ID to the question data
                serializer = self.get_serializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "something went wrong"},status=500)
    def get_serializer_class(self):
            return self.serializer_class
    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Listing is not allowed.")
    def retrieve(self, request, *args, **kwargs):
        raise PermissionDenied("Retrieving individual question instances by ID is not allowed.")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if AuthHandlerIns.is_faculty(request=self.request):
            id=AuthHandlerIns.get_id(request=self.request)
            # Check if the user is faculty, and if so, ensure they can only delete their own question
            if instance.user.id != id:
                raise PermissionDenied("You do not have permission to delete this question.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionPaperGeneration(viewsets.ModelViewSet):
    queryset=QuestionPaper.objects.all()
    serializer_class=QuestionPaperSerilizer
    pagination_class = SinglePagination

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method=='PATCH':
            return QuestionPaperSerilizer
        else:
            return GetQuestionPaperSerilizer

    def create(self, request, *args, **kwargs):
        # Extract the image data from the "data:image/png;base64,..." format
        icon_data = request.data.get('banner', None)
        notes_file=request.data.get('notes', None)
        if icon_data:
            _, image_data = icon_data.split(';base64,')
            
            # Decode the base64 data and create a ContentFile
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')

            request.data['banner'] = content_file
        if notes_file:
            _, image_data = icon_data.split(';base64,')
            
            # Decode the base64 data and create a ContentFile
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')

            request.data['notes'] = content_file

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        icon_data = request.data.get('banner', None)
        notes_file = request.data.get('notes', None)
        if icon_data:
            _, image_data = icon_data.split(';base64,')
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')
            request.data['banner'] = content_file
        if icon_data:
            _, image_data = icon_data.split(';base64,')
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')
            request.data['notes'] = content_file

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionSearchView(viewsets.ReadOnlyModelViewSet):
    serializer_class = QustionpoolNew

    def get_queryset(self):
        queryset = NewQuestionPool.objects.all().order_by('id')

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)

        course = self.request.query_params.get('course', None)
        if course is not None:
            queryset = queryset.filter(course=course)

        level = self.request.query_params.get('level', None)
        if level is not None:
            queryset = queryset.filter(level=level)

        topic = self.request.query_params.get('topic', None)
        if topic is not None:
            queryset = queryset.filter(topic=topic)

        subject = self.request.query_params.get('subject', None)
        if subject is not None:
            queryset = queryset.filter(subject=subject)

        qtype = self.request.query_params.get('type', None)
        if qtype is not None:
            queryset = queryset.filter(type=qtype)

        user_type = self.request.query_params.get('user_type', None)
        if user_type == 'faculty':
            queryset = queryset.filter(user__is_faculty=True)
        elif user_type == 'admin':
            queryset = queryset.filter(user__is_superuser=True)

        return queryset
    
class RoleUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_roleuser=True)
    serializer_class = RoleUserSerializer
    pagination_class = SinglePagination
    permission_classes =[AdminAndRolePermission]

    def get_queryset(self):
        queryset=User.objects.filter(is_roleuser=True)
        id = self.request.query_params.get('id')
        username = self.request.query_params.get('username')
        email = self.request.query_params.get('email')
        mobile = self.request.query_params.get('mobile')
        branch = self.request.query_params.get('branch')
        if id:
            queryset=queryset.filter(id=id)
        if username:
            queryset=queryset.filter(username__icontains=username)
        if email:
            queryset=queryset.filter(email__icontains=email)
        if mobile:
            queryset=queryset.filter(mobile__startswith=mobile)
        if branch:
            branchs=Branch.objects.filter(name__icontains=branch).values_list('user')
            queryset=queryset.filter(id__in=branchs)



        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # excel = queryset_to_excel(queryset,['id','name'])
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
            fields = ['id', 'username', 'email', 'mobile']
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
            nameheading = 'Inhouse Faculty'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'roleuser.pdf')  
            return resp
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class NewQuestionPoolViewSet(viewsets.ModelViewSet):
    serializer_class = QustionpoolNew
    queryset = NewQuestionPool.objects.all()
    pagination_class = SinglePagination

    @action(detail=False, methods=['GET'])
    def topic_question_count(self, request):
        user_id = request.query_params.get('user_id')

        # Retrieve faculty course additions for the user
        courses = FacultyCourseAddition.objects.filter(user=user_id, status='approved')

        topics=[]
        for x in courses:
           topics.append(x.topic.pk)

        topic_count = NewQuestionPool.objects.filter(user=user_id).values('topic__name', 'topic__id', 'publish')\
            .annotate(count=Count('id'), questions_count=Count('id', filter=Q(status=True)))\
            .order_by('topic__id')
        topic_list = []
        faculty_courses = courses.filter(user=user_id,topic__in=topics)
        print(faculty_courses,'facult')
        for faculty_course in faculty_courses:
            faculty_course_data = {
                'category_id': faculty_course.category.pk,
                'category': faculty_course.category.name,
                'level_id': faculty_course.level.pk,
                'level': faculty_course.level.name,
                'course_id': faculty_course.course.pk,
                'course': faculty_course.course.name+"-"+faculty_course.course.batch_type.name,
                'subject_id': faculty_course.subject.pk,
                'subject': faculty_course.subject.name,
                'module_id': faculty_course.module.pk,
                'module': faculty_course.module.name,
                'topic_id': faculty_course.topic.pk,
                'topic': faculty_course.topic.name,
                'count':NewQuestionPool.objects.filter(user=user_id,topic=faculty_course.topic.pk).count(),
                'topic_name': faculty_course.topic.name,
                'publish':NewQuestionPool.objects.filter(user_id=user_id, topic_id=faculty_course.topic.pk, publish=True).exists()

                    
                  
                }
        
            topic_list.append(faculty_course_data)
        return Response(topic_list)



class ApprovedFacultiesListForHistory(APIView):
    
    serializer_class = FacultySerializer

    def get_queryset(self):
        approved_additions = FacultyCourseAddition.objects.filter(is_approved=True)
        print(approved_additions)
        queryset = Faculty.objects.filter(is_blocked=False, user__in=approved_additions.values('user'))
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class PasswordResetStaff(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        print(kwargs['pk'],"id",request.data.get('newpassword'))
        if AuthHandlerIns.is_staff(request=request):
            
            user = User.objects.get(id=kwargs['pk'])
            new_password = request.data.get('newpassword')
            # print(new_password,"new")
            # user.password = AuthHandlerIns.get_password_hash(new_password)
            # # user.set_password(new_password)
            # user.save()
            # user.password = new_password
            user.set_password(new_password)
            user.save()
            return Response({"message":"Success"})
        else:
            return Response({"message":"Only Admin Can Change Password"},status=status.HTTP_401_UNAUTHORIZED)
        

    
class PassWordVerify(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        id=AuthHandlerIns.get_id(request=request)
        print(id)
        user = User.objects.get(id = id) 
        password  = request.data.get("password")
        if check_password(password,user.password):
            return Response(True)
        else:
            return Response(False)
        

class FacultyImageViewSet(viewsets.ModelViewSet):
    queryset = QuestionFile.objects.all()
    serializer_class = FacultyFileSerializer



@api_view(['POST'])
def Update_Faculty_File(request, faculty_id):  # We are actually passing userid####
    try:
        img=QuestionImage.objects.get(id=request.data['photo']).questionimage
        # print(type(img.name),"mmmmm")
        # return
        imgdata= urllib.request.urlopen(img.url).read()
        image_file = ContentFile(imgdata, name=f'{img.name}')
        image_file=File(image_file)
        idcard=QuestionFile.objects.get(id=request.data['id_card']).facultyfile
        print(idcard,"=ssss")
        iddata= urllib.request.urlopen(idcard.url).read()
        id_file = ContentFile(iddata, name=f'{idcard.name}')
        id_file=File(id_file)
        resume=QuestionFile.objects.get(id=request.data['resume']).facultyfile
        resumedata= urllib.request.urlopen(resume.url).read()
        resume_file = ContentFile(resumedata, name=f'{resume.name}')
        resume_file=File(resume_file)
        print(image_file,'imggg',resume_file,id_file)
        faculty = Faculty.objects.filter(user=faculty_id).update(identity_card=id_file,resume=resume_file,photo=image_file)
        print("kkkkkkkkkkkkkk")
        return Response({'status':True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e,"eeeeee")
        faculty = Faculty.objects.get(user=faculty_id)
        print(faculty.user.id)
        user = User.objects.get(id=faculty.user.id)
        user.delete()
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    


class FacultyImagesUpdateByadmin(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultyPhotoSerializer
    # permission_classes = [AdminAndRolePermission]

    # @create_history_user__decorator
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    # @set_history_user_delete
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs) 


class FacultyCourseAdditionDelete(APIView):
    def delete(self, request, pk, *args, **kwargs):
        if not AuthHandlerIns.is_staff(request=request):
            return Response({"message": "Only admin can verify faculty subject"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            faccourse = FacultyCourseAddition.objects.get(id=pk)
            faccourse.delete()
            return Response({"message": "Faculty course addition deleted successfully."}, status=status.HTTP_200_OK)
        except (FacultyCourseAddition.DoesNotExist, Faculty.DoesNotExist) as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.exceptions import MethodNotAllowed
    
class FacultyApprovedCoursesViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    @action(detail=False, methods=['GET'])
    def approved_faculty(self, request):
        # queryset_Course = FacultyCourseAddition.objects.filter(is_approved = True).values('user').distinct()
        # queryset = Faculty.objects.filter(is_blocked = False,user__in = queryset_Course)
        queryset = Faculty.objects.filter(is_verified = True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
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

  

class FacultyWithSubjectViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySubjectGetSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        queryset = FacultyCourseAddition.objects.filter(subject=subject_id).order_by('user').distinct('user')
        return queryset

    
class InhouseFacultyList(viewsets.ModelViewSet):
    queryset = Faculty.objects.filter(inhouse_fac=True)
    serializer_class =facultyviewDetails
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
           inhouse_fac=True, is_verified=True, is_rejected=False).order_by('-joined_date')

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
            nameheading = 'Inhouse Faculty'
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

class QuestionViewSets(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionPoolSerializer
    pagination_class = SinglePagination
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRoleOrFacultyPermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            user_id=self.request.query_params.get('user_id')
        else:
            user_id=AuthHandlerIns.get_id(request=self.request)
        user_type=self.request.query_params.get('user_type')
        category_id = self.request.query_params.get('category_id')
        level_id = self.request.query_params.get('level_id')
        course_id = self.request.query_params.get('course_id')
        subject_id = self.request.query_params.get('subject_id')
        module_id = self.request.query_params.get('module_id')
        topic_id = self.request.query_params.get('topic_id')
        subtopic_id = self.request.query_params.get('subtopic_id')
        question_type = self.request.query_params.get('type')
        question_text = self.request.query_params.get('question_text')
        question_id=self.request.query_params.get('id')
        username=self.request.query_params.get('username')
        
        ##queryset based on faculty a
        if AuthHandlerIns.is_faculty(request=self.request):
            queryset = NewQuestionPool.objects.filter(user=user_id).order_by('-created_at')
        else:
            # queryset = NewQuestionPool.objects.filter(publish=True)
            queryset = NewQuestionPool.objects.all().order_by('-created_at')
        
        if user_id:
            queryset=queryset.filter(user=user_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        if module_id:
            queryset = queryset.filter(module_id=module_id)

        if category_id:
            queryset = queryset.filter(categorys_id=category_id)

        if level_id:
            queryset = queryset.filter(levels_id=level_id)

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)

        if question_type:
            queryset = queryset.filter(type=question_type)

        if user_type=='admin':
            queryset=queryset.filter(user__is_superuser=True)
        elif user_type=='faculty':
            queryset=queryset.filter(user__is_faculty=True)

        if subtopic_id:
            queryset = queryset.filter(subtopic_id=subtopic_id)
    
        if question_text:
            queryset=queryset.filter(Q(question_text__icontains=question_text))

        if question_id:
            queryset=queryset.filter(Q(id=question_id))
        
        if username:
            queryset=queryset.filter(Q(user__username__icontains=username))
           
            
        return queryset

class QuestionViewSetsPublishedAll(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionPoolSerializer
    pagination_class = SinglePagination
    # def get_permissions(self):
    #     """Set custom permissions for each action."""
    #     if self.action in ['list']:
    #         self.feature=self.action
    #         self.permission="QuestionPool"
    #         self.permission_classes=[AdminAndRoleOrFacultyPermission,]
    #     return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            user_id=self.request.query_params.get('user_id')
        else:
            user_id=AuthHandlerIns.get_id(request=self.request)
        user_type=self.request.query_params.get('user_type')
        category_id = self.request.query_params.get('category_id')
        level_id = self.request.query_params.get('level_id')
        course_id = self.request.query_params.get('course_id')
        subject_id = self.request.query_params.get('subject_id')
        module_id = self.request.query_params.get('module_id')
        topic_id = self.request.query_params.get('topic_id')
        subtopic_id = self.request.query_params.get('subtopic_id')
        question_type = self.request.query_params.get('type')
        question_text = self.request.query_params.get('question_text')
        question_id=self.request.query_params.get('id')
        username=self.request.query_params.get('username')
        
        ##queryset based on faculty a
        if AuthHandlerIns.is_faculty(request=self.request):
            queryset = NewQuestionPool.objects.filter(user=user_id)
        else:
            queryset = NewQuestionPool.objects.filter(publish=True)
            # queryset = NewQuestionPool.objects.all()
        
        if user_id:
            queryset=queryset.filter(user=user_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        if module_id:
            queryset = queryset.filter(module_id=module_id)

        if category_id:
            queryset = queryset.filter(categorys_id=category_id)

        if level_id:
            queryset = queryset.filter(levels_id=level_id)

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)

        if question_type:
            queryset = queryset.filter(type=question_type)

        if user_type=='admin':
            queryset=queryset.filter(user__is_superuser=True)
        elif user_type=='faculty':
            queryset=queryset.filter(user__is_faculty=True)

        if subtopic_id:
            queryset = queryset.filter(subtopic_id=subtopic_id)
    
        if question_text:
            queryset=queryset.filter(Q(question_text__icontains=question_text))

        if question_id:
            queryset=queryset.filter(Q(id=question_id))
        
        if username:
            queryset=queryset.filter(Q(user__username__icontains=username))
           
            
        return queryset
class QuestionCourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = QuestionCourseSerializer

    @action(detail=True, methods=['get'], url_path='question-count')
    def question_count(self, request, pk=None):
        course = self.get_object()
        question_count = NewQuestionPool.objects.filter(course=course).count()
        return Response({'question_count': question_count})
    

import pandas as pd
# class ExcelQuestionPoolCreate(viewsets.ModelViewSet):
#     queryset = NewQuestionPool.objects.all()
#     serializer_class = QustionpoolNew

#     def create(self, request, *args, **kwargs):
#         file_obj = request.FILES['file']  # Get the uploaded file
#         df = pd.read_excel(file_obj)  # Load the Excel file into a pandas dataframe
#         print("**********")
#         topic = df['Topic Id']
#         print(topic,'topic dasfasfid')
#         print("^^^^^^^^^^")
#         data = []  # List to store the data to be added to the model
       
#         # Loop through each row in the dataframe and create a dictionary of values for the new question
#         for index, row in df.iterrows():
#             question_data = {
#                 'user': 1,  # Set the current user as the user who created the question
#                 # 'categorys': row['Category'],  # Set the category based on the Category column in the Excel file
#                 'categorys': 1, 
#                 # 'levels': row['Level'],  # Set the level based on the Level column in the Excel file
#                  'levels': 1,
#                 # 'course': row['Course'],  # Set the course based on the Course column in the Excel file
#                 'course': 1,
#                 'subject': 1,  # Set the subject based on the Subject column in the Excel file
#                 # 'module': row['Module'],  # Set the module based on the Module column in the Excel file
#                  'module': 1,
#                 # 'topic': row['Topic'],  # Set the topic based on the Topic column in the Excel file
#                  'topic': row['Topic Id'],
#                 'question_text': row['Question'],  # Set the question text based on the Question column in the Excel file
#                 'option_1': row['OptionA'],  # Set option 1 based on the OptionA column in the Excel file
#                 'option_2': row['OptionB'],  # Set option 2 based on the OptionB column in the Excel file
#                 'option_3': row['OptionC'],  # Set option 3 based on the OptionC column in the Excel file
#                 'option_4': row['OptionD'],  # Set option 4 based on the OptionD column in the Excel file
#                 'answer': 'option_1',  # Set the answer based on the Answer column in the Excel file
#                 'type': 1,  # Set the type based on the Type column in the Excel file
                
#             }
#             data.append(question_data)  # Add the dictionary to the list of data to be added
        
#         serializer = self.get_serializer(data=data, many=True)  # Create the serializer with the list of data
#         serializer.is_valid(raise_exception=True)  # Check that the data is valid
#         self.perform_create(serializer)  # Add the questions to the model

#         return Response(serializer.data)
import requests
from course.views import  getsubtopic, gettopic
class ExcelQuestionPoolCreateNew(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all()
    serializer_class = QustionpoolNew

    def create(self, request, *args, **kwargs):
        try:
            useridintoken=AuthHandlerIns.get_id(request)
            print(useridintoken)
            getuser=User.objects.get(id=useridintoken)
            print(getuser)
            file_obj = request.FILES['file']  # Get the uploaded file
            df = pd.read_excel(file_obj)  # Load the Excel file into a pandas dataframe
            data = []  # List to store the data to be added to the model
            # topic_details = gettopic(request._request, 2)
            # print(topic_details.data,'*********************')
            # print(topic_details['category_id'])
            # Loop through each row in the dataframe and create a dictionary of values for the new question
            for index, row in df.iterrows():
                print("vv")
                # Call the gettopic function with the topic_id parameter to get the details of the topic
                topic_id = row['SubTopicId']
                id=topic_id
                print(topic_id)
                # topic_details = gettopic(request, topic_id).data[0]
                print(request._request,'###############')
                request._request.method = "GET"  # Set the method attribute of the request object to "GET"
                print(request._request,'###############')
                topic_details = getsubtopic(request._request, id)
                print("^^^^^^^^^^^^^kjkjjj")
                print(topic_details,'topic details')
                print(topic_details.data,'daaaaaaaaaaaaaaaa')
                # print(topic_details.data['category_id'])
                category_id = topic_details.data[0]['category_id']
                level_id = topic_details.data[0]['level_id']
                course_id = topic_details.data[0]['course_id']
                subject_id = topic_details.data[0]['subject_id']
                module_id = topic_details.data[0]['module_id']
                topic_id=topic_details.data[0]['topic']
                print(category_id,'YYYYYYYYYYYYYYYYYYY')
                answer=row['Answer']
                answerhint=row['Answer_Hint']
                answerhints=str(answerhint)
                if answerhints=='nan':
                    answerhints=None
                else:
                    answerhints=row['Answer_Hint']
                print(answer,'anssssssssssssssss')
                try:
                    if answer=='A':
                        answer='option_1'
                    elif answer=='B':
                        answer='option_2'
                    elif answer=='C':
                        answer='option_3'
                    elif answer=='D':
                        answer='option_4'
                    else:
                        answer='option_5'
                except:
                    print("OOOOOOOOOOOOOOOOO")
                    pass

                # try:
                #     if row['OptionE']:
                #         print('7777777s')
                #         if str(row['OptionE'])=='nan':
                #             print('dddddddddddddd')
                #             row['OptionE']=None
                # except:
                #     pass
            
                print('99999999999999999')
                print(row['Type'],'**************cccc')
                print(type(row['Type']),'SSSSSSSSSSSSSSSSS')
                if row['Type']=='simple':
                    row['Type']=2
                elif row['Type']=='medium':
                    row['Type']=1
                elif row['Type']=='tough':
                    row['Type']=3
                elif row['Type']=='all':
                    row['Type']=4
            
                    
                # if row['Type']
            
                
                
                question_data = {
                    'user': useridintoken,  # Set the current user as the user who created the question
                    'categorys': category_id,  # Set the category based on the category ID of the topic
                    'levels': level_id,  # Set the level based on the level ID of the topic
                    'course': course_id,  # Set the course based on the course ID of the topic
                    'subject': subject_id,  # Set the subject based on the subject ID of the topic
                    'module': module_id,  # Set the module based on the module ID of the topic
                    'topic': topic_id,
                    'subtopic':id, # Set the topic based on the topic ID in the Excel file
                    'question_text': row['Question'],  # Set the question text based on the Question column in the Excel file
                    'option_1': row['OptionA'],  # Set option 1 based on the OptionA column in the Excel file
                    'option_2': row['OptionB'],  # Set option 2 based on the OptionB column in the Excel file
                    'option_3': row['OptionC'],  # Set option 3 based on the OptionC column in the Excel file
                    'option_4': row['OptionD'],  # Set option 4 based on the OptionD column in the Excel file
                    # 'option_5': row['OptionE'],
                    'answer': answer,  # Set the answer based on the Answer column in the Excel file
                    'type': row['Type'],  # Set the type based on the Type column in the Excel file
                    'answerhint':answerhints
                }
                data.append(question_data)  # Add the dictionary to the list of data to be added
                
                 


              
                print(data,'data')
                
            serializer = self.get_serializer(data=data, many=True)  # Create the serializer with the list of data
            serializer.is_valid(raise_exception=True)  # Check that the data is valid
            self.perform_create(serializer)  # Add the questions to the model

            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({"error":"something went wrong","exception":error_message})

class ExcelAddingDtpSections(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all()
    serializer_class = QustionpoolNewone
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature=self.action
            self.permission="QuestionPool"
            print("****")
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()  
    

    def create(self, request, *args, **kwargs):
        try:
            useridintoken=AuthHandlerIns.get_id(request)
            getuser=User.objects.get(id=useridintoken)
            file_obj = request.FILES['file']  # Get the uploaded file
            userid=request.data['userid']
            df = pd.read_excel(file_obj)  # Load the Excel file into a pandas dataframe
            data = []  # List to store the data to be added to the model
            for index, row in df.iterrows():
                # Call the gettopic function with the topic_id parameter to get the details of the topic
                topic_id = row['SubTopicId']
                id=topic_id
                # topic_details = gettopic(request, topic_id).data[0]
                request._request.method = "GET"  # Set the method attribute of the request object to "GET"
                topic_details = getsubtopic(request._request, id)
                category_id = topic_details.data[0]['category_id']
                level_id = topic_details.data[0]['level_id']
                course_id = topic_details.data[0]['course_id']
                subject_id = topic_details.data[0]['subject_id']
                module_id = topic_details.data[0]['module_id']
                topic_id=topic_details.data[0]['topic']
                answer=row['Answer']
                answerhint=row['Answer_Hint']
                answerhints=str(answerhint)
                if answerhints=='nan':
                    answerhints=None
                else:
                    answerhints=row['Answer_Hint']
                try:
                    if answer=='A':
                        answer='option_1'
                    elif answer=='B':
                        answer='option_2'
                    elif answer=='C':
                        answer='option_3'
                    elif answer=='D':
                        answer='option_4'
                    else:
                        answer='option_5'
                except:
                    pass
            
                if row['Type']=='simple':
                    row['Type']=2
                elif row['Type']=='medium':
                    row['Type']=1
                elif row['Type']=='tough':
                    row['Type']=3
                elif row['Type']=='all':
                    row['Type']=4
            
                
                question_data = {
                    'user': userid,  # Set the current user as the user who created the question
                    'categorys': category_id,  # Set the category based on the category ID of the topic
                    'levels': level_id,  # Set the level based on the level ID of the topic
                    'course': course_id,  # Set the course based on the course ID of the topic
                    'subject': subject_id,  # Set the subject based on the subject ID of the topic
                    'module': module_id,  # Set the module based on the module ID of the topic
                    'topic': topic_id,
                    'subtopic':id, # Set the topic based on the topic ID in the Excel file
                    'question_text': row['Question'],  # Set the question text based on the Question column in the Excel file
                    'option_1': row['OptionA'],  # Set option 1 based on the OptionA column in the Excel file
                    'option_2': row['OptionB'],  # Set option 2 based on the OptionB column in the Excel file
                    'option_3': row['OptionC'],  # Set option 3 based on the OptionC column in the Excel file
                    'option_4': row['OptionD'],  # Set option 4 based on the OptionD column in the Excel file
                    # 'option_5': row['OptionE'],
                    'answer': answer,  # Set the answer based on the Answer column in the Excel file
                    'type': row['Type'],  # Set the type based on the Type column in the Excel file
                    'add_user':useridintoken,
                    # 'publish':True
                    'answerhint':answerhints
                }
                data.append(question_data)  # Add the dictionary to the list of data to be added
                
            serializer = self.get_serializer(data=data, many=True)  # Create the serializer with the list of data
            serializer.is_valid(raise_exception=True)  # Check that the data is valid
            self.perform_create(serializer)  # Add the questions to the model

            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({"error":"something went wrong","exception":error_message})


import requests
from course.views import gettopic
class ExcelQuestionget(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all()
    serializer_class = QustionpoolNew

    def create(self, request, *args, **kwargs):
        try:
            useridintoken=AuthHandlerIns.get_id(request)
            getuser=User.objects.get(id=useridintoken)
            file_obj = request.FILES['file']  # Get the uploaded file
            df = pd.read_excel(file_obj)  # Load the Excel file into a pandas dataframe
            data = []  # List to store the data to be added to the model
            for index, row in df.iterrows():
                # Call the gettopic function with the topic_id parameter to get the details of the topic
                subtopic_id = row['SubTopicId']
                id=subtopic_id
                request._request.method = "GET"  # Set the method attribute of the request object to "GET"
                # print(request._request,'###############')
                topic_details = getsubtopic(request._request, id)
                category_id = topic_details.data[0]['category_id']
                level_id = topic_details.data[0]['level_id']
                course_id = topic_details.data[0]['course_id']
                subject_id = topic_details.data[0]['subject_id']
                module_id = topic_details.data[0]['module_id']
                topic_id=topic_details.data[0]['topic']
                answer=row['Answer']
                answerhint=row['Answer_Hint']
                answerhints=str(answerhint)
                if answerhints=='nan':
                    answerhints='null'
                else:
                    answerhints=row['Answer_Hint']
                question_data = {
                    'user': useridintoken, 
                    'categorys': category_id,  
                    'levels': level_id,  
                    'course': course_id,  
                    'subject': subject_id, 
                    'module': module_id,  
                    'topic': topic_id,
                    'subtopic':id,
                    'question_text': row['Question'], 
                    'option_1': row['OptionA'],  
                    'option_2': row['OptionB'], 
                    'option_3': row['OptionC'], 
                    'option_4': row['OptionD'],         
                    'answer': answer, 
                    'type': row['Type'],
                    'answerhint':answerhints
                    
                }
                data.append(question_data)  

            return Response(data)
        except Exception as e:
            error_message = str(e)
            return Response({"error": "something went wrong", "exception": error_message})


# class MaterialViewSet(viewsets.ModelViewSet):
#     queryset = Material.objects.all()
#     serializer_class = MaterialUploadGetSerializer


from django.db.models import Q

class FacultyCourseAdditionViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = MaterialTopicSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user']=self.request.query_params.get('user_id')
        return context

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = Topic.objects.filter(facultycourseaddition__user=user_id, facultycourseaddition__status='approved').order_by('name').distinct('name')
        queryset = queryset.prefetch_related('materials')
        

        return queryset

class FacultyCourseApprovedViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseApproveNewSerializer  
    # permission_classes = [AdminAndRoleOrFacultyPermissi
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
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
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
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        fac=FacultyCourseAddition.objects.filter(user__id=user_id,status='approved').distinct('course').values('course')
        queryset = Course.objects.filter(id__in=fac,active=True).order_by('name')
        return queryset
    

# class FacultyApprovedCourseDetailsViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         print("Inside")
#         course_id = self.request.query_params.get('course_id')
#         course = Course.objects.filter(id=course_id).values()
#         course_det = []
#         for i in course:
#             # print(i.id)
            
#             subject = Subject.objects.filter(course=i['id']).values()

#             course_det.append({"subject":subject})
#             for sub in subject:
#                 # print("in sub")
#                 # print(sub['id'])
#                 module = Module.objects.filter(subject=sub['id']).values()
#                 course_det.append({"Module":module})
#                 # print(course_det)
#                 for mod in module:
#                     topic = Topic.objects.filter(module=mod['id']).values()
#                     course_det.append({"Topic":topic})
#                     for top in topic:
#                         subtopic = SubTopic.objects.filter(topic=top['id']).values()
#                         course_det.append({"subtopic":subtopic})
#         print(course_det)
#         return Response({"hh":course_det})


    
# class FacultyCourseAdditionViewSet(viewsets.ModelViewSet):
#     queryset = Topic.objects.all()
#     serializer_class = MaterialTopicSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)

#         # Include materials for each topic
#         for topic, data in zip(queryset, serializer.data):
#             materials = topic.materials.all()
#             material_serializer = MaterialSerializer(materials, many=True)
#             data['materials'] = material_serializer.data

#         return Response(serializer.data)
class MaterialCRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class PublishDraftQuestuion(viewsets.ViewSet):
    def update(self, request, pk=None):
        user_id = request.data['user_id']
        questions = NewQuestionPool.objects.filter(topic_id=pk, user_id=user_id)    
        countofqustions=questions.count()
        for i,question in enumerate(questions,start=1):
            if question.publish==False:
                question.publish=True
                question.save()
            else:
                question.publish=False
                question.save()

            if i==countofqustions:
                if question.publish==True:
                    message="update {} questions True suceesfully".format(countofqustions)
                    return Response({"message":message,"publish":"True"},status=200)
                else:
                    question.publish==False
                    message="update {} questions False suceesfully".format(countofqustions)
                    return Response({"message":message,"publish":"False"},status=200)
            else:
                pass
        return Response({"message":"No question found"},status=403)




class DeleteQuestionAll(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    allowed_methods = ['GET', 'DESTROY']  # Specify allowed methods
    
    def get_queryset(self):
        return self.queryset  # Return the queryset
    
    def list(self, request, *args, **kwargs):
        print('kkk')
        # Delete all instances of NewQuestionPool
        print(self.queryset,'dddd')
        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StudioVideoCourse(viewsets.ModelViewSet):
    queryset = StudioCourse.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return StudioCourseSeializerforCrating
        elif self.action == 'list':
            return StudioCourseSeializerforList
        return StudioCourseSeializerforList  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer,'dkkk')
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudioCourseSeializerforCrating(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class StudionNames(viewsets.ModelViewSet):
    queryset=StudioNames.objects.all()
    serializer_class=StudionameSerializer


class FacultyApplicationsViews(viewsets.ViewSet):
    # queryset=FacultyStudioApplication.objects.all()
    # serializer_class=FacultyStudioApplicationSerializer

    def list(self,request):
        print('(((((())))))')
        if  AuthHandlerIns.is_staff(request=request): 
            print("is staff")   
            queryset=FacultyStudioApplication.objects.all()
            serializers=FacultyStudioApplicationSerializer(queryset,many=True)
            return Response(serializers.data,status=200)
        elif AuthHandlerIns.is_faculty(request=request):
            print('******************')
            print('kkkkdddkkk')
            id=AuthHandlerIns.get_id(request)
            print(id,'faculty id')
            
            facultycourse=Faculty.objects.filter(user=id,modeofclasschoice__in=['2','3'])
            print(facultycourse,'faculty')
            if facultycourse:
                topics = StudioCourse.objects.filter(topic__in=FacultyCourseAddition.objects.filter(user=id,status='approved').values('topic'))
                # serializers=StudioCourseSeializer(topics,many=True)
                serializers = StudioCourseSeializer(topics, many=True, context={'request': id})

                print(topics,'topics ')
                print('fff')
                return Response(serializers.data,status=200)
        else:
            return Response(status=401)
    def post(self,request):
        serializers=FacultyStudioApplicationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'staus':'create'},status=201)
        return Response({'staus':False},status=403)


class addexcels3(viewsets.ViewSet):
    def create(self, request):
        file_obj = request.FILES.get('facultyfile')  # Assuming the file field in the request is named 'facultyfile'

        if file_obj is not None:
            question_file = QuestionFile.objects.create(facultyfile=file_obj)
            return Response({'id': question_file.id}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            question_file = QuestionFile.objects.get(pk=pk)
        except QuestionFile.DoesNotExist:
            return Response({'message': 'Question file not found'}, status=status.HTTP_404_NOT_FOUND)

    # Generate the response with the file content
        response = HttpResponse(question_file.facultyfile, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(question_file.facultyfile.name)
        return response
    
class PublishDraftQuestuion(viewsets.ViewSet):
    def update(self, request, pk=None):
        user_id = request.data['user_id']
        questions = NewQuestionPool.objects.filter(topic_id=pk, user_id=user_id)
        questions.update(publish=False)
        return Response(status=200)
########################ADDING MULTIPLE COURSES #########################
# class OnlineCourseAssign(viewsets.ModelViewSet):
#     queryset = StudioCourseAssign.objects.all()
#     serializer_class = VideoAssignmentSerializer

#     def create(self, request, *args, **kwargs):
#         video_assignment_data = request.data.copy()
#         courses = video_assignment_data.pop('courses', [])  # Retrieve the list of courses

#         serializer = self.get_serializer(data=video_assignment_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         # Assign the video to each course
#         video_assignment = serializer.instance
#         if video_assignment is not None:
#             for course_id in courses:
#                 course = Course.objects.get(id=course_id)
#                 video_assignment.course = course
#                 video_assignment.save()

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#########SUBTOPIC EMPTY########################
class OnlineCourseAssign(viewsets.ModelViewSet):
    queryset = StudioCourseAssign.objects.all()
    serializer_class = VideoAssignmentSerializer

    def create(self, request, *args, **kwargs):
        video_assignment_data = request.data.copy()
        courses = video_assignment_data.pop('courses', [])
        subjects = video_assignment_data.pop('subject', [])
        modules = video_assignment_data.pop('module', [])
        topics = video_assignment_data.pop('topic', [])
        subtopics = video_assignment_data.pop('subtopic', [])

        if len(courses) != len(subjects) or len(courses) != len(modules) or len(courses) != len(topics):
            raise serializers.ValidationError("The lengths of the lists do not match.")

        for course_id, subject_id, module_id, topic_id in zip(courses, subjects, modules, topics):
            video_assignment_data_copy = video_assignment_data.copy()
            video_assignment_data_copy['course'] = course_id
            video_assignment_data_copy['subject'] = subject_id
            video_assignment_data_copy['module'] = module_id
            video_assignment_data_copy['topic'] = topic_id

            if subtopics:
                subtopic_id = subtopics.pop(0)
                video_assignment_data_copy['subtopic'] = subtopic_id

            serializer = self.get_serializer(data=video_assignment_data_copy)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





class StudioApplicationApprove(viewsets.ModelViewSet):
    queryset = StudioCourse.objects.all()
    serializer_class = StudioApplicationApproveSerializer

    def partial_update(self, request, pk=None):
        if AuthHandlerIns.is_staff(request):
            print(pk,'paramid')
            studiocourse = self.get_object()  # Retrieve the instance to update
            print(studiocourse,'jjj')
            faculty_id = request.data.get('faculty')  # Get the faculty ID from request data

            # Retrieve the User instance based on the faculty_id
            try:
                faculty = User.objects.get(pk=faculty_id)
                print(faculty,'ddd')
                studiocourse.faculty = faculty
                studiocourse.save()  # Save the updated instance
                try:
                    facapplication=FacultyStudioApplication.objects.get(studiocourse=pk,faculty=faculty_id)
                    facapplication.is_approved=True
                    facapplication.save()
                except:
                    pass
                print(facapplication,'facapplication')
                return Response({"message": "Faculty updated successfully."})

            except User.DoesNotExist:
                return Response({"message": "Invalid faculty ID."}, status=400)

        return Response({"message": "Something went wrong."}, status=401)

class AddVediotoStudioCourse(viewsets.ModelViewSet):
    queryset=StudioVideo.objects.all()
    serializer_class=AddVediotoStudioCourseSerializer
    permission_classes= [AdminAndRolePermission]

class AddVideoToStudioCourse(viewsets.ReadOnlyModelViewSet):
    queryset=StudioVideo.objects.all()
    pagination_class = SinglePagination
    serializer_class=AddVideoToStudioCourseSerializer
    permission_classes= [AdminAndRolePermission]


class NotAssignVedioTopics(viewsets.ModelViewSet):
    queryset=StudioCourse.objects.all()
    # serializer_class=StudioCourseSeializer

    def list(self, request):
        pk = request.query_params.get('id', None)
        # pk = self.args.get('pk')
        print(pk)
        print("*******************")
        course=Course.objects.get(id=pk)
        print(course,'kkkk')
        topic=Topic.objects.filter(module__subject__course=pk).values('id')
        print(topic,"topic")
        studio = self.get_queryset().values('topic').distinct('topic')
        print(studio,"studio")
        # new = topic.exclude(id__in=studio)
        news = Topic.objects.filter(id__in=[i['topic'] for i in studio])
        print(news,'kkkk    ')
        new = Topic.objects.filter(id__in=topic).exclude(id__in=[i['topic'] for i in studio])
        print(new,"new")
        
        return Response(TopicSerializer(new,many=True).data)
 
    



class CountofApplication(viewsets.ViewSet):
    def create(self, request):
        pk = request.query_params.get('id', None)
        print(pk,'******************')
        application=FacultyStudioApplication.objects.filter(studiocourse=pk)
        print(application,'app')
        serializer=TopicApplicationCountSerializer(application,many=True)
        return Response(serializer.data,status=200)
        # Retrieve the count of applications based on topics in the StudioCourse model
        # topic_counts = StudioCourse.objects.values('name').annotate(application_count=models.Count('facultystudioapplication'))

        # Serialize the data
        # serializer = TopicApplicationCountSerializer(topic_counts,many=True)  
        # serializer = TopicApplicationCountSerializer(serializer.data)  
       
    
class CountofApplicationBased(viewsets.ModelViewSet):
    queryset=StudioCourse.objects.all()
    serializer_class=StudiocoursebasedstudioSerializer

    def create(self, request):
        # Retrieve the count of applications based on topics in the StudioCourse model
        courseid=request.data.get('courseid')
        print(courseid,'iddd')
        topiccourse=StudioCourse.objects.filter(topic__module__subject__course=courseid).distinct()
        data=[]
        for topics in topiccourse:
            count=FacultyStudioApplication.objects.filter(studiocourse=topics).count()
            serializer=self.serializer_class(topics)
            serialized_data=serializer.data
            serialized_data['application_count']=count
            data.append(serialized_data)
        
        return Response(data,status=200)



# class TopicStatusVedioCourse(viewsets.ViewSet):
#     def retrieve(self,request,pk):
#         course=Course.objects.filter(id=pk)
#         topic=Topic.objects.filter(module__subject__course=course)
#         print(topic,'ssssha')
#         studiotopiccheck=StudioCourse.objects.filter(topic__in=topic)
#         print(studiotopiccheck,'kkkk')
#         if studiotopiccheck:
#             return Response({"data": DupCourseNewDragSerializer(course, many=True).data})
           
#         else:
#             return Response({"message":"Pending"})
#         serializers=TopicSerializer(topic,many=True)
#         return Response(serializers.data)
#         print(course,'courses')

# class TopicStatusVedioCourse(viewsets.ViewSet):
#     def retrieve(self, request, pk):
#         course = Course.objects.get(id=pk)
#         topics = Topic.objects.filter(module__subject__course=course)
#         print(topics, 'ssssha')
#         studiotopiccheck = StudioCourse.objects.filter(topic__in=topics)
#         print(studiotopiccheck, 'kkkk')
#         if studiotopiccheck:
#             return Response({"data": DupCourseNewDragSerializer(course).data})
#         else:
#             return Response({"message": "Pending"}) 
#         serializer = TopicSerializer(topics, many=True)
#         return Response(serializer.data)
class TopicStatusVedioCourse(viewsets.ViewSet):
    def retrieve(self, request, pk):
        course = Course.objects.get(id=pk)
        subjects = Subject.objects.filter(course=course)
        
        course_data = DupCourseNewDragSerializer(course).data
        course_data['subjects'] = []

        for subject in subjects:
            subject_data = DupSubjectNewDragSerializer(subject).data
            modules = Module.objects.filter(subject=subject)
            subject_data['modules'] = []

            for module in modules:
                module_data = DupModuleNewDragSerializer(module).data
                topics = Topic.objects.filter(module=module)
                module_data['topics'] = []

                for topic in topics:
                    topic_data = DupTopicNewDragSerializer(topic).data

                    # studiotopiccheck = StudioCourse.objects.filter(topic=topic)
                    # print(studiotopiccheck,'kkkk')
                    # print(studiotopiccheck.values())
                    # for studio_course in studiotopiccheck:
                    #     if studio_course.assignvideo:
                    #         print(studio_course.assignvideo,'ddd')
                    #         topic_data['status'] = 'Completed'
                    #         break
                    # else:
                    #     if studiotopiccheck:
                    #         print(studio_course,'dddd')
                    #         topic_data['status'] = 'Scheduled'
                    #     else:
                    #         print('**********dddd')
                    #         topic_data['status'] = 'Pending'
 

                    # studiotopiccheck = StudioCourse.objects.filter(topic=topic)
                    # for x in studiotopiccheck:
                    #     print(x.assignvideo,'##')
                    # print(studiotopiccheck,'topicchekc  ')
                    # if studiotopiccheck:
                    #     print(studiotopiccheck,'studions')
                    #     topic_data['status'] = 'Scheduled'
                    # elif studiotopiccheck.assignvideo==True:
                    #     topic_data['status'] = 'Completed'
                
                    # else:
                    #     topic_data['status'] = 'Pending'

                    module_data['topics'].append(topic_data)

                subject_data['modules'].append(module_data)

            course_data['subjects'].append(subject_data)

        return Response({"data": course_data})
    

class RolesViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.filter().order_by('created_at')
    serializer_class = RolesSerializer

    def update(self, request,pk=None, *args, **kwargs):
        try:
            if request.data['adduser']:
                queryset =self.get_object()
                print(queryset)
                user = User.objects.get(id=request.data['user'][0])
                queryset.user.add(user)
                queryset.save()
                print("heloo")
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
        try:
            if request.data['removeuser']:
                queryset =self.get_object()
                user = User.objects.get(id=request.data['user'][0])
                queryset.user.remove(user)
                queryset.save()
                return Response(status=status.HTTP_200_OK)
        except:
            pass

        return super().update(request, *args, **kwargs)
    

        


    


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionSerializer


class Photoidresumeverification(viewsets.ModelViewSet):
    queryset=Faculty.objects.all()
    serializer_class=FacultySerializerssProfile
    permission_classes= [AdminAndRolePermission, ]

class FacultySubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=False, methods=['get'])
    def distinct_subjects(self, request):
        distinct_subjects = Subject.objects.order_by('subject__name').values('subject__name').distinct('subject__name')
        return Response({'distinct_subjects': list(distinct_subjects.values('subject__name'))})



class UserForRoles(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # pagination_class = SinglePagination

    def get_queryset(self):
        role = self.request.query_params.get('role',None)
        if role:
            role_queryset =Role.objects.get(id=role).user
            queryset = User.objects.filter(is_roleuser=True).exclude(id__in=role_queryset.all().values('id'))
        else:
            queryset = User.objects.filter(is_roleuser=True)
        return queryset
    

class BranchUser(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = Branch.objects.exclude(user__id=user_id)
        else:
            queryset = super().get_queryset()
        return queryset

    def update(self, request,pk=None, *args, **kwargs):
        try:
            if request.data['adduser']:
                queryset =Branch.objects.get(id=request.data['branch'])
                print(queryset)
                user = User.objects.get(id=request.data['user'][0])
                queryset.user.add(user)
                queryset.save()
                print("heloo")
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))
        try:
            if request.data['removeuser']:
                queryset =Branch.objects.get(id=request.data['branch'])
                user = User.objects.get(id=request.data['user'][0])
                queryset.user.remove(user)
                queryset.save()
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))

        return super().update(request, *args, **kwargs)\
        
    # def list(self, request, *args, **kwargs):
    #     user_id = self.request.query_params.get('user',None)
    #     branch= Branch.objects.filter(user__in=user_id)
    #     return branch


class BranchUserlist(viewsets.ModelViewSet):
    serializer_class = BranchSerializer

    # def get_queryset(self):
    #     user_id = self.request.query_params.get('user',None)
    #     if user_id:
    #         branch= Branch.objects.filter(user__in=user_id)
    #         ids= [x['id'] for x in branch.values('id')]
    #         print(branch.values('id'),[x['id'] for x in branch.values('id')])
    #         queryset = Branch.objects.filter().exclude(id__in=ids)
    #     else:
    #         queryset =Branch.objects.all()
    #     return queryset
    
    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user',None)
        if user_id:
            branch= Branch.objects.filter(user__in=User.objects.get(id=user_id))
            ids= [x['id'] for x in branch.values('id')]
            print(branch.values('id'),[x['id'] for x in branch.values('id')])

            queryset = Branch.objects.filter().exclude(id__in=ids)
        # else:
        #     queryset =Branch.objects.all()
            return Response(BranchSerializer(queryset,many=True).data)
        


class BlockRoleUser(viewsets.ModelViewSet):
    serializer_class = RoleUserSerializer
    queryset = User.objects.filter(is_roleuser=True)
    permission_classes = [AdminAndRolePermission]

    def list(self, request, *args, **kwargs):
        """Disable list endpoint"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        """Disable create endpoint"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        """Disable retrieve endpoint"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """Disable destroy endpoint"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request,pk=None, *args, **kwargs):
        user= User.objects.get(id=pk)
        if user.is_roleuser:
            user.is_active= False if user.is_active else True
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
class NotassignedFaculties(viewsets.ViewSet):
    serializer_class=NotassignedFacultiesSerialilzer


    def create(self,request):
        course_id=request.data['courseid']
        print(course_id,'iddd')
        studiocourse=StudioCourse.objects.filter(topic__module__subject__course=course_id,faculty=None)
        print(studiocourse,'fff')
        serializers=NotassignedFacultiesSerialilzer(studiocourse,many=True)
        return Response(serializers.data,status=200)



class AssignedFacultiesList(viewsets.ViewSet):
    serializer_class=StudioassignedFacultiesSerialilzer


    def create(self,request):
        course_id=request.data['courseid']
        print(course_id,'iddd')
        studiocourse=StudioCourse.objects.filter(topic__module__subject__course=course_id,faculty__isnull=False,video__isnull=True)
        print(studiocourse,'fff')
        serializers=StudioassignedFacultiesSerialilzer(studiocourse,many=True)
        return Response(serializers.data,status=200)
    

class VedioAssignedStudio(viewsets.ViewSet):
    serializer_class=vedioassignedStudioSerialilzer


    def create(self,request):
        course_id=request.data['courseid']
        print(course_id,'iddd')
        studiocourse=StudioCourse.objects.filter(topic__module__subject__course=course_id,video__isnull=False)
        print(studiocourse,'fff')
        serializers=vedioassignedStudioSerialilzer(studiocourse,many=True)
        return Response(serializers.data,status=200)






class VideoAPIView(APIView):
    def get(self, request, video_id):
        access_token = vimeo_access_token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        url = f'https://player.vimeo.com/video/{video_id}'
        response = requests.get(url, headers=headers)
        print(response.url, 'data')
        print(response, 'response')
        print(response.content, 'content')

        try:
            # Extract URL using regular expression
            url_regex = r'href="([^"]*)"'
            matches = re.findall(url_regex, response.content.decode())
            if matches:
                video_link = matches[0]
                return Response({'video_link': video_link})
            else:
                return Response({'error': 'Video link not found', "data": response.content},
                                status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            print('Error parsing JSON:', e)
            return Response({'error': 'Error parsing JSON'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)



#####not working properly####
class GetAllVideoAPIViews(APIView):
    def get(self, request):
        access_token = vimeo_access_token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        # Retrieve video data from Vimeo API
        vimeo_url = f'https://vimeo.com/manage/videos'
        response = requests.get(vimeo_url, headers=headers)
        print(response,'res')
        print(response.raw)
        print("^^^^^^^^^^^^^^^^^^^^^")
        print(response.content,'conten')
        print("^^^^^^^^^^^^^^^^^^^^^")
        print("******************")
        print(response.json)
        if response.status_code == 200:
            video_data = response.json()
            videos = video_data.get('data', [])
            
            video_links = []
            
            # Iterate over the videos and extract the video links
            for video in videos:
                video_link = video.get('link')
                if video_link:
                    video_links.append(video_link)
            
            return Response({'video_links': video_links})
        
        else:
            print(f"Error retrieving video data: {response.content}")
            return Response({'error': 'Error retrieving video data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#####end working properly####


class FacultyAssignedStudioCourseStudiouser(viewsets.ModelViewSet):
    serializer_class=vedioassignedStudioSerialilzer
    queryset=StudioCourse.objects.all()


    def list(self, request):
        querysets = StudioCourse.objects.filter(faculty__isnull=False)
        serializer = self.serializer_class(querysets, many=True)  # Fixed serializer_class reference
        return Response(serializer.data, status=status.HTTP_200_OK)

class VidioaddingTovimeoandDb(viewsets.ModelViewSet):
    serializer_class=AddVediotoStudioCourseSerializer

    def create(self,request):
        request_data=request.data
        studiocourse=request.data['studiocourseid']
        file=request.data['file']
        if file:
            print(request_data,'kkkk')
            video_name=request.data['video_name']
            video_description=request.data['video_description']
            print("***********************")
            response_data = upload_video_to_vimeo(file, video_name, video_description)
            print(response_data,'response data')
            if response_data.get('message')=="Video upload complete":
                print("*************************")
                videolinks=response_data['link']
                print(videolinks,'vidoelinkrespone')

                shootingdaytimes=request.data['shootingdaytime']
                shootingenddaytimes=request.data['shootingenddaytime']
                editingdaytimes=request.data['editingdaytime']
                editingenddaytimes=request.data['editingdaytime']
                
                editingstaffs=request.data['editingstaff']
                totalhours=request.data['totalhours']
                faculty=request.data['faculty']
                thumbnail=request.data['thumbnail']
                # videolink=request.data['videolink']
                # faculty=request.data['faculty']
                # studiocourse=request.data['studiocourse']
                # vimeoid=request.data['vimeoid']
                # videolength=request.data['videolength']
                # content=request.data['content']
                # applicationvideo=request.data['applicationvideo']

                serializer = AddVediotoStudioCourseSerializer(data={
                    'name': video_name,
                    'description': video_description,
                    'shootingdaytime': shootingdaytimes,
                    'shootingenddaytime': shootingenddaytimes,
                    'editingdaytime': editingdaytimes,
                    'editingenddaytime': editingenddaytimes,
                    'editingstaff': editingstaffs,
                    'videolink': videolinks,
                    'totalhours':totalhours,
                    'faculty':faculty,
                    'thumbnail':thumbnail 
                })

                if serializer.is_valid():
                    instance = serializer.save()
                    serialized_data = serializer.data
                    serialized_data['id'] = instance.id
                    print(serialized_data['id'], 'dddd')

                    studiocourse = get_object_or_404(StudioCourse, pk=studiocourse)
                    studiovideo = get_object_or_404(StudioVideo, pk=instance.id)
                    studiocourse.video = studiovideo
                    studiocourse.assignvideo = True
                    studiocourse.save()

                    serializerss = vedioassignedStudioSerialilzer(studiocourse)
                    return Response({"vimeoresponse":response_data,"data": serializer.data, "data1": serializerss.data}, status=200)
            else:
                return Response({"message":"upload video to vimeo is failed"},status=500)

        return Response(status=400)
    

class VideoAssigningForCourseEtc(viewsets.ModelViewSet):
    queryset = StudioCourseAssign.objects.all()
    serializer_class = VideoAssignForCourseetcSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("***********")
            video_id = request.data['video']
            video = get_object_or_404(StudioVideo, id=video_id)
            print(video,'video')

            courses = request.data.get('course', [])
            print(courses, 'ddd')
            subjects = request.data.get('subject', [])
            print(subjects, 'ddd')

            modules = request.data.get('module', [])
            print(modules, 'ddd')

            topics = request.data.get('topic', [])
            print(topics, 'ddd')

            subtopics = request.data.get('subtopic', [])
            print(subtopics, 'ddd')

            created_instances = []

            if courses:
                for course_id in courses:
                    print("*********")
                    course = get_object_or_404(Course, id=course_id)
                    print('LLLL')
                    instance = StudioCourseAssign.objects.create(video=video, course=course)
                    created_instances.append(instance)

            if subjects:
                for subject_id in subjects:
                    print("*********")
                    subject = get_object_or_404(Subject, id=subject_id)
                    print(subject, 'ddd')
                    instance = StudioCourseAssign.objects.create(video=video, subject=subject)
                    print(instance,'ddd')
                    created_instances.append(instance)
                    print("%%%")

            if modules:
                for module_id in modules:
                    print("*********")
                    module = get_object_or_404(Module, id=module_id)
                    instance = StudioCourseAssign.objects.create(video=video, module=module)
                    created_instances.append(instance)

            if topics:
                for topic_id in topics:
                    print("*********")
                    topic = get_object_or_404(Topic, id=topic_id)
                    instance = StudioCourseAssign.objects.create(video=video, topic=topic)
                    created_instances.append(instance)

            if subtopics:
                for subtopic_id in subtopics:
                    print("*********")
                    subtopic = get_object_or_404(SubTopic, id=subtopic_id)
                    instance = StudioCourseAssign.objects.create(video=video, subtopic=subtopic)
                    created_instances.append(instance)

            print("*********")
            serializer = self.get_serializer(created_instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "error"}, status=status.HTTP_401_UNAUTHORIZED)



class AllvideoDB(ModelViewSet):
    serializer_class=AddVediotoStudioCourseSerializer
    queryset=StudioVideo.objects.all()


from rest_framework.exceptions import ValidationError


class MaterialUploadViewSet(viewsets.ModelViewSet):
    queryset = MaterialUploads.objects.all().order_by('-created_at')
    serializer_class = MaterialUploadSerializer
    pagination_class = SinglePagination
    ####add permissions
    def get_serializer_class(self):
        if self.action == 'partial_update':
            self.serializer_class = MaterialUploadPatchSerializer

        # Fallback to default serializer class for other actions
        return super().get_serializer_class()
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature = 'create'
            self.permission = "Material"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        elif self.action in [ 'destroy']:
            self.feature = 'delete'
            self.permission = "Material"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        elif self.action in ['list']:
            self.feature=self.action
            self.permission="Material"
            self.permission_classes=[AdminAndRoleOrFacultyPermission,]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Material"
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                self.feature = "edit"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        return super().get_permissions()
    def get_queryset(self):
        user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
        print(user)

        queryset = MaterialUploads.objects.filter()
        if user.is_faculty:
            queryset=queryset.filter(user=user)
        elif user.is_staff or user.is_roleuser:
            user_id = self.request.query_params.get('user_id')
            queryset = queryset.filter(user=user_id)
            print(queryset)
                    
        return queryset
        

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        material_upload = serializer.save()

        # Validate user is faculty
        # if not material_upload.user.is_faculty:
        #     material_upload.delete()
        #     raise ValidationError("Material uploads can only be done by faculty users.")
        
    # def partial_update(self, request, pk=None):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
        
    #     # Validate user is faculty
    #     # if not instance.user.is_faculty:
    #     #     raise ValidationError("Material uploads can only be updated by faculty users.")

    #     serializer.save()

        # return Response(serializer.data, status=status.HTTP_200_OK)


class MaterialAllotedForStudents(ModelViewSet):
    serializer_class = ConvertedMaterialSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        topic_id = self.request.query_params.get('topic_id')
        queryset = ConvertedMaterials.objects.filter(user=user_id, topic=topic_id)
        return queryset

class AllFacultyMaterialAdminViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=AdminViewMaterialUploadSerializer
    queryset = MaterialUploads.objects.all()
    pagination_class = SinglePagination

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = MaterialUploads.objects.filter(user=user_id).order_by('-created_at')
            print(queryset)
        else:
            queryset = MaterialUploads.objects.all().order_by('-created_at')

        return queryset
    
class NewMaterialListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=AdminViewMaterialUploadSerializer
    queryset = MaterialUploads.objects.all()
    pagination_class = SinglePagination
    permission_classes= [AdminAndRolePermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = MaterialUploads.objects.filter(user=user_id,updated_file__isnull=True).order_by('-created_at')
        else:
            queryset = MaterialUploads.objects.filter(updated_file__isnull=True).order_by('-created_at')

        return queryset

class AllPendingMaterialAdminViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=AdminViewMaterialUploadSerializer
    queryset = MaterialUploads.objects.all()
    pagination_class = SinglePagination
    permission_classes= [AdminAndRolePermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = MaterialUploads.objects.filter(Q (user=user_id)& (Q(updated_file__isnull=True) | Q(vstatus_research=False, vstatus_faculty=False))
            ).order_by('-created_at')
        else:
            queryset = MaterialUploads.objects.filter(
            Q(updated_file__isnull=True) & Q(vstatus_research=False, vstatus_faculty=False)).order_by('-created_at')

        return queryset

class AllCompletedMaterialAdminViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=AdminViewMaterialUploadSerializer
    queryset = MaterialUploads.objects.all()
    pagination_class = SinglePagination
    permission_classes= [AdminAndRolePermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = MaterialUploads.objects.filter(Q (user=user_id)& (Q(updated_file__isnull=False) & (Q(vstatus_research=True) | Q(vstatus_faculty=True)))
            ).order_by('-created_at')
        else:
            queryset = MaterialUploads.objects.filter(Q(updated_file__isnull=False) & (Q(vstatus_research=True) | Q(vstatus_faculty=True))
            ).order_by('-created_at')
        return queryset


# class MaterialReferenceViewSet(ModelViewSet):
#     queryset = MaterialReference.objects.all()
#     serializer_class = MaterialReferenceSerializer

#     def create(self, request, *args, **kwargs):
#         user_id = request.data.get('user')
#         material_id = request.data.get('materialupload')
#         category_list = request.data.get('category',[])
#         level_list =request.data.get('level',[])
#         course_list = request.data.get('course',[])
#         subject_list =request.data.get('subject',[])
#         module_list = request.data.get('module',[])
#         topic_list = request.data.get('topic',[])
#         subtopic_list = request.data.get('subtopic',[])

#         max_length = max(len(category_list),len(level_list),len(subject_list),len(module_list),
#                          len(topic_list),len(subtopic_list))
#         for i in range(max_length):
#             category_id = category_list[i] if i < len(category_list) else None
#             level_id = level_list[i] if i < len(level_list) else None
#             course_id = course_list[i] if i < len(course_list) else None
#             subject_id = subject_list[i] if i < len(subject_list) else None
#             module_id = module_list[i] if i < len(module_list) else None
#             topic_id = topic_list[i] if i < len(topic_list) else None
#             subtopic_id = subtopic_list[i] if i < len(subtopic_list) else None
#             category = Category.objects.get(id=category_id) if category_id else None
#             level = Level.objects.get(id=level_id) if level_id else None
#             course = Course.objects.get(id=course_id) if course_id else None
#             subject = Subject.objects.get(id=subject_id) if subject_id else None
#             module = Module.objects.get(id=module_id) if module_id else None
#             topic = Topic.objects.get(id=topic_id) if topic_id else None
#             subtopic = SubTopic.objects.get(id=subtopic_id) if subtopic_id else None
#             materialupload = MaterialUploads.objects.get(id=material_id) 
#             user = User.objects.get(id=user_id)
#             material_reference = MaterialReference.objects.create(
#                 user = user,
#                 materialupload = materialupload,
#                 category = category,
#                 level = level,
#                 course = course,
#                 subject = subject,
#                 module = module,
#                 topic = topic,
#                 subtopic = subtopic
#         )
#         serializer = self.get_serializer(material_reference)
#         return Response(serializer.data,status = status.HTTP_201_CREATED)

class MaterialReferenceViewSet(ModelViewSet):
    queryset = MaterialReference.objects.all()
    serializer_class = MaterialReferenceSerializer
            #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature = 'AssignMaterial'
            self.permission = "Material"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        return super().get_permissions()
    

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        material_id = request.data.get('materialupload')
        category_list = request.data.get('category', [])
        level_list = request.data.get('level', [])
        subject_list = request.data.get('subject', [])
        module_list = request.data.get('module', [])
        if module_list:
            if MaterialReference.objects.filter(materialupload__id=material_id, module__in=module_list).exists():
                raise ValidationError(f"A MaterialReference with this name and topic already exists.")

        topic_list = request.data.get('topic', [])
        if topic_list:
            if MaterialReference.objects.filter(materialupload__id=material_id, topic__in=topic_list).exists():
                raise ValidationError(f"A MaterialReference with this name and topic already exists.")

        subtopic_list = request.data.get('subtopic', [])
        if subtopic_list:
            if MaterialReference.objects.filter(materialupload__id=material_id, subtopic__in=subtopic_list).exists():
                raise ValidationError(f"A MaterialReference with this name and topic already exists.")

        course_list = request.data.get('course', [])

        
        
        non_null_fields = [
            (category_list, 'category'),
            (level_list, 'level'),
            (subject_list, 'subject'),
            (module_list, 'module'),
            (topic_list, 'topic'),
            (subtopic_list, 'subtopic'),
            (course_list,'course')
        ]

        valid_fields = 0
        valid_field_names = []

        for field_list, field_name in non_null_fields:
            if len(field_list) > 0:
                valid_fields += 1
                valid_field_names.append(field_name)

        if valid_fields != 1:
            error_message = f"Only one field should be not null. Fields: {', '.join(valid_field_names)}"
            return Response({'Error': [error_message]}, status=status.HTTP_400_BAD_REQUEST)

        # Existing code to retrieve related objects

        max_length = max(len(category_list),len(level_list),len(subject_list),len(module_list),
                         len(topic_list),len(subtopic_list))
        for i in range(max_length):
            category_id = category_list[i] if i < len(category_list) else None
            level_id = level_list[i] if i < len(level_list) else None
            course_id = course_list[i] if i < len(course_list) else None
            subject_id = subject_list[i] if i < len(subject_list) else None
            module_id = module_list[i] if i < len(module_list) else None
            topic_id = topic_list[i] if i < len(topic_list) else None
            subtopic_id = subtopic_list[i] if i < len(subtopic_list) else None
            materialupload = MaterialUploads.objects.get(id=material_id) 
            user = User.objects.get(id=user_id)
            try:
                category = Category.objects.get(id=category_id) if category_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Category does not exist']}, status=status.HTTP_400_BAD_REQUEST)

            try:
                level = Level.objects.get(id=level_id) if level_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Level does not exist']}, status=status.HTTP_400_BAD_REQUEST)


            try:
                course = Course.objects.get(id=course_id) if course_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Course does not exist']}, status=status.HTTP_400_BAD_REQUEST)

            try:
                subject = Subject.objects.get(id=subject_id) if subject_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Subject does not exist']}, status=status.HTTP_400_BAD_REQUEST)

            
            try:
                module = Module.objects.get(id=module_id) if module_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Module does not exist']}, status=status.HTTP_400_BAD_REQUEST)


            try:
                topic = Topic.objects.get(id=topic_id) if topic_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['Topic does not exist']}, status=status.HTTP_400_BAD_REQUEST)

            try:
                subtopic = SubTopic.objects.get(id=subtopic_id) if subtopic_id else None
            except ObjectDoesNotExist:
                return Response({'Error': ['SubTopic does not exist']}, status=status.HTTP_400_BAD_REQUEST)

            material_reference = MaterialReference.objects.create(
                user = user,
                materialupload = materialupload,
                category = category,
                level = level,
                course = course,
                subject = subject,
                module = module,
                topic = topic,
                subtopic = subtopic
        )
        serializer = self.get_serializer(material_reference)
        return Response(serializer.data,status = status.HTTP_201_CREATED)



    
class StudioCourseallDetails(ModelViewSet):
    serializer_class=studiocoursegetallsdetils
    queryset=StudioCourse.objects.all()
    

class DeleteVideomanuallyAssigning(viewsets.ModelViewSet):
    serializer_class = DeleteVideomanuallyAssigningSerializer
    queryset = StudioCourseAssign.objects.all()

class ConvertedMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = ConvertedMaterialSerializer
    queryset = ConvertedMaterials.objects.all()

        #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = 'AddVerified'
            print(self.request.data,"datdtdas")
            self.permission = "Material"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Material"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Material"
            print(self.request.data,"dadadd")
            if "active" in self.request.data:
                self.feature = "Block"
            else:
                print("yes")
                self.feature = "edit"
                print("PP")
            print("MMMM")
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    def create(self,request,*args,**kwargs):
        file = request.data['file']
        name = request.data['name']
        description = request.data['description']
        faculty = request.data['user']
        faculty = User.objects.get(id=faculty)
        print(faculty,"FACC")
        created_by = request.data['created_by']
        created_by = User.objects.get(id=created_by)
        print(created_by,"CREBY")
        try:
            active = request.data['active']
        except:
            active = False
        ######ManyToMany relationship###
        upload = request.data.get('uploads', [])
        print(upload)
        # upload = request.data['upload']
        upload_list = eval(upload)


        

        topic = request.data['topic']
        topic_list = eval(topic)
        

        converted_materials = ConvertedMaterials.objects.create(
                                file = file,
                                name = name,
                                description = description,
                                user =faculty,
                                created_by = created_by,
                                active = active

        )
        converted_materials.uploads.set(upload_list)
        converted_materials.topic.set(topic_list)
        serializer = self.serializer_class(converted_materials)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        upload = request.data.get('uploads', [])
        if upload:
            if not isinstance(upload, str):
                return Response({'error': 'Upload must be a string'}, status=status.HTTP_400_BAD_REQUEST)
            carr = json.loads(upload)
            instance.uploads.set(carr)

        topic = request.data.get('topic', [])
        if topic:
            if not isinstance(topic, str):
                return Response({'error': 'Topic must be a string'}, status=status.HTTP_400_BAD_REQUEST)
            top = json.loads(topic)
            instance.topic.set(top)

        # Update other fields based on your requirements
        
        instance.file = request.data.get('file', instance.file)
        instance.name = request.data.get('name', instance.name)
        instance.description = request.data.get('description', instance.description)
        instance.active = request.data.get('active', instance.active)
        # created_by = request.data.get('created_by', instance.created_by.id)
        # instance.created_by = User.objects.get(id=created_by)
        # user = request.data.get('user', instance.user.id)
        # instance.user = User.objects.get(id=user)
        instance.save()

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)











class ChangeUserDetails(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_staff=False)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Validate mobile number
        mobile_number = serializer.validated_data.get('mobile')
        if mobile_number and len(mobile_number) != 10:
            return Response({"error": "Mobile number must be 10 characters"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
    

class CommonVideoAdd(viewsets.ModelViewSet):
    serializer_class=CommonVideoSerializer

    def create(self,request):
        try:
            try:
                file=request.data['file']
                name=request.data['name']
                description=request.data['description']
                video_length=request.data['video_length']
                user=request.data['user']
                videocontent=request.data['videocontent']
            
           
                response_data=upload_video_to_vimeo(file,name,description)
                print(response_data,"Reponse")
                headers = {
                        'Authorization': f'Bearer d9a01813f50cf7a68e966e285d557f36',
                        'Content-Type': 'application/json',
                        'Accept': 'application/vnd.vimeo.*+json;version=3.4',
                    }
                if response_data.get('message')=="Video upload complete":
                    print(response_data,'response data')
                    print("*************************")
                    videolinks=response_data['link']
                    print(videolinks,'vidoelinkrespone')
                    vimeoid=videolinks.split('/')[-1]
                    request = requests.get(f'https://api.vimeo.com/videos/{vimeoid}?fields=uri,upload.status,transcode.status',headers=headers)
                    print("request",request.json())

                    print(vimeoid,'vimeoid')
                    serializer = CommonVideoSerializer(data={
                        'name': name,
                        'description': description,
                        'video_length':video_length,
                        'editingstaff': user,
                        'videolink': videolinks,
                        'videocontent':videocontent,
                        'vimeoid':vimeoid
                    })

                    if serializer.is_valid():
                        serializer.save()
                        return Response({"data":serializer.data},status=200)
                    else:
                        return Response({'message':"serilizer is not valids"},status=403)
            except:
           
                video_link=request.data['video_link']
                print(request.data['video_link'],'ddd')
                name=request.data['name']
                description=request.data['description']
                video_length=request.data['video_length']
                user=request.data['user']
                videocontent=request.data['videocontent']
                vimeoid=video_link.split('/')[-1]
                serializer = CommonVideoSerializer(data={
                        'name': name,
                        'description': description,
                        'video_length':video_length,
                        'editingstaff': user,
                        'videolink': video_link,
                        'videocontent':videocontent,
                        'vimeoid':vimeoid
                    })

                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data},status=200)
                else:
                    return Response({'message':"serilizer is not valids"},status=403)
        except Exception as e:
            print(e,"^^^^^^^^^^^^^^^^^^^^^")
            return Response({"message":"something went wrong"},status=403)
           
    
class Facultylistonline(viewsets.ModelViewSet):
    serializer_class=facultyviewDetailsStudioClass

    def list(self,request):
         
            stdcrseid=request.query_params.get('studiocourseid',None)
            print(stdcrseid,'dddd')
            faculty_list = Faculty.objects.filter(
            modeofclasschoice=2,
            user__in=FacultyCourseAddition.objects.filter(status='approved',topic__in=StudioCourse.objects.filter(id=stdcrseid).values('topic')).values('user')
        )

            serializer = facultyviewDetailsStudioClass(faculty_list, many=True)
            return Response(serializer.data, status=200)
     


class FacultylistonlineBoth(viewsets.ModelViewSet):
    serializer_class=facultyviewDetailsStudioClass

    def list(self,request):
      
            stdcrseid=request.query_params.get('studiocourseid',None)
            faculty_list = Faculty.objects.filter(
            modeofclasschoice=3,
            user__in=FacultyCourseAddition.objects.filter(status='approved',topic__in=StudioCourse.objects.filter(id=stdcrseid).values('topic')).values('user')
        )

            serializer = facultyviewDetailsStudioClass(faculty_list, many=True)
            return Response(serializer.data, status=200)
   
class MaterialUploadFacultyBasedViewSet(ModelViewSet):
    queryset = MaterialUploads.objects.all()
    serializer_class = MaterialUploadSerializer
    permission_classes= [AdminOrFaculty]

    def get_queryset(self):
        user_id=AuthHandlerIns.get_id(request=self.request)
        print(user_id)
        if user_id:
            queryset = MaterialUploads.objects.filter(user=user_id)
            print("No userid")
            # raise ValidationError("No user Id Found.")
        else:
            queryset = MaterialUploads.objects.filter()

        name = self.request.query_params.get('name', None)

        uniqueid = self.request.query_params.get('uniqueid', None)
        

        if name:
            queryset = queryset.filter(name__icontains = name)
        
        if uniqueid:
            queryset = queryset.filter(Q(id__icontains=uniqueid) | Q( user__id__icontains = uniqueid))




        return queryset
    
    # def destroy(self, request, pk=None):
    #     user_id = AuthHandlerIns.get_id(request=request)
    #     print(user_id)
    #     try:
    #         material = MaterialUploads.objects.get(pk=pk, user=user_id)
    #         material.delete()
    #         return Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    #     except MaterialUploads.DoesNotExist:
    #         return Response({'message': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)

    # def partial_update(self, request, pk=None):
    #     user_id = AuthHandlerIns.get_id(request=request)
    #     print(user_id)
    #     try:
    #         material = MaterialUploads.objects.get(pk=pk, user=user_id)
    #     except MaterialUploads.DoesNotExist:
    #         return Response({'message': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = self.serializer_class(material, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class MaterialUploadFacultyBasedUserIdViewSet(ModelViewSet):
    queryset = MaterialUploads.objects.all()
    serializer_class = MaterialUploadSerializer

    def get_queryset(self):
        # user_id=AuthHandlerIns.get_id(request=self.request)
        user_id = self.request.query_params.get('user_id')
        queryset = MaterialUploads.objects.filter(user=user_id)
        return queryset
        
class OfflineOnlineSalaryAssign(ModelViewSet):
    serializer_class=FacultyNewonlineoffSalarySerializer

    def retrieve(self,request,*args,**kwargs):
        facultyid=kwargs['pk']
        faculty_sal = Faculty_Salary.objects.filter(faculty=facultyid)
        serializer = FacultyNewonlineoffSalarySerializer(faculty_sal, many=True)
        return Response(serializer.data)

class MaterialRatingViewsSet(viewsets.ModelViewSet):
    queryset = MaterialRating.objects.all()
    serializer_class = MaterialRatingSerializer


from django.db.models import Avg, Count


from student.models import StudentBatch,Student
# class PopularFacultyViewSet(viewsets.ModelViewSet):
#     queryset = Faculty.objects.filter(is_verified=True)
#     serializer_class = PopularTeacherSerializer
#     pagination_class = SinglePagination

#     def list(self, request, *args, **kwargs):
#         student = Student.objects.get(user=AuthHandlerIns.get_id(request=request))
#         if student is None:
#             return Response({"message":"No Student found"})
#         course_id = student.selected_course.id
#         if course_id is None:
#             return Faculty.objects.none()
#         if not AuthHandlerIns.is_student(request=request):
#             return Response({"message": "Only Student can View Popular Teachers"}, status=status.HTTP_401_UNAUTHORIZED)
#         # Get the count from the request query parameters
#         count = request.query_params.get('count')
#         # Validate and parse the count parameters
#         try:
#             count = int(count)
#             if count <= 0:
#                 raise ValueError("Count must be a positive integer.")
#         except (ValueError, TypeError):
#             return Response(
#                 {"error": "Invalid count parameter."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         faculty_additions = FacultyCourseAddition.objects.filter(course_id=course_id,is_approved=True)
#         print(faculty_additions.count(),"CNT")
#         # Get all the faculties
#         faculties = Faculty.objects.filter(user__facultycourseaddition__in=faculty_additions)

#         # faculties = Faculty.objects.filter(is_verified=True)
#         print(faculties,"Facult")
#         # Dictionary to store faculty ratings
#         faculty_ratings = {}

#         # Iterate over each faculty
#         for faculty in faculties:
#             print(faculty.id, "In FOR")
#             # Get all timetables related to the faculty
#             timetables = TimeTable.objects.filter(faculty=faculty.id)
#             print(timetables, "TIME")
#             # Calculate the average rating for the faculty
#             avg_rating = timetables.aggregate(Avg('rating__choice'))['rating__choice__avg']
#             if avg_rating is None:
#                 avg_rating = 0.0
#             print(avg_rating, "Rating")
#             # Store the faculty and their average rating in the dictionary
#             faculty_ratings[faculty] = avg_rating

#         # Sort the faculty_ratings dictionary by the average rating in descending order
#         sorted_faculty_ratings = sorted(faculty_ratings.items(), key=lambda x: x[1], reverse=True)

#         # Extract the sorted faculty list
#         sorted_faculty_list = [item[0] for item in sorted_faculty_ratings]

#         # Limit the faculty list based on the count
#         limited_faculty_list = sorted_faculty_list[:count]

#         # Serialize the limited faculty list
#         serializer = self.get_serializer(limited_faculty_list, many=True)
#         return Response(serializer.data)
    

########################QUERYSET#########################################
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound,APIException,PermissionDenied
class PopularFacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.filter(is_verified=True,modeofclasschoice__in=[1,3])
    serializer_class = PopularTeacherSerializer
    pagination_class = SinglePagination

    def get_queryset(self):
        try:
            if not AuthHandlerIns.is_student(request=self.request):
                raise PermissionDenied("Only Student can View Popular Teachers")
            
            student = Student.objects.get(user=AuthHandlerIns.get_id(request=self.request))
            if student is None:
                raise Student.DoesNotExist("No Student found")
            if student.selected_course is None:
                raise ValueError("No Course found")
            course_id = student.selected_course.id
            print(course_id)

            

            faculty_additions = FacultyCourseAddition.objects.filter(course_id=course_id, status='approved').values('user')
            faculties = Faculty.objects.filter(user__id__in=faculty_additions)

            faculty_ratings = {}

            for faculty in faculties:
                timetables = TimeTable.objects.filter(faculty=faculty.id)
                avg_rating = timetables.aggregate(Avg('rating__choice'))['rating__choice__avg']
                print(avg_rating,"avg")
                if avg_rating is None:
                    avg_rating = 0.0
                faculty_ratings[faculty] = avg_rating

            sorted_faculty_ratings = sorted(faculty_ratings.items(), key=lambda x: x[1], reverse=True)
            sorted_faculty_list = [item[0] for item in sorted_faculty_ratings]

            return sorted_faculty_list

        except Student.DoesNotExist:
            raise NotFound("No Student found")
        except Exception as e:
            raise APIException(str(e))





#####################################################



# class PopularFacultyViewSet(viewsets.ModelViewSet):
#     queryset = Faculty.objects.filter(is_verified=True)
#     serializer_class = PopularTeacherSerializer
#     pagination_class = SinglePagination

#     def list(self, request, *args, **kwargs):
#         try:
#             student = Student.objects.get(user=AuthHandlerIns.get_id(request=request))
#             if student is None:
#                 return Response({"message": "No Student found"}, status=status.HTTP_404_NOT_FOUND)
#             course_id = student.selected_course.id
#             # course_id =request.query_params.get('course_id')
#             if course_id is None:
#                 return Response({"message": "No Course found"}, status=status.HTTP_204_NO_CONTENT)
#             if not AuthHandlerIns.is_student(request=request):
#                 return Response({"message": "Only Student can View Popular Teachers"}, status=status.HTTP_401_UNAUTHORIZED)

#             # Get the count from the request query parameters
#             count = request.query_params.get('count')

#             if count is None:
#                 # No count value provided, return the total list
#                 count = len(Faculty.objects.filter(is_verified=True))
#             else:
#                 # Validate and parse the count parameter
#                 try:
#                     count = int(count)
#                     if count <= 0:
#                         raise ValueError("Count must be a positive integer.")
#                 except (ValueError, TypeError):
#                     return Response({"error": "Invalid count parameter."}, status=status.HTTP_400_BAD_REQUEST)

#             faculty_additions = FacultyCourseAddition.objects.filter(course_id=course_id, is_approved=True)
#             faculties = Faculty.objects.filter(user__facultycourseaddition__in=faculty_additions)

#             # Dictionary to store faculty ratings
#             faculty_ratings = {}

#             # Iterate over each faculty
#             for faculty in faculties:
#                 timetables = TimeTable.objects.filter(faculty=faculty.id)
#                 avg_rating = timetables.aggregate(Avg('rating__choice'))['rating__choice__avg']
#                 if avg_rating is None:
#                     avg_rating = 0.0
#                 faculty_ratings[faculty] = avg_rating

#             # Sort the faculty_ratings dictionary by the average rating in descending order
#             sorted_faculty_ratings = sorted(faculty_ratings.items(), key=lambda x: x[1], reverse=True)

#             # Extract the sorted faculty list
#             sorted_faculty_list = [item[0] for item in sorted_faculty_ratings]

#             # Limit the faculty list based on the count
#             limited_faculty_list = sorted_faculty_list[:count]

#             # Serialize the limited faculty list
#             serializer = self.get_serializer(limited_faculty_list, many=True)
#             return Response(serializer.data)
#         except Student.DoesNotExist:
#             return Response({"message": "No Student found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    
class Completedstudiiocourselist(ModelViewSet):
    serializer_class = AssingSalaryStudioDetails

    def get_queryset(self):
        return StudioCourse.objects.filter(faculty__isnull=False, video__isnull=False, assignvideo=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class UploadedMaterialsFacultyBased(viewsets.ModelViewSet):
    queryset = MaterialReference.objects.all()
    serializer_class = MaterialReferenceSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        query = MaterialReference.objects.filter(user_id=user_id)
        serializers = MaterialReferenceSerializer(query,many=True)
        return Response(serializers.data)
    
class CreateOnlineSalary(ModelViewSet):
    serializer_class=CreateOnlineSalarySerializer
    queryset=OnlineSalary.objects.all()



class NewQuestionPoolViewSetCopy(viewsets.ModelViewSet):
    serializer_class = QustionpoolNew
    queryset = NewQuestionPool.objects.all()
    def get_permissions(self):
        if self.action in ['update']:
            self.permission_classes =[AdminOrFaculty]
        else:
            self.permission_classes =[NonePermission]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        original_subtopic = request.data['original_subtopic']
        new_subtopic = request.data['new_subtopic']
        user_id=AuthHandlerIns.get_id(request=request)
        nq= NewQuestionPool.objects.filter(user__id=user_id,subtopic=original_subtopic)
        old_topic=SubTopic.objects.get(id=original_subtopic).topic
        new_topic=SubTopic.objects.get(id=new_subtopic).topic
        fac= FacultyCourseAddition.objects.filter(topic=old_topic,status='approved',user__id=user_id).exists()
        # print({
        #         "old":len(NewQuestionPool.objects.filter(user__id=user_id,subtopic=original_subtopic)),
        #         "new":len(NewQuestionPool.objects.filter(user__id=user_id,subtopic=new_subtopic)),
        #         "topic_old":SubTopic.objects.get(id=original_subtopic).topic,
        #         "topic_new":SubTopic.objects.get(id=new_subtopic).topic,
        #     })
        if not fac:
            return Response({"Message":"Not Permited"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            for i in nq:
                fields = model_to_dict(i)
                # print(i,fields,"kkkkkkkkkkkkkkkk",new_subtopic)

                fields['subtopic'] =SubTopic.objects.get(id=new_subtopic) 
                fields['user']=User.objects.get(id=fields['user'])
                fields['categorys']=new_topic.module.subject.course.level.category
                fields['levels']=new_topic.module.subject.course.level
                fields['course']=new_topic.module.subject.course
                fields['subject']=new_topic.module.subject
                fields['module']=new_topic.module
                fields['topic']=new_topic
                s=fields.pop('id')
                # print(s)
                



                pp = NewQuestionPool.objects.create(**fields)
                # kk=QustionpoolNew(data=fields)
                # kk.is_valid()
                # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                # kk.save()
            # print({
            #     "old":len(NewQuestionPool.objects.filter(user__id=user_id,subtopic=original_subtopic)),
            #     "new":len(NewQuestionPool.objects.filter(user__id=user_id,subtopic=new_subtopic)),
            #     "topic_old":SubTopic.objects.get(id=original_subtopic).topic,
            #     "topic_new":SubTopic.objects.get(id=new_subtopic).topic,
            # })
            return Response({"meassage":"done"})
        except Exception as e:
            return Response({"meassage":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class QuestionPoolCreateNewCopy(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew

    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'destroy', 'create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRolePermissionCopy, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRolePermissionCopy, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "QuestionPool"
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
        queryset = super().get_queryset()
        if self.action == 'list' and AuthHandlerIns.is_faculty(request=self.request):
            if AuthHandlerIns.is_faculty(request=self.request): 
                queryset = queryset.filter(user=AuthHandlerIns.get_id(request=self.request))
        return queryset

    def create(self,request,*args,**kwargs):
        try:
            useridintoken=AuthHandlerIns.get_id(request)
            print(useridintoken)
            getuser=User.objects.get(id=useridintoken)
            print(getuser)
            data=request.data
            print(data,'data')
            data['user']=useridintoken
            questionexist=NewQuestionPool.objects.filter(user=getuser,question_text=data['question_text']).exists()
            if questionexist:
                return Response({"error":"question allready added"},status=status.HTTP_409_CONFLICT)
            else:
                serializer=QustionpoolNew(data=request.data)
                if serializer.is_valid():
                    print('serilizer')
                    serializer.save()
                    return Response({"message":"Question created successfully"},status=status.HTTP_201_CREATED)
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error":"something went wrong"})
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            useridintoken = AuthHandlerIns.get_id(request)
            data = request.data.copy()  # Make a copy of the request data
            data['user'] = useridintoken  # Add the user ID to the question data
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "something went wrong"})
    def get_serializer_class(self):
        if self.action == 'list':
            return QustionpoolNew
        else:
            return self.serializer_class


class MaterialUploadViewSetCopy(viewsets.ModelViewSet):
    queryset = MaterialUploads.objects.all()
    serializer_class = MaterialUploadSerializer
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature = self.action
            self.permission = "Material"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        elif self.action in [ 'destroy']:
            self.feature = 'delete'
            self.permission = "Material"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        elif self.action in ['list']:
            self.feature=self.action
            self.permission="Material"
            self.permission_classes=[AdminAndRoleOrFacultyPermission,]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "Material"
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                self.feature = "edit"
            self.permission_classes = [AdminAndRoleOrFacultyPermission, ]
        return super().get_permissions()    


    def get_queryset(self):
        user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
        queryset = MaterialUploads.objects.filter()
        if user.is_faculty:
            queryset=queryset.filter(user=user)
        return queryset


    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        material_upload = serializer.save()

        # Validate user is faculty
        if not material_upload.user.is_faculty:
            material_upload.delete()
            raise ValidationError("Material uploads can only be done by faculty users.")


class SpecialHolidaysViewsetCopy(ModelViewSet):
    serializer_class=SpecialHolidaySerializer
    queryset=SpecialHoliday.objects.all()
        #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Holiday"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Holiday"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Holiday"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Holiday"
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


class TimeTableAttendanceViewSetCopy(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimetableAttendanceSerializer
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            print(self.action,'uuuu')
            self.feature = self.action
            print(self.request.data,"datdtdas")
            self.permission = "Attendance"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in [ 'destroy']:
            print(self.action,'uuuusss')
            self.feature = 'delete'
            print(self.request.data,"datdtdasss")
            self.permission = "Attendance"
            self.permission_classes = [AdminAndRolePermission, ]
            print("%%%%%%%%%%")
        elif self.action in ['list']:
            print(self.request.data,'data')
            self.feature = self.action
            # print(self.permission,'ddd')
            print("list")
            self.permission = "Attendance"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in ['update', 'partial_update'] :
            print('update')
            self.permission = "Attendance"
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
    def retrieve(self, request, pk):
        timetable = TimeTable.objects.filter(date=pk)
        serializer = self.serializer_class(timetable, many=True)
        return Response({"date": serializer.data})
    
# class MaterialUploadAdminViewSet(viewsets.ModelViewSet):
#     queryset = MaterialUploads.objects.all()
#     serializer_class = MaterialUploadAdminViewSerializer

#     def get_queryset(self):
#         user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
#         print(user)

#         queryset = MaterialUploads.objects.filter()
#         if user.is_staff:
#             print("in staff")
#             user_id = self.request.query_params.get('user_id')
#             queryset = queryset.filter(user=user_id)
#             print(queryset)
                    
        # return queryset


class IncentivesViews(ModelViewSet):
    serializer_class=IncentivesSerializer
    queryset=Incentives.objects.all().order_by('-created_at')
    pagination_class = SinglePagination

    def get_queryset(self):
        queryset=Incentives.objects.all().order_by('-created_at')
        name=self.request.query_params.get('name')
        if name is not None:
            queryset=queryset.filter(Q(name__icontains=name))
        return queryset


class StaffIncentivesViews(ModelViewSet):
    # serializer_class=StaffIncentivesSerializer 
    queryset=StaffIncentives.objects.all().order_by('-created_at')
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method=='PATCH':
            return StaffIncentivesSerializerPOST  # Your serializer for POST requests
        else:
            return StaffIncentivesSerializer 

class Incentiveslistbyusers(viewsets.ReadOnlyModelViewSet):
    serializer_class=incentiveSalarySerializersmall
    permission_classes=[AdminAndRolePermission]

    def list(self,request,*args,**kwargs):
        if AuthHandlerIns.is_staff(request=request):
            staff_id=request.query_params.get('staff_id')
            querysets = StaffIncentives.objects.filter(staff=staff_id)
            serializer=incentiveSalarySerializersmall(querysets,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message":"you dont have permission to get the data"})

class IncentivelistnotinUsers(viewsets.ReadOnlyModelViewSet):
    serializer_class=IncentiveSmall
    
    def list(self,request,*args,**kwargs):
        try:
            staff_id=self.request.query_params.get('staff_id')
            user=StaffIncentives.objects.filter(staff=staff_id).values('incentives')
            values_list=[]
            for item in user:
                values_list.append(item['incentives'])
            incentives=Incentives.objects.exclude(id__in=values_list)
            serilizer=IncentiveSmall(incentives,many=True)
            return Response(serilizer.data)
        except:
            return Response({"message":"something went wrong"},status=400)



class StaffSalaryViews(ModelViewSet):
    serializer_class=StaffSalarySerializer
    queryset=StaffSalary.objects.all()

class StaffIncentiveAmount(ModelViewSet):
    serializer_class=StaffIncentiveAmountSerializer
    queryset=StaffIncentiveAmount.objects.all()
    

class ActiveStafflist(viewsets.ReadOnlyModelViewSet):
    serializer_class=ActiveStafflistSerializer
    queryset=User.objects.filter(is_roleuser=True,is_active=True)
    pagination_class=SinglePagination

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)
        mobile = self.request.query_params.get('mobile', None)
        branch_name = self.request.query_params.get('branch_name', None)
        location = self.request.query_params.get('location', None)

        if username:
            queryset = queryset.filter(Q(username__icontains=username))
        if email:
            queryset = queryset.filter(Q(email__icontains=email))
        if mobile:
            queryset = queryset.filter(Q(mobile__icontains=mobile))
        if branch_name:
            queryset = queryset.filter(Q(branch__name__icontains=branch_name))
        if location:
            queryset = queryset.filter(Q(branch__location__icontains=location))

        return queryset


class FacultyListByTopicIdViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class=FacultyList_AutoTimeTable_Topic_Serializer
    permission_classes = [AdminAndRolePermission]
    pagination_class = SinglePagination

    # def get_serializer_context(self):
    #     topic=self.request.query_params.get('topic')
    #     context = super().get_serializer_context()
    #     topic_batch = Topic_batch.objects.filter(id=topic).values('topic')
    #     print(topic_batch, "topicBatch")
    #     topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')
    #     print(topic, "hellooooo")

    #     # faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
    #     #     topic__in=topic, status='approved').values('user')
    #     salary = Topic.objects.get(id__in=topic)
     
    #     level = salary.module.subject.course.level
    #     context['level']=level
    #     return context

    def get_queryset(self):
        topic=self.request.query_params.get('topic')
        internal=self.request.query_params.get('internal')
        queryset = Faculty.objects.filter()
        if internal:
            topic_batch = Topic_batch.objects.filter(id=topic).values('topic')
            topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')

            faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
                topic__in=topic, status='approved').values('user')
            salary = Topic.objects.get(id__in=topic)
            queryset = queryset.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3],inhouse_fac=True)
            # level = salary.module.subject.course.level
            # serializer_context = self.get_serializer_context()

            # # Add additional context data based on the queryset
            # serializer_context['level'] = level

            # # Set the serializer context
            # self.get_serializer().context = serializer_context
        
        elif topic:
        
            topic_batch = Topic_batch.objects.filter(id=topic).values('topic')
            topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')

            faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
                topic__in=topic, status='approved').values('user')
            salary = Topic.objects.get(id__in=topic)
            queryset = queryset.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3]).exclude(inhouse_fac=True)
        

            # level = salary.module.subject.course.level
            # serializer_context = self.get_serializer_context()

            # # Add additional context data based on the queryset
            # serializer_context['level'] = level

            # # Set the serializer context
            # self.get_serializer().context = serializer_context

        queryset = Faculty.objects.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3])

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        topic=kwargs['pk']
        print(topic,"topiccccccccccccccccc")
        internal=self.request.query_params.get('internal')
        queryset = Faculty.objects.filter()
        if internal:
            topic_batch = Topic_batch.objects.filter(id=topic).values('topic')
            topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')

            faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
                topic__in=topic, status='approved').values('user')
            
            salary = Topic.objects.get(id__in=topic)
           
            queryset = queryset.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3],inhouse_fac=True)
            # level = salary.module.subject.course.level
            # serializer_context = self.get_serializer_context()

            # # Add additional context data based on the queryset
            # serializer_context['level'] = level

            # # Set the serializer context
            # self.get_serializer().context = serializer_context
        
        elif topic:
            print("helloooo")
            topic_batch = Topic_batch.objects.filter(id=topic).values('topic')
            topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')
            print("topic",topic)
            faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
                topic__in=topic, status='approved').values('user')
            print(topic,"hhhhhhhhhhhhhhhhhhhhhhh")
            salary = Topic.objects.get(id__in=topic)
            print(salary,"salaaaa")
            queryset = queryset.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3]).exclude(inhouse_fac=True)
        

            level = salary.module.subject.course.level
    

         

   

        queryset = Faculty.objects.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3])
        id=self.request.query_params.get('id')
        name=self.request.query_params.get('name')
        address=self.request.query_params.get('address')
        faculty_salary=self.request.query_params.get('faculty_salary')
        if id :
            queryset=queryset.filter(id=id)
        if name:
            queryset=queryset.filter(name__icontains=name)
        if address:
            queryset=queryset.filter(address__icontains=address)
        if faculty_salary:
            sal= Faculty_Salary.objects.filter(fixed_salary__salaryscale=faculty_salary,faculty__id__in=queryset.values('id')).values('faculty')
            queryset=queryset.filter(id__in=sal)
        # faculty = FacultyList_AutoTimeTable_Topic_Serializer(queryset, many=True,context={'level':level})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True,context={'level':level})
        return Response(serializer.data)
        return Response({"Facukty_List": faculty.data})


# @api_view(['GET'])
# def facultyList_AutoTimeTable_Topic(request, pk):
#     if not AuthHandlerIns.is_staff(request) and not AuthHandlerIns.is_role(request=request):
#         return Response({"message": "Only Admin can access this"}, status=status.HTTP_401_UNAUTHORIZED)

#     # print(Subject.objects.filter(course=pk).values('id'))
#     topic_batch = Topic_batch.objects.filter(id=pk).values('topic')
#     print(topic_batch, "topicBatch")
#     topic = Topic_branch.objects.filter(id__in=topic_batch).values('topic')
#     print(topic, "hellooooo")

#     faculty_with_topic_approved = FacultyCourseAddition.objects.filter(
#         topic__in=topic, status='approved').values('user')
#     salary = Topic.objects.get(id__in=topic)
#     level = salary.module.subject.course.level
#     print(level, "hellllllll")

#     fac = Faculty.objects.filter(user__in=faculty_with_topic_approved,is_blocked=False,modeofclasschoice__in=[1,3])
#     faculty = FacultyList_AutoTimeTable_Topic_Serializer(fac, many=True,context={'level':level})
    

#     return Response({"Facukty_List": faculty.data})

@api_view(['GET'])
def getbranchletters(request, id):
    batch=Batch.objects.filter(branch=id).values('name')
    used=[i['name'][-1:] for i in batch]
    print([i['name'][-1:] for i in batch])
    letters=[chr(ord('A') + i)  for i in range(26)]
    updated_letters = [letter for letter in letters if letter not in used]

    print(updated_letters)
    # pp=letters.remove(used)
    # print(pp)
    return Response(updated_letters)

from Sockets.celery import send_daily_emails
@api_view(['GET'])
def getavailablity(request, id):
   
    # batch=Batch.objects.filter(branch=id).values('name')
    # timetable=TimeTable.objects.get(id=id)
    # timetables=TimeTable.objects.filter(date=timetable.date)
    print(request.user,"user")
    celery = send_daily_emails()
    print(celery,"       Celery")
    

    return Response({"11112dsfsd3344":"gggsfsdfs44"})


class MaterialReferenceDeleteViewSet(viewsets.ModelViewSet):
    queryset = MaterialReference.objects.all()
    serializer_class = MaterialReferenceSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
class CategoriesforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.all().order_by('-created_at')

    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            return self.queryset
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            category=FacultyCourseAddition.objects.filter(user=faculty_userid).values('category')
            cat=Category.objects.filter(id__in=category).order_by('-created_at')
            return cat


class LevelforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = LevelSerializer

    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            category_id=self.request.query_params.get('category_id', None)
            level=Level.objects.filter(category__id=category_id).order_by('-created_at')
            return level
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            category_id=self.request.query_params.get('category_id', None)
            level=FacultyCourseAddition.objects.filter(user=faculty_userid,category__id=category_id).values('level')
            cat=Level.objects.filter(id__in=level).order_by('-created_at')
            return cat

    
class CourseforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer


    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            level_id=self.request.query_params.get('level_id', None)
            course=Course.objects.filter(level__id=level_id).order_by('-created_at')
            return course
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            level_id=self.request.query_params.get('level_id', None)
            course=FacultyCourseAddition.objects.filter(user=faculty_userid,level__id=level_id).values('course')
            courses=Course.objects.filter(id__in=course).order_by('-created_at')
            return courses
        
class SubjectforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            course_id=self.request.query_params.get('course_id', None)
            subject=Subject.objects.filter(course__id=course_id).order_by('-created_at')
            print(subject,'dd')
            return subject
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            course_id=self.request.query_params.get('course_id', None)
            subject=FacultyCourseAddition.objects.filter(user=faculty_userid,course__id=course_id).values('subject')
            subjects=Subject.objects.filter(id__in=subject).order_by('-created_at')
            return subjects

class ModuleforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModuleSerializer
    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            subject_id=self.request.query_params.get('subject_id', None)
            module=Module.objects.filter(subject__id=subject_id).order_by('-created_at')
            return module
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            subject_id=self.request.query_params.get('subject_id', None)
            module=FacultyCourseAddition.objects.filter(user=faculty_userid,subject__id=subject_id).values('module')
            modules=Module.objects.filter(id__in=module).order_by('-created_at')
            return modules

class TopicforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = TopicSerializer
    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            module_id=self.request.query_params.get('module_id', None)
            topic=Topic.objects.filter(module__id=module_id).order_by('-created_at')
            return topic
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            module_id=self.request.query_params.get('module_id', None)
            topic=FacultyCourseAddition.objects.filter(user=faculty_userid,module__id=module_id).values('topic')
            topics=Topic.objects.filter(id__in=topic).order_by('-created_at')
            return topics

class SubTopicforExcel(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubTopicSerializer
    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request):
            topic_id=self.request.query_params.get('topic_id', None)
            subtopic=SubTopic.objects.filter(topic__id=topic_id).order_by('-created_at')
            return subtopic
        elif AuthHandlerIns.is_faculty(request=self.request):
            faculty_userid=AuthHandlerIns.get_id(request=self.request)
            topic_id=self.request.query_params.get('topic_id', None)
            topic=FacultyCourseAddition.objects.filter(user=faculty_userid,topic__id=topic_id).values('topic')
            subtopics=SubTopic.objects.filter(topic__in=topic).order_by('-created_at')
            return subtopics


class BranchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

    def get_queryset(self):
        branch_history = Branch.history.all()
        return branch_history

from Sockets.qr import qr
from django.http import StreamingHttpResponse
from PIL import Image
import base64
from io import BytesIO

@api_view(['GET'])
def branch_qr(request,id):
    # Retrieve the image file path based on the image_id
    # image_path = f'/path/to/your/images/{image_id}.jpg'  # Replace with the actual path
    qr_img=qr(id)
    # Ensure that qr() returns a Pillow Image object
    if not isinstance(qr_img, Image.Image):
        return HttpResponseServerError("QR code generation failed")

    # Create a BytesIO object to hold the image data in memory
    image_byte_io = BytesIO()

    # Specify the format when saving the image (e.g., 'PNG')
    qr_img_format = 'PNG'
    qr_img.save(image_byte_io, format=qr_img_format)

    # Retrieve the image data as bytes
    image_data = image_byte_io.getvalue()

    # Determine the content type based on the image format
    content_type = f'image/{qr_img_format.lower()}'  # Lowercase format

    # Function to generate chunks of the image data
    def image_data_generator():
        yield image_data

    # Create a StreamingHttpResponse and set the content type
    response = StreamingHttpResponse(
        streaming_content=image_data_generator(),
        content_type=content_type,
    )

    return response
    # Create a StreamingHttpResponse and set the content type to 'image/png'
    response = StreamingHttpResponse(image_data_generator(), content_type='image/png')

    # Set content disposition to make the browser display or download the image
    response['Content-Disposition'] = 'inline; filename="qr_code.png"'

    return response


class TopicBasedOnCourse(viewsets.ReadOnlyModelViewSet):
    serializer_class=TopicBasedFacCourseSerilaizer

    def get_queryset(self):
        try:
            course_id = self.request.query_params.get('courseid')
            user=AuthHandlerIns.get_id(request=self.request)
            faculty_course_additions = FacultyCourseAddition.objects.filter(
                user=user,
                course_id=course_id,
                status='approved'
            )
            topic_ids = faculty_course_additions.values_list('topic_id', flat=True)
            queryset = Topic.objects.filter(id__in=topic_ids).order_by('created_at')
            return queryset
        except Exception as e:
            return None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = AuthHandlerIns.get_id(request=self.request)
        return context

class CourseBasedOnCategory(viewsets.ReadOnlyModelViewSet):
    serializer_class=CoursebasedFacCourseSerializer

    def get_queryset(self):
        try:
            categoryid=self.request.query_params.get('categoryid')
            user=AuthHandlerIns.get_id(request=self.request)
            faculty_course_additions = FacultyCourseAddition.objects.filter(
                    user=user,
                    category__id=categoryid,
                    status='approved'
            )
            topic_ids = faculty_course_additions.values_list('course_id', flat=True)
            queryset = Course.objects.filter(id__in=topic_ids).order_by('created_at')
            return queryset
        except Exception as e:
            return None
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = AuthHandlerIns.get_id(request=self.request)
        return context
class FacultyCategory(viewsets.ReadOnlyModelViewSet):
    serializer_class=facutlycategorySerialzer
    queryset=Category.objects.all()


    def get_queryset(self):
        user_id = AuthHandlerIns.get_id(request=self.request)
        print(user_id,'ddd')
        fac=FacultyCourseAddition.objects.filter(user__id=user_id,status='approved').distinct('category').values('category')
        queryset = Category.objects.filter(id__in=fac,active=True).order_by('name')
        return queryset


class FacultyPendingQuestions(viewsets.ReadOnlyModelViewSet):
    serializer_class=QuestionPoolSerializer

    def get_queryset(self):
        userid=AuthHandlerIns.get_id(request=self.request)
        subtopicid=self.request.query_params.get('subtopicid')
        pending=self.request.query_params.get('pending')
        nonapprove=self.request.query_params.get('nonapprove')
        ###pending dtp not touch
        if subtopicid and pending:
            queryset=NewQuestionPool.objects.filter(
                Q(user_id=userid)&
                Q(subtopic_id=subtopicid)&
                (Q(admin_verify=False) | Q(dtp_verify=False))&      
                Q(dtp_edit=False)&
                Q(faculty_verify=False)&
                Q(faculty_reject=False)&
                Q(publish=False)&
                Q(status=False)
            )
            return queryset
        ###faculty not approve
        elif subtopicid and nonapprove:
            queryset=NewQuestionPool.objects.filter(
                Q(user_id=userid)&
                Q(subtopic_id=subtopicid)&
                (Q(admin_verify=True) | Q(dtp_verify=True))& 
                Q(dtp_edit=True)&
                Q(faculty_verify=False)&
                Q(faculty_reject=False)&
                Q(publish=False)&
                Q(status=False)
            )
            return queryset
        else:
            None
class FacultyApproveButton(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.none()
    serializer_class=QuestionPoolSerializer

    @action(detail=False, methods=['post'])
    def approve_questions(self, request):
        # Get the user ID from the token
        print("(((())))")
        user_id_in_token = AuthHandlerIns.get_id(request=request)
        subtopic_id=request.query_params.get('subtopicid')
        if user_id_in_token and subtopic_id:
            print("$$$$$$$$$")
            # Get a list of question IDs from the request data
            question_ids = request.data.get('question_ids', [])

            # Update the NewQuestionPool objects for the specified question IDs
            updated_count = NewQuestionPool.objects.filter(
                user_id=user_id_in_token,
                id__in=question_ids
            ).update(faculty_verify=True)

            return Response({'message': f'{updated_count} questions have been approved by faculty.'})
        else:
            return Response({"message":"userid and subtopic id dont match"},status=400)
        


class FacultyRejectButton(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.none()
    serializer_class=QuestionPoolSerializer

    @action(detail=False, methods=['post'])
    def reject_questions(self, request):
        # Get the user ID from the token
        print("(((())))")
        user_id_in_token = AuthHandlerIns.get_id(request=request)
        subtopic_id=request.query_params.get('subtopicid')
        if user_id_in_token and subtopic_id:
            print("$$$$$$$$$")
            # Get a list of question IDs from the request data
            question_ids = request.data.get('question_ids')
            reject_reason = request.data.get('reject_reason')

            # Update the NewQuestionPool objects for the specified question IDs
            updated_count = NewQuestionPool.objects.filter(
                user_id=user_id_in_token,
                id=question_ids
            ).update(faculty_verify=False,faculty_reject_reason=reject_reason,faculty_reject=True,
                     dtp_verify=False,admin_verify=False
            )

            return Response({'message': f'question id:{question_ids} reject with this reason:{reject_reason}'})
        else:
            return Response({"message":"userid and subtopic id dont match"},status=400)

class FacultyQuestionSearch(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew

    def get_queryset(self, *args, **kwargs):
        userid = AuthHandlerIns.get_id(request=self.request)
        # subtopicid = self.request.query_params.get('subtopicid')
        questiontext = self.request.query_params.get('questiontext')
        questiontype = self.request.query_params.get('type')
        
        queryset = NewQuestionPool.objects.filter(user=userid)
        
        if questiontext:
            queryset = queryset.filter(question_text__icontains=questiontext)
        
        if questiontype == "Medium":
            queryset = queryset.filter(type=1)
        elif questiontype == "Simple":
            queryset = queryset.filter(type=2)
        elif questiontype == "Tough":
            queryset = queryset.filter(type=3)
        
        # No need to check for "All" as it's not a type filter.
        
        return queryset


class FacultyRejectQuestion(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            subtopicid=self.request.query_params.get('subtopicid')
            userid=self.request.query_params.get('userid')
            queryset=NewQuestionPool.objects.filter(subtopic=subtopicid,user=userid,admin_verify=False,dtp_verify=True,faculty_verify=False,faculty_reject=False,status=False,publish=False,dtp_edit=True)
            return queryset

class FacultySideDtpApprovedquestions(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            subtopicid=self.request.query_params.get('subtopicid')
            userid=self.request.query_params.get('userid')
            queryset=NewQuestionPool.objects.filter(subtopic=subtopicid,user=userid,admin_verify=False,dtp_verify=True,faculty_verify=False,faculty_reject=False,status=False,publish=False,dtp_edit=True)
            return queryset

class FacappQuestinEdit(viewsets.ModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['create']:
            self.feature = self.action
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRolePermission, ]
        elif self.action in [ 'destroy']:
            self.feature = 'delete'
            self.permission = "QuestionPool"
            self.permission_classes = [AdminAndRolePermission, ]
        # elif self.action in ['list']:
        #     self.feature=self.action
        #     self.permission="QuestionPool"
        #     self.permission_classes=[AdminAndRolePermission,]
        elif self.action in ['update', 'partial_update'] :
            self.permission = "QuestionPool"
            if "status" in self.request.data:
                self.feature = "Block"
            else:
                self.feature = "edit"
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()    

    def create(self,request,*args,**kwargs):
        print("hsahilllllllllllllllllllllllllll")
        try:
            if request.data['user'] != '' and (AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request)):
                print("DTP")
                useridintokens=AuthHandlerIns.get_id(request)
                request.data['add_user']=useridintokens
                request.data['dtp_verify']=True
                request.data['dtp_edit']=True
                questionexist=NewQuestionPool.objects.filter(user=request.data['user'],question_text=request.data['question_text']).exists()

                if questionexist:
                    return Response({"error":"question allready added"},status=status.HTTP_409_CONFLICT)
                else:

                    serializer=QustionpoolNewoneDtpCreate(data=request.data)

                    if serializer.is_valid():
                        serializer.save()
                        return Response({"message":"Question Created Successfully"},status=status.HTTP_201_CREATED)
                    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"You dont have permissions"},status=500)
        except Exception as e:
            print(e)
            return Response({"error":"something went wrong","message":e},status=500)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        try:
            if request.data['user'] != '' and (AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request)):
                data = request.data.copy()  # Make a copy of the request data
                data['dtp_edit']=True
                data['dtp_verify']=True
                serializer = self.get_serializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"You dont have permissions"},status=500)
        except:
            return Response({"error": "something went wrong"},status=500)
    def get_serializer_class(self):
            return self.serializer_class
    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Listing is not allowed.")
    def retrieve(self, request, *args, **kwargs):
        raise PermissionDenied("Retrieving individual question instances by ID is not allowed.")

class Facultynewaddedquestios(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            subtopicid=self.request.query_params.get('subtopicid')
            userid=self.request.query_params.get('userid')
            queryset=NewQuestionPool.objects.filter(subtopic=subtopicid,user=userid,admin_verify=False,dtp_verify=False,faculty_verify=False,faculty_reject=False,status=False,publish=False)
            return queryset

class FacultyRejectQuestion(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            subtopicid=self.request.query_params.get('subtopicid')
            userid=self.request.query_params.get('userid')
            queryset=NewQuestionPool.objects.filter(subtopic=subtopicid,user=userid,admin_verify=False,dtp_verify=False,faculty_verify=False,faculty_reject=True,status=False,publish=False)
            return queryset

class FacApprovedQuestions(viewsets.ReadOnlyModelViewSet):
    queryset = NewQuestionPool.objects.all().order_by('id')
    serializer_class = QustionpoolNew
    #####add permissions
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['list']:
            self.feature=self.action
            self.permission="QuestionPool"
            self.permission_classes=[AdminAndRolePermission,]
        return super().get_permissions()    
    def get_queryset(self):
        if AuthHandlerIns.is_staff(request=self.request) or AuthHandlerIns.is_role(request=self.request):
            subtopicid=self.request.query_params.get('subtopicid')
            userid=self.request.query_params.get('userid')
            queryset=NewQuestionPool.objects.filter(subtopic=subtopicid,user=userid,admin_verify=False,dtp_verify=True,faculty_verify=True,faculty_reject=False,status=False,publish=False)
            return queryset

