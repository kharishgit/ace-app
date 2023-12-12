from django.http import QueryDict
from django.shortcuts import get_object_or_404, render

from requests import Response# Create your views here.
from rest_framework import generics,views,status
from MobileApp.models import StudentFeeCollection,QuestionBook,StudyMaterial,BatchPackages
from finance.models import OnlineOrderPayment
from permissions.permissions import AdminAndRolePermission, AdminStudentFaculty,StudentPermission,AdminOrStudent
from .serializers import StudentForExcelSerializer, studentlogin,offlineserializer
from accounts.models import Faculty
from .serializers import *
from rest_framework.response import Response
from course.models import *
from course.serializers import *
from rest_framework import viewsets
from rest_framework.decorators import api_view
from course.views import SinglePagination
from email.message import EmailMessage
from accounts.api.vimeo import upload_video_to_vimeo
from searchall.utils import generate_pdf,get_queryset_headers_data
from searchall.views import queryset_to_excel, queryset_to_pdf

# class FacultyRegisterView(views.APIView):
#     def post(self, request):
#         serializer = studentlogin(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             print('save')
#             response = {
#                 "messages" : "Your registration  succesfull.",
#             }
#             return Response(data=response)
#         else:
#             response = {
#                 "messages" : "Your registration  succesfull.",
#             }
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# import urllib, urllib.request, urllib.parse       
# class FacultyRegisterViewss(views.APIView):
#     def get(self, request):
            
#         url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
#         values = {
#             'user': 'acemanjeri',
#             'passwd': 'babu2769220',
#             'message': 'Dear test, Your OTP for accessing AceApp is 123456. Do not share your OTP with anyone. -AceApp testing',
#             'mobilenumber': 919809956701,
#             'mtype': 'N',
#             'DR': 'Y',
#             'sid':'ACEAPP'
#         }
#         data = urllib.parse.urlencode(values)
#         data = data.encode('utf-8')
#         request = urllib.request.Request(url, data)
#         response = urllib.request.urlopen(request)
#         response_str = response.read().decode('utf-8')
#         response = {
#                 "messages" : "Your registration  succesfull.",
#             }
#         return Response(data=response_str)
        # if "OK:" in response_str:
        #     print("Message sent successfully.")
        # else:
        #     print("Failed to send message.")

# Create an object of SendSms class and send the message


import random
import urllib.parse
import urllib.request

from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response


# class SendOTPView(views.APIView):
#     def post(self, request):
#         mobile_number = request.data.get('mobile_number')
#         print(mobile_number,'mob')
#         if not mobile_number:
#             return Response({'error': 'Mobile number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Generate a 6-digit OTP
#         otp = ''.join(random.choices('0123456789', k=6))
#         print(otp,'otp')
        
#         url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
#         values = {
#             'user': 'acemanjeri',
#             'passwd': 'babu2769220',
#             'message': f'Dear user, Your OTP for accessing AceApp is {otp}. Do not share your OTP with anyone. -AceApp testing',
#             'mobilenumber': mobile_number,
#             'mtype': 'N',
#             'DR': 'Y',
#             'sid':'ACEAPP'
#         }
#         data = urllib.parse.urlencode(values)
#         data = data.encode('utf-8')
#         request = urllib.request.Request(url, data)
#         response = urllib.request.urlopen(request)
#         response_str = response.read().decode('utf-8')
#         print(response_str)
#         if "OK:" in response_str:
#             print("Message sent successfully.")
        
        
        # Send OTP via SMS Country API
        # url = 'http://www.smscountry.com/smscwebservice_bulk.aspx'
        # values = {
        #     'user': 'acemanjeri',
        #     'passwd': 'babu2769220',
        #     'message': f'Dear student, Your OTP for registration is {otp}. Do not share your OTP with anyone. -AceApp testing',
        #     'mobilenumber': mobile_number,
        #     'mtype': 'N',
        #     'DR': 'Y',
        #     'sid':'ACEAPP'
        # }
        # data = urllib.parse.urlencode(values).encode('utf-8')
        # response = urllib.request.urlopen(url, data)
        # response_str = response.read().decode('utf-8')
        # if "OK:" in response_str:
        #     request.session['otp'] = otp
        #     request.session['mobile_number'] = mobile_number
        #     return Response({'message': 'OTP sent successfully.'})
        # else:
        #     return Response({'error': 'Failed to send OTP.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class VerifyOTPView(views.APIView):
#     def post(self, request):
#         mobile_number = request.data.get('mobile_number')
#         otp = request.data.get('otp')
#         if not mobile_number or not otp:
#             return Response({'error': 'Mobile number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Verify OTP
#         if request.session.get('mobile_number') == mobile_number and request.session.get('otp') == otp:
#             # Clear OTP and mobile number from session
#             request.session.pop('otp', None)
#             request.session.pop('mobile_number', None)
#             return Response({'message': 'OTP verified successfully ...😍😍'})
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)



from datetime import datetime, timedelta
import random
import string
import pytz
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import urllib.parse
import urllib.request
from .models import OnlineStudent, StudentBatch
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OnlineStudent
import random
import pandas as pd
from accounts.models import User
import random
import string

from django.utils import timezone


