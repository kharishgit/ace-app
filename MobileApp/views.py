from itertools import chain
from django.forms import BooleanField
from django.shortcuts import render
from rest_framework import viewsets,status
from accounts.api.authhandle import AuthHandlerIns ,attendanceIns
from accounts.api.serializers import FacultyCourseAdditionSerializer, FacultyQuestionSerchserializer, FacultySerializer, QuestionPoolSerializer
# from aceapp.settings.base import AWS_STORAGE_BUCKET_NAME
from searchall.utils import generate_pdf,get_queryset_headers_data
from searchall.views import queryset_to_excel
from course.serializers import CourseSerializer, OnlineCategorySerializer, OnlineLevelSerializer,ReviewSerializer,BatchSerializer
from student.models import Publications, Student
from student.serializers import CurrentAffairsSerializer, PublicationSerializer, StudentSyllabusSerializer
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from permissions.permissions import AdminAndRolePermission, AdminStudentFaculty, FacultyPermission, NonePermission, StudentFacultyPermission, StudentPermission,AdminOrStudent,AdminOrFaculty,AdminAndRoleOrFacultyPermission
from course.views import SinglePagination
from django.db.models import F, Window
from django.db.models.functions import DenseRank
from finance.razorpay import razorpay_client
from django.utils.timezone import now    
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
import base64
from django.core.files.base import ContentFile
from course.views import create_history_user__decorator,set_history_user_delete,set_history_user
from course.serializers import HistorySerializer,HistoryCourseSerializer
from django.db.models import Case, When, BooleanField
# Create your views here.


class QuizPoolViewset(viewsets.ModelViewSet):
    permission_classes =[AdminAndRolePermission]
    queryset = QuizPool.objects.all()
    serializer_class = QuizPoolViewsetSerializer
    pagination_class = SinglePagination


    def get_serializer_class(self):
        if self.action == 'retrieve':
            if 'category' in self.request.query_params:
                return OnlineCategorySerializer
            elif 'level' in self.request.query_params:
                return OnlineLevelSerializer
            elif 'question' in self.request.query_params:
                return QuestionSerializer

            else:
                return QuizPoolUserViewsetSerializer

        # Fallback to default serializer class for other actions
        return super().get_serializer_class()

    def get_queryset(self):
        queryset=QuizPool.objects.all().order_by('-created_at')
        levels = self.request.query_params.get('levels', None)
        if levels:
            queryset = queryset.filter( level__name__icontains=levels)

        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        id = self.request.query_params.get('id', None)
        if id:
            queryset = queryset.filter(id__icontains=id)
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        category = self.request.query_params.get('category', None)
        if category:
            quiz= QuizPool.objects.filter().values('level')
            level = Level.objects.filter().exclude(id__in=quiz).values('category')
            category = Category.objects.filter(id__in=level)
            ser = OnlineCategorySerializer(category, many=True)
            return Response(ser.data)
        level = self.request.query_params.get('level', None)
        if level:
            quiz= QuizPool.objects.filter().values('level')
            level = Level.objects.filter(category__id=kwargs['pk']).exclude(id__in=quiz)
            
            ser = OnlineLevelSerializer(level, many=True)
            return Response(ser.data)
        question = self.request.query_params.get('question', None)
        if question:
            quiz= QuizPool.objects.filter(id=kwargs['pk']).values('question')
            # queryset = QuestionPool.objects.filter(id__in=quiz).values('questions')

            queryset= NewQuestionPool.objects.filter(id__in=quiz)
            id = self.request.query_params.get('id') 
            if id:
                queryset= queryset.filter(id__icontains=id)
            question_text = self.request.query_params.get('question_text')

            if question_text:
                queryset= queryset.filter(question_text__icontains=question_text)
            
            # print(queryset,"ggggggggggggggggggg")
            serializer = QuestionSerializer(queryset, many=True)
            page = self.paginate_queryset(queryset)
            
        
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    

import json

class DailyNewsHistory(viewsets.ModelViewSet):
    queryset = DailyNews.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= DailyNews.history.filter(id=branch_id)
        else:
            queryset= DailyNews.history.all().order_by('-history_date')
        
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
    
class QuestionPoolHistory(viewsets.ModelViewSet):
    queryset = QuizPool.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= QuizPool.history.filter(id=branch_id)
        else:
            queryset= QuizPool.history.all().order_by('-history_date')
        
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

class SuccessStoriesHistory(viewsets.ModelViewSet):
    queryset = SuccessStories.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= SuccessStories.history.filter(id=branch_id)
        else:
            queryset= SuccessStories.history.all().order_by('-history_date')
        
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
class MobileBannerHistory(viewsets.ModelViewSet):
    queryset = MobileBanner.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= MobileBanner.history.filter(id=branch_id)
        else:
            queryset= MobileBanner.history.all().order_by('-history_date')
        
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
    
class QuestionCategoryHistory(viewsets.ModelViewSet):
    queryset = QuestionCategory.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= QuestionCategory.history.filter(id=branch_id)
        else:
            queryset= QuestionCategory.history.all().order_by('-history_date')
        
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
    
class QuestionBookHistory(viewsets.ModelViewSet):
    queryset = QuestionBook.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= QuestionBook.history.filter(id=branch_id)
        else:
            queryset= QuestionBook.history.all().order_by('-history_date')
        
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
class StudyMaterialHistory(viewsets.ModelViewSet):
    queryset = StudyMaterial.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= StudyMaterial.history.filter(id=branch_id)
        else:
            queryset= StudyMaterial.history.all().order_by('-history_date')
        
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
class BatchPackagesHistory(viewsets.ModelViewSet):
    queryset = BatchPackages.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= BatchPackages.history.filter(id=branch_id)
        else:
            queryset= BatchPackages.history.all().order_by('-history_date')
        
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
    
class ShortsHistory(viewsets.ModelViewSet):
    queryset = Shorts.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= Shorts.history.filter(id=branch_id)
        else:
            queryset= Shorts.history.all().order_by('-history_date')
        
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
class GeneralVideoHistory(viewsets.ModelViewSet):
    queryset = GeneralVideos.history.all().order_by('-history_date')
    serializer_class = HistoryCourseSerializer
    pagination_class =SinglePagination

    def get_queryset(self):
        
        branch_id = self.request.query_params.get('branch_id', None)
        if branch_id:
            queryset= GeneralVideos.history.filter(id=branch_id)
        else:
            queryset= GeneralVideos.history.all().order_by('-history_date')
        
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

class DailyNewsViewset(viewsets.ModelViewSet):
    queryset = DailyNews.objects.all()
    serializer_class = DailyNewsSerializer
    pagination_class = SinglePagination

    def get_queryset(self):
        queryset = DailyNews.objects.all().order_by('-id')
        return queryset
    

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        title = request.data['title']
        description = request.data['description']
        file = request.data['file']
        video = request.data['video']
        publish_on = request.data['publish_on']
        url = request.data['url']
        created_by = User.objects.get(id=request.data['created_by']) 



        try:
            published = bool(request.data['published'])
        except:
            published = False
        # course = request.data['course']
        # carr=eval(course)
        # print(carr)
        
        dailynews=DailyNews.objects.create(
            title=title,
            description=description,
            file=file,
            video=video,
            url=url,
            published=published,
            created_by=created_by,
    
            publish_on=publish_on
            
        )
        
        ser = self.serializer_class(dailynews)
        return Response(ser.data)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 

class DailyNewsViewOnlyset(viewsets.ModelViewSet):
    queryset = DailyNews.objects.all()
    serializer_class = DailyNewsSerializer
    pagination_class = SinglePagination

    def get_queryset(self):
        queryset = DailyNews.objects.filter(published=True).order_by('-id')
        return queryset


class QuizPoolAppView(viewsets.ModelViewSet):
    serializer_class = QuizPoolUserViewsetSerializer
    pagination_class = SinglePagination
    def get_queryset(self):
        level = self.request.query_params.get('level') 
        if level:
            queryset= QuizPool.objects.filter(level__id=level)
            return queryset

        return Response({"level":"Not Provided"})
    
    def create(self, request, *args, **kwargs):
        question_id= request.data['questions']
        question_ans = NewQuestionPool.objects.filter(id__in=question_id).values('id','answer')
   
        return Response(question_ans)
    


    
class QuestionViewset(viewsets.ModelViewSet):
    serializer_class = QuestionPoolSerializer
    pagination_class = SinglePagination
    queryset = NewQuestionPool.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        # queryset = QuestionPool.get_questions(level_id=kwargs['pk'])
        queryset = NewQuestionPool.objects.filter(levels__id=kwargs['pk'])
        print(queryset,"ques")
        # queryset= Question.objects.filter(id__in=queryset)
        id = self.request.query_params.get('id') 
        if id:
            queryset= queryset.filter(id__icontains=id)
        question_text = self.request.query_params.get('question_text') 
        if question_text:
            queryset= queryset.filter(question_text__icontains=question_text)
        
        # print(queryset,"ggggggggggggggggggg")
        serializer = QuestionPoolSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        
      
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DailyNewsSortedViewSet(viewsets.ModelViewSet):
    queryset = DailyNews.objects.filter(published=True)  # Only published Daily News
    serializer_class = DailyNewsSerializer
    def get_queryset(self):
        days = self.request.query_params.get('days') 
        
        if days is not None:
            current_date = timezone.now().date()
            filter_date = current_date - timedelta(days=int(days))
            queryset = self.queryset.filter(
            Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
        )
            return queryset
        return Response({'No Detail'})
    


class PublicationsListViewset(viewsets.ReadOnlyModelViewSet):
    pagination_class = SinglePagination
    serializer_class = PublicationSerializer

    def get_queryset(self):
        queryset= Publications.objects.all()
        # student = Student.objects.get(user__id=AuthHandlerIns.get_id(request=self.request)).id
        return queryset
    
class SuccessStoriesViewSet(viewsets.ModelViewSet):
    queryset = SuccessStories.objects.all()
    serializer_class = SuccessStoriesSerializer
    pagination_class = SinglePagination
    permission_classes =[AdminStudentFaculty]
    ############################SEARCH STARTS####################################
    def get_queryset(self):
        # Apply search filter
        search_query = self.request.query_params.get('search', None)
        print(search_query)
        if AuthHandlerIns.is_student(request=self.request):
            queryset = SuccessStories.objects.filter(published=True,active=True)
        else:
            queryset = SuccessStories.objects.all().order_by('-created_at')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) |
                                       Q(description__icontains=search_query) |
                                       Q(created_at__icontains=search_query) |
                                       Q(url__icontains=search_query) |
                                       Q(video__icontains=search_query)).distinct()
            
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        description = self.request.query_params.get('description', None)
        if description:
            queryset = queryset.filter(description__icontains=description)
        
        video = self.request.query_params.get('video', None)
        if video:
            queryset = queryset.filter(video__icontains=video)
        
        url = self.request.query_params.get('url', None)
        if url:
            queryset = queryset.filter(url__icontains=url)
        
        queryset = queryset.order_by(F('created_at').desc())
    
        return queryset

    ############################ SEARCH ENDS ####################################

    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        ########################## SEARCH EXCEL PDF######################################
        pdf_query = self.request.query_params.get('pdf', None)

        excel_query = self.request.query_params.get('excel', None)
        # queryset = SuccessStories.objects.filter(published=True,active=True)
        print(excel_query,"NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                            'video': {'V': 'VIMEO', 'Y': 'YOUTUBE'},
                            'published': {'True': 'Yes', 'False': 'No'},
                            'active': {'True': 'Yes', 'False': 'No'}
                            
                        })
            return response
        if pdf_query:
            fields = ['title', 'description', 'created_at']
            headers, data = get_queryset_headers_data(queryset, fields=fields)
            print(headers, 'headers')
            modified_headers = []
            modified_headers.append(headers[0].replace('title', 'Title'))
            modified_headers.append(headers[1].replace('description', 'Description'))
            modified_headers.append(headers[2].replace('created_at', 'Created Date'))
            print(modified_headers, 'modified headers')
               
            nameheading = 'SuccessStories'
            current_datetime = timezone.now()
            # Generate the PDF 
            pdf_data = {
                'headers': modified_headers,
                'data': data,
                'current_datetime': current_datetime,
                'model': nameheading
            } 
            resp = generate_pdf('commonpdf.html', pdf_data, 'SuccessStories.pdf')  
            return resp

        ########################## SEARCH EXCEL PDF END ######################################

        page =self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response({"data": serializer.data})
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
#     def retrieve(self,request,*args,**kwargs):
#         print(kwargs['pk'],"KWARGS")
#         try :
#             print("1")
#             succes_stories = SuccessStories.objects.get(id = kwargs['pk'])
#             print("2",succes_stories)
#             serializer = SuccessStoriesSerializer(succes_stories,many=False)
#             return Response({"data":serializer.data})
#         except Exception as e:
#             print("3",e)
#             return Response({
#     "detail": "Not found"
# },status=status.HTTP_404_NOT_FOUND)   
        # return super().retrieve(request, *args, **kwargs)

        
    
class PopularFacultyListView(viewsets.ReadOnlyModelViewSet):
   
    # queryset = Faculty.objects.filter(modeofclasschoice__in=[2,3])
    serializer_class = FacultySerializer

    def get_queryset(self):
        queryset = Faculty.objects.filter(modeofclasschoice__in=[2,3])
        # rat = Rating.objects.filter(rate).values()
        # print(rat,"ggggggggggggggggggggggh")
        # queryset = Faculty.objects.filter(id__in=rat)
        rat = Rating.objects.all()
        for i in rat:
            print(i.rating_on.faculty)
            # i.fac_rat=Faculty.objects.get(user__id=i.rating_on.faculty.id) 
            # i.save
        # print(queryset,"hhhhhhhhhhhhhhhhhhhhhhhh")
        return queryset


class FeedBackForFacultyViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = SinglePagination

    
    def list(self, request, user_id=None):
        user_id = AuthHandlerIns.get_id(request=request)
        timetable = TimeTable.objects.filter(faculty = user_id).order_by('-date')
        timetable_id = self.request.query_params.get('review_on')
        reviews = Review.objects.filter(review_on=timetable_id).order_by('review_on__date')
        feedback_data = [review.feedback for review in reviews if review.feedback]

        return Response(feedback_data)

class FacultyBasedFeedBack(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class  = SinglePagination
    permission_classes = [AdminOrFaculty]
    
    def get_queryset(self):
        queryset=Review.objects.all()
        if AuthHandlerIns.is_staff(request=self.request):
            user_id = self.request.query_params.get('user')
        else:
            user_id = AuthHandlerIns.get_id(request=self.request)
        queryset = queryset.filter(review_on__faculty = user_id).order_by('-review_on__date')
        return queryset


    

class BannerAddViewSet(viewsets.ModelViewSet):
    queryset = MobileBanner.objects.all()
    serializer_class = MobileBannerSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminStudentFaculty]

    def get_queryset(self):
        if AuthHandlerIns.is_faculty(request=self.request):
            queryset = self.queryset.filter(is_faculty = True)
        else:
            queryset = self.queryset.filter(is_faculty = False)
        
        return queryset
        
        


    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    


# class CourseAppList(viewsets.ModelViewSet):
#     queryset = FacultyCourseAddition.objects.all()
#     serializer_class = FacultyCourseAdditionSerializer
#     permission_classes = [AdminOrFaculty]

#     # def get_serializer_class(self):
#     #     category = self.request.query_params.get('category')
#     #     level = self.request.query_params.get('level')
#     #     course = self.request.query_params.get('course')
#     #     if category:
#     #         self.serializer_class=[LevelAppSerializer]
#     #     elif level:
#     #         self.serializer_class=[CourseAppSerializer]
#     #     elif course:
#     #         self.serializer_class=[FacultyCourseAdditionSerializer]
#     #     else:
#     #         self.serializer_class=[CategoryAppSerializer]
#     #     return super().get_serializer_class()

#     def get_queryset(self):
#         user_id= AuthHandlerIns.get_id(request=self.request)
#         # if AuthHandlerIns.is_staff(request=request):
#         #     faculty = request.query_params.get('faculty',None)
#         #     course = request.query_params.get('course',None)
#         #     print(faculty,course)
#         #     cou = Course.objects.filter(id=course)
#         #     fac= FacultyCourseAddition.objects.filter(course=course,user__id=faculty).values('course','subject','module','topic')
#         #     fd={

#         #     }
#         #     cous=[]
#         #     subj=[]
#         #     modl=[]
#         #     topi=[]
#         #     for i in fac:
#         #         print(i['course'])
#         #         cous.append(i['course'])
#         #         subj.append(i['subject'])
#         #         modl.append(i['module'])
#         #         topi.append(i['topic'])


#         #     fd={
#         #         "course":cous,
#         #         "subject":subj,
#         #         "module":modl,
#         #         "topic":topi

#         #     }
#         #     # print(fd,"kkkkkkkkkk")
#         #     # return
#         #     ser=CourseNewMaterialAdminSerializer(cou ,many=True,context={"fac":fd})
#         #     return Response({"data":ser.data}) 

#         faculty = self.request.query_params.get('faculty',None)
#         # course = self.request.query_params.get('course',None)
#         # print(faculty,course)
#         fac= FacultyCourseAddition.objects.filter(user__id=user_id).values('category','level','course','subject','module','topic')
#         cou = Category.objects.filter(id__in=[i['category'] for i in fac])
#         fd={

#         }
#         cate=[]
#         leve=[]
#         cous=[]
#         subj=[]
#         modl=[]
#         topi=[]
#         for i in fac:
#             print(i['course'])
#             cate.append(i['category'])
#             leve.append(i['level'])
#             cous.append(i['course'])
#             subj.append(i['subject'])
#             modl.append(i['module'])
#             topi.append(i['topic'])


#         fd={
#             "category":cate,
#             "level":leve,
#             "course":cous,
#             "subject":subj,
#             "module":modl,
#             "topic":topi

#         }
#         # print(fd,"kkkkkkkkkk")
#         # return
#         ser=CategoryNewMaterialSerializer(cou ,many=True,context={"fac":fd})
#         return Response({"data":ser.data}) 
    


#         return super().get_queryset()





@api_view(['GET'])
def CourseAppList(request):
    if AuthHandlerIns.is_faculty(request=request):
        user_id= AuthHandlerIns.get_id(request=request)
        faculty = request.query_params.get('faculty',None)
        profile = request.query_params.get('profile')
        # print(faculty,course)
        if profile:
            fac= FacultyCourseAddition.objects.filter(user__id=user_id).values('category','level','course','subject','module','topic')
        else:
            fac= FacultyCourseAddition.objects.filter(user__id=user_id,status='approved').values('category','level','course','subject','module','topic')


        cou = Category.objects.filter(id__in=[i['category'] for i in fac])
        fd={

        }
        cate=[]
        leve=[]
        cous=[]
        subj=[]
        modl=[]
        topi=[]
        for i in fac:
            print(i['course'])
            cate.append(i['category'])
            leve.append(i['level'])
            cous.append(i['course'])
            subj.append(i['subject'])
            modl.append(i['module'])
            topi.append(i['topic'])


        fd={
            "category":cate,
            "level":leve,
            "course":cous,
            "subject":subj,
            "module":modl,
            "topic":topi,
            'user':user_id,

        }
        # print(fd,"kkkkkkkkkk")
        # return
        ser=CategoryNewMaterialSerializer(cou ,many=True,context={"fac":fd})
        return Response({"data":ser.data}) 
    else:
        return Response({"data":"UnAuthorized"},status=403) 