# Register view
class RegisterView(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')

        # Check if mobile number already exists
        if OnlineStudent.objects.filter(mobile_number=mobile_number).exists():
            # return Response({'error': 'Mobile number already registered'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate OTP and save in database
            otp = str(random.randint(100000, 999999))
            if OnlineStudent.objects.get(mobile_number=mobile_number) :
        
                student = OnlineStudent.objects.update( otp=otp)

                # Send OTP via SMS or other means
                # ...
                url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
                values = {
                    'user': 'acemanjeri',
                    'passwd': 'babu2769220',
                    'message': f'Dear user, Your OTP for accessing AceApp is {otp}. Do not share your OTP with anyone. -AceApp testing',
                    'mobilenumber': mobile_number,
                    'mtype': 'N',
                    'DR': 'Y',
                    'sid':'ACEAPP'
                }
                data = urllib.parse.urlencode(values)
                data = data.encode('utf-8')
                request = urllib.request.Request(url, data)
                response = urllib.request.urlopen(request)
                response_str = response.read().decode('utf-8')
                if "OK:" in response_str:
                    return Response({'success': 'OTP sent to mobile number'}, status=status.HTTP_200_OK)
                else:
                    print("Failed to send message.")
        else:
            # Generate OTP and save in database
            otp = str(random.randint(100000, 999999))
            
        
            student = OnlineStudent.objects.create( mobile_nimber=mobile_number,otp=otp)

            # Send OTP via SMS or other means
            # ...
            url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
            values = {
                'user': 'acemanjeri',
                'passwd': 'babu2769220',
                'message': f'Dear user, Your OTP for accessing AceApp is {otp}. Do not share your OTP with anyone. -AceApp testing',
                'mobilenumber': mobile_number,
                'mtype': 'N',
                'DR': 'Y',
                'sid':'ACEAPP'
            }
            data = urllib.parse.urlencode(values)
            data = data.encode('utf-8')
            request = urllib.request.Request(url, data)
            response = urllib.request.urlopen(request)
            response_str = response.read().decode('utf-8')
            if "OK:" in response_str:
                return Response({'success': 'OTP sent to mobile number'}, status=status.HTTP_200_OK)
            else:
                print("Failed to send message.")

##############################################
from .models import Student

class Loginview(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        # Check if mobile number already exists in Student
        try:
            student = Student.objects.get(user__mobile=mobile_number)
            print("offline except")
            # Update OTP
            otp = str(random.randint(100000, 999999))
            student.otp= otp
            print('DDDDDDDDDDDDD')
            student.save()
        except Student.DoesNotExist:
            print("pass")
            pass
            # Create new Student
            # student = Student.objects.create(mobile=mobile_number, otp=otp)
        # Check if mobile number already exists in OnlineStudent
        try:
            student = OnlineStudent.objects.get(mobile_number=mobile_number)
            print("online")
            # Update OTP
            otp = str(random.randint(100000, 999999))
            student.otp = otp
            
            student.save()
            print("))))))))))))))")
        except OnlineStudent.DoesNotExist:
            print("online except")
            # Create new OnlineStudent
            otp = str(random.randint(100000, 999999))
            print('**********')
            student = OnlineStudent.objects.create(mobile_number=mobile_number, otp=otp)

 


        # Send OTP via SMS or other means
        # ...
        url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
        values = {
            'user': 'acemanjeri',
            'passwd': 'babu2769220',
            'message': f'Dear user, Your OTP for accessing AceApp is {otp}. Do not share your OTP with anyone. -AceApp testing',
            'mobilenumber': mobile_number,
            'mtype': 'N',
            'DR': 'Y',
            'sid': 'ACEAPP'
        }
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        request = urllib.request.Request(url, data)
        response = urllib.request.urlopen(request)
        response_str = response.read().decode('utf-8')
        if "OK:" in response_str:
            return Response({'success': 'OTP sent to mobile number'}, status=status.HTTP_200_OK)
        else:
            print("Failed to send message.")
###################################


class VerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        
        try:
            # Try to get the student with the given OTP from OnlineStudent model
            student = OnlineStudent.objects.get(otp=otp)
            if student.is_otp_valid():
                # OTP exists in OnlineStudent model and is valid
                return Response({'success': 'OTP verified  welcome online student'}, status=status.HTTP_200_OK)
        except OnlineStudent.DoesNotExist:
            pass

        try:
            # Try to get the student with the given OTP from Student model
            student = Student.objects.get(otp=otp)
            if student.is_otp_valid():
                # OTP exists in Student model and is valid
                return Response({'success': 'OTP verified welcome offline student'}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            pass

        # OTP not found in either model or is invalid
        return Response({'error': 'Invalid OTP or Mobile number not registered'}, status=status.HTTP_400_BAD_REQUEST)


class StudentRegistrationAPIView(APIView):
    def post(self, request):
        serializer = offlineserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def generate_random_string(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

class StudentExcelAdd(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentForExcelSerializer

    def create(self, request, *args, **kwargs):
        print(request.body)
        file = request.FILES['excel']  # Assuming the file is uploaded using the 'file' field in the request
        df = pd.read_excel(file)  # Read the Excel file using pandas
      
        for _, row in df.iterrows():
            user = User.objects.filter(Q(mobile=row.Phone) | Q(email=row.Email))
            if user.exists():
                students = Student.objects.filter(user__in=user)
                if students.exists():
                    for student in students:
                        try:
                            StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName)
                        except Exception as e:
                            print(e,"00",row.SLNO)
                            pass
                else:
                    for users in user:
                        try:
                            student = Student.objects.create(user=users,name=row.FirstName,exam_number=row.ExamNumber,admission_number=row.AdminstionNumber,father_name=row.FatherName,dob=row.BirthDate,gender=str(row.Gender)[0],marital_status=1 if row.MaritalStatus == "Single" else 2, religion=row.Religion, caste=row.Community, address = row.Address, admission_date=timezone.make_aware(row.JoinDate),is_offline=True)
                            StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName)
                        except Exception as e:
                            print(e,"11",row.SLNO)
                            pass
            else:
                try:
                    user = User.objects.create_student(username=row.Email,email=row.Email,mobile=row.Phone,password=generate_random_string(10))
                    
                    student = Student.objects.create(user=user,name=row.FirstName,exam_number=row.ExamNumber,admission_number=row.AdminstionNumber,father_name=row.FatherName,dob=row.BirthDate,gender=str(row.Gender)[0],marital_status=1 if row.MaritalStatus == "Single" else 2, religion=row.Religion, caste=row.Community, address = row.Address, admission_date=timezone.make_aware(row.JoinDate),is_offline=True )
                    StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName)
                except Exception as e:
                            print(e,"22",row.SLNO)
                            pass

                   

        return Response({"done":"ok"})
    

    def update(self, request, *args, **kwargs):
        print(request.body)
        file = request.FILES['excel']  # Assuming the file is uploaded using the 'file' field in the request
        df = pd.read_excel(file)  # Read the Excel file using pandas
        batch = Batch.objects.get(id=kwargs['pk'])
        branch = batch.branch
        for _, row in df.iterrows():
            user = User.objects.filter(Q(mobile=row.Phone) | Q(email=row.Email))
            if user.exists():
                students = Student.objects.filter(user__in=user)
                if students.exists():
                    for student in students:
                        try:
                            StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName,batch=batch,branch=branch)
                        except Exception as e:
                            print(e,"00",row.SLNO)
                            pass
                else:
                    for users in user:
                        try:
                            student = Student.objects.create(user=users,name=row.FirstName,exam_number=row.ExamNumber,admission_number=row.AdminstionNumber,father_name=row.FatherName,dob=row.BirthDate,gender=str(row.Gender)[0],marital_status=1 if row.MaritalStatus == "Single" else 2, religion=row.Religion, caste=row.Community, address = row.Address, admission_date=timezone.make_aware(row.JoinDate),is_offline=True)
                            StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName,batch=batch,branch=branch)
                        except Exception as e:
                            print(e,"11",row.SLNO)
                            pass
            else:
                try:
                    user = User.objects.create_student(username=row.Email,email=row.Email,mobile=row.Phone,password=generate_random_string(10))
                    
                    student = Student.objects.create(user=user,name=row.FirstName,exam_number=row.ExamNumber,admission_number=row.AdminstionNumber,father_name=row.FatherName,dob=row.BirthDate,gender=str(row.Gender)[0],marital_status=1 if row.MaritalStatus == "Single" else 2, religion=row.Religion, caste=row.Community, address = row.Address, admission_date=timezone.make_aware(row.JoinDate),is_offline=True )
                    StudentBatch.objects.create(student=student,batch_name=row.BatchTimeName,branch_name=row.BranchName,batch=batch,branch=branch)
                except Exception as e:
                            print(e,"22",row.SLNO)
                            pass

                   

        return Response({"done":"ok"})


    
from accounts.api.authhandle import AuthHandlerIns
from .otp import sendsms
class Studentlogin(ModelViewSet):
    queryset=Student.objects.all()
    serializer_class = StudentloginSeializer

    def create(self,request):
        try:
            mobile_number = request.data.get('mobile_number')
            print(mobile_number,'kkkkk')
            print(type(mobile_number))
            if mobile_number==str(7012195451):
                print("PPPPPPPPPP")
                student=Student.objects.get(user__mobile=mobile_number)
                studentid=student.pk
                num=1251
                otps = str(num)
                student.otp=otps
                print('11ddd111')
                student.save()
                print("******************")
                return Response({"studetnid":studentid},status=200)
            elif Student.objects.filter(user__mobile=mobile_number).exists():
                print("DDDDDDDDDDDDDDDDDDDdd")
                students=Student.objects.get(user__mobile=mobile_number)

                print("PPPPPPPPPPP")
                # print(students.name,'kkkk')
                otps = str(random.randint(1000, 9999))
                print(otps,'oppp')
             
                sendsms(mobile_number,otps)
               
                students.otp=otps
              
                students.save()
                print('1mmm111')
            

                return Response({"studetnid":students.id},status=200)
            elif Faculty.objects.filter(user__mobile=mobile_number).exists(): 
                print("DDDDBBBBBBBBBBBBBDDDDDDDDDdd")
                print(mobile_number,'ddd')
                faculty=Faculty.objects.get(user__mobile=mobile_number)
                print(faculty,"fffffffffffff")
               
        
                otps = str(random.randint(1000, 9999))
           
                sendsms(mobile_number,otps)
                print(otps,'faculty otp')
             
                faculty.otp=otps
           
                faculty.save()
                print('1mmm111')
            

                return Response({"facultyid":faculty.pk},status=200)
            else:
                print("%%%%%%%%%%%%%%%%%%%%%%")
                return Response({"message":"user is not found"},status=403)

            # sendsms(mobile_number,otp)
        except:
           return Response({"message":"something went wrong"},status=403)

class Verifyotp(ModelViewSet):
    queryset=Student.objects.all()
    serializer_class = StudentloginSeializer   

    def create(self,request):
        try:
            getotp=request.data.get('otp')
            print(getotp,'ddd')
            studentid=request.data.get('studentid')
            print(studentid,'dddddddd')
            facultyid=request.data.get('facultyid')
            print(facultyid,'dddddddddf')
        except:
            return Response({"message":"invalida request data"},status=400)
        if studentid and not facultyid:
            print("((((((((((((((()))))))))))))))")
            student=Student.objects.get(id=studentid)

            otps=Student.objects.get(id=studentid)
         
            dbotp=otps.otp

            #check otp is verified then response with token f

            if dbotp == getotp:
                    students=Student.objects.get(id=studentid)

                    if student:
                        # payload={'studentid': students.id,'name':students.name,'exam_number':students.exam_number,'admission_number':students.admission_number,'is_online':students.is_online,'is_offline':students.is_offline,'username': student.user.username, 'email': student.user.email,'is_student': student.user.is_student,'id':student.user.id}
                        payload = {'id': students.user.pk, 'username': students.user.username, 'email': students.user.email,
                       'admin': student.user.is_superuser,'role': students.user.is_roleuser, 'faculty': students.user.is_faculty,'student':students.user.is_student}

                    print(payload,'payload')

                    token = AuthHandlerIns.get_token(payload=payload)
                    otps.otp=None
                    otps.save()
                    batchdetails=StudentBatch.objects.filter(student=students.id)
                    serializers=StudentOTPBatchSerialiazer(batchdetails,many=True)
                    
                
                    return Response({"token":token,"facultyid":None,"userid":payload['id'],"studentid":students.id,"batch_details":serializers.data,"message":"Otp verirfication is successfull"},status=200)
            else:
                return Response({"message": "Otp verification failed"},status=403)
        elif facultyid and not studentid:
                faculty=Faculty.objects.get(id=facultyid)

                
                print("&&&&")
                otps=Faculty.objects.get(id=facultyid)
                # otp=Student.objects.get(id=studentid,otp=getotp)
                dbotp=otps.otp

                #check otp is verified then response with token f

                if dbotp == getotp:
                        # faculty=Faculty.objects.get(id=facultyid)
                        user=Faculty.objects.get(id=facultyid)
                    

                        if user:   
                            # payload = {'id': user.user.id, 'username': user.user.username, 'email': user.user.email,'admin': user.user.is_superuser, 'role': user.user.is_roleuser, 'faculty': user.user.is_faculty,'faculty_id':user.id}                          
                            payload = {'id': user.user.id, 'username': user.user.username, 'email': user.user.email,'admin': user.user.is_superuser, 'role': user.user.is_roleuser, 'faculty': user.user.is_faculty,'student':user.user.is_student}
                        print(payload,'payload')

                        token = AuthHandlerIns.get_token(payload=payload)
                        otps.otp=None
                        otps.save()
                        facultyprofile=Faculty.objects.filter(id=faculty.id)
                        # serializers=facultyviewDetailsProfile(facultyprofile,many=True)
                        
                    
                        return Response({"token":token,"facultyid":user.id,"userid":payload['id'],"studentid":None,"message":"Otp verirfication is successfull"},status=200)
                else:
                    return Response({"message": "Otp verification failed"},status=403)   
                
        else:
            return Response({"message":"field error in data"},status=403)

        

            


class Studentcoursedetails(ModelViewSet):
   queryset=StudentBatch.objects.all()
   serializer_class=StudentBatchSerialiazer

   def list(self,request):
        try:
            s=AuthHandlerIns.get_id(request=request)
            student=StudentBatch.objects.filter(student=Student.objects.get(user__pk=s))


                    
            print(student,'batch')
            serializers=StudentBatchSerialiazer(student,many=True)
            return Response(serializers.data,status=200)
        except:
             return Response({"message":"Invalid Data"})


class StudentBatchDetails(ModelViewSet):
    queryset=TimeTable.objects.all()
    serializer_class=StudentTimetableserializers
    
    
    def list(self, request, *args, **kwargs):
        return Response(status=405)    

    def create(self,request):
        try:
            batchid=request.data.get('batchid')
            print(batchid,'jjjjj')
            print("list pk")
            batch=TimeTable.objects.filter(batch=batchid).order_by('date')
            print(batch,'batch')
            
            serializers=StudentTimetableserializers(batch,many=True)
            return Response(serializers.data,status=200)
        except:
            return Response({"message":"something went wrong"})
        
    

from django.db import transaction,IntegrityError

class StudentRegister(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentRegisterSerializer

    def create(self, request, *args, **kwargs):
        user = None
        user_data = {
            'username': request.data['username'],
            'email': request.data['email'],
            'mobile': request.data['mobile'],
            'password': request.data['password'],
        }

        
        try:
            user_exists = User.objects.filter(username=request.data['username']).exists()
            mobile_exists = User.objects.filter(mobil=request.data['mobile']).exists()
            email_exists = User.objects.filter(email=request.data['email']).exists()
            if user_exists:
                return Response({"message": "Username already exists"})
            if mobile_exists:
                return Response({"message": "Mobile already exists"})
            if email_exists:
                return Response({"message": "Email already exists"})
        except:
            pass

        with transaction.atomic():
            try:       
                user = User.objects.create_student(**user_data)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                student = serializer.save(user=user)
                students = Student.objects.get(user=user)

                student_batch_data = {
                        "student":students,
                        'batch': request.data['batch'],
                        'branch': request.data['branch'],
                        'batch_name': request.data['batch_name'],
                        'branch_name': request.data['branch_name'],
                    }

                # student_batch_serializer = StudentBatchSerializer(data=student_batch_data)
                # student_batch_serializer.is_valid(raise_exception=True)
                # student_batch = student_batch_serializer.save()
                # student = Student.objects
                print("hellllllllllllllllllllllll")
                sb= StudentBatch.objects.create(
                        student=students,
                        batch= Batch.objects.get(id=request.data['batch']),
                        branch=Branch.objects.get(id=request.data['branch']),
                        batch_name=request.data['batch_name'],
                        branch_name= request.data['branch_name']
                    )
                print(sb,"sbbbbb")

                return Response({'message': 'Student registered successfully', 'student_id': student.id}, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # Handle unique constraint violation
                if 'accounts_user_email_key' in str(e):
                    return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'accounts_user_mobile_key' in str(e):
                    return Response({'message': 'mobilenumber already exists'}, status=status.HTTP_400_BAD_REQUEST)  
                else:
                    return Response({'message': f'An error occurred {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                # Rollback the transaction if an exception occurs
                if user:
                    user.delete()
                raise

class StudentViewSet(viewsets.ViewSet):
    permission_classes=[StudentPermission]
    def retrieve(self, request, pk=None):
        try:
            pk=  AuthHandlerIns.get_id(request=request)
            student = Student.objects.get(user_id=pk)
            student_serializer = StudentProfileSerializer(student)
            student_batch = StudentBatch.objects.filter(student=student)
            student_batch_serializer = StudentBatchSerializer(student_batch, many=True)
            fee_payments = FeePayment.objects.filter(student=student)
            fee_payment_serializer = FeePaymentSerializer(fee_payments, many=True)
            
            response_data = {
                'student': student_serializer.data,
                'student_batch': student_batch_serializer.data,
                'fee_payments': fee_payment_serializer.data
            }
            
            return Response(response_data)
        
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class StudentUserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = Student.objects.get(id=pk)
        return Response({"UserId": user.user.id})
    
class CurrentAffairsViewSet(viewsets.ModelViewSet):
    queryset = CurrentAffairs.objects.all().order_by('-created_at')
    serializer_class = CurrentAffairsSerializerN
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]


    # def create(self, request, *args, **kwargs):
    #     title = request.data['title']
    #     description = request.data['description']
    #     file = request.data['file']
    #     vname = request.data['vname']
    #     videolength = request.data['videolength']
    #     try:
    #         published = request.data['published']
    #     except:
    #         published = False
    #     created_by = request.data['created_by']
    #     course = request.data['course']
    #     lst = course[1:-1]
    #     carr=[]
    #     print(course)
    #     publish_on =request.data['publish_on']
    #     video =request.data['video']
    #     response_data = upload_video_to_vimeo(file,vname,description)
    #     if response_data.get('message') == 'Video upload complete':
    #         videolink = response_data['link']
    #         print(videolink)
    #         curnt=CurrentAffairs.objects.create(
    #             title=title,
    #             description=description,
    #             file=file,
    #             video=video,
    #             url=videolink,
    #             vname=vname,
    #             videolength=videolength,
    #             published=published,
        
    #             publish_on=publish_on,
    #             created_by=created_by,
    #         )
    #         for i in lst:
    #             if i not in ['[', ',', ']']: 
    #                 carr.append(int(i))

    #         curnt.course.set(carr)
    #         ser = self.serializer_class(curnt)
    #         return Response(ser.data)
    #     else:
    #         return Response({"error":"error"},status=500)


            


        


    # def list(self, request, *args, **kwargs):
    #     pass
# class CurrentAffairsDaySortedViewSet(viewsets.ModelViewSet):
#     queryset = CurrentAffairs.objects.filter(published=True)  # Only published current affairs
#     serializer_class = CurrentAffairsSerializer
#     pagination_class = SinglePagination
#     def get_queryset(self):
#         # if not AuthHandlerIns.is_student(request=self.request):
#         #     return Response({"message": "Only Student can View Popular Teachers"}, status=status.HTTP_401_UNAUTHORIZED)
#         days = self.request.query_params.get('days') 
        
#         if days is not None:
#             current_date = timezone.now().date()
#             filter_date = current_date - timedelta(days=int(days))
#             queryset = self.queryset.filter(
#             Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
#         )
#             return queryset
#         return Response({'No Detail'})

# class CurrentAffairsDaySortedViewSet(viewsets.ModelViewSet):
#     queryset = CurrentAffairs.objects.filter(published=True)  # Only published current affairs
#     serializer_class = CurrentAffairsSerializer
#     pagination_class = SinglePagination

#     def list(self, request, *args, **kwargs):
#         if not AuthHandlerIns.is_student(request=request):
#             return Response(
#                 {"message": "Only students can view Current Affairs."},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         days = self.request.query_params.get('days')

#         if days is not None:
#             current_date = timezone.now().date()
#             filter_date = current_date - timedelta(days=int(days))
#             queryset = self.queryset.filter(
#                 Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
#             )
#         else:
#             queryset = CurrentAffairs.objects.none()  # Return an empty queryset

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


############################## WITH COUNT INPUT ##################################
from django.utils.dateparse import parse_date

# class CurrentAffairsDaySortedViewSet(viewsets.ModelViewSet):
#     queryset = CurrentAffairs.objects.filter(published=True,status=True).order_by('-id')  # Only published current affairs
#     serializer_class = CurrentAffairsSerializer
#     pagination_class = SinglePagination
#     permission_classes = [StudentPermission]

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['user'] = AuthHandlerIns.get_id(request=self.request)
#         print(context['user'],"Context")
#         return context
    
#     def get_queryset(self):
        
#         publish_on_start = self.request.query_params.get('publish_on_start', None)
#         publish_on_end = self.request.query_params.get('publish_on_end', None)
        
#         if publish_on_start and publish_on_end:
#             start_date = parse_date(publish_on_start)
#             end_date = parse_date(publish_on_end)
#             if start_date and end_date:
#                 queryset = self.queryset.filter(publish_on__range=(start_date, end_date))


#         days = self.request.query_params.get('days')
#         if days is not None:
#             current_date = timezone.now().date()
#             filter_date = current_date - timedelta(days=int(days))
#             queryset = self.queryset.filter(
#                 Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
#             )
#             print(queryset)
#             if not queryset.exists():
#                 queryset = CurrentAffairs.objects.filter(published=True,status=True).order_by('-publish_on')[:10]
#         else:
#             queryset = CurrentAffairs.objects.filter(published=True,status=True).order_by('-publish_on')  # Return total queryset

        
#         return queryset

class CurrentAffairsDaySortedViewSet(viewsets.ModelViewSet):
    queryset = CurrentAffairs.objects.filter(published=True, status=True).order_by('-id')  # Only published current affairs
    serializer_class = CurrentAffairsSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = AuthHandlerIns.get_id(request=self.request)
        return context

    def get_queryset(self):
        publish_on_start = self.request.query_params.get('publish_on_start', None)
        publish_on_end = self.request.query_params.get('publish_on_end', None)
        days = self.request.query_params.get('days')

        queryset = self.queryset

        if publish_on_start and publish_on_end:
            start_date = parse_date(publish_on_start)
            end_date = parse_date(publish_on_end)
            if start_date and end_date:
                queryset = queryset.filter(publish_on__range=(start_date, end_date))

        if days is not None:
            current_date = timezone.now().date()
            filter_date = current_date - timedelta(days=int(days))
            queryset = queryset.filter(
                Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
            )
            print(queryset)
            if not queryset.exists():
                queryset = CurrentAffairs.objects.filter(published=True, status=True).order_by('-publish_on')[:10]
        else:
            queryset = queryset.order_by('-publish_on')  # Return total queryset

        return queryset





class StudentRegisterOrg(ModelViewSet):
    serializers_class=StudentOrgerializer

    def create(self,request):
        try:
            try:
                mobile_number=request.data['mobile_number']
                print(mobile_number,'kkkkk')
            except:
                return Response({"message":"invalida request data"},status=400)
            try:
                user=User.objects.get(mobile=mobile_number,is_faculty=False,is_student=False)
                otps = str(random.randint(1000, 9999))
                sendsms(mobile_number,otps)
                serializer=UserOrgerializer(user)
                return Response(serializer.data,status=200)
            except:
                pass
            try:
                mobile=Faculty.objects.get(user__mobile=mobile_number)
                otps = str(random.randint(1000, 9999))
                print("*******************vvvv")
                sendsms(mobile_number,otps)
                print(mobile,'mobile')
                print(otps,'facultyotp')
                mobile.otp=otps
                mobile.save()
            
                serializer=FacutlyOrgerializer(mobile)
                
                print(serializer.data,'dd')
                print(mobile,'mobile')

                return Response(serializer.data,status=200)

                
            except:
            
            

                try:
                    mobile=Student.objects.get(user__mobile=mobile_number)
                    otps = str(random.randint(1000, 9999))
                    print(otps,'otps')
                    print("^^^^")
                    sendsms(mobile_number,otps)
                    print(mobile,'mobile')
                    print(otps,'student otp')
                    mobile.otp=otps
                    mobile.save()
                    print("************")
                    serializer=StudentOrgerializer(mobile)
                    print("************")
                    print(serializer.data,'dd')
                    print(mobile,'mobile')

                    return Response(serializer.data,status=200)
                except:
                    print("noooo")
                    # try:
                    print("1")
                    if StudentOtp.objects.filter(mobile=mobile_number).exists():
                        studentotp=StudentOtp.objects.get(mobile=mobile_number)
                        print(studentotp,'uuuu')
                        print("hhhh")
                        if studentotp.otp is not None:
                            print("PPP")
                            studentotp.otp=None
                            print("PPP")

                            otps = str(random.randint(1000, 9999))
                            sendsms(mobile_number,otps)
                            print(otps,'studentotpmodelotp')
                            studentotp.otp=otps
                            print("PPP")
                            studentotp.save()
                            print("else save")
                            studentotp=StudentOtp.objects.get(mobile=mobile_number)
                            serializer=FirstregSerilizer(studentotp)
                            print("PPP")
                            print(serializer,'ddd')

                            return Response(serializer.data,status=200)
                        else:
                            otps = str(random.randint(1000, 9999))
                            sendsms(mobile_number,otps)
                            # print(mobile,'mobile')
                            print(otps,'studentotpmodelotp')
                            studentotp.otp=otps
                            studentotp.save()
                            print("else save")
                            serializer=FirstregSerilizer(studentotp)
                            print(serializer.data,'kkkk')
                            return Response(serializer.data,status=200)
                    else:   # except:
                        print("2")
                        firstreg=StudentOtp.objects.create(mobile=mobile_number)
                        id=firstreg.id
                        firstregister=StudentOtp.objects.get(id=id)
                        otps = str(random.randint(1000, 9999))
                        print(otps,'firstotp')
                        sendsms(mobile_number,otps)
                        print("************")
                        firstreg.otp=otps
                        firstreg.save()
                        serializer=FirstregSerilizer(firstregister)
                        print("DDDDDD")
                        print(serializer.data,'LLLLLLLLLL')
                        return Response(serializer.data,status=201)
        except:
            return Response({"message":"something went wrong"},status=403)

class NewStudentBatchDetials(ModelViewSet):
    queryset=TimeTable.objects.all()
    serializer_class=StudentTimetableserializers
    permission_classes =[StudentPermission]


    def list(self,request):
        try:
            token = AuthHandlerIns.get_id(request=request)
            if token:
                try:
                    if  request.query_params.get('batchid'):
                        batch_idparams=request.query_params.get('batchid')
                        print(batch_idparams,'shamil')
                        if batch_idparams:
                            studentdetials = Student.objects.get(user=token)
                            print(studentdetials, 'dddd')
                            studentid = studentdetials.pk
                            batchdetials= TimeTable.objects.filter(batch=batch_idparams).order_by('date')
                            print(batchdetials,'kkk')
                            query_set = Rating.objects.filter(user=token).exists()

                            serializers=StudentTimetableserializers(batchdetials,many=True,context={'student_id': studentid,'status': query_set})
                            print("&&&&&&&&&&&&&")
                            return Response(serializers.data,status=200)
                        else:
                            return Response({"something went wrong"})
                    else:

                        print(token, 'dddd')
                        studentdetials = Student.objects.get(user=token)
                        print(studentdetials, 'dddd')
                        studentid = studentdetials.pk
                        # student=StudentBatch.objects.filter(student=Student.objects.get(user__pk=s))
                        if StudentBatch.objects.filter(student=studentid).values():

                            studentbatch=StudentBatch.objects.filter(student=studentid).values()
                            print(studentbatch,'ghjkh')
                            batchid = []
                            for x in studentbatch:
                                batchid.append(x['batch_id'])
                            print(batchid, 'jjjj')
                            print(batchid[0])
                            firstbatch=batchid[0]
                            print(firstbatch,'ooooo')
                            
                            batch=TimeTable.objects.filter(batch=firstbatch).order_by('date')
                            print(batch,'dd')
                            query_set = Rating.objects.filter(user=token).exists()
                            serializers=StudentTimetableserializers(batch,many=True,context={'student_id': studentid,'status': query_set})
                            print('**********************')
                            return Response(serializers.data,status=200)
                        else:
                            return Response([],status=200)
                except:
                    return Response({"message":"something went wrong"},status=403)
                
            else:
                return Response({"message":"tokne missing"},status=401)    
        except:
             return Response({"message":"Invalid Data"},status=403)




class StudentlistTemp(ModelViewSet):
    pagination_class = SinglePagination
    serializer_class=StudentProfileSerializer

    def get_queryset(self):
        print("hello")
        queryset = Student.objects.filter().order_by('-user__joined_date')
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        mobile = self.request.query_params.get('mobile')
        admisn_no = self.request.query_params.get('admission_number')
        exam_no = self.request.query_params.get('exam-no')
        fathers_name = self.request.query_params.get('father_name')
        dob = self.request.query_params.get('dob')
        gender = self.request.query_params.get('gender')
        batch_name = self.request.query_params.get('batch_name')
        branch_name = self.request.query_params.get('branch_name')
        if mobile:
            queryset=queryset.filter(user__mobile__startswith=mobile)

        if name:
            queryset= queryset.filter(name__icontains=name)
        if email:
            queryset=queryset.filter(user__email__icontains=email)
        if admisn_no:
            queryset=queryset.filter(admission_number__icontains=admisn_no)
        if exam_no:
            queryset=queryset.filter(exam_number__icontains=exam_no)
        if fathers_name:
            queryset=queryset.filter(father_name__icontains=fathers_name)
        if dob:
            queryset=queryset.filter(dob__icontains=dob)
        if gender:
            queryset=queryset.filter(dob__icontains=gender)

        if batch_name:
            batch = Batch.objects.filter(name__icontains=batch_name)
            sb= StudentBatch.objects.filter(batch__in=batch).values('student')
            queryset=queryset.filter(id__in=sb)

        if branch_name:
            branch = Branch.objects.filter(name__icontains=branch_name)
            sb = StudentBatch.objects.filter(batch__branch__in=branch).values('student')
            queryset=queryset.filter(id__in=sb)
        
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        if AuthHandlerIns.is_staff(request=request):
            return super().partial_update(request, *args, **kwargs)
        elif AuthHandlerIns.is_student(request=request):
            # student = Student.objects.get(user__id=AuthHandlerIns.get_id(request=request))
            return super().partial_update(request,  *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['admission_number','name','user__username','user__email','user__mobile','scholarship','is_online','is_offline','exam_number','dob'])

        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                'marital_status' : { 1 : 'Single', 2 : 'Married'},
                'emailverified' : {'True': 'Yes','Flase' : 'No'},
                'is_online' : {'True': 'Yes', 'False' :'No' },
                'is_offline' : {'True': 'Yes', 'False' :'No' },
                'scholarship' : {'True' : 'Yes','False':'No'},
            })
            return response
        
        if pdf_query:
            fields = ['admission_number','name','user__username','user__email','exam_number','dob','user__mobile','scholarship','is_online','is_offline']
            headers,data = get_queryset_headers_data(queryset,fields=fields)

            modified_headers = []
            modified_headers = [header
                                .replace('Exam_number','Exam Number')
                                .replace('Admission_number','Admission Number')
                                .replace('Is_online','Online')
                                .replace('Is_offline','Offline')
                                .replace('Scholarshi\np','Scholarship')
                                for header in headers]
            

            
            nameheading = 'Student'
            current_datetime = timezone.now()
            # generating pdf
            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading
            }
            resp = generate_pdf('commonpdf.html',pdf_data,'studentlist.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



            



from django.db.models import Max

class VersionViewSet(ModelViewSet):
    queryset = Version.objects.all().order_by('-id')
    serializer_class = VersionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance= Version.objects.filter(status=True).order_by('-id').first()
         
        serializer = self.get_serializer(instance)
        response_data = {
            
            "data": 
                 serializer.data
            
            
        }
        return Response(response_data)

class EmailVerification(ModelViewSet):
    serializer_class=OnllineStudentSerializer

    def create(self,request):
        id=request.data['id']
        otp=request.data['otp']
        if Student.objects.get(otp=otp,id=id):
            student=Student.objects.get(otp=otp,id=id)
            if student.otp==otp:
                student.emailverified=True
                return Response({"message":"otp and mail are verified"})
            else:
                return Response({"message":"otp is not matching"},status=401)
        else:
            return Response({"message":"something went wrong"})



class StudentOtpVerificationOrg1(ModelViewSet):
    serializer_class=FirstregSerilizer
    # queryset = StudentOtp.objects.all()

    def create(self,request):
        try:
            try:
                user=request.data['userid']
                print(user,'ppp')
                print(user is None,'dddddd')
                print(type(user))
                otp=request.data['otp']
                print(otp,';;;')
                id=request.data['studentotpid']
                print(id,'MMMMMMMM')
            except:
                 return Response({"message":"invalida request data"},status=400)
            if user is not None and user != '':
                print('LLLLLLLL')
                if User.objects.filter(id=user).exists():
                    users = User.objects.filter(id=user).exists()
                    # if user
                    print("***")
                    userss = User.objects.get(id=user)
                    print(userss,'user')
                    print("*******")

                    if userss.is_faculty:
                        print("&&&&&&&&&")
                        faculty = Faculty.objects.get(user=userss.id)
                        
                        print(faculty, 'faculty')
                        if faculty.is_verified == False:
                            print("****d**")
                            return Response({'error': "Account Not verified"}, 403)
                        else:
                            if faculty.otp==otp:
                                print("$$$$")
                                payload = {'id': faculty.user.pk, 'username': faculty.user.username, 'email': faculty.user.email,'admin': faculty.user.is_superuser, 'role': faculty.user.is_roleuser, 'faculty': faculty.user.is_faculty,'student':faculty.user.is_student} 


                                token = AuthHandlerIns.get_token(payload=payload)
                                faculty.otp=None
                                faculty.save()
                            
                        
                                return Response({"token":token,"facultyid":faculty.pk,"userid":payload['id'],"studentid":None,"message":"Otp verirfication is successfull"},status=200)
                            else:
                                return Response({"message":"otp is not matching "},status=401)


                    elif userss.is_student:
                        print("******************DDDDDDDDD")
                        students=Student.objects.get(user__id=user)
                        if students.otp==otp:
                            
                        
                                # payload={'studentid': students.id,'name':students.name,'exam_number':students.exam_number,'admission_number':students.admission_number,'is_online':students.is_online,'is_offline':students.is_offline,'username': students.user.username, 'email': students.user.email,'student': students.user.is_student,'id':students.user.id}
                                payload = {'id': students.user.pk, 'username':students.user.username, 'email': students.user.email,'admin': students.user.is_superuser, 'role': students.user.is_roleuser, 'faculty': students.user.is_faculty,'student':students.user.is_student}
                                if students.is_offline and students.selected_course ==None:
                                    sb=StudentBatch.objects.filter(student=students)
                                    if sb.exists():
                                        students.selected_course=sb.first().batch.course.course
                                print(payload,'payload')

                                token = AuthHandlerIns.get_token(payload=payload)
                                students.otp=None
                                students.save()
                                
                            
                                return Response({"token":token,"facultyid":None,"userid":payload['id'],"studentid":students.pk,
                                                 "is_online":students.is_online,"is_offline":students.is_offline,"message":"Otp verirfication is successfull"},status=200)
                        return Response({"message":"otp is not matching"},status=401)
                    else:
                        return Response({"message":"User login not allowed"}, status=403)
                else:
                    return Response({'error': "No User Found"}, status=404)
            else:
                if StudentOtp.objects.get(id=id):
                    print("PPPPPPPPPPP")
                    firstreg=StudentOtp.objects.get(id=id)
                    if firstreg.otp==otp:
                        firstreg.isverified=True
                        firstreg.save()
                        print("(((())))")
                        # serializers=FirstregOtpSerializer(firstreg)
                        print("LLLL")
                        print(serializers,'dd')
                        return Response({"message":"otp verifaction is successfull","studentotp":id,"Register":False},status=200)
                    else:
                        return Response({"message":"otp is not matching "},status=401)
        except:
            return Response("something went wrong",status=403)
        
from django.core.mail import EmailMessage 
class EmailVerifaction(ModelViewSet):
    serializer_class=FirstregSerilizer
    # queryset = StudentOtp.objects.all()
    def create(self,request):
        try:
            email=request.data['email']
            studentotpid=request.data['studentotpid']
        except:
            return Response({"message":"invalid form data"},status=400)
        if email and studentotpid:
            email=request.data['email']
            mail_subject = f'Subject: Mail verification'
            to_email = email
            otps = str(random.randint(1000, 9999))
            print(otps,'otps')
            body = f"Your otp is {otps}"
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()
            studentotp=StudentOtp.objects.get(id=studentotpid)
            studentotp.otp=otps
            studentotp.save()
            return Response({"mailsend":True,"studentotpid":studentotp.id},status=200)
        return Response(status=403)

class EmailOtpVerification(ModelViewSet):

    def create(self,request):
        try:
            name=request.data['name']
            email=request.data['email']
            dob=request.data['dob']
            gender=request.data['gender']
            id=request.data['id']
            otp=request.data['otp']
        except:
            return Response({"message":"inavalid form data","status":False},status=400)
        if otp:
            student_otp=StudentOtp.objects.get(id=id)
            mobile_num=student_otp.mobile
            if otp==student_otp.otp:
                if User.objects.filter(mobile=mobile_num).exists():
                    return Response({"message":"mobile number allready exist"},status=400)
                elif User.objects.filter(email=email).exists():
                    return Response({"message":"email allready exist"},status=400)
                else:
                    user=User.objects.create_student(username=name,email=email,mobile=mobile_num,password=generate_random_string(10))
                    student=Student.objects.create(user=user,name=name,is_online=True,gender=gender,dob=dob)
                    payload={'studentid': student.id,'name':student.name,'exam_number':student.exam_number,'admission_number':student.admission_number,'is_online':student.is_online,'is_offline':student.is_offline,'username': student.user.username, 'email': student.user.email,'is_student': student.user.is_student,'id':student.user.id}

                    print(payload,'payload')

                    token = AuthHandlerIns.get_token(payload=payload)
                    student.otp=None
                    student.save() 
                    return Response({"token":token,"facultyid":None,"userid":payload['id'],"studentid":payload['studentid'],"message":"Otp verirfication is successfull"},status=200)
                
            else:
                return Response({"message":"Otp miss match","status":False},status=403)
        else:
            return Response({"message":"please enter otp"},status=403)

from django.utils.timezone import now             
class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publications.objects.all().order_by('-id')
    serializer_class = PublicationSerializer
    pagination_class = SinglePagination
    permission_classes =[AdminStudentFaculty]



    def get_queryset(self):
        queryset = Publications.objects.all().order_by('-id')
        # queryset = Publications.objects.all()
        book_name = self.request.query_params.get('bookname',None)
        if book_name:
            queryset = queryset.filter(bookname__icontains = book_name)
        


        return queryset
    
    def list(self,request,*args, **kwargs):

        queryset = self.get_queryset()
        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(request,[field.name for field in queryset.model._meta.fields],{
                'published':{'True':'Yes','Flase':'No'},
                'is_online' : {'True':'Yes','Flase':'No'},
                'paperback' : {'True':'Yes','Flase':'No'},
            })
            return response
        
        if pdf_query:
            fields = ['id','bookname','category','book_price','offlinebook_price','course','edition','publish_on','discount_price','stock','outsider']
            headers,data = get_queryset_headers_data(queryset,fields=fields,)
            # print("iiiiiiiiiiiiiiiiiiii",queryset.course.name)
            modified_headers = []
            modified_headers = [header.replace('Publish_on','Published on')
                                .replace('Book_price','Book Price')
                                .replace('Offlinebook_pric\ne','Offline Price')
                                .replace('Bookname','Book name')
                                .replace('Discount_price','Discount Price')
                                .replace('Offlinebook_price','Offline Book Price')
                                # .replace('Name','Course Name')
                                for header in headers

                                ]
            print('}}}}}}}}}}}}}}}',data)
            nameheading = 'Publication'
            current_datetime = timezone.now()
            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading
            }
            resp = generate_pdf('commonpdf.html',pdf_data,'Publicationlist.pdf')
            return resp
        
        # continue with pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    # def list(self, request, *args, **kwargs):
    #     query = Publications.objects.order_by('-id')
    #     return Response(PublicationSerializer(query,many=True).data)

   
    def create(self, request, *args, **kwargs):
        bookname = request.data['bookname']
        book_price = request.data['book_price']
        icon = request.data['icon']
        discount_price = request.data['discount_price']
        offlinebook_price = request.data['offlinebook_price']
        no_of_pages = request.data['no_of_pages']
        publish_on = request.data['publish_on']
        description = request.data['description']
        edition = request.data['edition']
        category = request.data['category']
        stock = request.data['stock']
        is_online = bool(request.data.get('is_online', False))
        medium = request.data['medium']
        try:
            order_count = request.data['order_count']
        except KeyError:
            order_count = None
        paperback = bool(request.data.get('paperback', True))
        admission_time_price = request.data['adminssion_time_price']
        outsider = request.data['outsider']
        old_student = request.data['old_student']


        try:
            published = request.data['published']
        except:
            published = False
        print(published, 'published')
        course = request.data['course']
        carr=eval(course)
        
        publications=Publications.objects.create(
            bookname=bookname,
            description=description,
            icon=icon,
            book_price=book_price,
            discount_price=discount_price,
            offlinebook_price = offlinebook_price,
            no_of_pages=no_of_pages,
            edition=edition,
            published=published,
            category = category,
            publish_on=publish_on,
            stock = stock,
            is_online=is_online,
            medium=medium,
            order_count=order_count,
            paperback=paperback,
            admission_time_price=admission_time_price,
            old_student=old_student,
            outsider=outsider
            
        )
        

        publications.course.set(carr)
        ser = self.serializer_class(publications)
        return Response(ser.data)
        
    # return Response({"error":"error"},status=500)

    def partial_update(self, request, *args, **kwargs):
        # Retrieve the object to be updated
        instance = self.get_object()

        # Update the required fields
        instance.bookname = request.data.get('bookname', instance.bookname)
        instance.book_price = request.data.get('book_price', instance.book_price)
        instance.icon = request.data.get('icon', instance.icon)
        instance.discount_price = request.data.get('discount_price', instance.discount_price)
        instance.offlinebook_price = request.data.get('offlinebook_price', instance.offlinebook_price)
        instance.no_of_pages = request.data.get('no_of_pages', instance.no_of_pages)
        instance.publish_on = request.data.get('publish_on', instance.publish_on)
        instance.description = request.data.get('description', instance.description)
        instance.edition = request.data.get('edition', instance.edition)
        instance.category = request.data.get('category', instance.category)
        instance.stock = request.data.get('stock', instance.stock)
        instance.is_online = bool(request.data.get('is_online', instance.is_online))
        instance.medium = request.data.get('medium', instance.medium)
        instance.order_count = request.data.get('order_count', instance.order_count)
        instance.paperback = bool(request.data.get('paperback', instance.paperback))
        instance.admission_time_price = request.data.get('admission_time_price', instance.admission_time_price)
        instance.outsider = request.data.get('outsider', instance.outsider)
        instance.old_student = request.data.get('old_student', instance.old_student)
        instance.published = request.data.get('published', instance.published)

        # Save the updated object
        instance.save()

        # Update the related courses
        course = request.data.get('course')
        if course:
            carr = eval(course)
            instance.course.set(carr)

        # Serialize the updated object and return the response
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        print('hellooooooooooooo1')
        obj=self.get_object()
        print('hellooooooooooooo2',)

        raz = razorpay_client.order.create(data={'amount':int(obj.book_price*100), 'currency':'INR'})
        print(raz)
        current_time = now()
        timestamp = datetime.strftime(current_time, "%Y%m%d%H%M%S")
        random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))
        order_id = f"{timestamp}-{random_string}"
        user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        pay=OnlineOrderPayment.objects.create(user=user,user_ref=user.id,order_number=order_id,product='publication',product_id=obj.id,razor_id=raz['id'],total_amount=obj.book_price,paid_amount=raz['amount_paid']/100,off_amount=0,offer_choice='none',payment_status='pending',delivery_status='pending')

        return Response(raz)
    