class StudyMetrialPurchase(viewsets.ModelViewSet):
    serializer_class=StudyMaterialSerializer
    permission_classes=[AdminAndRolePermission]
    queryset = StudyMaterial.objects.all()
    pagination_class = SinglePagination

    def get_queryset(self):
        queryset = StudyMaterial.objects.order_by('-id')

        book_name = self.request.query_params.get('bookname', None)
        if book_name:
            queryset = queryset.filter(bookname__icontains=book_name)
        
        book_price = self.request.query_params.get('book_price', None)
        if book_price:
            queryset = queryset.filter(book_price = book_price)

        discount_price = self.request.query_params.get('discount_price', None)
        if discount_price:
            queryset = queryset.filter(discount_price=discount_price)
        
        admission_time_price = self.request.query_params.get('admission_time_price', None)
        if admission_time_price:
            queryset = queryset.filter(admission_time_price=admission_time_price)

        old_student = self.request.query_params.get('old_student', None)
        if old_student:
            queryset = queryset.filter(old_student=old_student)

        outsider = self.request.query_params.get('outsider', None)
        if outsider:
            queryset = queryset.filter(outsider=outsider)

        stock = self.request.query_params.get('stock', None)
        if stock:
            queryset = queryset.filter(stock=stock)

        no_of_pages = self.request.query_params.get('no_of_pages', None)
        if no_of_pages:
            queryset = queryset.filter(no_of_pages=no_of_pages)
        
        course = self.request.query_params.get('cc', None)
        if book_name:
            queryset = queryset.filter(course__name__icontains=course)
        

        return queryset
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        bookname = request.data['bookname']
        book_price = request.data['book_price']
        icon = request.data['icon']
        discount_price = request.data['discount_price']
        no_of_pages = request.data['no_of_pages']
        publish_on = request.data['publish_on']
        description = request.data['description']
        edition = request.data['edition']
        category = request.data['category']
        stock = request.data['stock']
        is_online =bool(request.data['is_online'])
        medium = request.data['medium']
        order_count = request.data['order_count']
        paperback = bool(request.data['paperback'])
        admission_time_price = request.data['admission_time_price']
        old_student = request.data['old_student']
        outsider = request.data['outsider']

        try:
            published = request.data['published']
        except:
            published = False
        print(published, 'published')
        course = request.data['course']
        carr=eval(course)
        
        studymaterials=StudyMaterial.objects.create(
            bookname=bookname,
            description=description,
            icon=icon,
            book_price=book_price,
            discount_price=discount_price,
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
            admission_time_price = admission_time_price,
            old_student = old_student,
            outsider = outsider
            
        )
        

        studymaterials.course.set(carr)
        ser = self.serializer_class(studymaterials)
        return Response(ser.data)
    
    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.serializer_class(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     course = request.data['course']
    #     # course ="[1,2,3]"
    #     carr = json.loads(course)
    #     instance.course.set(carr)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    @set_history_user_delete
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        course = request.data.get('course')
        if course is not None:
            carr = json.loads(course)
            instance.course.set(carr)

        # Update other fields based on your requirements
        instance.bookname = request.data.get('bookname', instance.bookname)
        instance.icon = request.data.get('icon', instance.icon)
        instance.category = request.data.get('category', instance.category)
        instance.book_price = request.data.get('book_price', instance.book_price)
        instance.discount_price = request.data.get('discount_price', instance.discount_price)
        instance.no_of_pages = request.data.get('no_of_pages', instance.no_of_pages)
        instance.edition = request.data.get('edition', instance.edition)
        instance.stock = request.data.get('stock', instance.stock)
        instance.is_online = request.data.get('is_online', instance.is_online)
        instance.medium = request.data.get('medium', instance.medium)
        instance.order_count = request.data.get('order_count', instance.order_count)
        instance.paperback = request.data.get('paperback', instance.paperback)
        instance.publish_on = request.data.get('publish_on', instance.publish_on)
        instance.description = request.data.get('description', instance.description)
        instance.published = request.data.get('published', instance.published)
        instance.paperback=request.data.get('paperback', instance.paperback)
        instance.admission_time_price = request.data.get('admission_time_price', instance.admission_time_price)
        instance.old_student = request.data.get('old_student', instance.old_student)
        instance.outsider = request.data.get('outsider', instance.outsider)

        instance.save()

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        # excel = queryset_to_excel(queryset,['bookname','book_price','discount_price','course','edition','admission_time_price','old_student','outsider'])

        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],
                                   {
                                       'is_online' : {'True':'Yes','False':'No'},
                                       'published' : { 'True':'Yes','False':'No'}

                                   })
            return response
        if pdf_query:
            fields = ['bookname','book_price','discount_price','course','edition','admission_time_price','old_student','outsider']
            headers,data = get_queryset_headers_data(queryset,fields=fields)
            modified_headers = []
            modified_headers = [header.replace('Bookname','Book Name')
                                .replace('Book_price','Book Price')
                                .replace('Discount_price','Discount Price')
                                .replace('Admission_time_price','Admission Price')
                                .replace('Old_student','Old Student')
                                for header in headers]
            
            nameheading = 'Material '
            current_datetime = timezone.now()
            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading
            }
            resp = generate_pdf('commonpdf.html',pdf_data,'MaterialList.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
   


class QuestionCategoryViewSet(viewsets.ModelViewSet):
    serializer_class=QuestionCategorySerializer
    permission_classes=[AdminAndRolePermission]
    queryset = QuestionCategory.objects.all()
    pagination_class = SinglePagination

    def get_queryset(self):

        queryset = QuestionCategory.objects.all()

        return queryset
    
    def list(self,request, *args, **kwargs):

        queryset =self.get_queryset()

        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        # checking for excel or pdf is requested
        if excel_query:
            response = queryset_to_excel(queryset,[field.name  for field in queryset.model._meta.fields])
            return response
        
        if pdf_query:
            fields = ['title','description']
            headers , data = get_queryset_headers_data(queryset, fields = fields)
            name_heading = 'Question Category'
            current_datetime = timezone.now()

            pdf_data = {
                'headers' : headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : name_heading

            }
            resp = generate_pdf('commonpdf.html',pdf_data,'QuestionCategory.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 


        



    
class QuestionBookPurchase(viewsets.ModelViewSet):
    serializer_class=QuestionBookSerializer
    permission_classes=[AdminAndRolePermission]
    queryset = QuestionBook.objects.all()
    pagination_class = SinglePagination

    def get_queryset(self):

        queryset = QuestionBook.objects.all().order_by('-created_at')

        question_bookname = self.request.query_params.get('bookname',None)
        book_price = self.request.query_params.get('book_price',None)
        discount_price = self.request.query_params.get('discount_price',None)
        admission_price = self.request.query_params.get('admission_time_price',None)
        old_Student = self.request.query_params.get('old_student',None)
        outsider = self.request.query_params.get('outsider',None)
        stock = self.request.query_params.get('stock',None)
        page_no = self.request.query_params.get('no_of_pages',None)
        course = self.request.query_params.get('course',None)

        if question_bookname:
            queryset = queryset.filter(bookname__icontains = question_bookname)
        
        if book_price:
            queryset = queryset.filter(book_price = book_price)
        
        if discount_price:
            queryset = queryset.filter(discount_price = discount_price)

        if admission_price:
            queryset = queryset.filter(admission_time_price = admission_price)
        
        if old_Student:
            queryset = queryset.filter(old_tudent = old_Student)
        
        if outsider:
            queryset = queryset.filter(outsider = outsider)
        
        if stock:
            queryset = queryset.filter(stock = stock)
        
        if page_no:
            queryset = queryset.filter(no_of_pages = page_no)

        if course:
            queryset = queryset.filter(course__name__icontains = course)

        return queryset
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        q_category = request.data['q_category']
        q_category = QuestionCategory.objects.get(id=q_category)
        bookname = request.data['bookname']
        book_price = request.data['book_price']
        icon = request.data['icon']
        discount_price = request.data['discount_price']
        no_of_pages = request.data['no_of_pages']
        publish_on = request.data['publish_on']
        description = request.data['description']
        edition = request.data['edition']
        category = request.data['category']
        stock = request.data['stock']
        try:
            is_online = bool(request.data['is_online'])
        except:
            is_online = False
        medium = request.data['medium']
        try:
            paperback = bool(request.data['paperback'])
        except:
            paperback = False
        order_count = request.data['order_count']
        admission_time_price = request.data['admission_time_price']
        old_student = request.data['old_student']
        outsider = request.data['outsider']


        try:
            published = bool(request.data['published'])
        except:
            published = False
        print(published, 'published')
        course = request.data['course']
        carr=eval(course)
        
        questionbook=QuestionBook.objects.create(
            q_category=q_category,
            bookname=bookname,
            description=description,
            icon=icon,
            book_price=book_price,
            discount_price=discount_price,
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
            old_student = old_student,
            outsider=outsider
            
        )
        

        questionbook.course.set(carr)
        ser = self.serializer_class(questionbook)
        return Response(ser.data)
    
    @set_history_user_delete
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        course = request.data.get('course')
        if course is not None:
            carr = json.loads(course)
            instance.course.set(carr)

        # Update other fields based on your requirements
        instance.bookname = request.data.get('bookname', instance.bookname)
        instance.icon = request.data.get('icon', instance.icon)
        instance.category = request.data.get('category', instance.category)
        instance.book_price = request.data.get('book_price', instance.book_price)
        instance.discount_price = request.data.get('discount_price', instance.discount_price)
        instance.no_of_pages = request.data.get('no_of_pages', instance.no_of_pages)
        instance.edition = request.data.get('edition', instance.edition)
        instance.stock = request.data.get('stock', instance.stock)
        instance.is_online = request.data.get('is_online', instance.is_online)
        instance.medium = request.data.get('medium', instance.medium)
        instance.order_count = request.data.get('order_count', instance.order_count)
        instance.paperback = request.data.get('paperback', instance.paperback)
        instance.publish_on = request.data.get('publish_on', instance.publish_on)
        instance.description = request.data.get('description', instance.description)
        instance.published = request.data.get('published', instance.published)
        instance.admission_time_price = request.data.get('admission_time_price', instance.admission_time_price)

        instance.save()

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def list(self,request, *args, **kwargs):
        queryset = self.get_queryset()

        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                    'is_online' :{'True': 'Yes','False':'No'},
                    'paperback' : {'True': 'Yes','False':'No'},
                    'published' : {'True': 'Yes','False':'No'}
            })
            return response
        
        if pdf_query:
            fields = ['bookname','book_price','course','discount_price','admission_time_price','old_student','outsider','publish_on']
            headers,data = get_queryset_headers_data(queryset,fields = fields)

            modified_headers = []
            modified_headers = [header.replace('Book_price','Book Price')
                                .replace('Bookname','Book Name')
                                .replace('Admission_time_price','Admission Price')
                                .replace('Old_student','Old Student')
                                
                                .replace('Discount_price','Discount Price')
                                .replace('Publish_on','Published On')
                                for header in headers]
            
            name_heading = 'Question Book '
            current_datetime = timezone.now()

            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : name_heading
            }
            resp = generate_pdf('commonpdf.html',pdf_data,'QuestionBook.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class ShortsViewSet(viewsets.ModelViewSet):
    queryset = Shorts.objects.all()
    serializer_class = ShortsSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminOrStudent]

    def get_serializer_context(self):
        # Get the default context from the parent method
        context = super().get_serializer_context()

        # Add your custom context data based on the viewset action
        context['user'] = AuthHandlerIns.get_id(request=self.request)
          

        return context

    def get_queryset(self):
        if AuthHandlerIns.is_student(request=self.request):
            user = AuthHandlerIns.get_id(request=self.request)
            student = Student.objects.get(user=user)
            try:
                level = student.selected_course.level.id
            except:
                return Response({'error':'Need to select a Batch'})
            watched_videos = ShortsWatched.objects.filter(student=user, watched=True)
            unwatched_videos = Shorts.objects.exclude(shortswatched__in=watched_videos)
            unwatched_videos =unwatched_videos.filter(level=level)
            print(unwatched_videos)

            if unwatched_videos.exists():
                return unwatched_videos
            else:
                return Shorts.objects.filter(level=level)
        else:
            return Shorts.objects.all().order_by('-id')
        
    @create_history_user__decorator
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 

class ShortsWatchedViewset(viewsets.ModelViewSet):
    queryset = ShortsWatched.objects.all()
    serializer_class = ShortsWatchedSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminOrStudent]

    
    


    def create(self, request, *args, **kwargs):
        user = AuthHandlerIns.get_id(request=self.request)
        print(user)
        student =  User.objects.get(id=user)
        print(student)
        shorts_id = request.data.get('shorts')
        shorts = Shorts.objects.get(id=shorts_id)
        
        

        try:
            watched = bool(request.data['watched'])
        except:
            watched = False
        
        
        shortswatched=ShortsWatched.objects.create(
            student=student,
            shorts=shorts,
            
            watched=watched,
            
            
        )
        
        ser = self.serializer_class(shortswatched)
        return Response(ser.data)   
    

class FacultyDashboarViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultyDashboardSerializer
    # pagination_class = SinglePagination
    permission_classes = [FacultyPermission]

    def get_queryset(self):
        queryset=Faculty.objects.filter(user__id=AuthHandlerIns.get_id(request=self.request))
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        
        queryset=Faculty.objects.get(user__id=AuthHandlerIns.get_id(request=request))
        serializer = FacultyDashboardSerializer(queryset, many=False)
        return Response(serializer.data) 
    

class AppStudentQuiz(viewsets.ReadOnlyModelViewSet):
    queryset = QuizPool.objects.all()
    permission_classes = [StudentPermission]
    serializer_class =QuizPoolUserViewsetSerializer

    # def get_permissions(self):
    #     user = User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
    #     if self.action in ['retrieve']:
            
    #     return super().get_permissions()

    def list(self, request, *args, **kwargs):
        
        user = User.objects.get(id=AuthHandlerIns.get_id(request=request))
        student = Student.objects.get(user=user)
        level = student.selected_course.level 
        queryset = QuizPool.objects.get(level=level)
        ser =QuizPoolUserViewsetSerializerNew(queryset, many=False)
        return Response({"data":ser.data})
    
    
    def retrieve(self, request, *args, **kwargs):
        lead = request.query_params.get('leaderboard')
        if lead:
            leaderboard = (
                QuizPoolUserRoom.objects
                .filter(quiz=kwargs['pk'], is_submited=True, total_score__isnull=False)
                .values('user__username')  # Group by user ID
                .annotate(total_score_sum=Sum('total_score'))  # Combine scores of the same user ID
                .order_by('-total_score_sum')  # Order by total_score_sum descending
                .annotate(rank=Window(expression=DenseRank(), order_by=F('total_score_sum').desc()))
            )
            # print(leaderboard)
            # ser=QuizPoolUserRoomLeaderBoardSerializer(leaderboard,many=True)
            target_user_rank = leaderboard.filter(user__username=User.objects.get(id=AuthHandlerIns.get_id(request=self.request)).username).values('rank','total_score_sum','user__username').first()
            # print(target_user_rank)
            return Response({"message":leaderboard[:10],"my_rank":target_user_rank})
        return super().retrieve(request, *args, **kwargs)
    

class AppStudentStartQuiz(viewsets.ModelViewSet):
    queryset = QuizPoolUserRoom.objects.all()
    permission_classes = [StudentPermission]
    serializer_class =QuizPoolUserStartSerializer

    def retrieve(self, request, *args, **kwargs):
        ins=self.get_object()
        answer = request.query_params.get('answer')
        if answer:
            if ins.is_submited:
                answerkey=QuizPoolAnswers.objects.filter(room=ins)
                serializer= QuizPoolAnswersUserSubmitSerializer(answerkey, many=True)
                return Response({"data": serializer.data})
        return super().retrieve(request, *args, **kwargs)




class AppStudentSubmitAnswerQuiz(viewsets.ModelViewSet):
    queryset = QuizPoolAnswers.objects.all()
    permission_classes = [StudentPermission]
    serializer_class =QuizPoolAnswersUserStartSerializer

    def update(self, request, *args, **kwargs):
        print("hereeee")
        submit= self.request.query_params.get('submit',None)
        skipped= self.request.query_params.get('skipped',None)
        if submit:
            pk=kwargs['pk']
            qr=QuizPoolUserRoom.objects.get(id=pk)
            if qr.is_submited:
                return Response({"message":"already submitted"},status=status.HTTP_400_BAD_REQUEST)
            else:
                qr.is_submited=True
                qr.save()
            queryset = QuizPoolUserRoom.objects.filter(id=pk)
            ser =QuizPoolUserRoomSubmitSerializer(queryset,many=True)
            
            return Response({"message":"ok","data":ser.data[0] if len(ser.data[0])>0 else {}})
        if skipped:
            arr=request.data['skipped']
            for i in arr:
                
                ser=QuizPoolAnswersUserStartSerializer(data=i)
                if ser.is_valid(raise_exception=True):
                    ser.save()
                else:
                    return Response({"message":"not valid"},status=status.HTTP_417_EXPECTATION_FAILED)
            return Response({"message":"Ok"},status=status.HTTP_201_CREATED)
        else:
            return super().update(request, *args, **kwargs)
    

    

from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, Value, DecimalField, IntegerField, ExpressionWrapper

class BatchPackagesViewSet(viewsets.ModelViewSet):
    queryset = BatchPackages.objects.all()
    serializer_class = BatchPackagesSerializer
    # permission_classes =[AdminAndRolePermission]
    pagination_class = SinglePagination
    
    def get_queryset(self):

        queryset  = BatchPackages.objects.all()

        return queryset
    
    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def list(self,request, *args, **kwargs):
        queryset  = self.get_queryset()

        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        # checking for pdf or excel is requested

        if pdf_query:
            
            queryset = BatchPackages.objects.annotate(
                total_study_material_price=Sum(F('study_meterial__book_price'), output_field=DecimalField()),
                total_question_book_price=Sum(F('question_book__book_price'), output_field=DecimalField()),
                total_publications_price=Sum(F('publications__book_price'), output_field=DecimalField())
            ).annotate(grand_total=F('total_study_material_price')+F('total_question_book_price')+F('total_publications_price'))
            print(queryset.values(),"\\\\\\\\\\\\\\\\\\")
            total_study_material_price_sum = 0
            total_question_book_price_sum = 0
            total_publications_price_sum = 0
            for item in queryset:
                total_study_material_price_sum += item.total_study_material_price or 0
                total_question_book_price_sum += item.total_question_book_price or 0
                total_publications_price_sum += item.total_publications_price or 0

            grand_total = (
                total_study_material_price_sum +
                total_question_book_price_sum +
                total_publications_price_sum
            )

            # Print or use the grand total as needed
            print(f"Grand Total: {grand_total}")


            
            print(queryset.values())
            fields = ['name','batch__name','question_book','study_meterial','grand_total']
            manyKey = {'question_book':'bookname','study_meterial':'bookname'}
            arr = ['question_book','study_meterial']
            headers,data = get_queryset_headers_data(queryset,fields=fields,manyKey=manyKey,arr=arr)

            replacement_values = ["Package name", "Batch Name "]

            modified_headers = []
            replacement_index = 0  # Initialize index for replacement_values

            for header in headers:
                
                if header == "Name" and replacement_index < len(replacement_values):
               
                    modified_header = replacement_values[replacement_index]
                    replacement_index += 1
                else:
                    modified_header = header
                modified_header = modified_header.replace('Grand_total','Grand Total')
                modified_header = modified_header.replace('Bookname','Book Name')
                modified_header = modified_header.replace('Study_meterial', 'Study Material')
                

                modified_headers.append(modified_header)
           
                
            

            name_heading = 'Batch Offline Package '
            current_datetime = timezone.now()
            pdf_data = {
                'headers' : modified_headers,
                'data' :data,
                'current_datetime' : current_datetime,
                'model' : name_heading
            }
            resp = generate_pdf('commonpdf.html',pdf_data,'BatchOfflinePackageList.pdf')
            return resp
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class BookTypeViewSet(viewsets.ModelViewSet):
    queryset = BooksType.objects.all()
    serializer_class = BooksTypeSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]
    def get_queryset(self):
        queryset = BooksType.objects.all().order_by('-id')
        book_name = self.request.query_params.get('book_name',None)
        if book_name:
                queryset= queryset.filter(name__icontains = book_name)
        return queryset

class ReadBookTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BooksType.objects.all()
    serializer_class = BooksTypeSerializer
    permission_classes = [AdminAndRolePermission]

class BooksinBranch(viewsets.ReadOnlyModelViewSet):
    queryset = Books.objects.all().order_by('-id')
    serializer_class = BooksSerializer
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id', None)
        queryset = Books.objects.filter(branch=branch_id).order_by('-id')
        serializer = BooksSerializer(queryset,many=True)
        return serializer.data
    
    




import random

class LibraryBooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def create(self, request, *args, **kwargs):
        try:
            if 'branch' not in request.data:
                return Response('Invalid request. Missing required fields.')
        
            branch_id = int(request.data['branch'])
            print(branch_id)
            if not AuthHandlerIns.is_staff(request=request):
                user_id = AuthHandlerIns.get_id(request=request)
                user_list = Branch.objects.filter(id=branch_id, user__in=[user_id])
                if not user_list.exists():
                    return Response('You cannot add Books to Library in which You are not In.') 
            
            # branch_id = request.data['branch']
            branch = Branch.objects.get(id = branch_id)
            name = request.data['name']
            btype = request.data['type']
            b_type = BooksType.objects.get(id = btype)
            no_due_days = request.data['no_due_days']
            price = request.data['price']
            purchased_on = request.data['purchased_on']
            subscription_upto = request.data['subscription_upto']
            is_lend = bool(request.data.get('is_lend', False))
            isbn = request.data['ISBN']
            outsider_allowed = bool(request.data.get('outsider_allowed', False))
            status = bool(request.data.get('status', False))
            random_number = random.randint(100000, 999999)
            current_time = str(timezone.now().strftime("%Y%m%d%H%M%S"))
            description = request.data['description']
            qrcode = (str(branch_id) + str(btype)[:2] + name[:4] + str(random_number) + current_time).upper()

            books = Books.objects.create(
                branch=branch,
                name =name,
                type = b_type,
                no_due_days = no_due_days,
                price = price,
                purchased_on = purchased_on,
                subscription_upto = subscription_upto,
                is_lend = is_lend,
                outsider_allowed = outsider_allowed,
                ISBN=isbn,
                description =description,
                status = status,
                qrcode = qrcode

            )
            serializer = self.serializer_class(books)
            return Response(serializer.data)
        except KeyError:
            return Response('Invalid request. Missing required fields.')

        except Exception as e:
            return Response(str(e))
        
    def get_queryset(self):
        queryset = self.queryset

        id = self.request.query_params.get('id',None)

        name = self.request.query_params.get('name',None)
        type_name = self.request.query_params.get('type_name',None)
        branch_name = self.request.query_params.get('branch_name',None)
        price = self.request.query_params.get('price',None)
        purchased_on = self.request.query_params.get('purchased_on',None)
        subscription_upto = self.request.query_params.get('subscription_upto',None)

        if id:
            queryset = queryset.filter(id__in = id)
        
        if name:
            queryset = queryset.filter(name__icontains = name)
        
        if type_name:
            queryset = queryset.filter(type__name__icontains = name)
        
        if branch_name:
            queryset = queryset.filter(branch__name__icontains = branch_name)
        
        if price:
            queryset = queryset.filter(price__in = price)

        if purchased_on:
            queryset = queryset.filter(purchased_on = purchased_on)
        
        if subscription_upto:
            queryset = queryset.filter(subscription_upto__in = subscription_upto)

        return queryset



class BatchPackagesOnId(viewsets.ModelViewSet):
    queryset = BatchPackages.objects.all()
    serializer_class = BatchPackagesSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def list(self, request, *args, **kwargs):
        batch_id = self.request.query_params.get('batch_id')
        queryset = BatchPackages.objects.filter(batch = batch_id)
        if not queryset.exists():
            return Response({'error':'Batches not found'})
        serializer = BatchPackagesSerializer(queryset.first())
        return Response(serializer.data)

class BatchPackagesOnBranchId(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def list(self, request, *args, **kwargs):
        branch_id = self.request.query_params.get('branch_id')
        batchpackages = BatchPackages.objects.filter(batch__branch=branch_id).values('batch')
        queryset = Batch.objects.filter(id__in=batchpackages)
        if not queryset.exists():
            return Response([])
        serializer = BatchSerializer(queryset,many=True)
        return Response(serializer.data)

   
        
    




class CartItemViewset(viewsets.ModelViewSet):
    serializer_class =CartItemSerializer
    queryset = CartItems.objects.all()
    permission_classes=[StudentPermission]

    def get_permissions(self):
        if self.action in ['list','create',None]:

            self.permission_classes =[StudentPermission]
        else:
            ci=get_object_or_404(CartItems, pk=self.kwargs['pk'])
            if ci.user.id==AuthHandlerIns.get_id(request=self.request):
                self.permission_classes =[StudentPermission]
            else:
                self.permission_classes =[NonePermission]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset=CartItems.objects.filter(user__id=AuthHandlerIns.get_id(request=self.request)).order_by('created_at')
        return queryset
    
    def update(self, request, *args, **kwargs):
        purchase=self.request.query_params.get('purchase')
        print(purchase,'dd')
        if purchase:

            obj=self.get_object()
            total_price = CartItems.objects.filter(user=obj.user).aggregate(total=Sum(F('publication__book_price') * F('quantity')))['total']
            print(total_price,'dd')
            raz = razorpay_client.order.create(data={'amount':int(total_price*100), 'currency':'INR'})
            print(raz)
            current_time = now()
            timestamp = datetime.strftime(current_time, "%Y%m%d%H%M%S")
            random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))
            order_id = f"{timestamp}-{random_string}"
            user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
            items=CartItems.objects.filter(user=obj.user)
            for x in items:
                pay=OnlineOrderPayment.objects.create(user=user,user_ref=x.user.id,order_number=order_id,product='publication',product_id=x.publication.id,razor_id=raz['id'],total_amount=x.publication.book_price,paid_amount=raz['amount_paid']/100,off_amount=0,offer_choice='none',payment_status='pending',delivery_status='pending')

            return Response(raz)
        else:
            return super().update(request, *args, **kwargs)


    


class StudentBatchDetailsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Batch.objects.filter(active=True)
    serializer_class = BatchStudentAppSerializer
    permission_classes=[StudentPermission]

    def get_queryset(self):
        queryset= Batch.objects.filter(active=True)
        sb=StudentBatch.objects.filter(student__user__id=AuthHandlerIns.get_id(request=self.request))
        batch= self.request.query_params.get('batch')
        if batch:
            queryset=queryset.filter(id=batch)
        else:
            if not sb.exists():
                return Response({"invalid":"no batch assigned for the user"},status=status.HTTP_400_BAD_REQUEST)

            queryset=queryset.filter(id=sb.values('batch').first()['batch'])
        return queryset
    

class GeneralVideosViewset(viewsets.ModelViewSet):
    permission_classes =[AdminAndRolePermission]
    queryset = GeneralVideos.objects.filter().order_by('-created_at')
    serializer_class = GenralVideosSerializer
    pagination_class =SinglePagination

    @create_history_user__decorator
    def create(self, request, *args, **kwargs):
        # Create a mutable copy of the request.data
        print("rammmmmmmmmmmmmmmmmm")
        mutable_data = request.data.copy()
        try:
            mutable_data['files'] = json.loads(mutable_data['files'])
        # Modify the 'files' key in the mutable_data

            files=mutable_data['files']
        # mutable_data['files'] = [2,3]
            mutable_data.pop('files',None)
        except:
            files=[]
        serializer = self.get_serializer()  # Call the get_serializer() method to retrieve the serializer class

        ser = GenralVideosSerializer(data=mutable_data)
      
        if ser.is_valid(raise_exception=True):
            ser.save()
        gv=GeneralVideos.objects.get(id=ser.data['id'])
        gv.files.set(files)
        gv.save()
        serializer=GenralVideosSerializer(gv,many=False)

       

        return Response(serializer.data)
        # Replace the original request.data with the modified mutable_data
        request.data = mutable_data

        # Call the super method with the modified request
        return super().create(request, *args, **kwargs)
    
    @set_history_user_delete
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        mutable_data = request.data.copy()
        try:
            files = json.loads(mutable_data['files'])
            mutable_data.pop('files',None)
            instance.files.set(files)
            instance.save()
            instance = self.get_object()
        except:
            pass
        serializer = self.get_serializer(instance, data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = GeneralVideos.objects.filter().order_by('-created_at')

        video_id = self.request.query_params.get('id',None)
        video_title = self.request.query_params.get('title',None)
        video_category = self.request.query_params.get('category_name',None)
        course_category = self.request.query_params.get('level_name',None)
        video_name = self.request.query_params.get('videoobject_name',None)
        video_description =self.request.query_params.get('description',None)

        if video_id:
            queryset = queryset.filter(video__id__startswith = video_id)
        
        if video_title:
            queryset = queryset.filter(title__icontains = video_title)

        if video_category:
            queryset = queryset.filter(category__name__icontains = video_category)

        if course_category:
            queryset = queryset.filter(level__name__icontains = course_category)
        
        if video_name:
            queryset = queryset.filter(video__name__icontains = video_name)

        if video_description:
            queryset = queryset.filter(description__icontains = video_description)
        
        return queryset
    
    def list(self,request, *args, **kwargs):

        queryset = self.get_queryset()
        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                'active' : {'True' : 'Yes','False' : 'No' } 
            })
            return response
        
        if pdf_query:
            fields = ['video__id','title','category__name','level__name','video__name']
            headers,data = get_queryset_headers_data(queryset,fields=fields)
            modified_headers = []

            


            # Define replacement values
            replacement_values = ["Category name", "Course category", "Video name"]

            modified_headers = []
            replacement_index = 0  # Initialize index for replacement_values

            for header in headers:
                if header == "Name" and replacement_index < len(replacement_values):
                    modified_header = replacement_values[replacement_index]
                    replacement_index += 1
                else:
                    modified_header = header
                

                modified_headers.append(modified_header)
                print
                

            print(modified_headers)


            nameheading = 'General Video'
            currrent_datetime = timezone.now()

            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime'  : currrent_datetime,
                'model' : nameheading

            }
            resp = generate_pdf('commonpdf.html',pdf_data,'GeneralVideoList.pdf')
            print("Ashhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",modified_headers)
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @set_history_user_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GeneralVideosCategoryViewset(viewsets.ModelViewSet):
    permission_classes =[AdminAndRolePermission]
    queryset = GeneralVideosCategory.objects.filter().order_by('created_at')
    serializer_class = GeneralVideosCategorySerializer
    pagination_class =SinglePagination




class GeneralVideosUserViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes =[StudentPermission]
    queryset = GeneralVideos.objects.filter().order_by('created_at')
    serializer_class = GenralVideosUserSerializer
    pagination_class =SinglePagination

    def get_serializer(self, *args, **kwargs):
        if self.action in ['retrieve']:
            self.serializer_class = GenralVideosUserRetriveSerializer
        return super().get_serializer(*args, **kwargs)
    
    def get_serializer_context(self):
        # Get the default context from the parent method
        context = super().get_serializer_context()

        # Add your custom context data based on the viewset action
        if self.action == 'retrieve':
            context['user'] = AuthHandlerIns.get_id(request=self.request)
            # You can also access request, user, or other viewset attributes
            # to customize the context further.
            # For example:
            # context['user_id'] = self.request.user.id

        return context
    
    # @method_decorator(cache_page(60 * 15))
    def get_queryset(self):
        student=Student.objects.get(user__id=AuthHandlerIns.get_id(request=self.request))
        queryset=GeneralVideos.objects.filter(active=True)
        try:
            if student.selected_course:
                queryset= queryset.filter(level=student.selected_course.level)
        except:
            pass
        category_name=self.request.query_params.get('category_name')
        if category_name:
            queryset=queryset.filter(category__name__icontains=category_name)
        category=self.request.query_params.get('category')
        if category:
            queryset=queryset.filter(category=category)
        watched=self.request.query_params.get('watched')
        if watched:
            watch=Views.objects.filter(user=AuthHandlerIns.get_id(request=self.request),view_assign='VIDEOS').values('view_id')
            queryset=queryset.filter(video__id__in=watch)
        notwatched=self.request.query_params.get('notwatched')
        if notwatched:
            watch=Views.objects.filter(user=AuthHandlerIns.get_id(request=self.request),view_assign='VIDEOS').values('view_id')
            queryset=queryset.exclude(video__id__in=watch)

        return queryset.order_by('?')
    
    # @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



class GeneralVideosCategoryUserViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes =[StudentPermission]
    queryset = GeneralVideosCategory.objects.filter(active=True).order_by('created_at')
    serializer_class = GeneralVideosCategoryUserSerializer
    # pagination_class =SinglePagination

import random
import string
class LibraryUserViewSet(viewsets.ModelViewSet): 
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer
    permission_classes = [AdminAndRolePermission]
    pagination_class=SinglePagination
 

    def create(self, request, *args, **kwargs):
        try:
            branch_id = int(request.data['branch']) 
            user_id = request.data['user']
            print(user_id)
            branch = Branch.objects.get(id=branch_id)
            user = User.objects.get(id=user_id)
            existing_member = LibraryUser.objects.filter(user=user).exists()
            if existing_member:
                return Response({'Error':'User already a member'}, status=status.HTTP_400_BAD_REQUEST)
            card_no_user_id = str(user.id)
            card_no_branch_id = str(branch.id)
            uppercase_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
            digits = ''.join(random.choice(string.digits) for _ in range(4))
            cardno = card_no_user_id+card_no_branch_id+uppercase_letters+digits
            book_limit = request.data['book_limit']

            user = LibraryUser.objects.create(
                user=user,
                branch=branch,
                cardno=cardno,
                book_limit=book_limit
                )
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except KeyError:
            return Response('Invalid request. Missing required fields.')

        except Exception as e:
            return Response(str(e))



class UserNotInLibraryUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.exclude(libraryuser__isnull=False)  
    serializer_class = UserLibrarySerializer
    permission_classes=[AdminAndRolePermission]
    pagination_class= SinglePagination

    def get_queryset(self):
        queryset = User.objects.exclude(libraryuser__isnull=False).order_by('id')

        username = self.request.query_params.get('username',None)
        

        if username:
            queryset = queryset.filter(username__icontains = username)
        
        return queryset




import vimeo
import requests
from django.http import StreamingHttpResponse
     

# def stream_vimeo_video_fc(request,id):
#     # Initialize the Vimeo API client with your API credentials
#     client = vimeo.VimeoClient(
#         token='d9a01813f50cf7a68e966e285d557f36',
#         # key='YOUR_VIMEO_API_KEY',
#         # secret='YOUR_VIMEO_API_SECRET'
#     )

#     # Retrieve the video data from Vimeo API
#     video_id = id
#     video = client.get('/videos/{video_id}'.format(video_id=video_id))

#     # Retrieve the streaming URL for the video
#     streaming_url = video['files'][0]['link']

#     # Create a generator function to stream the video content
#     def video_stream_generator():
#         response = requests.get(streaming_url, stream=True)
#         for chunk in response.iter_content(chunk_size=8192):
#             yield chunk

#     # Stream the video content as a response
#     response = StreamingHttpResponse(video_stream_generator(), content_type='video/mp4')
#     response['Content-Disposition'] = 'inline'
#     return response
        
from django.http import HttpResponse