class PublicationViewSetForStudent(viewsets.ReadOnlyModelViewSet):
    queryset = Publications.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = SinglePagination
    permission_classes =[StudentPermission]

    def get_queryset(self):
            queryset = Publications.objects.filter(published=True).order_by('-id')

            return queryset


from finance.razorpay import razorpay_client 
import re
from bs4 import BeautifulSoup

@api_view(['GET'])
def deletestudent(request):
    print("heysssssssssssss")
    ss = NewQuestionPool.objects.get(id=79592)
    print(ss.question_text)
    html_string=ss.question_text
    # li_elements = re.findall(r"<li>(.*?)<\/li>", html_string)
    # li_elements_without_tags = [re.sub(r"<.*?>", "", li) for li in li_elements]
    soup = BeautifulSoup(html_string, 'html.parser')
    li_elements = [li.get_text(strip=True) for li in soup.find_all('li')]
    return Response({ss.question_text:li_elements})


class EmailOtpVerification1(ModelViewSet):
    
    def create(self,request):
        # try:
            try:
                name=request.data['name']
                email=request.data['email']
                dob=request.data['dob']
                gender=request.data['gender']
                id=request.data['id']
                otp=request.data['otp']
                emailverified=request.data['emailverified']
            except:
                return Response({"message":"inavalid form data","status":False},status=400)
            
            if emailverified==True:
                print("tttt")
                if StudentOtp.objects.filter(id=id).exists():
                    student_otp=StudentOtp.objects.get(id=id)
                    mobile_num=student_otp.mobile
                    if User.objects.filter(mobile=mobile_num).exists():
                        return Response({"message":"mobile number allready exist"},status=400)
                    elif User.objects.filter(email=email).exists():
                        return Response({"message":"email allready exist"},status=400)
                    else:
                        user=User.objects.create_student(username=name,email=email,mobile=mobile_num,password=generate_random_string(10))
                        student=Student.objects.create(user=user,name=name,is_online=True,gender=gender,dob=dob)
                        # payload={'studentid': student.id,'name':student.name,'exam_number':student.exam_number,'admission_number':student.admission_number,'is_online':student.is_online,'is_offline':student.is_offline,'username': student.user.username, 'email': student.user.email,'is_student': student.user.is_student,'id':student.user.id}
                        payload = {'id': student.user.pk, 'username':student.user.username, 'email': student.user.email,'admin': student.user.is_superuser, 'role': student.user.is_roleuser, 'faculty': student.user.is_faculty,'student':student.user.is_student}

                        print(payload,'payload')

                        token = AuthHandlerIns.get_token(payload=payload)
                        student.otp=None
                        student.save() 
                        return Response({"token":token,"facultyid":None,"userid":payload['id'],"studentid":student.pk,"is_online":student.is_online,"is_offline":student.is_offline,"message":"Otp verirfication is successfull"},status=200)
                else:
                    return Response({'message':"Student otp matching query does not exist"},status=404)
            elif emailverified==False:
                print("kkkkkk")
                if otp:
                    student_otp=StudentOtp.objects.get(id=id)
                    mobile_num=student_otp.mobile
                    if otp==student_otp.otp:
                        if User.objects.filter(mobile=mobile_num).exists():
                            return Response({"message":"mobile number allready exist"},status=400)
                        elif User.objects.filter(email=email).exists():
                            return Response({"message":"email allready exist"},status=400)
                        else:
                            user=User.objects.create_student(username=name,email=email,mobile=mobile_num,password=generate_random_string(10))
                            student=Student.objects.create(user=user,name=name,is_online=True,gender=gender,dob=dob)
                            # payload={'studentid': student.id,'name':student.name,'exam_number':student.exam_number,'admission_number':student.admission_number,'is_online':student.is_online,'is_offline':student.is_offline,'username': student.user.username, 'email': student.user.email,'is_student': student.user.is_student,'id':student.user.id}
                            payload = {'id': student.user.pk, 'username':student.user.username, 'email': student.user.email,'admin': student.user.is_superuser, 'role': student.user.is_roleuser, 'faculty': student.user.is_faculty,'student':student.user.is_student}
                            print(payload,'payload')

                            token = AuthHandlerIns.get_token(payload=payload)
                            student.otp=None
                            student.save() 
                            return Response({"token":token,"facultyid":None,"userid":payload['id'],"studentid":student.pk,"is_online":student.is_online,"is_offline":student.is_offline,"message":"Otp verirfication is successfull"},status=200)
                        
                    else:
                        return Response({"message":"Otp miss match","status":False},status=403)
                else:
                    return Response({"message":"please enter otp"},status=403)
            else:
                return Response({"message":"invalida request data"},status=400)
                
        # except:
        #     return Response({"something went wrong"},status=403)

class EditStudentBatchDetials(viewsets.ModelViewSet):
    serializer_class = EditStudentBatchSerializer
    queryset = StudentBatch.objects.all()


class StudentUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_student=True)
    serializer_class = UserSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]



class StudentApplicationViewSet(viewsets.ModelViewSet):
    queryset = StudentApplicationOffline.objects.all().order_by('-created_at')
    pagination_class = SinglePagination
    serializer_class = StudentApplicationSerializer
    
    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in [ 'create']:
            self.permission_classes = [ ]
        elif self.action in ['list','retrieve','update', 'partial_update']:
            self.permission_classes = [AdminAndRolePermission, ]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset=StudentApplicationOffline.objects.all().order_by('-created_at')
        branch = self.request.query_params.get('branch')
        if branch:
            queryset = queryset.filter(branch=branch)
        
        branch_name = self.request.query_params.get('branch_name')
        if branch_name:
            queryset = queryset.filter(branch__name__icontains=branch_name)
        
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        phone = self.request.query_params.get('phone')
        if phone:
            queryset = queryset.filter(phone__startswith=phone)
        
        father_name = self.request.query_params.get('father_name')
        if father_name:
            queryset = queryset.filter(father_name__icontains=father_name)
        
        guardian_name = self.request.query_params.get('guardian_name')
        if guardian_name:
            queryset = queryset.filter(guardian_name__icontains=guardian_name)

        guardian_mobile = self.request.query_params.get('guardian_mobile')
        if guardian_mobile:
            queryset = queryset.filter(guardian_name__icontains=guardian_mobile)
        
        approved = self.request.query_params.get('approved')
        if approved:
            queryset = queryset.filter(approved__icontains=approved)
        
        batch = self.request.query_params.get('batch')
        if batch:
            queryset = queryset.filter(batch__icontains=batch)
        
        return queryset