@api_view(['GET'])
def stream_vimeo_video(request, id):
    # Initialize the Vimeo API client with your API credentials
    client = vimeo.VimeoClient(
        token='d9a01813f50cf7a68e966e285d557f36',
        # key='YOUR_VIMEO_API_KEY',
        # secret='YOUR_VIMEO_API_SECRET'
    )

    # Retrieve the video data from Vimeo API
    video_id = id
    response = client.get('/videos/{video_id}'.format(video_id=video_id))
    video = response.json()

    # Retrieve the streaming URL for the video
    files = video.get('files', [])
    if files:
        streaming_url = files[0]['link']
    else:
        # Handle the case when the files array is empty
        return HttpResponse(status=404)

    # Create a generator function to stream the video content
    def video_stream_generator():
        response = requests.get(streaming_url, stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

    # Set the appropriate response headers
    response = HttpResponse(video_stream_generator(), content_type='video/mp4')
    response['Content-Disposition'] = 'inline'
    return response

# from datetime import datetime, timedelta
from datetime import datetime, timedelta, date
import traceback
# class BookLendViewSet(viewsets.ModelViewSet):
#     queryset = BookLend.objects.all()
#     serializer_class = BookLendSerializer
#     pagination_class = SinglePagination
#     permission_classes = [AdminAndRolePermission] 

#     def create(self, request, *args, **kwargs):  
#         user = AuthHandlerIns.get_id(request=self.request)
#         user = User.objects.get(id =user)
#         if user.is_staff or user.is_role: 
#             lendee = request.data['user']
#             userset = LibraryUser.objects.get(cardno=lendee)
#             if userset.status == 'False':
#                 return Response({'Message': 'The user library subcription is Over'})
#             limit = userset.book_limit
#             count_borrowed_books = BookLend.objects.filter(
#                         user__cardno=lendee,
#                         returned_on__isnull=True,  # Books not returned yet
#                         lost=False  # Exclude lost books
#                         ).count()
#             if limit <= count_borrowed_books:
#                 return Response({'Alert': 'Limit Exceeded'})
#             lendee = LibraryUser.objects.get(cardno = lendee)
#             book = Books.objects.get(id = request.data['book'])
#             borrowed_on = request.data['borrowed_on']
#             due_date = Books.objects.get(id=book.id)
#             duedate = due_date.no_due_days
#             borrowed_on_date = datetime.strptime(borrowed_on, '%Y-%m-%d').date()
#             duedate = borrowed_on_date + timedelta(days=duedate)
#             current_date = datetime.today().date()
#             difference = duedate - current_date
#             number_of_days = difference.days
#             fine = number_of_days * 5
#             description = request.data['description']

#             lend = BookLend.objects.create(
#                 user= lendee,
#                 book = book,
#                 borrowed_on=borrowed_on,
#                 description=description,
#                 duedate = duedate
#             )
#             serializer = self.serializer_class(lend)
#             return Response(serializer.data)
#         # except KeyError:
#         #     return Response('Invalid request. Missig required fields.')

#         # except Exception as e:
#         #     return Response(str(e))
class BookLendViewSet(viewsets.ModelViewSet):
    queryset = BookLend.objects.all()
    serializer_class = BookLendSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    
    

    def create(self, request, *args, **kwargs):
        try:
            user = AuthHandlerIns.get_id(request=self.request)
            user = User.objects.get(id=user)
            

            if not user.is_staff and not user.is_role:
                return Response({'Message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            lendee = request.data['user']
            userset = LibraryUser.objects.get(cardno=lendee)
            
            if not userset.status:
                return Response({'Message': 'The user library subscription is Over'}, status=status.HTTP_400_BAD_REQUEST)

            limit = userset.book_limit
            count_borrowed_books = BookLend.objects.filter(
                user__cardno=lendee,
                returned_on__isnull=True,
                lost=False
            ).count()

            if limit <= count_borrowed_books:
                return Response({'Alert': 'Limit Exceeded'}, status=status.HTTP_400_BAD_REQUEST)

            lendee = LibraryUser.objects.get(cardno=lendee)
            book = Books.objects.get(id=request.data['book'])
 
            # borrowed_on = request.data['borrowed_on']
            borrowed_on = date.today()
            due_date = Books.objects.get(id=book.id)
            duedate = due_date.no_due_days
            # borrowed_on_date = datetime.strptime(borrowed_on, '%Y-%m-%d').date()
            borrowed_on_date = borrowed_on
            duedate = borrowed_on_date + timedelta(days=duedate)
            # current_date = datetime.today().date()
            current_date = date.today()
            difference = duedate - current_date
            number_of_days = difference.days
            fine = number_of_days * 5
            description = request.data.get('description', None)

            lend = BookLend.objects.create(
                user=lendee,
                book=book,
                borrowed_on=borrowed_on,
                description=description,
                duedate=duedate
            )

            serializer = self.serializer_class(lend)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except LibraryUser.DoesNotExist:
            return Response({'Message': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)

        except Books.DoesNotExist:
            return Response({'Message': 'Invalid book'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            print(request.data)
            if 'lost' in request.data:
                instance.lost = True
                instance.save()

            if 'returned_on' in request.data:
                returned_on = request.data['returned_on']
                if returned_on:
                    returned_on_date = datetime.strptime(returned_on, '%Y-%m-%d').date()
                    instance.returned_on = returned_on_date

                    # Calculate fine for overdue books if 'lost' is False
                    if not instance.lost:
                        duedate = instance.duedate
                        current_date = datetime.today().date()
                        difference = current_date - duedate
                        number_of_days = difference.days
                        fine = number_of_days * 5
                        instance.fine = fine if fine > 0 else 0
                    else:
                        instance.fine = None

                else:
                    instance.returned_on = None
                    instance.fine = None

            if 'description' in request.data:
                description = request.data['description']
                if not description:
                    return Response({'Message': 'Description is required'}, status=status.HTTP_400_BAD_REQUEST)
                instance.description = description

            
            if instance.lost == True:
                if 'fine' in request.data:
                    fine = request.data['fine']
                    if fine is None:
                        return Response({'Message': 'When "lost" is True, "fine" must be manually entered.'}, status=status.HTTP_400_BAD_REQUEST)
                    instance.fine = fine
                else:
                    return Response({'Message': 'When "lost" is True, "fine" must Mandatory'}, status=status.HTTP_400_BAD_REQUEST)

                instance.returned_on = None
                
            instance.save()
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except BookLend.DoesNotExist:
            return Response({'Message': 'Invalid BookLend ID'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            traceback.print_exc()
            return Response({'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoriesCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoriesCategory.objects.all().order_by('-id')
    serializer_class = StoriesCategorySerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        queryset = StoriesCategory.objects.all()

        # Apply search filter
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        id = self.request.query_params.get('id', None)
        if id:
            queryset = queryset.filter(id__icontains=id)
        
        return queryset.order_by('-id')


class RecentCourseViewset(viewsets.ReadOnlyModelViewSet):
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]
    serializer_class=CourseAppStudentSerilizer
    

    def get_queryset(self):
        seleceted_level=Student.objects.get(user__id=AuthHandlerIns.get_id(request=self.request)).selected_course.level
        level=Level.objects.filter(priority__lte=seleceted_level.priority).values('id')
        queryset= Course.objects.filter(level__in=level,is_online=True)

        return queryset
    
class StoriesViewSet(viewsets.ModelViewSet):
    queryset = Stories.objects.all().order_by('-id')
    serializer_class = StoriesCreateSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminOrStudent]

    def get_queryset(self):
        if AuthHandlerIns.is_student(request=self.request):
            user = AuthHandlerIns.get_id(request=self.request)
            category_id = self.request.query_params.get('category')
            print(category_id, "category")
            
            try:
                student = Student.objects.get(user=user)
                level = student.selected_course.level.id
            except:
                return Response({'error':'Need to select a Batch'})
            watched_videos = StoriesWatched.objects.filter(student=user, watched=True)
            unwatched_videos = Stories.objects.exclude(storieswatched__in=watched_videos)
            unwatched_videos =unwatched_videos.filter(level=level,category=category_id)
            print(unwatched_videos)

            if unwatched_videos.exists():
                return unwatched_videos
            else:
                return Stories.objects.filter(level=level,category=category_id,active=True)
        else:
            return Stories.objects.all().order_by('-id')



class StoriesWatchedViewset(viewsets.ModelViewSet):
    queryset = StoriesWatched.objects.all()
    serializer_class = StoriesWatchedSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminOrStudent]

    
    


    def create(self, request, *args, **kwargs):
        user = AuthHandlerIns.get_id(request=self.request)
        print(user)
        student =  User.objects.get(id=user)
        print(student)
        stories_id = request.data.get('stories')
        stories = Stories.objects.get(id=stories_id)
        
        

        try:
            watched = bool(request.data['watched'])
        except:
            watched = False
        
        
        storieswatched=StoriesWatched.objects.create(
            student=student,
            stories=stories,
            
            watched=watched,
            
            
        )
        
        ser = self.serializer_class(storieswatched)
        return Response(ser.data)   
    

class PackageMaterialsViewset(viewsets.ModelViewSet):
    serializer_class=PackageMaterialsSerializer
    queryset=PackageMaterials.objects.all()
    pagination_class = SinglePagination

class VedioMeterialAndQuestionsViewset(viewsets.ModelViewSet):
    serializer_class=VedioMeterialAndQuestionsSerializer
    queryset=VedioMeterialAndQuestions.objects.all()
    pagination_class = SinglePagination
    def get_serializer_class(self):
            # Check if it's a GET request
        if self.action == 'list' or self.action == 'retrieve':
            return VedioMeterialAndQuestionsSerializer
        # For other methods (POST, PUT, PATCH, DELETE), use the POST serializer
        return VedioMeterialAndQuestionsPostSerializer

    def update(self, request, *args, **kwargs):
        instance=self.get_object()
        name=request.data.get('name')
        description=request.data.get('description')
        video=request.data.get('video')
        thumbnail=request.data.get('thumbnail')
        materials=request.data.get('material')
        questionpapers=request.data.get('questionpaper')

        if 'name' in request.data:
            instance.name=name
        if 'description' in request.data:
            instance.description=description
        if 'thumbnail' in request.data:
            instance.thumbnail=thumbnail
        if 'video' in request.data:
            try:
                video_instance = StudioVideo.objects.get(id=video)
                instance.video = video_instance
            except StudioVideo.DoesNotExist:
                return Response({"message": f"The video with ID {video} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if 'material' in request.data:
            instance.material.clear()
            materialss=json.loads(materials)
            for material in materialss:
                try:
                    mat=PackageMaterials.objects.get(id=material)
                    instance.material.add(mat)
                except:
                    return Response({"message":f"the material id {material} not found"},status=404)
                
        if 'questionpaper' in request.data:
            instance.questionpaper.clear()
            questionpaper=json.loads(questionpapers)
            for paper in questionpaper:
                try:
                    papers=QuestionPaper.objects.get(id=paper)
                    instance.questionpaper.add(papers)
                except:
                    return Response({"message":f"the questiopaper id {paper} not found"},status=404)
                
        instance.save()
        serializers=VedioMeterialAndQuestionsPostSerializer(instance)
        return Response(serializers.data,status=200)


        return super().retrieve(request, *args, **kwargs)


class ReadonlyVideopPckage(viewsets.ReadOnlyModelViewSet):
    serializer_class=VedioPackageREadonlySerializer
    queryset=VedioPackage.objects.filter(status=True).order_by('-created_at')
    pagination_class=SinglePagination

class VideoPackagefullDetils(viewsets.ReadOnlyModelViewSet):
    serializer_class=VedioPackageREadonlySerializer
    queryset=VedioPackage.objects.all()
    pagination_class=SinglePagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Block the 'list' method and return a MethodNotAllowed response.
        return Response(
            {"detail": "Method 'list' not allowed on this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        ) 
class VedioPackageViewset(viewsets.ModelViewSet):
    serializer_class=VedioPackageSerializer
    queryset=VedioPackage.objects.all().order_by('-created_at')
    pagination_class = SinglePagination

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        image = request.data.get('image')
        banner=request.data.get('banner')
        videos = request.data.get('videos')
        price = request.data.get('price')
        discount_price = request.data.get('discount_price')
        premiums = request.data.get('premium')
        premium=json.loads(premiums)
        statuses=request.data.get('status')
        sts=json.loads(statuses)
        description=request.data.get('description')
        try:
            cat=request.data.get('category')
            category=json.loads(cat)
            levl=request.data.get('level')
            level=json.loads(levl)
        
            cat=Category.objects.get(id=category)
            lev=Level.objects.get(id=level)
        except:
            pass

        if cat and lev:
            vedio_package = VedioPackage.objects.create(
                name=name,
                image=image,
                banner=banner,
                price=price,
                discount_price=discount_price,
                premium=premium,
                status=sts,
                description=description,
                category=cat,
                level=lev
            )
        else:
            vedio_package = VedioPackage.objects.create(
                name=name,
                image=image,
                banner=banner,
                price=price,
                discount_price=discount_price,
                premium=premium,
                status=sts,
                description=description,
            )


        serializer = VedioPackageSerializer(vedio_package)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        name = request.data.get('name')
        image = request.data.get('image')
        videos = request.data.get('videos')
        price = request.data.get('price')
        discount_price = request.data.get('discount_price')
        premiumes = request.data.get('premium')
        statuses=request.data.get('status')
        description=request.data.get('description')
    
        # Update the instance fields
        if 'name' in request.data:
            instance.name=name
        if 'image' in request.data:
            instance.image=image
        if 'price' in request.data:
            instance.price=price
        if 'discount_price' in request.data:
            instance.discount_price=discount_price
         # Check if "premium" key exists in the request data before updating
        if 'premium' in request.data:
            print("ddd")
            premium=json.loads(premiumes)
            instance.premium = premium
        if 'status' in request.data:
            status_data=json.loads(statuses)
            instance.status = status_data
        if 'description' in request.data:
            instance.description=description

        # Clear existing videos and add the new ones
        if 'videos' in request.data:
            instance.videos.clear()
            videos_list = json.loads(videos)
            for video_id in videos_list:
                try:
                    video = VedioMeterialAndQuestions.objects.get(pk=video_id)
                    instance.videos.add(video)
                except VedioMeterialAndQuestions.DoesNotExist:
                    return Response({"message": f"Video with ID {video_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        instance.save()
        serializer = VedioPackageSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):

        queryset = VedioPackage.objects.all().order_by('-created_at')
        print("qqqqqqqqqqqqqqqqq",queryset)
        package_name = self.request.query_params.get('name',None)
        package_price = self.request.query_params.get('price',None)
        discount_price = self.request.query_params.get('discount_price',None)
        # premium = self.request.query_params.get('imaddge',None)
        # status = self.request.query_params.get('dddn',None)

        if package_name:
            queryset = queryset.filter(name__icontains = package_name)
        
        if package_price:
            queryset = queryset.filter(price = package_price)
        
        if discount_price:
            queryset = queryset.filter(discount_price = discount_price)
        print(queryset.values())
        
        return queryset
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        print(queryset.values)


        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                'premium':{'True':'Yes','False':'No'},
                'status':{'True':'Yes','False':'No'}
            }) 
            return response
        if pdf_query:
            fields = ['name','category__name','level__name','price','discount_price']
            headers,data = get_queryset_headers_data(queryset,fields=fields)

            replacement_values = ["Video Name", "Category Name", "Level Name"]

            modified_headers = []
            replacement_index = 0  # Initialize index for replacement_values

            for header in headers:
                if header == "Name" and replacement_index < len(replacement_values):
                    modified_header = replacement_values[replacement_index]
                    replacement_index += 1
                else:
                    modified_header = header
                
                modified_header = modified_header.replace('Discount_price','Discount Price')

                modified_headers.append(modified_header)
                
            print(modified_headers)

            nameheading = 'Video package'
            current_datetime = timezone.now()
            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'currrent_datetime' : current_datetime,
                'model' : nameheading

            }
            resp = generate_pdf('commonpdf.html',pdf_data,'VideoPackageList.pdf')
            return resp

        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
        

    
class ReadonlyVideopPckageDashboard(viewsets.ReadOnlyModelViewSet):
    serializer_class=VedioPackageDashboardREadonlySerializer
    queryset=VedioPackage.objects.filter(status=True).order_by('-created_at')
    pagination_class=SinglePagination
    # permission_classes=[StudentPermission]

    def get_serializer_context(self):
        # Get the default context from the parent method
        context = super().get_serializer_context()
        # Add your custom context data based on the viewset action
        context['id'] = AuthHandlerIns.get_id(request=self.request)
        return context
    
    def get_queryset(self):
        id = AuthHandlerIns.get_id(request=self.request)
        if id:
            # Fetch purchased items
            purchased_items = PurchaseDetails.objects.filter(
                user=id, purchase_item='VIDEO_PACKAGE'
            ).values_list('purchase_item_id', flat=True)

            # Annotate with is_purchased field based on whether the item has been purchased or not
            queryset = VedioPackage.objects.filter(status=True).annotate(
                is_purchased=Case(
                    When(id__in=purchased_items, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            ).order_by('-is_purchased', '-created_at')
        else:
            # If no user is logged in, just list all exam packages by created_at
            queryset = VedioPackage.objects.filter(status=True).order_by('-created_at')

        return queryset

    def list(self, request, *args, **kwargs):
        # if AuthHandlerIns.get_id(request=self.request):
            return super().list(request, *args, **kwargs) 
        # else:
            # return Response({"message":"you dont have permmission"})


class VideoPackageViewdetails(viewsets.ReadOnlyModelViewSet):
    serializer_class=VideopacakgeviewdetialsSerializer
    queryset=VedioPackage.objects.all().order_by('-created_at')
    pagination_class=SinglePagination
    permission_classes=[StudentPermission]


    def retrieve(self, request, *args, **kwargs):
        id = AuthHandlerIns.get_id(request=self.request)
        wathced=self.request.query_params.get('watched')
        unwatched=self.request.query_params.get('unwatched')
        if id and not wathced and not unwatched:
            instance = self.get_object()
            serializer = self.get_serializer(instance, context={'id': id})
            return Response(serializer.data)

        if wathced or unwatched:
            instance = self.get_object()
            ids = instance.id
            videopackagess = VedioPackage.objects.get(id=ids)
            videoss = videopackagess.videos.all()
            video_ids = [x.video.id for x in videoss]

            watch = Views.objects.filter(user=id, view_assign='VIDEOS', view_id__in=video_ids)
            watchedvideo = [x.view_id for x in watch]
            
            unwatchedvideo = [video_id for video_id in video_ids if video_id not in watchedvideo]


            if wathced:
                # watched_packages = VedioPackage.objects.filter(id=ids, videos__video__id__in=watchedvideo)
                watched_packages =  VedioPackage.objects.get(id=ids)
                serializer = VideopacakgeviewdetialsSerializerWatched(watched_packages, context={'watchedvideo': watchedvideo,'id': id})
            elif unwatched :
                # unwatched_packages = VedioPackage.objects.filter(id=ids, videos__video__id__in=unwatchedvideo)
                unwatched_packages = VedioPackage.objects.get(id=ids)
                print(unwatched_packages,'unpackae')
                serializer = VideopacakgeviewdetialsSerializerWatched(unwatched_packages, context={'unwatchedvideo': unwatchedvideo,'id': id})
            else:
                pass
            return Response(serializer.data)
        else:
            return Response({"message": "permission is not allowed"})
               
    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'list' not allowed on this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

class VideoPackagePurchase(viewsets.ModelViewSet):
    serializer_class=VedioPackageSerializer
    queryset=VedioPackage.objects.all()
    pagination_class = SinglePagination
    http_method_names = ['patch']


    def partial_update(self, request, *args, **kwargs):
        print('hellooooooooooooo1')
        obj=self.get_object()
        print('hellooooooooooooo2',)

        raz = razorpay_client.order.create(data={'amount':int(obj.discount_price*100), 'currency':'INR'})
        print(raz)
        current_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(current_time, "%Y%m%d%H%M%S")
        random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))
        order_id = f"{timestamp}-{random_string}"
        user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        print(user,'user')
        pay=OnlineOrderPayment.objects.create(user=user,user_ref=user.id,order_number=order_id,product='videopackages',product_id=obj.id,razor_id=raz['id'],total_amount=obj.discount_price,paid_amount=raz['amount_paid']/100,off_amount=0,offer_choice='none',payment_status='pending',delivery_status='pending')
        print("$$$")
        return Response(raz)
    
class CommentsViewset(viewsets.ModelViewSet):
    queryset=Comments.objects.all()
    serializer_class=CommentsAppSerializer
    pagination_class=SinglePagination
    permission_classes = [StudentPermission]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = AuthHandlerIns.get_id(request=self.request)
        return context

    def get_queryset(self):
        queryset=Comments.objects.all()
        # print(self.action,"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        if self.action in ['list','retrieve']:
            queryset=queryset
        else:
            queryset=queryset.filter(user__id=AuthHandlerIns.get_id(request=self.request))
        feature=self.request.query_params.get('feature')
        if feature :
            queryset=queryset.filter(comment_assign=feature)
        id=self.request.query_params.get('id')
        if id :
            queryset=queryset.filter(commented_id=id)
        
        
        return queryset.order_by('-created_at')

    
from django.db.models import Count, OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist

class StoriesAllCategoryViewSet(viewsets.ModelViewSet):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminOrStudent]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = AuthHandlerIns.get_id(request=self.request)
        print(context['user'],"Context")
        return context

    def get_queryset(self):
        if AuthHandlerIns.is_student(request=self.request):
            user = AuthHandlerIns.get_id(request=self.request)
            try:
                categories = StoriesCategory.objects.all()
            except ObjectDoesNotExist:
                return Response({'error': 'No categories available.'}, status=status.HTTP_404_NOT_FOUND)


            
            try:
                student = Student.objects.get(user=user)
                level = student.selected_course.level.id
            except:
                return Response({'error':'The Student Dosent exists or Need to select a Batch'})

            
            watched_stories = StoriesWatched.objects.filter(student=user, watched=True).values('stories__id')
            unwatched_videos = Stories.objects.filter(level=level, category__in=categories) \
                .exclude(id__in=Subquery(watched_stories))

            return unwatched_videos

        else:
            return Stories.objects.all().order_by('-id')
        

class StoriesUserAllCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoriesCategory.objects.all()
    serializer_class = StoriesCategoryUserSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        print(context['request'],"Context")
        return context


    


class LikesViewset(viewsets.ModelViewSet):
    queryset=Likes.objects.all()
    serializer_class=LikesAppSerializer
    pagination_class=SinglePagination
    permission_classes = [StudentPermission]

    def get_queryset(self):
        queryset=Likes.objects.all()
        # print(self.action,"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        if self.action in ['list','retrieve']:
            queryset=queryset
        else:
            queryset=queryset.filter(user__id=AuthHandlerIns.get_id(request=self.request))
        feature=self.request.query_params.get('feature')
        if feature :
            queryset=queryset.filter(like_assign=feature)
        id=self.request.query_params.get('id')
        if id :
            queryset=queryset.filter(liked_id=id)
        
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        data = request.data

        # Extract the fields you use to check if the object already exists
        # For example, if your model has a unique field 'name', you can use it for checking
        # name = data.get('name')
        like_assign = data.get('like_assign')
        liked_id = data.get('liked_id')
        user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        
            # Check if an object with the same name exists
        try:
            existing_object = Likes.objects.get(user=user,like_assign=like_assign,liked_id=liked_id)
            # If the object exists, delete it
            existing_object.delete()
            return Response({"Status":True},status=status.HTTP_201_CREATED)  # Successfully deleted
        except Likes.DoesNotExist:
            print("11111111111111111")
            pass  # The object does not exist, continue with creation

        # If the object does not exist or no unique field was provided, proceed with creation
        serializer = LikesAppSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
        
    
import boto3
from botocore.exceptions import ClientError

# @api_view(['GET'])
# def stream_s3_image(request, id):
#     # Fetch the appropriate QuestionImage instance using the provided 'id'
#     img = get_object_or_404(QuestionImage, id=id)

#     # Get the image key from the 'name' attribute of the 'image' field
#     image_key = img.questionimage.url
#     print(image_key,"hhhhhhhhhhhhhhhhhhhhhhhhhhhx   ")

#     # Initialize the S3 client
#     s3_client = boto3.client('s3')
#     bucket_name = AWS_STORAGE_BUCKET_NAME  # Replace with your S3 bucket name

#     try:
#         response = s3_client.get_object(Bucket=bucket_name, Key=image_key)
#         image_data = response['Body'].read()
#         content_type = response['ContentType']

#         # Stream the image as a response
#         response = StreamingHttpResponse(
#             streaming_content=(chunk for chunk in iter(lambda: image_data.read(8192), b'')),
#             content_type=content_type,
#         )
#         response['Content-Length'] = response.get('Content-Length', len(image_data))
#         response['Content-Disposition'] = 'inline; filename="{}"'.format(image_key)
#         return response

#     except ClientError as e:
#         return HttpResponse(status=404)

@api_view(['GET'])
def stream_s3_image(request, id):
    # Fetch the appropriate QuestionImage instance using the provided 'id'
    img = get_object_or_404(QuestionImage, id=id)

    # Get the image data from the 'image' field
    image_data = img.questionimage.file

    # Get the content type of the image (e.g., 'image/jpeg', 'image/png', etc.)
    content_type = 'image/jpeg'

    # Stream the image data as a response
    return StreamingHttpResponse(
        streaming_content=(chunk for chunk in iter(lambda: image_data.read(8192), b'')),
        content_type=content_type,
    )

class ExampaperpackageViewset(viewsets.ModelViewSet):
    serializer_class=ExampaperpackageSerializerforAdmin
    queryset=ExampaperPackage.objects.all().order_by('-created_at')
    pagination_class=SinglePagination


    def list(self,request,*args,**kwargs):
        queryset=self.get_queryset()
        page =self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return (self.get_paginated_response(serializer.data))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self,request,*args,**kwargs):
        title=request.data.get('title')
        imagetitle=request.data.get('imagetitle')
        thumbnail=request.data.get('thumbnail')
        banners=request.data.get('banner')
        description=request.data.get('description')
        price=request.data.get('price')
        discount_price=request.data.get('discount_price')
        premiums=request.data.get('premium')
        premium=json.loads(premiums)
        statuses=request.data.get('status')
        status=json.loads(statuses)
        level=request.data.get('level')
        exampaper=request.data.get('exampaper')
       
        try:
            exampaper=json.loads(exampaper)
        except json.JSONDecodeError:
            return Response({'message':"invalid formate for exampaper field"})
        try:
            levels=Level.objects.get(pk=level)
        except:
            return Response({"message":"level ID not found"})

        exampaperpackage=ExampaperPackage.objects.create(
            title=title,
            imagetitle=imagetitle,
            thumbnail=thumbnail,
            banner=banners, 
            description=description,
            price=price,
            discount_price=discount_price,
            premium=premium,
            status=status,
            level=levels,
        )
        for examppper_id in exampaper:
            try:
                exampapers=QuestionPaper.objects.get(pk=examppper_id)
                exampaperpackage.exampaper.add(exampapers)
            except VedioMeterialAndQuestions.DoesNotExist:
                return Response({"message": f"Video with ID {examppper_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExampaperpackageSerializerforAdmin(exampaperpackage)
        return Response(serializer.data,status=201)
    
    def partial_update(self,request,*args,**kwargs):
        instance=self.get_object()
        print('update')
        title=request.data.get('title')
        imagetitle=request.data.get('imagetitle')
        thumbnail=request.data.get('thumbnail')
        banners=request.data.get('banner')
        description=request.data.get('description')
        price=request.data.get('price')
        discount_price=request.data.get('discount_price')
        premiums=request.data.get('premium')
        statuses=request.data.get('status')
        level=request.data.get('level')
        exampaper=request.data.get('exampaper')
        
        if 'title' in request.data:
            instance.title=title
        if 'imagetitle' in request.data:
            instance.imagetitle=imagetitle
        if 'thumbnail' in request.data:
            instance.thumbnail=thumbnail
        if 'banner' in request.data:
            instance.banner=banners
        if 'description' in request.data:
            instance.description=description
        if 'price' in request.data:
            instance.price=price
        if 'discount_price' in request.data:
            instance.discount_price=discount_price
        if 'premium' in request.data:
            premium=json.loads(premiums)
            instance.premium=premium
        if 'status' in request.data:
            status=json.loads(statuses)
            instance.status=status
        if 'level' in request.data:
            try:
                levels=Level.objects.get(pk=level)
            except:
                return Response({"message":"level ID not found"})
            instance.level=levels
        
        #clear existing exampaper and add the new ones
        if 'exampaper' in request.data:
            instance.exampaper.clear()
            exampaper_list=json.loads(exampaper)
            for exampaper_id in exampaper_list:
                try:
                    exampapers=QuestionPaper.objects.get(pk=exampaper_id)
                    instance.exampaper.add(exampapers)
                except VedioMeterialAndQuestions.DoesNotExist:
                    return Response({"message": f"Video with ID {exampaper_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.save()
        serializer=ExampaperpackageSerializerforAdmin(instance)
        return Response(serializer.data,status=200)

from datetime import datetime
class PurchaseExamPackages(viewsets.ModelViewSet):
    serializer_class=ExampaperpackageSerializerforAdmin
    queryset=ExampaperPackage.objects.all().order_by('-created_at')
    pagination_class=SinglePagination
    http_method_names=['patch']

    def partial_update(self, request, *args, **kwargs):
        print('partial update')
        print('hellooooooooooooo1')
        obj=self.get_object()
        print('hellooooooooooooo2',)

        raz = razorpay_client.order.create(data={'amount':int(obj.discount_price*100), 'currency':'INR'})
        print(raz,'razzz')
        current_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(current_time, "%Y%m%d%H%M%S")
        #current_time = datetime.now()  # Get the current datetime
        # timestamp = current_time.strftime("%Y%m%d%H%M%S") 
        random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))
        order_id = f"{timestamp}-{random_string}"
        user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        pay=OnlineOrderPayment.objects.create(user=user,user_ref=user.id,order_number=order_id,product='exampackages',product_id=obj.id,razor_id=raz['id'],total_amount=obj.discount_price,paid_amount=raz['amount_paid']/100,off_amount=0,offer_choice='none',payment_status='pending',delivery_status='pending')

        return Response(raz)

class Exampackagebeforepurchase(viewsets.ReadOnlyModelViewSet):
    serializer_class=ExampackagebeforeSerializer
    queryset=ExampaperPackage.objects.filter(status=True).order_by('-created_at')
    pagination_class=SinglePagination


    def get_queryset(self):
        id = AuthHandlerIns.get_id(request=self.request)
        if id:
            # Fetch purchased items
            purchased_items = PurchaseDetails.objects.filter(
                user=id, purchase_item='EXAM_PACKAGE'
            ).values_list('purchase_item_id', flat=True)

            # Annotate with is_purchased field based on whether the item has been purchased or not
            queryset = ExampaperPackage.objects.filter(status=True).annotate(
                is_purchased=Case(
                    When(id__in=purchased_items, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            ).order_by('-is_purchased', '-created_at')
        else:
            # If no user is logged in, just list all exam packages by created_at
            queryset = ExampaperPackage.objects.filter(status=True).order_by('-created_at')

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        id = AuthHandlerIns.get_id(request=self.request)
        context['id'] = id
        return context

class ExampackageviewsDetials(viewsets.ReadOnlyModelViewSet):
    serializer_class=ExampackageviewsDetialsSeriilaizer
    queryset=ExampaperPackage.objects.filter(status=True).order_by('-created_at')
    pagination_class=SinglePagination



class ReadOnlyExampaperpackageViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExampaperpackageSerializer
    queryset = ExampaperPackage.objects.filter(status=True).order_by('-created_at')
    pagination_class = SinglePagination

    def retrieve(self, request, *args, **kwargs):
        id = AuthHandlerIns.get_id(request=self.request)
        if id:
            attend=self.request.query_params.get('attend')
            notattend=self.request.query_params.get('notattend')
            if id and not attend and not notattend:
                instance = self.get_object()
                serializer = self.get_serializer(instance, context={'id': id})
                return Response(serializer.data)
            elif id and attend or notattend:
                obj_id = kwargs.get('pk')
                attended=QuestionpaperAttend.objects.filter(student=id,exampackage=obj_id)
                print(attended,'LLLL')
                if attended:
                    instance = self.get_object()
                    serializer = self.get_serializer(instance, context={'id': id,'attend':attend,'notattend':notattend})
                    return Response(serializer.data)
                else:
                    instance = self.get_object()
                    serializer = self.get_serializer(instance, context={'id': id,'attend':attend,'notattend':notattend})
                    return Response(serializer.data)
        else:
            return Response({"message":"token missing"},status=400)


class CurrentAffairsQuestionViewSet(viewsets.ModelViewSet):
    queryset=CurrentAffairsQuestions.objects.all()
    serializer_class=CurrentAffairsQuestionsSerializer
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]




class CurrentAffairsQuestionsDaySortedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrentAffairsQuestions.objects.filter(published=True,status=True).order_by('-id')  # Only published current affairs
    serializer_class = CurrentAffairsQuestionsSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]
    
    def get_queryset(self):
        
        

        days = self.request.query_params.get('days')
        if days is not None:
            current_date = timezone.now().date()
            filter_date = current_date - timedelta(days=int(days))
            queryset = self.queryset.filter(
                Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
            )
            print(queryset)
            if not queryset.exists():
                queryset = CurrentAffairsQuestions.objects.filter(published=True).order_by('-publish_on')
        else:
            queryset = CurrentAffairsQuestions.objects.filter(published=True).order_by('-publish_on')  # Return total queryset

        
        return queryset
    
class CurrentAffairsVideosViewSet(viewsets.ModelViewSet):
    queryset=CurrentAffairsVideos.objects.all()
    serializer_class=CurrentAffairsVideosSerializer
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]





class CurrentAffairsVideosDaySortedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrentAffairsVideosAssign.objects.filter(published=True,status=True).order_by('-id')  # Only published current affairs
    serializer_class = CurrentAffairsVideosAssignSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]
    
    def get_queryset(self):
        
        

        days = self.request.query_params.get('days')
        if days is not None:
            current_date = timezone.now().date()
            filter_date = current_date - timedelta(days=int(days))
            queryset = self.queryset.filter(
                Q(publish_on__gte=filter_date) & Q(publish_on__lte=current_date)
            )
            print(queryset)
            if not queryset.exists():
                queryset = CurrentAffairsVideosAssign.objects.filter(published=True).order_by('-publish_on')
        else:
            queryset = CurrentAffairsVideosAssign.objects.filter(published=True).order_by('-publish_on')  # Return total queryset

        
        return queryset
    
class DailyExamViewSet(viewsets.ModelViewSet):
    queryset = DailyExams.objects.all()
    serializer_class = DailyExamsSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def create(self, request, *args, **kwargs):
        title = request.data['title']
        imagetitle = request.data['imagetitle']
        exampaper = QuestionPaper.objects.get(id=request.data['exampaper'])
        level = Level.objects.get(id=request.data['level'])
        thumbnail = request.data['thumbnail']
        created_by = User.objects.get(id=request.data['created_by']) 
        try:
            status = bool(request.data['status'])
        except:
            status = False
    
        dailyexam=DailyExams.objects.create(
                    title=title,
                    imagetitle=imagetitle,
                    exampaper=exampaper,
                    level=level,
                    thumbnail=thumbnail,
                    created_by=created_by,
            
                    status=status
                    
            )
        
        ser = self.serializer_class(dailyexam)
        return Response(ser.data)
    
class DailyExamsAppView(viewsets.ReadOnlyModelViewSet):
    queryset = DailyExams.objects.all()
    serializer_class = DailyExamsSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]

    def get_queryset(self):
        user_id = AuthHandlerIns.get_id(request=self.request)
        try:
            student = Student.objects.get(user=user_id)
            level = student.selected_course.level.id
        except:
            return Response({'error':'There must be a student with a proper course'})
        
        queryset = DailyExams.objects.filter(level=level,status=True)
        return queryset


from django.utils.dateparse import parse_date

class CurrentAffairsVideosAssaignViewSet(viewsets.ModelViewSet):
    queryset=CurrentAffairsVideosAssign.objects.all().order_by('-id')
    serializer_class=CurrentAffairsVideosAssignSerializer
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]  

    def get_queryset(self):
        queryset = CurrentAffairsVideosAssign.objects.all()
        
        publish_on_start = self.request.query_params.get('publish_on_start', None)
        publish_on_end = self.request.query_params.get('publish_on_end', None)

        if publish_on_start and publish_on_end:
            start_date = parse_date(publish_on_start)
            end_date = parse_date(publish_on_end)
            if start_date and end_date:
                queryset = queryset.filter(publish_on__range=(start_date, end_date))


        # Apply search filter
        video = self.request.query_params.get('video', None)
        if video:
            queryset = queryset.filter( video__name__icontains=video)

        publish_on = self.request.query_params.get('publish_on', None)
        if publish_on:
            queryset = queryset.filter(publish_on__icontains=publish_on)
        
        return queryset.order_by('-publish_on')


class SpecialExamsViewset(viewsets.ModelViewSet):
    queryset=SpecialExams.objects.all()
    serializer_class=SpecialExamsSerializer
    pagination_class=SinglePagination

    def get_serializer_class(self):
        if self.action=='create':
            print("create")
            return SpecialExamsPOSTSerializer
        return super().get_serializer_class()


class FacultyListforvideopackage(viewsets.ReadOnlyModelViewSet):
    serializer_class = FacultyQuestionSerchserializer
    pagination_class = SinglePagination

    #####add permissions
    # def get_permissions(self):
    #     if self.action in ['list']:
    #         print(self.request.data,'data')
    #         self.feature = self.action
    #         # print(self.permission,'ddd')
    #         print("list")
    #         self.permission = "Videopackage"
    #         self.permission_classes = [AdminAndRolePermission, ]
    #     return super().get_permissions()
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
        return queryset
    

class GeneralVideosMaterialViewset(viewsets.ModelViewSet):
    permission_classes=[AdminAndRolePermission]
    pagination_class=SinglePagination
    queryset= GeneralVideosMaterial.objects.all()
    serializer_class=GeneralVideosMaterialSerializer


class PreviousExamViewSet(viewsets.ModelViewSet):
    queryset = PreviousExams.objects.all()
    serializer_class = PreviousExamsSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def create(self, request, *args, **kwargs):
        title = request.data['title']
        imagetitle = request.data['imagetitle']
        exampaper = QuestionPaper.objects.get(id=request.data['exampaper'])
        course = Course.objects.get(id=request.data['course'])
        thumbnail = request.data['thumbnail']
        created_by = User.objects.get(id=request.data['created_by']) 
        try:
            status = bool(request.data['status'])
        except:
            status = False
    
        previousexam=PreviousExams.objects.create(
                    title=title,
                    imagetitle=imagetitle,
                    exampaper=exampaper,
                    course=course,
                    thumbnail=thumbnail,
                    created_by=created_by,
            
                    status=status
                    
            )
        
        ser = self.serializer_class(previousexam)
        return Response(ser.data)
    
class PreviousExamsAppView(viewsets.ReadOnlyModelViewSet):
    queryset = PreviousExams.objects.all()
    serializer_class = PreviousExamsSerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]

    def get_queryset(self):
        user_id = AuthHandlerIns.get_id(request=self.request)
        try:
            student = Student.objects.get(user=user_id)
            course = student.selected_course.id
        except:
            return Response({'error':'There must be a student with a proper course'})
        
        queryset = PreviousExams.objects.filter(course=course,status=True)
        return queryset

from django.db import IntegrityError

class PopularFacultyEntryViewSet(viewsets.ModelViewSet):
    queryset = PopularFaculty.objects.all()
    serializer_class = PopularFacultySerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def create(self, request,*args, **kwargs):
        

        faculty_ids = request.data.get('faculty_ids', [])
        priorities = request.data.get('priorities', [])
        course_id = request.data.get('course')
        # delete=request.query_params.get('delete', False)
        # if delete :
        #     deleted_count = PopularFaculty.objects.filter(course_id=course_id, faculty_id__in=faculty_ids)
        #     for i in deleted_count:
        #         i.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)



        if len(faculty_ids) != len(priorities):
            return Response({'error': 'Faculty IDs and Priorities should have the same number of elements'}, status=400)

        created_entries = []
        for faculty_id, priority in zip(faculty_ids, priorities):
            faculty = Faculty.objects.get(pk=faculty_id)
            course = Course.objects.get(pk=course_id)
            try:
                entry = PopularFaculty.objects.create(faculty=faculty, priority=priority, course=course)
                created_entries.append(entry)
            except IntegrityError:
                duplicate_entry = PopularFaculty.objects.filter(
                    faculty=faculty, course=course
                ).first()

                if duplicate_entry:
                    return Response({'Error': "Duplication of Faculty on Same course not allowed"})

        serializer = PopularFacultySerializer(created_entries, many=True)
        return Response(serializer.data, status=201)
    
    def get_queryset(self):
        
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = PopularFaculty.objects.filter(course_id=course_id).order_by('priority')
        else:
            queryset = PopularFaculty.objects.all()
        
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter( faculty__name__icontains=name)

        
        course = self.request.query_params.get('course_name', None)
        if course:
            queryset = queryset.filter(course__name__icontains=course)

        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course__id__icontains=course_id)
        
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority__icontains=priority)
        
        return queryset.order_by('priority','course')

    
    def update(self, request, *args, **kwargs):
        faculty_ids = request.data.get('faculty_ids', [])
        priorities = request.data.get('priorities', [])
        course_id = request.data.get('course')
        delete=request.query_params.get('delete', False)
        if delete :
            deleted_count = PopularFaculty.objects.filter(course_id=course_id, faculty_id__in=faculty_ids)
            for i in deleted_count:
                i.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



        if not (faculty_ids and priorities and course_id):
            return Response({'error': 'Faculty IDs, Priorities, and Course are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if len(faculty_ids) != len(priorities):
            return Response({'error': 'Faculty IDs and Priorities should have the same number of elements'}, status=status.HTTP_400_BAD_REQUEST)

        for faculty_id, priority in zip(faculty_ids, priorities):
            try:
                faculty = Faculty.objects.get(pk=faculty_id)
                existing_entries = PopularFaculty.objects.filter(course_id=course_id, faculty=faculty)
                if existing_entries.exists():
                    # Update existing entries
                    existing_entries.update(priority=priority)
                else:
                    # Create a new entry
                    PopularFaculty.objects.create(faculty=faculty, priority=priority, course_id=course_id)
            except Faculty.DoesNotExist:
                return Response({'error': f'Faculty with ID {faculty_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError:
                return Response({'error': f'IntegrityError: Duplicate entry for faculty {faculty_id} and course {course_id}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Updated faculties and priorities successfully'}, status=status.HTTP_200_OK)
    
    
    

class Viewviewset(viewsets.ModelViewSet):
    queryset = Views.objects.all()
    serializer_class = ViewSerializeruser
    permission_classes = [StudentPermission]
    pagination_class = SinglePagination

from rest_framework.exceptions import NotFound,APIException,PermissionDenied

class PopularFacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PopularFaculty.objects.all()
    serializer_class = PopularFacultySerializer
    pagination_class = SinglePagination
    permission_classes = [StudentPermission]


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
            queryset = PopularFaculty.objects.filter(course=course_id).order_by('priority')
            if queryset.exists():
                return queryset
            else:
                return Response({'Warning': 'No Popular faculty Found'})
        except Student.DoesNotExist:
            raise NotFound("No Student found")
        except Exception as e:
            raise APIException(str(e))
        
# class PopularFacultyOnCoursePriorityForAdminViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PopularFaculty.objects.all()
#     serializer_class = PopularFacultySerializer
#     pagination_class = SinglePagination
#     permission_classes = [AdminAndRolePermission]

#     def get_queryset(self):

    
        
class ScholarshipTypeViewset(viewsets.ModelViewSet):
    queryset = ScholarshipType.objects.all().order_by('-created_at')
    serializer_class = ScholarshipTypeSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        queryset=self.queryset

        scholarship_id = self.request.query_params.get('id',None)
        if scholarship_id:
            queryset = ScholarshipType.objects.filter(id=scholarship_id)

        scholarship_name = self.request.query_params.get('name',None)
        if scholarship_name:
            queryset = ScholarshipType.objects.filter(name__icontains = scholarship_name)
        
        scholarship_percentage = self.request.query_params('percentage',None).values()
        if scholarship_percentage:
            queryset = ScholarshipType.objects.filter(percentage__icontains = scholarship_percentage,discount_amount__icontain = scholarship_percentage )

        scholarship_created = self.request.query_params('created_at',None)
        if scholarship_created:
            queryset = ScholarshipType.objects.filter(created_at = scholarship_created)
        
        return queryset
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        # checking if PDF download is requested
        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                                             'status':{'True':'Yes','False':'No'}
                                         })
            return response
        if pdf_query:
            fields = ['id','name','discount_amount','percentage','created_at']
            headers, data = get_queryset_headers_data(queryset, fields = fields)

            # changing headers
            # modified_headers = []
            modified_headers = [header
                                .replace('Discount_amount','Discount Amount')
                                .replace('Admission_number','Admission Number')
                                .replace('Created_at','Created At')
                                for header in headers]
            nameheading = 'Types Scholarship'
            current_datetime =timezone.now()

            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading
            }
            resp = generate_pdf('commonpdf.html',pdf_data, 'scholarshipType.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



from rest_framework.pagination import PageNumberPagination
class PopularFacultyEntryAdminGETViewSet(viewsets.ModelViewSet):
    queryset = PopularFaculty.objects.all()
    serializer_class = PopularFacultySerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def list(self, request, *args, **kwargs):
        page_size = 8
        page_number = int(request.query_params.get('page', 1))
        queryset = PopularFaculty.objects.filter(is_delete=False).select_related('faculty', 'course')

        total_records = queryset.count()
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        courses = {}
        for entry in paginated_queryset:  # Loop through paginated queryset
            course_id = entry.course.id
            if course_id not in courses:
                courses[course_id] = {
                    'course_name': entry.course.name,
                    'course_id':entry.course.id,
                    'level_name': entry.course.level.name,
                    'category_name': entry.course.level.category.name,
                    'level_id': entry.course.level.id,
                    'category_id': entry.course.level.category.id,
                    'faculties': []
                }
            courses[course_id]['faculties'].append({
                'id':entry.id,
                'faculty': FacultyDetailsSerilaizer(entry.faculty).data,
                'priority': entry.priority,
                
            })

        response_data = {
            'count': total_records,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'current': page_number,
            'courses': list(courses.values())
        }

        return Response(response_data, status=status.HTTP_200_OK)


from rest_framework.decorators import action
# class FacultyOnCourseViewSet(viewsets.ModelViewSet):
#     queryset = FacultyCourseAddition.objects.all()
#     serializer_class = FacultyCourseAdditionSerializer
#     pagination_class = SinglePagination
#     permission_classes = [AdminAndRolePermission]

#     @action(detail=True, methods=['get'])
#     def faculty_info(self, request, pk=None):
#         print(pk)
#         try:
#             faculty_course = FacultyCourseAddition.objects.filter(course=pk,status='approved')
#             print(faculty_course)
#             if faculty_course:
#                 faculty_list = []
#                 for faculty in faculty_course:
#                     print(faculty.user.id,"INSTANCE")
#                     faculty = Faculty.objects.get(user=faculty.user)
#                     print(faculty,"FACU")
#                     serializer = FacultyInfoSerializer({
#                         'faculty_id': faculty.id,
#                         'faculty_name': faculty.name,
#                         'email': faculty.user.email,
#                         'mobile': faculty.user.mobile,
#                         # 'photo': faculty.photo.url,
#                     })
#                     faculty_list.append(serializer.data)
#                 return Response (faculty_list)
#             else:
#                 return Response({'error': 'Faculty course is not approved.'}, status=400)
#         except FacultyCourseAddition.DoesNotExist:
#             return Response({'error': 'Faculty course not found.'}, status=404)

class FacultyOnCourseViewSet(viewsets.ModelViewSet):
    queryset = FacultyCourseAddition.objects.all()
    serializer_class = FacultyInfoSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        pk = self.request.query_params.get('course_id')
        try:
            faculty_course = FacultyCourseAddition.objects.filter(course=pk, status='approved').distinct('user').order_by('user')
            print(faculty_course)
            if faculty_course:
                faculty_list = []
                processed_faculty_ids = set()
                for faculty_addition in faculty_course:  
                    print(faculty_addition.user.id, "INSTANCE")
                    if faculty_addition.user.id not in processed_faculty_ids:
                        faculty = Faculty.objects.get(user=faculty_addition.user)
                        print(faculty, "FACU")
                        faculty_data = {
                            'faculty_id': faculty.id,
                            'faculty_name': faculty.name,
                            'email': faculty.user.email,
                            'mobile': faculty.user.mobile,
                            # 'photo': faculty.photo.url,
                        }
                        faculty_list.append(faculty_data)
                        faculty_id = faculty.id
                        processed_faculty_ids.add(faculty_id)
                        print(faculty_list)
                return faculty_list 
            else:
                return Response({'error': 'Faculty course is not approved.'}, status=status.HTTP_400_BAD_REQUEST)
        except FacultyCourseAddition.DoesNotExist:
            return Response({'error': 'Faculty course not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PopularFacultyOnCourseGETViewSet(viewsets.ModelViewSet):
    queryset = PopularFaculty.objects.all()
    serializer_class = PopularFacultySerializer
    # pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')  
        if course_id:
            return self.queryset.filter(course_id=course_id).order_by('priority')
        return self.queryset

class AvailableCoursesOnPopularFaculty(viewsets.ModelViewSet):
    queryset = PopularFaculty.objects.all().distinct('course').order_by('course')
    serializer_class = PopularFacultyCourseSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        queryset = PopularFaculty.objects.all().distinct('course').order_by('course')
        course_name = self.request.query_params.get('course_name', None)
        if course_name:
            queryset = queryset.filter(course__name__icontains=course_name)

        created_at = self.request.query_params.get('created_at', None)
        if created_at:
            queryset = queryset.filter(created_at__icontains=created_at)
        
        return queryset
    

 



    
from asgiref.sync import async_to_sync
from Sockets.Consumer import pollins
from channels.layers import get_channel_layer
@api_view(['GET'])
def get_socket(request):
    # print(pollins.channel_layers)
    user_id='pf1'
    channel_layer = get_channel_layer()
    print(channel_layer,"hhhhh")
    async_to_sync(channel_layer.group_send)(
        f"{user_id}",  # Use the recipient's group
        {"type": "group_message", "message": "New message received! 1"}
    )
    # async_to_sync(pollins.msg("message"))

    
    return Response( True)

class ScholarshipApprovalViewSet(viewsets.ModelViewSet):
    # queryset = ScholarshipApproval.objects.all().order_by('-created_at')
    serializer_class = ScholarshipApprovalSerializer
    pagination_class = SinglePagination
    permission_classes = [AdminAndRolePermission]

    def get_queryset(self):
        queryset = ScholarshipApproval.objects.all()
        
    #   studentid = [x.student.pk for x in queryset]
    #   print("student id : ",studentid)

        scholarshipStudent_id = self.request.query_params.get('id',None)
        if scholarshipStudent_id:
            queryset = ScholarshipApproval.objects.filter(student__in=scholarshipStudent_id,student__scholarship=True)
    
        student_name = self.request.query_params.get('student',None)
        print("asssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        if student_name:
            queryset = ScholarshipApproval.objects.filter(student__name__icontains = student_name,student__scholarship=True)
        print("student name:      ",student_name)
        scholarship_type = self.request.query_params.get('type',None)
        if scholarship_type:
            queryset = ScholarshipApproval.objects.filter(type__name = scholarship_type,approved = True)
        print("ggggggggggggggggggggggggggggggggggggggggg")

        scholarship_approvedby = self.request.query_params.get('approved_byname',None)
        if scholarship_approvedby:
            queryset = ScholarshipApproval.objects.filter(approved_by__email__icontains = scholarship_approvedby)
    
        scholarship_createdat = self.request.query_params.get('created_at',None)
        if scholarship_createdat:
            queryset = ScholarshipApproval.objects.filter(created_at = scholarship_createdat)
        
        scholarship_approvedOn = self.request.query_params.get('approved_on',None)
        if scholarship_approvedOn:
            queryset = ScholarshipApproval.objects.filter(approved_on = scholarship_approvedOn)
        print("scholarship approval student queryset :",queryset)
        return queryset
    
    def create(self, request, *args, **kwargs):
        print("creation: ")
        types = request.data.get('type')
        s_type = json.loads(types)
        student = Student.objects.get(id = request.data.get('student'))
        checks = ScholarshipApproval.objects.filter(student=student)
        if checks:
            return Response({'Message':'Student already has a scholarship'})
        # if student.scholarship==False:
        #     return Response({'Warning': 'Student not elegible for Scholarship'})
        if AuthHandlerIns.is_staff(request=self.request):
            approved_by = User.objects.get(id=AuthHandlerIns.get_id(request=request))
            approve = True
            approved_on = timezone.now().strftime("%Y-%m-%d")
        else:
            approved_by = None
            approve = False
            approved_on = None
        description_request=request.data.get('description_request')
        description_approv_reject=request.data.get('description_approv_reject')



        scholarship_approval = ScholarshipApproval.objects.create(
            
            student = student,
            approved_by = approved_by,
            description_request =  description_request,
            description_approv_reject=description_approv_reject,
            approve = approve,
            approved_on = approved_on
        )
        scholarship_approval.type.set(s_type)
        print("scholarship approval student creation ")
        serializer = ScholarshipApprovalSerializer(scholarship_approval)
        print("serializers: ",serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # s_type = '[1]'
        s_type = request.data.get('type')
        if s_type is not None:
            s_type = json.loads(s_type)
            instance.type.set(s_type)

        instance.description_request = request.data.get('description_request', instance.description_request)
        student_id = request.data.get('student', instance.student)
        validate_approval = ScholarshipApproval.objects.filter(student=student_id, approve=True)
        if validate_approval.exists():
            return Response({'Warnings': 'Student Scholarship Approved, Student can\'t be changed'})
        
        instance.student = Student.objects.get(id=student_id)
        # print(instance.student)
        instance.description_approv_reject=request.data.get('description_approv_reject', instance.description_approv_reject)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # print(request.data,"Data")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("scholarship approval student updation")
        return Response(serializer.data)
    
    
    
    def list(self,request, *args,**kwargs):
        queryset = self.get_queryset()
        excel = queryset_to_excel(queryset,['id','name'])
        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)
        print("scholarship approval student list:  ")
        # check if PDF or Excel   download  is requested
        if excel_query:
            response = queryset_to_excel(queryset,[field.name for field in queryset.model._meta.fields],{
                'status':{'True':'Yes','Flase':'No'},
                'approve':{'True':'Yes','False':'No'}
            })
            print("response from excel   :          ",response)
            return response
        
        if pdf_query:
            fields = ['student__name','type','approved_by','approved_on','created_at'] 
            headers,data = get_queryset_headers_data(queryset, fields = fields)
            print("headers of scholarship students: ",headers)
            modified_headers = []

            modified_headers = [header.replace('Approved_by','Approved by')
                                .replace('Approved_on','Approved On')
                                .replace('Created_at','Created at')
                                for header in headers]
            nameheading = 'Approved students for scholarship'
            current_datetime = timezone.now()

            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading               
            }
            print("pdf datas :         ",pdf_data)
            resp = generate_pdf('commonpdf.html',pdf_data,'scholarship students list.pdf')
            return resp
        
        # pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
import datetime
class DailyClassViewsets(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    permission_classes = [StudentPermission]
    serializer_class = DailyClassSerializer

    def get_queryset(self):
        today  = datetime.date.today()
        user = User.objects.get(id = AuthHandlerIns.get_id(request=self.request))
        student_batch = StudentBatch.objects.filter(student__user = user).values_list('batch')
        queryset = self.queryset.filter(batch__id__in = student_batch,date = today)
        return queryset




              
              
        
        
    


    

@api_view(['GET'])
def get_lobby(request):
    if AuthHandlerIns.is_student(request=request):
        try:
            current_time = timezone.now()
            time_threshold = current_time - timedelta(seconds=30)


            loby=PollFightLobby.objects.filter(Q(user1__isnull=True)|Q(user2__isnull=True),status=True,created_at__gte=time_threshold).first()
            if loby:
                print(loby)
                if not loby.user1:
                    print("here")
                    loby.user1=User.objects.get(id=AuthHandlerIns.get_id(request=request))
                elif not loby.user2:
                    print("here2")
                    loby.user2=User.objects.get(id=AuthHandlerIns.get_id(request=request))
                loby.save()
            else:
                loby=PollFightLobby.objects.create(user1=User.objects.get(id=AuthHandlerIns.get_id(request=request)))
            serial=PollFightLobbySerializer(loby,many=False)
            return Response({"message":True,"data":serial.data})
        except Exception as e:
            print(e,"E")
            try:
                loby=PollFightLobby.objects.create(user1=User.objects.get(id=AuthHandlerIns.get_id(request=request)))
                serial=PollFightLobbySerializer(loby,many=False)
                return Response({"message":True,"data":serial.data})
            except:
                return Response({"message":False,})

    else:
        return Response(status=401
        )


class ScholarshipTypeViewsetReadOnly(viewsets.ReadOnlyModelViewSet):
    # queryset = ScholarshipType.objects.all().order_by('-created_at')
    serializer_class = ScholarshipTypeSerializer
    permission_classes = [AdminAndRolePermission]  
    
    def get_queryset(self):
        # queryset=self.queryset()
        queryset = ScholarshipType.objects.all()
        print("query: ")
        scholarship_id = self.request.query_params.get('id',None)
        if scholarship_id:
            queryset = ScholarshipType.objects.filter(id=scholarship_id).values()

        scholarship_name = self.request.query_params.get('name',None)
        if scholarship_name:
            queryset = ScholarshipType.objects.filter(name__icontains = scholarship_name).values()
        
        scholarship_percentage = self.request.query_params.get('percentage',None)
        print("scholarship: ",scholarship_percentage)
        if scholarship_percentage:
            queryset = ScholarshipType.objects.filter(Q(percentage = scholarship_percentage) | Q(discount_amount = scholarship_percentage )).distinct()

        scholarship_created = self.request.query_params.get('created_at',None)
        if scholarship_created:
            queryset = ScholarshipType.objects.filter(created_at = scholarship_created).values()
        print("kkkkkkkkkkkkkkkkkkkkkkkkk")
        return queryset
    
    def list(self,request,*args,**kwargs):
        print("///////////////////////")
        queryset = self.get_queryset()
        print("self: ")
        excel = queryset_to_excel(queryset,['id','name'])
        # checking if PDF download is requested
        pdf_query = self.request.query_params.get('pdf',None)
        excel_query = self.request.query_params.get('excel',None)

        if excel_query:
            response = queryset_to_excel(queryset,[fields.name for fields in queryset.model._meta.fields],{
                                             'status':{'True':'Yes','False':'No'}
                                         })
            return response
        if pdf_query:
            
            fields = ['name','discount_amount','percentage']
            headers, data = get_queryset_headers_data(queryset, fields = fields)
            print("headers: ",headers)
            modified_headers=[]
            modified_headers=[header.replace('Discount_a\nmount','Discount amount')
                              for header in headers]
            print("modified",modified_headers)
            nameheading = 'Scholarship Types'
            current_datetime =timezone.now()

            pdf_data = {
                'headers' : modified_headers,
                'data' : data,
                'current_datetime' : current_datetime,
                'model' : nameheading
            }
            resp = generate_pdf('commonpdf.html',pdf_data, 'scholarshipType.pdf')
            return resp
        
        # Continue with pagination and serializer for regular list view
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentlistForScholarship(viewsets.ModelViewSet):
    pagination_class = SinglePagination
    serializer_class=StudentProfileSerializer
    queryset = Student.objects.all().order_by('-admission_date')

    def get_queryset(self):
        students_with_scholarship = ScholarshipApproval.objects.values_list('student_id', flat=True)
        # students_with_scholarship = ScholarshipApproval.objects.all()

        queryset = Student.objects.exclude(id__in=students_with_scholarship).order_by('-admission_date')
        # return queryset
    
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        
        id = self.request.query_params.get('id', None)
        if id:
            queryset = queryset.filter(id__icontains=id)
        return queryset
    

class PollFightSubmitViewSet(viewsets.ModelViewSet):
    pagination_class = SinglePagination
    serializer_class = PollFightSubmitSerializer
    queryset = PollFightSubmit.objects.all()


class PollFightQuestionViewset(viewsets.ModelViewSet):
    pagination_class=SinglePagination
    # serializer_class=PollFightQuestionSerializer
    permission_classes=[]
    queryset =PollFightQuestion.objects.all()

    
    def get_serializer_context(self):
        # Get the default context from the parent method
        print("heresss")
        context = super().get_serializer_context()
        if self.action=='retrieve':
            context["paginated"]=self.paginate_queryset
            context["page"]=self.request.query_params.get('pageq',0)
            context["pagesize"]=self.request.query_params.get('pagesizeq',0)
            # page =self.paginate_queryset(queryset)
            # if page is not None:
                # serializer = self.get_serializer(page,many=True)
                # return self.get_paginated_response({"data": serializer.data})
            print("hhhhhhhhh123")
            context["ids"] =  self.request.query_params.get('ids',None)
            # print(self.request.query_params.get('question_text',None),"Views")
            context["question_text"] =  self.request.query_params.get('question_text',None)
        return context

    def get_serializer_class(self):
        if self.action=='retrieve':
            print("hello")
            self.serializer_class=PollFightQuestionRetrieveSerializer
        else:
            self.serializer_class=PollFightQuestionSerializer
        return super().get_serializer_class()
        

    

    def get_queryset(self):
        queryset=PollFightQuestion.objects.all()
        id = self.request.query_params.get('id')
        status = self.request.query_params.get('status')
        points = self.request.query_params.get('points')
        count = self.request.query_params.get('count')
        duration = self.request.query_params.get('duration')
        if id:
            queryset=queryset.filter(id=id)
        if status:
            queryset=queryset.filter(status=status)
        if points:
            queryset=queryset.filter(points__icontains=points)
        if count:
            queryset=queryset.filter(count=count)
        if duration:
            queryset=queryset.filter(duration=duration)
        return queryset
    
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)


class PollFightSubmitUserViewset(viewsets.ModelViewSet):
    serializer_class=PollFightSubmitSerializer
    pagination_class=SinglePagination
    permission_classes=[StudentPermission]
    queryset=PollFightSubmit.objects.all()

    def get_queryset(self):
        return super().get_queryset()
    
    def retrieve(self, request, *args, **kwargs):
        queryset=PollFightSubmit.objects.filter(room=kwargs['pk'])
        room=PollFightLobby.objects.get(id=kwargs['pk'])
        users=[room.user1,room.user2]
        if queryset:
            pass
        else:
            ss=PollFightQuestion.objects.filter(status=True).first()
            print(ss.count,"count",len(ss.question.all()))
            for i in range(0,ss.count):
                submitquestions=PollFightSubmit.objects.filter(room=kwargs['pk']).values_list('question',flat=True)
                print(submitquestions)
                pp=ss.question.all().exclude(id__in=submitquestions).order_by('?').first()
                print(pp,"ppppppppp",i)
                for j in users:
                    qps=PollFightSubmit.objects.create(room=room,question=pp,question_copy=pp.question_text,option_1=pp.option_1,option_2=pp.option_2,option_3=pp.option_3,option_4=pp.option_4,option_5=pp.option_5,crct_answer=pp.answer,index=i,created_by=j)
        
        queryset=PollFightSubmit.objects.filter(room=kwargs['pk'],created_by=AuthHandlerIns.get_id(request=request))
        ser=PollFightSubmitSerializer(queryset,many=True)
        return Response(ser.data)
    

class NewFacultyTimeTable(viewsets.ModelViewSet):
    queryset=TimeTable.objects.all()
    serializer_class=TimeTableNewSerializer
    permission_classes=[FacultyPermission]
    pagination_class=SinglePagination

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Add custom value to the context
        context['request'] = self.request

        return context
    
    def get_queryset(self):
        user=User.objects.get(id=AuthHandlerIns.get_id(request=self.request))
        topics=FacultyCourseAddition.objects.filter(status='approved',user=user).values_list('topic',flat=True)
        topics=Topic_batch.objects.filter(topic__topic__id__in=topics)
        queryset=TimeTable.objects.filter(topic__in=topics)
        app = Approvals.objects.filter(faculty__id=user.id).values('timetable')
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
        available = self.request.query_params.get('available')
        if available:
            queryset = TimeTable.objects.filter(topic__in=topics,faculty__isnull=True).order_by('date').exclude(date__lte=datetime.date.today()).exclude(id__in=app).exclude(branch__id__in=bid)
        applied = self.request.query_params.get('applied')
        if applied:
            time=queryset.values_list('id',flat=True)
            # aprovals=Approvals.objects.filter(faculty=user, timetable__in=time).values_list('timetable',flat=True)
            queryset = TimeTable.objects.filter(id__in=app).order_by('date').exclude(date__lte=datetime.date.today()).exclude(faculty__id=user.id)
        
        booked = self.request.query_params.get('booked')
        if booked:
            queryset = TimeTable.objects.filter(faculty=user.id).order_by('date').exclude(date__lte=timezone.now().date() - timedelta(days=1))
        completed = self.request.query_params.get('completed')
        if completed:
            queryset = TimeTable.objects.filter(topic__status="F",faculty__id=AuthHandlerIns.get_id(request=self.request)).order_by('-date')
        else:
            queryset=queryset.exclude(faculty=user,topic__status='F')
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
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        if year and month:
            queryset=queryset.filter(date__year=year,date__month=month)
        return queryset.order_by('-date')


class GroupsViewsSet(viewsets.ModelViewSet):
    permission_classes=[AdminAndRolePermission]
    pagination_class=SinglePagination
    queryset=Groups.objects.all().order_by('-created_at')
    serializer_class=GroupSerializer

    def create(self, request, *args, **kwargs):
        # Extract the image data from the "data:image/png;base64,..." format
        icon_data = request.data.get('icon', None)
        if icon_data:
            _, image_data = icon_data.split(';base64,')
            
            # Decode the base64 data and create a ContentFile
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')

            request.data['icon'] = content_file

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
    # Extract the image data from the "data:image/png;base64,..." format
        icon_data = request.data.get('icon', None)
        if icon_data:
            _, image_data = icon_data.split(';base64,')
            
            # Decode the base64 data and create a ContentFile
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')

            request.data['icon'] = content_file

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     body={}
    #     try:
    #         body['admins']=json.loads(request.data.get('admins',[])) 
    #         body['members']=json.loads(request.data.get('members',[])) 
    #         print(body['admins'],'llll',body['members'])
    #         body['name'] = request.data.get('name',None)
    #         body['description'] = request.data.get('description',None)
    #         body['icon'] = request.FILES.get('icon',None)
    #         body['created_by'] = request.data.get('created_by',None)
    #         body['is_open'] = request.data.get('is_open',None)
    #         body['is_admin_only'] = request.data.get('is_admin_only',None)
    #     except Exception as e:
    #         print(e)
    #     serializer=GroupSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()

    #     return Response(serializer.data,status=status.HTTP_201_CREATED)

class GroupsUserViewsSet(viewsets.ModelViewSet):
    permission_classes=[StudentPermission]
    pagination_class=SinglePagination
    serializer_class=GroupUserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Add custom value to the context
        context['request'] = self.request

        return context

    def get_queryset(self):
        queryset=Groups.objects.filter(members__id=AuthHandlerIns.get_id(request=self.request))
        return queryset
    
    def create(self, request, *args, **kwargs):
        data=request.data
        data['members']=[AuthHandlerIns.get_id(request=request)]
        data['admins']=[AuthHandlerIns.get_id(request=request)]
        data['created_by']=AuthHandlerIns.get_id(request=request)
        ser=GroupSerializer(data=data)
        queryset=Groups.objects.filter(created_by__id=AuthHandlerIns.get_id(request=request))
        if queryset.count()>=5:
            return Response({"message":"CAnt Create More Group You Reached Your Limit"},status=status.HTTP_406_NOT_ACCEPTABLE)

        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
    

class ChatViewset(viewsets.ModelViewSet):
    queryset=GroupChat.objects.prefetch_related('mcq','post')
    serializer_class=GroupChatSerializer
    pagination_class=SinglePagination
    permission_classes=[StudentPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Add your custom context data based on the viewset action
        context['user'] = AuthHandlerIns.get_id(request=self.request)
          

        return context

    def create(self, request, *args, **kwargs):
        user_id=AuthHandlerIns.get_id(request=self.request)
        ser= GroupChatSerializer(data=request.data,context={'user':user_id})
        ser.is_valid()
        print(ser.data['post']['images'])
        
        final=[]
        for i in ser.data['post']['images']:
            _, image_data = i['image'].split(';base64,')
                    
            # Decode the base64 data and create a ContentFile
            decoded_image = base64.b64decode(image_data)
            content_file = ContentFile(decoded_image, name='icon.png')
            final.append({'image':content_file})
        print(final)
        image_serializer=ImageSerializerChat(data=final,many=True)
        image_serializer.is_valid()
        post_data=ser.data['post']
        post_data['images']=final
        print(post_data)
        post_serializer = PostsSerializer(data=ser.data['post'])
        post_serializer.is_valid()

        print(";;;;;;;;")
        # Deserialize and validate the mcq data
        mcq_serializer = GroupMCQSerializer(data=ser.data['mcq'])
        mcq_serializer.is_valid()
        if not post_serializer.is_valid() and not mcq_serializer.is_valid():
            mcq_serializer.is_valid(raise_exception=True), post_serializer.is_valid(raise_exception=True)
            
            

        # Deserialize and validate the group chat data
        

        # Create the post, mcq, and group chat objects in a single transaction
        with transaction.atomic():
            post = post_serializer.save() if post_serializer.is_valid() else None
            mcq = mcq_serializer.save() if mcq_serializer.is_valid() else None
            data=ser.data
            if post:
                image_serializer.is_valid(raise_exception=True)

                data['post']=post
            if mcq:
                data['mcq']=mcq
            data.mcq= mcq if mcq else None
            data.post=post if post else None
            group_chat_serializer = GroupChatSerializer1(data=data)
            group_chat_serializer.is_valid(raise_exception=True)
            group_chat = group_chat_serializer.save(mcq=mcq,post=post)
        
            # Associate the created mcq and group chat with the post
            group_chat.mcq = mcq if mcq else None
            group_chat.post = post if post else None
            group_chat.save()
        ser=GroupChatSerializer(group_chat,many=False,context={'user':user_id})
        return Response(ser.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        queryset=GroupChat.objects.filter(group=kwargs['pk'])
        print(queryset)
        page = self.paginate_queryset(queryset)    
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        serializer=GroupChatSerializer(queryset,many=True)
        return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)
    


@api_view(['GET'])
def get_lobby_user(request):
    queryset=PollFightLobby.objects.filter(status=True).values_list('user1')
    user=User.objects.filter(id__in=queryset)
    print(user)
    ser=UserSerializerLobbyList(user,many=True)
    return Response(ser.data)


class GroupWiseUserList(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    permission_classes=[AdminAndRolePermission]
    serializer_class=UserSerializerGroupList
    pagination_class= SinglePagination

    def get_queryset(self):
        queryset=User.objects.all()
        group=self.request.query_params.get('group', None)
        if group:
            g=get_object_or_404(Groups,id=group)
            queryset=queryset.filter(id__in=g.members.all().values_list('id',flat=True))

        return queryset
        return super().get_queryset()

class StudentFeeCollectionViewSet(viewsets.ModelViewSet):
    queryset = StudentFeeCollection.objects.all()
    # permission_classes=[AdminAndRolePermission]
    serializer_class=StudentFeeCollectionSerializer
    pagination_class= SinglePagination

    def create(self, request, *args, **kwargs):
        batch_id = self.request.query_params.get('batch_id', None)
        user_id = self.request.query_params.get('user_id', None)
        batch_package_id = self.request.query_params.get('batch_package', None)
        try:
            batch = Batch.objects.filter(id=batch_id).values('fees', 'installment_count').first()
            if batch:
                fees = batch['fees']
                installment_count = batch['installment_count']
        except Batch.DoesNotExist:
            pass
        student_fee_count = StudentFeeCollection.objects.filter(student=user_id, batch_package=batch_package_id).count()
        fee_collection_detail = StudentFeeCollection.objects.filter(student=user_id, batch_package=batch_package_id).first()
        print(fee_collection_detail.amountpaid)
        if fee_collection_detail.amountpaid == fees:
            return Response({'Message': 'Student has paid the fees Completly'})

        # student = Student.objects.get(id=request.data['student'])
        # batch_package = BatchPackages.objects.get(id=request.data['batch_package'])
        # amountpaid = request.data['amountpaid'] 
        # pub = json.loads(request.data['publication'])
        # studymat = json.loads(request.data['study_materials'])
        # qb = json.loads(request.data['question_bank'])   
        # 
        #      
class StudentFeeAfterAdmission(viewsets.ModelViewSet):
    queryset = StudentFeeCollection.objects.all()
    # permission_classes=[AdminAndRolePermission]
    serializer_class=StudentFeeAfterAdmissionSerializer
    pagination_class= SinglePagination

    def create(self, request, *args, **kwargs):
        try:

            batch_id = request.data['batch_id']
            user_id = request.data['student']
            batchpackage = request.data['batch_package']
            publication = request.data['publications']
            study = request.data['study_materials']
            question = request.data['question_banks']
        except:
            pass

        queryset = self.queryset.filter(student__id = user_id,batch_package__id = batchpackage)
        total_fee_paid = queryset.aggregate(total = Sum('amountpaid'))

        # getting syllabus based  and given books
        books_theyWant = BatchPackages.objects.get(id=batchpackage).publications.all().values_list('id',flat=True)
        books_given = queryset.values_list('publications',flat=True).distinct()
        
        # getting syllabus based study materials and given study materials
        material_theyWant = BatchPackages.objects.get(id=batchpackage).study_meterial.all().values_list('id',flat=True)
        materials_given = queryset.values_list('study_materials',flat=True).distinct()

        # getting question banks they want and already given
        qn_theyWant = BatchPackages.objects.get(id=batchpackage).question_book.all().values_list('id',flat=True)
        qn_given = queryset.values_list('question_banks',flat=True).distinct()

        

        install = Batch.objects.get(id=batch_id).installment_count
        install_counts = self.queryset.filter(student__id = user_id,batch_package__id = batchpackage).count()

        print("install",install_counts) 
        print("lololololololoolo",all(book in publication for book in books_theyWant) )
        print("p0p0p0p0",queryset.filter(publications__in = publication).exists())

        if books_theyWant == books_given:
            return Response({'Message':'all books were given'},status=500)
        
        elif  (not all(book in publication for book in books_theyWant) or queryset.filter(publications__in = publication).exists()) and not publication == [] :
            return Response({'Message':'Invalid book'},status=500)
        
        elif  material_theyWant == materials_given:
            return Response({'Message':'Materials are already given '},status=500)
        
        elif  (not all(material in study for material in material_theyWant) or queryset.filter(study_materials__in = study).exists()) and not study == []:
            return Response({'Message':'Invalid material'},status=500)
        
        elif  qn_theyWant == qn_given:
            return Response({'Message':'Question bank already given'},status=500)
        
        elif (not  all(qn in question for qn in qn_theyWant) or queryset.filter(question_banks__in = question).exists()) and not question == []:
            return Response({'Message':'Invalid question Bank'},status=500)
        
        
        else:
            try:
                batch_package =BatchPackages.objects.filter(id=batchpackage).annotate(
                        total_study_material_price=Sum(F('study_meterial__book_price'), output_field=DecimalField()),
                        total_question_book_price=Sum(F('question_book__book_price'), output_field=DecimalField()),
                        total_publications_price=Sum(F('publications__book_price'), output_field=DecimalField())
                    ).annotate(grand_total=F('total_study_material_price')+F('total_question_book_price')+F('total_publications_price'))
                
                grand_total = batch_package.first().grand_total


                fees = Batch.objects.get(id=batch_id).fees

                max_amount=grand_total - (total_fee_paid['total'] if total_fee_paid['total'] else 0)
                min_amount =0
                paying_amount=int(request.data['amountpaid'])

                if install_counts + 1 == install and paying_amount != max_amount and paying_amount != 0:
                    return Response({'Message':f'You should pay {max_amount}'})

                elif paying_amount > max_amount:
                    return Response({'Message':'Amount is higher than  due amount'})
                elif paying_amount < min_amount:
                    return Response({'Message':'Amount is lower  than  minimum amount'})
                
                elif total_fee_paid['total'] == fees:
                    return Response({'Message':'Fee already paid'})

                else:
                    serializer = StudentFeeAfterAdmissionSerializer(data=request.data)
                    if serializer.is_valid(raise_exception = True):
                        serializer.save()
                  
                    return Response({'status':serializer.data})
            except Exception as e:
                print(e,"   000000")

        return Response(status=201)

    def retrieve(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('student')
        batchpackage = self.request.query_params.get('batch_package')

       
        serialzer =StudentBatchSerializer(StudentBatch.objects.get(batch =BatchPackages.objects.get(id = batchpackage).batch),many=False)
        print(serialzer.data)
        return Response(serialzer.data)

class StudentSyllabusViewSet(viewsets.ModelViewSet):
    
    queryset = StudentBatch.objects.all()
    pagination_class= SinglePagination
    serializer_class = StudentSyllabusSerializer
    permission_class = [AdminAndRolePermission]


import datetime
@api_view(['GET'])
def get_faculty_dashboard(request):
    if AuthHandlerIns.is_faculty(request=request):
        # queryset=Faculty.objects.get(user_id=AuthHandlerIns.get_id(request=request))
        print(datetime.date.today())
        queryset=TimeTable.objects.filter(faculty_id=AuthHandlerIns.get_id(request=request)).exclude(date__lt=datetime.date.today()).order_by('-date')
        if queryset.exists():
            queryset=queryset.first()
        else:
            queryset=TimeTable.objects.filter(faculty_id=AuthHandlerIns.get_id(request=request)).exclude(date__gt=datetime.date.today()).order_by('date')
            queryset=queryset.first()
        

        ser=FacultyTimetableAppDashboardSerializer(queryset,many=False)
        return Response(ser.data)
    else:
        raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})


class FacultyFeedBackOnTimeTableViewSet(viewsets.ModelViewSet):
    queryset = FacultyFeedback.objects.all()
    permission_classes=[FacultyPermission]
    serializer_class=FacultyFeedbackSerializer
    pagination_class= SinglePagination



class StudentAttendanceViewset(viewsets.ModelViewSet):
    queryset=StudentAttendance.objects.all()
    serializer_class=StudentAttendanceSerializer
    pagination_class=SinglePagination
    permission_classes= [AdminAndRolePermission]

class StudentAttendanceViewsetUser(viewsets.ModelViewSet):
    queryset=StudentAttendance.objects.all()
    serializer_class=StudentAttendanceSerializer
    pagination_class=SinglePagination
    permission_classes= [StudentPermission]

 
    def get_queryset(self):
        studentattendance= StudentAttendance.objects.filter(student__id=AuthHandlerIns.get_id(request=self.request))

        return super().get_queryset()
    def list(self, request, *args, **kwargs):
        graph = self.request.query_params.get('graph', None)
        if graph:
            user_id=AuthHandlerIns.get_id(request=request)
            batchs_id=StudentBatch.objects.filter(student__user__id=user_id).values_list('batch__id',flat=True)
            batch=Batch.objects.filter(id__in=batchs_id)
            serializer=StudentAttendanceGraphSerializer(batch,many=True,context={'user_id':user_id})
            return Response({"data":serializer.data})

        return super().list(request, *args, **kwargs)
    


    def create(self, request, *args, **kwargs):
        try:
            token=request.data['token']
            token=attendanceIns.decode_token(token=token)
            id=token['id']
            branch=Branch.objects.get(id=id)
            student=User.objects.get(id=AuthHandlerIns.get_id(request=request))
            batch=StudentBatch.objects.filter(student__user=student).values_list('batch',flat=True)
            timetable=TimeTable.objects.get(branch=branch,date=datetime.date.today(),batch__in=batch)
            attendance=StudentAttendance.objects.create(student=student,timetable=timetable)
            ser=StudentAttendanceSerializer(attendance,many=False)
            return Response({"data":ser.data},status=status.HTTP_201_CREATED)
            return super().create(request, *args, **kwargs)
        except:
            return Response({"error":"invalid"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class QuestionPaperAttend(viewsets.ModelViewSet):
    serializer_class=QuestionpaperattendSerializer
    queryset=QuestionpaperAttend.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = AuthHandlerIns.get_id(request=request)
        data = request.data.copy()
        data['student'] = user_id
        serializer = QuestionpaperattendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "completed", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        return Response({"message": "PATCH method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "DELETE method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@api_view(['GET'])
def poll_fight_submit(request,id):
    if AuthHandlerIns.is_student(request=request):
        ins=PollFightLobby.objects.get(id=id)
        qins=PollFightSubmit.objects.filter(room=ins.id)
        if ins.user1:
            userqins1=qins.filter(created_by=ins.user1)##all the questions of user1
            user1crct=userqins1.filter(answer=F('crct_answer'))
        if ins.user2:
            userqins2=qins.filter(created_by=ins.user2)##all the questions of user2
            user2crct=userqins2.filter(answer=F('crct_answer'))
        if ins.user1 and ins.user2:
            if user1crct.count() > user2crct.count():
                ins.winner=ins.user1
            elif user1crct.count() < user2crct.count():
                ins.winner=ins.user2
            ins.save()
        ser=PollFightLobbySerializer(ins,many=False)
        return Response(ser.data)
    else:
        raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
    
# @api_view(['GET'])



class StudentPublicationUpdateViewSet(viewsets.ModelViewSet):
    queryset = StudentFeeCollection.objects.all()
    serializer_class = StudentFeeUpdationSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            study_materials = serializer.validated_data.get('study_materials', [])
            publications = serializer.validated_data.get('publications', [])
            question_banks = serializer.validated_data.get('question_banks', [])

            for material_id in study_materials:
                instance.study_materials.add(material_id)

            for publication_id in publications:
                instance.publications.add(publication_id)

            for question_bank_id in question_banks:
                instance.question_banks.add(question_bank_id)

            instance.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartPurchaseQuiz(viewsets.ModelViewSet):
    serializer_class=StartPurchaseQuizSerializer
    queryset=PackageQuizPoolUserRoom.objects.all()

    def create(self, request, *args, **kwargs):
        videopackage = self.request.query_params.get('videopackage_id', None)
        exampaperpackage = self.request.query_params.get('exampackage_id', None)
        studentid = AuthHandlerIns.get_id(request=self.request)
        if studentid:
            if 'question_paper' in request.data:
                question_paper = request.data['question_paper']
                counts = QuestionPaper.objects.filter(id=question_paper).values('questions').count()
                co = QuestionPaper.objects.filter(id=question_paper).values('questions')
                print(co,'co')
                print(counts,'ddd')
                print(counts,'PPPP')
                count = counts if counts else 0
                print(count,'oooo')

                if studentid and exampaperpackage:
                        data = {
                            'question_paper': question_paper,
                            'user': studentid,
                            'count': count,
                            'start_time': timezone.now(),
                            'Exampaper_package': exampaperpackage,
                        }
                elif studentid and videopackage:
                     data = {
                            'question_paper': question_paper,
                            'user': studentid,
                            'count': count,
                            'start_time': timezone.now(),
                            'video_package': videopackage,
                        }
                else:
                   
                    return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = StartPurchaseQuizSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "completed", "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseQuizInstructions(viewsets.ModelViewSet):
    serilaizer_class=PurchaseQuizInstructionSerializer
    queryset=QuestionPaper.objects.all()


class QuestionGetinQuiz(viewsets.ReadOnlyModelViewSet):
    serializer_class=QuestionGetQuizSerializer
    queryset=PackageQuizPoolAnswers.objects.all()

    def retrieve(self, request, *args, **kwargs):
        id=AuthHandlerIns.get_id(request=self.request)
        if id:
            # if AuthHandlerIns.is_student(request=self.request):
            #     pass
            roomid=self.kwargs['pk']
            questionid=self.request.query_params.get('questionid')        
            if questionid is not None:
                querysets = self.queryset.filter(id=questionid, room=roomid)
                serializer = self.get_serializer(querysets, many=True)
                return Response(serializer.data, status=200)
        else:
            return Response("ddd")
        return super().retrieve(request, *args, **kwargs)
        
    def list(self, request, *args, **kwargs):
        id=self.request.query_params.get('id')
        if id:
            querysets=self.queryset.filter(room=id)
            serializers=self.get_serializer(querysets,many=True)
            return Response(serializers.data)
        else:
            return Response({"error":"id missing"},status=400)

    def partial_update(self, request, *args, **kwargs):
        id=AuthHandlerIns.get_id(request=self.request)
        if id:
            # if AuthHandlerIns.is_student(request=self.request):
            #     pass
            roomid=self.kwargs['pk']
            questionid=self.request.query_params.get('questionid') 
            answer=request.data['answer']
            instance=PackageQuizPoolAnswers.objects.get(id=questionid,room=roomid)
            instance.answer=answer
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Missing or invalid 'answer' field in request data."}, status=status.HTTP_400_BAD_REQUEST)
        
class PurchaseQuizComplete(viewsets.ReadOnlyModelViewSet):
    serializer_class=PurchaseQuizCompleteSerializer
    queryset=PackageQuizPoolUserRoom.objects.all()

    def list(self, request, *args, **kwargs):
        userid=AuthHandlerIns.get_id(request=self.request)
        userroomid=self.kwargs['pk']
        print(userroomid,'userro')
        if id and userroomid:
            queryset=PackageQuizPoolUserRoom.objects.filter(id=userroomid,user=userid)
            if queryset:
                serializer=self.get_serializer(queryset,many=True)
                return Response(serializer.data,status=200)
            else:
                return Response({"message":serializer.error},status=400)
        return Response({"message":"id miss match"},status=400)
            

class PurchaseQuizInstructions(viewsets.ReadOnlyModelViewSet):
    serializer_class=QuizInstructionSerilaizer

    def get_queryset(self):
        id = self.request.query_params.get('questionpaperid')
        instructions = QuestionPaper.objects.filter(id=id)
        return instructions

class AnswerKeysPurchaseQuiz(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnswerKeySerializer  
    pagination_class = SinglePagination  

    def list(self, request, *args, **kwargs):
        id = AuthHandlerIns.get_id(request=self.request)
        room = self.request.query_params.get('roomid')
        if id and room:
            questionroom = PackageQuizPoolAnswers.objects.filter(room=room)
            # Paginate the queryset
            page = self.paginate_queryset(questionroom)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(questionroom, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
class NoticeBoardAdminViewset(viewsets.ModelViewSet):
    queryset = NoticeBoard.objects.all()
    pagination_class = SinglePagination
    permission_class = [AdminAndRolePermission]
    serializer_class = NoticeBoardSerailizer

    def get_queryset(self):

        queryset = self.queryset

        date = self.request.query_params.get('date',None)
        content = self.request.query_params.get('content',None)
        branch = self.request.query_params.get('branch_name',None)
        batch = self.request.query_params.get('batch_name',None)

        if date:
            queryset = queryset.filter(date__in = date)
        
        if content:
            queryset = queryset.filter(content__icontains = content)

        if branch:
            queryset = queryset.filter(branch__name__icontains = branch)

        if batch:
            queryset = queryset.filter(batch__name__icontains = batch)

        return queryset



class NoticeBoardUserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = NoticeBoard.objects.all()
    pagination_class = SinglePagination
    permission_class = [StudentPermission]
    serializer_class = NoticeBoardUserSerailizer

    # def get_queryset(self):
    #     student = Student.objects.get(user=AuthHandlerIns.get_id(request=self.request))
    #     student_batch = StudentBatch.objects.filter(student = student)
    #     queryset = self.queryset.filter(Q(batch__id__in = student_batch.values_list('batch')) | 
    #                                     Q(branch__id__in = student_batch.values_list('batch__branch')) | 
    #                                     Q(branch__isnull=True) |
    #                                     Q(batch__isnull = True))


    #     return queryset
    
    def get_queryset(self):
        student = Student.objects.get(user=AuthHandlerIns.get_id(request=self.request))
        student_batch = StudentBatch.objects.filter(student = student)
        queryset = self.queryset.filter(Q(batch__id__in = student_batch.values_list('batch')) | 
                                        Q(branch__id__in = student_batch.values_list('batch__branch')) | 
                                        Q(branch__isnull=True) |
                                        Q(batch__isnull = True))



        date = self.request.query_params.get('date',None)
        content = self.request.query_params.get('content',None)
        branch = self.request.query_params.get('branch_name',None)
        batch = self.request.query_params.get('batch_name',None)

        if date:
            queryset = queryset.filter(date__in = date)
        
        if content:
            queryset = queryset.filter(content__icontains = content)

        if branch:
            queryset = queryset.filter(branch__name__icontains = branch)

        if batch:
            queryset = queryset.filter(batch__name__icontains = batch)

        return queryset

        


class VideoClassesBatchViewset(viewsets.ModelViewSet):
    queryset = VideoClassesBatch.objects.all()
    pagination_class = SinglePagination
    permission_class = [AdminAndRolePermission]
    serializer_class = VideoClassesBatchSerializer

    def get_queryset(self):
        queryset = self.queryset
        video = self.request.query_params.get('video_name',None)
        batch = self.request.query_params.get('batch_name',None)
        subtopic = self.request.query_params.get('subtopic_name',None)
        topic = self.request.query_params.get('topic_name',None)
        module = self.request.query_params.get('module_name',None)
        subject = self.request.query_params.get('subject_name',None)

        if video:
            queryset = queryset.filter(video__name__icontains = video)

        if batch:
            queryset = queryset.filter(batch__name__icontains = batch)
        
        if subtopic:
            queryset = queryset.filter(subtopic__name__icontains = subtopic)
        
        if topic :
            queryset = queryset.filter(topic__name__icontains = topic)

        if module:
            queryset = queryset.filter(module__name__icontains = module)

        if subject:
            queryset = queryset.filter(subject__name__icontains = subject)
        
        return queryset





class VideoClassesBatchUserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = VideoClassesBatch.objects.all()
    pagination_class = SinglePagination
    permission_class = [StudentPermission]
    serializer_class = VideoClassesBatchUserSerializer

    def get_queryset(self):
        student = Student.objects.get(user=AuthHandlerIns.get_id(request=self.request))
        print(" studentttttttttttttttt  ",student)
        student_batch = StudentBatch.objects.filter(student = student)
        queryset = self.queryset.filter(batch__in = student_batch.values_list('batch'))
      
        video = self.request.query_params.get('video_name',None)
        batch = self.request.query_params.get('batch_name',None)
        subtopic = self.request.query_params.get('subtopic_name',None)
        topic = self.request.query_params.get('topic_name',None)
        module = self.request.query_params.get('module_name',None)
        subject = self.request.query_params.get('subject_name',None)

        if video:
            queryset = queryset.filter(video__name__icontains = video)

        if batch:
            queryset = queryset.filter(batch__name__icontains = batch)
        
        if subtopic:
            queryset = queryset.filter(subtopic__name__icontains = subtopic)
        
        if topic :
            queryset = queryset.filter(topic__name__icontains = topic)

        if module:
            queryset = queryset.filter(module__name__icontains = module)

        if subject:
            queryset = queryset.filter(subject__name__icontains = subject)
        
        return queryset






class StudnetDetaiApplView(viewsets.ReadOnlyModelViewSet):

    queryset = StudentFeeCollection.objects.all()
    permission_class = [StudentPermission]
    serializer_class = StudentFeeAppSerializer

    def list(self,request,*args,**kwargs):
        # if AuthHandlerIns.is_student(request=request):
            student=User.objects.get(id=AuthHandlerIns.get_id(request=request))
            print("    id     ",student)
            if student:
                batch = StudentBatch.objects.filter(student__user=student)
                print(' batchhhhhhh            ',batch)
                serializer = StudentFeeAppSerializer(batch,many=True)
                return Response(serializer.data)
            else:
                return 
            
            return Response()

class StudentTransactionAppView(viewsets.ReadOnlyModelViewSet):
    queryset = StudentFeeCollection.objects.all()
    permission_class = [StudentPermission]
    serializer_class = StudentFeeAppSerializer

    def list(self,request,*args,**kwargs):

        student=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        print("    id     ",student.pk)
        if student:
            print("       /////////            ",StudentFeeCollection.objects.filter(student=student))
            serializer = StudentTransactionSerializer(StudentFeeCollection.objects.filter(student=student),many=True)

            return Response(serializer.data)
        return Response()


class liveZoomclassViewset(viewsets.ModelViewSet):
    queryset = ZoomMeetings.objects.all()
    permission_class = [AdminAndRolePermission]
    serializer_class = livezoomSerializer
    pagination_class=SinglePagination

class liveZoomAppViewset(viewsets.ModelViewSet):
    queryset = ZoomMeetings.objects.all()
    permission_class = [AdminAndRolePermission]
    serializer_class = livezoomAppSerializer
    pagination_class=SinglePagination

    def get_queryset(self):
        queryset = self.queryset
        # today = datetime.date.today()
        queryset = queryset.all().exclude(start_time__lte=datetime.date.today())
        return queryset





from decimal import Decimal  # Import Decimal if you haven't already
from django.db.models import Max, F, Window
from django.db.models.functions import Rank
class LeaderBoardApi(viewsets.ReadOnlyModelViewSet):
    serializer_class=LeaderBoardSerializer
    pagination_class=SinglePagination

    def list(self, request, *args, **kwargs):
        videopackageid = self.request.query_params.get('videopakcageid')
        exampackageid = self.request.query_params.get('exampakcageid')
        # roomid=self.request.query_params.get('roomid')
        
        if videopackageid:
            quiz = PackageQuizPoolUserRoom.objects.filter(
                video_package=videopackageid,
                total_score__isnull=False, total_score__gt=0,
            ).order_by('-total_score')[:10]
            user_id = AuthHandlerIns.get_id(request=self.request)
            user_data = PackageQuizPoolUserRoom.objects.filter(
                user__id=user_id,
                video_package=videopackageid,
                total_score__isnull=False  # Exclude records with no total_score
            ).first()

            # Calculate rank for the user
            if user_data:
                window = Window(expression=Rank(), order_by=F('total_score').desc())
                user_rank = PackageQuizPoolUserRoom.objects.filter(
                    video_package=videopackageid,
                    total_score__gt=user_data.total_score
                ).annotate(rank=window).count() + 1  # +1 because ranks start from 1
            else:
                user_rank = None
            myrank = PackageQuizPoolUserRoom.objects.filter(
                user__id=AuthHandlerIns.get_id(request=self.request),
                video_package=videopackageid,
                total_score__isnull=False
            ).order_by('-total_score')[:1]

            # Serialize the data with the updated LeaderBoardSerializer
            serializer = LeaderBoardSerializer(quiz, many=True, context={'id': user_id})
            data = LeaderBoardSerializerUser(myrank,many=True)

            return Response({"data": serializer.data,"mymarks": data.data, "myrank": user_rank}, status=200)
        elif exampackageid:
            id=AuthHandlerIns.get_id(request=self.request)
            quiz = PackageQuizPoolUserRoom.objects.filter(
                Exampaper_package=exampackageid,
                total_score__isnull=False, total_score__gt=0,
            ).order_by('-total_score')[:10]

            # Retrieve user's data and calculate rank for the user
            user_id = AuthHandlerIns.get_id(request=self.request)
            user_data = PackageQuizPoolUserRoom.objects.filter(
                user__id=user_id,
                Exampaper_package=exampackageid,
                total_score__isnull=False  # Exclude records with no total_score
            ).first()

            # Calculate rank for the user
            if user_data:
                window = Window(expression=Rank(), order_by=F('total_score').desc())
                user_rank = PackageQuizPoolUserRoom.objects.filter(
                    Exampaper_package=exampackageid,
                    total_score__gt=user_data.total_score
                ).annotate(rank=window).count() + 1  # +1 because ranks start from 1
            else:
                user_rank = None
            LeaderBoardSerializerUser
            myrank = PackageQuizPoolUserRoom.objects.filter(
                user__id=AuthHandlerIns.get_id(request=self.request),
                Exampaper_package=exampackageid,
                total_score__isnull=False
            ).order_by('-total_score')[:1]

            # Serialize the data with the updated LeaderBoardSerializer
            serializer = LeaderBoardSerializer(quiz, many=True, context={'id': user_id})
            data = LeaderBoardSerializerUser(myrank,many=True)

            return Response({"data": serializer.data,"mymarks": data.data, "myrank": user_rank}, status=200)
        else:
            return Response([], status=200)  
        


        


        


class CoursePackage(viewsets.ModelViewSet):
    serializer_class=CoursePackageSerializer
    queryset=OnlineCoursePackage.objects.all()
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Use the CoursePackageSerializerPost for POST requests
            return CoursePackageSerializerPost
        else:
            # Use the CoursePackageSerializer for all other requests (GET, PUT, etc.)
            return CoursePackageSerializer




    # def create(self, request, *args, **kwargs):
        

    #     return super().create(request, *args, **kwargs)

class VideoReportViewset(viewsets.ModelViewSet):
    queryset = ReportFlag.objects.all()
    permission_class = [AdminAndRolePermission]
    pagination_class = SinglePagination
    serializer_class = VideoReportSerializer


class VideoReportUserViewset(viewsets.ModelViewSet):
    queryset = ReportFlag.objects.all()
    permission_class = [StudentFacultyPermission]
    pagination_class = SinglePagination
    serializer_class = VideoReportUserSerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class LibraryFineViewSet(viewsets.ViewSet):
    serializer_class = LibraryFineSerializer
    permission_classes = [AdminAndRolePermission]

    def list(self, request):
        
        library_fine = LibraryFine.objects.first()
        
        if library_fine:
            serializer = self.serializer_class(library_fine)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        library_fine = get_object_or_404(LibraryFine, pk=pk)
        serializer = self.serializer_class(library_fine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseCoursepackage(viewsets.ModelViewSet):
    serializer_class=PurchaseCoursepackageSerializer
    queryset=OnlineCoursePackage.objects.all().order_by('-created_at')
    pagination_class=SinglePagination
    http_method_names=['patch']

    def partial_update(self, request, *args, **kwargs):
        print('partial update')
        print('hellooooooooooooo1')
        obj=self.get_object()
        print('hellooooooooooooo2',)

        raz = razorpay_client.order.create(data={'amount':int(obj.strike_prize*100), 'currency':'INR'})
        print(raz,'razzz')
        current_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(current_time, "%Y%m%d%H%M%S")
        #current_time = datetime.now()  # Get the current datetime
        # timestamp = current_time.strftime("%Y%m%d%H%M%S") 
        random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))
        order_id = f"{timestamp}-{random_string}"
        user=User.objects.get(id=AuthHandlerIns.get_id(request=request))
        pay=OnlineOrderPayment.objects.create(user=user,user_ref=user.id,order_number=order_id,product='subscription',product_id=obj.id,razor_id=raz['id'],total_amount=obj.strike_prize,paid_amount=raz['amount_paid']/100,off_amount=0,offer_choice='none',payment_status='pending',delivery_status='pending')

        return Response(raz)


class DayWiseOnlineCourse(viewsets.ModelViewSet):
    serializer_class=DayWiseOnlineCourseSerializer
    queryset=OnlineCourseOrder.objects.all().order_by('day')
    pagination_class=SinglePagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Use the CoursePackageSerializerPost for POST requests
            return DayWiseOnlineCourseSerializerPost
        else:
            # Use the CoursePackageSerializer for all other requests (GET, PUT, etc.)
            return DayWiseOnlineCourseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        userid = AuthHandlerIns.get_id(request=self.request)
        data['created_by'] = userid
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"error": serializer.errors}, status=403)
        
        # return super().create(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        coursepakageid=self.request.query_params.get('coursepacakgeid','')
        if coursepakageid:
            queryset=OnlineCourseOrder.objects.filter(onlinecourse=coursepakageid)
            serializer=self.get_serializer(queryset,many=True)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data,status=200)
        return super().list(request, *args, **kwargs)

class ExamCategoryViewset(viewsets.ModelViewSet):
    serializer_class=ExamCategorySerializer
    queryset=ExamCategory.objects.all()
    pagination_class=SinglePagination
    permission_classes = [AdminAndRolePermission]

class ExamQuestionPaperViewset(viewsets.ModelViewSet):
    serializer_class=ExamQuestionPaperSerializer
    queryset=ExamQuestionPaper.objects.all()
    pagination_class=SinglePagination
    permission_classes=[AdminAndRolePermission]

class OfflineExamlist(viewsets.ReadOnlyModelViewSet):
    serializer_class=OfflineExamSerializer
    queryset=ExamQuestionPaper.objects.filter(status=True).order_by('-created_at')



    
class UpVotesViewset(viewsets.ModelViewSet):
    serializer_class=UpVotesSerializerUser
    queryset=UpVotes.objects.all()
    permission_classes=[]
    pagination_class=SinglePagination

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SubjectBatchViewset(viewsets.ModelViewSet):
    serializer_class= SubjectBatchSerializer
    queryset=Subject_batch.objects.all()
    permission_classes=[StudentPermission]

    def get_queryset(self):
        batch=self.request.query_params.get('batch',None)
        queryset=self.queryset
        queryset=queryset.filter(batch=batch)
        return queryset

    