import json
class NewStudentRegister(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentRegisterSerializer

    def create(self, request, *args, **kwargs):
        user = None
        print(request.data,'request data******')
        user_data = {
            'username': request.data['username'],
            'email': request.data['email'],
            'mobile': request.data['mobile'],
            'password': request.data['password'],
        }

        
        try:
            user_exists = User.objects.filter(username=request.data['username']).exists()
            mobile_exists = User.objects.filter(mobil=request.data['mobile']).exists()
            email_exists = User.objects.filter(email=request.data['email']).exists()
            if user_exists:
                return Response({"message": "Username already exists"})
            if mobile_exists:
                return Response({"message": "Mobile already exists"})
            if email_exists:
                return Response({"message": "Email already exists"})
        except:
            pass

        with transaction.atomic():
            try:       
                user = User.objects.create_student(**user_data)
                ids=request.data['id']
                studentapplications=StudentApplicationOffline.objects.get(id=ids)
                modified_data = request.data.copy() 
                if 'photo' not in request.data:
                    # If 'photo' is not in modified_data, set it from studentapplications.photo
                    modified_data['photo'] = studentapplications.photo
                    serializer = self.get_serializer(data=modified_data)
                    serializer.is_valid(raise_exception=True)
                    student = serializer.save(user=user)
                else:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    student = serializer.save(user=user)
                students = Student.objects.get(user=user)

                student_batch_data = {
                        "student":students,
                        'batch': request.data['batch'],
                        'branch': request.data['branch'],
                        'batch_name': request.data['batch_name'],
                        'branch_name': request.data['branch_name'],
                    }

                # student_batch_serializer = StudentBatchSerializer(data=student_batch_data)
                # student_batch_serializer.is_valid(raise_exception=True)
                # student_batch = student_batch_serializer.save()
                # student = Student.objects
                print("hellllllllllllllllllllllll")
                sb= StudentBatch.objects.create(
                        student=students,
                        batch= Batch.objects.get(id=request.data['batch']),
                        branch=Branch.objects.get(id=request.data['branch']),
                        batch_name=request.data['batch_name'],
                        branch_name= request.data['branch_name']
                    )
                fees = StudentFeeCollection.objects.create(
                    student=user,
                    batch_package = BatchPackages.objects.get(id=request.data['batch_package']),
                    
                    amountpaid = request.data['amountpaid']
                    )
                pub = json.loads(request.data['publication'])
                studymat = json.loads(request.data['study_materials'])
                qb = json.loads(request.data['question_bank']) 
                fees.publications.set(pub)
                fees.study_materials.set(studymat)
                fees.question_banks.set(qb)

                
                print(sb,"sbbbbb")

                return Response({'message': 'Student registered successfully', 'student_id': student.id}, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # Handle unique constraint violation
                if 'accounts_user_email_key' in str(e):
                    return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'accounts_user_mobile_key' in str(e):
                    return Response({'message': 'mobilenumber already exists'}, status=status.HTTP_400_BAD_REQUEST)  
                else:
                    return Response({'message': f'An error occurred {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                # Rollback the transaction if an exception occurs
                if user:
                    user.delete()
                raise
from MobileApp.serializers import StudentFeeAfterAdmissionSerializer
class StudentRegWithoutApplication(ModelViewSet):
    queryset = Student.objects.all()

    permission_class = [AdminAndRolePermission]
    serializer_class = StudentRegisterSerializer
    
    def create(self, request, *args, **kwargs):

        with transaction.atomic():


                userSerialzer = UserNewSerializer(data=request.data)
                
                studentSer = StudentFeeAfterAdmissionSerializer(data=request.data)

                batchpackage=request.data['batch_package']
                amount = request.data['amountpaid']

                try:
                    try:
                        photo = request.data['photo']  # Attempt to get 'photo' from request.data
                    except KeyError:
                        ids = request.data['id']
                        studentapplications = StudentApplicationOffline.objects.get(id=ids).photo
                        photo = None  # Set photo to None when 'photo' key is not found
                    except Exception as e:
                        # Handle other exceptions if necessary
                        photo = None  # Set photo to None in case of exceptions
                except:
                    studentapplications = None

                # print("   ----------------           ",userSerialzer.is_valid(),studentbatch.is_valid(),student.is_valid(),)
                # photo=None
                if userSerialzer.is_valid(raise_exception =True):
                    user_data = userSerialzer.save()
                    data = request.data
                    data['user']=user_data.id
                    try:
                        data['photo']=photo if photo else studentapplications
                    except:
                        data['photo']=None
                        

                    student = StudentRegisterSerializer(data = data)
                    print(user_data.id,"   78999999999999999999    ")
                    if student.is_valid(raise_exception =True):
                        print(" popyyyyyyyyyyyyyy")
                        student_data = student.save()

                        # print('  hhhhhhh        ',studentbatch.is_valid(),studentSer.is_valid())
                        # print("        ==========   ",studentbatch.errors)
                        data = request.data
                        data['student']=student_data.id
                        print()

                        studentbatch = EditStudentBatchSerializer(data=data)

                        print('  hhhhhhh        ',studentSer.is_valid())
                        print(" ppppp     ",studentSer.errors)

                        if  studentbatch.is_valid():
                            studentbatch_data = studentbatch.save()
                            data = request.data
                            data['student'] = user_data.id

                            if studentSer.is_valid(raise_exception =True):
                                    print("       ++++++++++++++++++++            ")
                                    studentBatchData = studentbatch.save(student=student_data)

                                    queryset =  BatchPackages.objects.get(id=batchpackage)

                                    books_theyWant = queryset.publications.values_list('id',flat=True)
                                    material_theyWant = queryset.study_meterial.values_list('id',flat=True)
                                    qn_theyWant = queryset.question_book.values_list('id',flat=True)
                                
                                    
                                    publication = request.data['publications']
                                    study = request.data['study_materials']
                                    question = request.data['question_banks']

                                    batch_package =BatchPackages.objects.filter(id=batchpackage).annotate(
                                                total_study_material_price=Sum(F('study_meterial__book_price'), output_field=DecimalField()),
                                                total_question_book_price=Sum(F('question_book__book_price'), output_field=DecimalField()),
                                                total_publications_price=Sum(F('publications__book_price'), output_field=DecimalField())
                                            ).annotate(grand_total=F('total_study_material_price')+F('total_question_book_price')+F('total_publications_price')+F('batch__fees'))
                                        
                                    grand_total = batch_package.first().grand_total

                                    if not queryset.study_meterial.filter(id__in = study).exists():
                                        return Response({'Message':'Invalid material'},status=500)
                                    elif not queryset.publications.filter(id__in = publication).exists():
                                        return Response({'Message':'Invalid book'},status=500)
                                    elif queryset.question_book.filter(id__in = question).exists():
                                        return Response({'Message':'Invalid question Bank'},status=500)
                                    elif amount > grand_total:
                                        return Response({'Message':'Amount is higher than the total amount'},status=500)

                                    else:
                                        pass
                                        

                                    # user_data = userSerialzer.save()
                                    # student_data = student.save(user=user_data,photo = photo if photo else studentapplications)
                                    # studentBatchData = studentbatch.save(student=student_data)
                                    studSeri = studentSer.save()
                                

                                    return Response({'message': 'Student registered successfully', 'student_id': student.data}, status=status.HTTP_201_CREATED)
                else:
                    print("ppppppppppppppppp")
                    userSerialzer.is_valid(raise_exception=True)
                    studentbatch.is_valid(raise_exception=True)
                    student.is_valid(raise_exception=True)
                    studentSer.is_valid(raise_exception = True)


                    # return Response
            

            


    

class DashBoardProfile(ModelViewSet):
    serializer_class=dashboradserializer
    permission_classes = [StudentPermission]

    def list(self, request, *args, **kwargs):
        if AuthHandlerIns.is_student(request=self.request):
            id = AuthHandlerIns.get_id(request=self.request)
            student = get_object_or_404(Student, user__id=id)
            serializer = dashboradserializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class Deliveryaddress(viewsets.ModelViewSet):
    serializer_class=DeliveryaddressSerializer
    queryset=DeliveryAddress.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = AuthHandlerIns.get_id(request=self.request)  # Assuming you have authentication set up
            request.data['user'] = user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message":"Authenication error"},status=403)

    
    def list(self,request,*args,**kwargs):
        try:
            user=AuthHandlerIns.get_id(request=self.request)
            if user:
                queryset=DeliveryAddress.objects.filter(user=user)
                serializers=self.get_serializer(queryset,many=True)
                return Response(serializers.data,status=200)
        except:
            return Response({"message":"Authenication error"},status=403)
    
    
    def update(self, request, *args, **kwargs):
        try:
            user = AuthHandlerIns.get_id(request=self.request)
            print(user,'jjjj')
            instance = self.get_object()
            if AuthHandlerIns.is_staff(request=self.request):
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif instance.user.id == user:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Authentication error"}, status=status.HTTP_403_FORBIDDEN)

        except:
            return Response({"message": "something went wrong"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        try:
            user = AuthHandlerIns.get_id(request=self.request)
            instance = self.get_object()
            if AuthHandlerIns.is_staff(request=self.request):
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif instance.user.id == user:
                self.perform_destroy(instance)
                return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Authentication error"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"message": "something went wrong"}, status=status.HTTP_403_FORBIDDEN)
        


class studentDeclarationsViewSet(viewsets.ModelViewSet):
    serializer_class=Studentdeclarationserializer
    queryset=StudentDeclaration.objects.all()

from rest_framework.parsers import MultiPartParser, FormParser
import re
# class RankListViewSet(viewsets.ModelViewSet):
#     serializer_class=RankListSerializer
#     queryset=RankList.objects.all()
#     pagination_class=SinglePagination
#     # permission_classes = [AdminAndRolePermission]
#     parser_classes = (MultiPartParser, FormParser)


#     def create(self, request, *args, **kwargs):
#         file = request.FILES['file'] 
#         exam_name = request.data.get('exam_name')
#         created_by = request.data.get('created_by')
        

#         df = pd.read_excel(file, usecols=["Name", "DOB"]) 
#         df['DOB'] = df['DOB'].astype(str)
#         df['Full_Name'] = df['Name'] + '' + df['DOB']
#         cleaned_full_names = {re.sub(r'[^a-zA-Z0-9]', '', full_name) for full_name in df['Full_Name']}
#         print(cleaned_full_names)
#         students = Student.objects.all()
#         student_info_set = {re.sub(r'[^a-zA-Z0-9]', '', f"{student.name.upper()} {student.dob}") for student in students}
        
#         common_info = cleaned_full_names.intersection(student_info_set)
#         common_info_list = list(common_info)
#         print(common_info_list,"common Info List")
#         def convert_to_date(date_str):
#             try:
#                 date = datetime.strptime(date_str[-8:], '%Y%m%d').date()
#                 return date.strftime('%Y-%m-%d')
#             except ValueError:
#                 return None
#         formatted_dates = [convert_to_date(entry[-8:]) for entry in common_info_list]
#         print(formatted_dates)
#         filtered_students = Student.objects.filter(
#         Q(name__istartswith=common_info_list[0][:4]) &
#         Q(dob__in=formatted_dates)
#     )
#         print(filtered_students,"FILTERED")
#         rank_list_entry = RankList.objects.create(
#             exam_name=exam_name,
#             file=file,
#             created_by=User.objects.get(id=created_by) 
#         )
        
#         serializer = StudentSerializer(filtered_students, many=True)
#         return Response(serializer.data)
#         # return super().create(request, *args, **kwargs)

#     # def get_queryset(self):
#     #     list_id = self.request.query_params.get('list_id', None)
#     #     pass



class RankListViewSet(viewsets.ModelViewSet):
    serializer_class = RankListSerializer
    queryset = RankList.objects.all()
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')  # Use get to avoid KeyError if 'file' is not in request
        exam_name = request.data.get('exam_name')
        created_by = request.data.get('created_by')

        if not file:
            return Response({'error': 'File not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, usecols=["Name", "DOB"])
            df['DOB'] = df['DOB'].astype(str)
            df['Full_Name'] = df['Name'] + '' + df['DOB']
            cleaned_full_names = {re.sub(r'[^a-zA-Z0-9]', '', full_name) for full_name in df['Full_Name']}

            if not cleaned_full_names:
                return Response({'error': 'No valid names found in the file.'}, status=status.HTTP_400_BAD_REQUEST)

            students = Student.objects.all()
            student_info_set = {re.sub(r'[^a-zA-Z0-9]', '', f"{student.name.upper()} {student.dob}") for student in students}

            common_info = cleaned_full_names.intersection(student_info_set)
            common_info_list = list(common_info)

            if not common_info_list:
                return Response({'error': 'No common info found with students.'}, status=status.HTTP_400_BAD_REQUEST)

            def convert_to_date(date_str):
                try:
                    date = datetime.strptime(date_str[-8:], '%Y%m%d').date()
                    return date.strftime('%Y-%m-%d')
                except ValueError:
                    return None

            formatted_dates = [convert_to_date(entry[-8:]) for entry in common_info_list if entry]
            formatted_dates = [date for date in formatted_dates if date]  # Remove None values

            if not formatted_dates:
                return Response({'error': 'No valid dates found in common info.'}, status=status.HTTP_400_BAD_REQUEST)

            if not common_info_list:
                return Response({'error': 'Common info list is empty.'}, status=status.HTTP_400_BAD_REQUEST)

            if not formatted_dates:
                return Response({'error': 'Formatted dates list is empty.'}, status=status.HTTP_400_BAD_REQUEST)

            filtered_students = Student.objects.filter(
                Q(name__istartswith=common_info_list[0][:4]) &
                Q(dob__in=formatted_dates)
            )

            if not filtered_students:
                return Response({'error': 'No matching students found.'}, status=status.HTTP_404_NOT_FOUND)

            rank_list_entry = RankList.objects.create(
                exam_name=exam_name,
                file=file,
                created_by=User.objects.get(id=created_by)
            )

            serializer = StudentSerializer(filtered_students, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    

