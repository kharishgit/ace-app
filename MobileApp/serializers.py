import asyncio
import base64
import requests
from rest_framework import serializers
from accounts.api.serializers import AddVediotoStudioCourseSerializer, CommonVideoSerializer, ConvertedMaterialSerializer, QustionpoolNew, staffserializerSmall
from accounts.api.authhandle import AuthHandlerIns
from course.serializers import Approvalserializers, CourseSerializer, Subtopic_batchSerializer

from student.serializers import MaterialClassDetailSerializer, PublicationClassDetailSerializer, PublicationSerializer, PublicationsViewSerializer, QuestionBookClassDetailSerializer, QuestionBookViewSerializer, StudyMaterialViewSerializer
from .models import *
from django.core.files.base import ContentFile
from django.db.models import Max
from datetime import datetime
from django.utils import timezone




class QuizPoolViewsetSerializer(serializers.ModelSerializer):
    level_name= serializers.SerializerMethodField()
    class Meta:
        model=QuizPool
        fields="__all__"

    def get_level_name(self, obj):
        return obj.level.name
    
class DailyNewsSerializer(serializers.ModelSerializer):
    # course_det= serializers.SerializerMethodField()

    class Meta:
        model = DailyNews
        fields = '__all__'

    # def get_course_det(self,obj):
    #     return [course.name for course in obj.course.all()]


class QuestionUserFirstSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    # answers = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    class Meta:
        model=NewQuestionPool
        exclude = ["answer","is_delete","option_1","option_2","option_3","option_4","option_5","created_at",
                    "postive_mark",
                    "negative_mark",
                    "duration",
                    "answerhint",
                    "type",
                    "status",
                    "publish",
                    "user",
                    "categorys",
                    "levels",
                    "course",
                    "subject",
                    "module",
                    "topic",
                    "subtopic"]


    def get_option(self,obj):
        return {"option_1":obj.option_1,"option_2":obj.option_2,"option_3":obj.option_3,"option_4":obj.option_4,"option_5":obj.option_5 if obj.option_5 else ''}  
    
    def get_answers(self,obj):
        return str(obj.answer)[-1]
    
    def get_count(self,obj):
        return 5 if obj.option_5 else 4


class QuestionUserSecondSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    class Meta:
        model=NewQuestionPool
        exclude = []

    def get_option(self,obj):
        return [obj.option_1,obj.option_2,obj.option_3,obj.option_4,]

class QuizPoolUserViewsetSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    class Meta:
        model=QuizPool
        fields="__all__"

    def get_question(self,obj):
        serializer = QuestionUserFirstSerializer(obj.question, many=True)
        return {"data":serializer.data}

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewQuestionPool
        exclude =[]

class SuccessStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessStories
        fields ='__all__'

class MobileBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileBanner
        fields ='__all__'



class CategoryAppSerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields ='__all__'



class LevelAppSerializer(serializers.ModelSerializer):
    class Meta:
        model= Level
        fields ='__all__'

             
class CourseAppSerializer(serializers.ModelSerializer):
    batch_type_name = serializers.SerializerMethodField()
    class Meta:
        model= Course
        fields ='__all__'

    def get_batch_type_name(self,obj):
        return obj.batch_type.name




class CategoryNewMaterialSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    
    def get_level(self, obj):
        print("subject")
        fac = self.context.get('fac')
        print(obj,"jkjjjjjj",fac,fac['level'])

        subject = Level.objects.filter(category=obj.id, id__in=fac['level'],active=True).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        ser=LevelNewMaterialSerializer(subject, many=True, context={"fac": fac})
        return ser.data




class LevelNewMaterialSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = Level
        fields = '__all__'

    
    def get_course(self, obj):
        print("subject")
        fac = self.context.get('fac')
        print(obj,"jkjjjjjj",fac,fac['course'])

        subject = Course.objects.filter(level=obj.id, id__in=fac['course'],active=True).order_by('id')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        ser=CourseNewMaterialSerializer(subject, many=True, context={"fac": fac})
        return ser.data






class CourseNewMaterialSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    batch_type_name=serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    
    def get_subject(self, obj):
        print("subject")
        fac = self.context.get('fac')
        print(obj,"jkjjjjjj",fac,fac['subject'])

        subject = Subject.objects.filter(course=obj.id, id__in=fac['subject'],active=True).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        ser=SubjectNewMatSerializer(subject, many=True, context={"fac": fac})
        return ser.data
    
    def get_batch_type_name(self,obj):
        return obj.batch_type.name

    
    
        

class SubjectNewMatSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    
    def get_modules(self,obj):
        print("get_modules")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # mid=[i.module.id for i in fac]
        subject = Module.objects.filter(subject=obj.id,id__in=fac['module'],active=True).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        mod=ModuleNewMatSerializer(subject, many=True,context={"fac":fac})
        return mod.data
    


class ModuleNewMatSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    

    class Meta:
        model = Module
        fields = '__all__'

    
    def get_topics(self,obj):
        print("get_topics")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # tid=[i.topic.id for i in fac]
        topic = Topic.objects.filter(module=obj.id,id__in=fac['topic'],active=True).order_by('priority')
        print(topic.values('id'),"hhhhhhhhhhhhhh")
        ser=TopicNewMatSerializer(topic, many=True,context={"fac":fac})
        return ser.data
    
    
    
    
class TopicNewMatSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    status=serializers.SerializerMethodField()
    question_count=serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    
    def get_subtopic(self,obj):
        print("get_subtopic")
        # fac=self.context.get('fac')
        # print(fac,"TIp")
        # tid=[i.topic.id for i in fac]
        subtopic = SubTopic.objects.filter(topic=obj.id,active=True).order_by('priority')
        ser=SubtopicNewMatSerializer(subtopic, many=True)
        return ser.data
    
    def get_status(self,obj):
        fac=self.context.get('fac')
        facs=FacultyCourseAddition.objects.filter(user=fac['user'],topic=obj.id)
        if facs.exists():
            return facs[0].status
        else:
            return None

    def get_question_count(self, obj):
        fac=self.context.get('fac')
        qq= NewQuestionPool.objects.filter(Q(topic=obj) | Q(subtopic__topic=obj),user=fac['user'])
        return len(qq)
    

class SubtopicNewMatSerializer(serializers.ModelSerializer):
    # meterial =serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        fields = '__all__'



class StudyMaterialSerializer(serializers.ModelSerializer):
    course_det = serializers.SerializerMethodField()

    class Meta:
        model=StudyMaterial
        fields = '__all__'

    def get_course_det(self,obj):
        return [course.name for course in obj.course.all()]

class QuestionBookSerializer(serializers.ModelSerializer):
    course_det = serializers.SerializerMethodField()

    class Meta:
        model=QuestionBook
        fields = '__all__'

    def get_course_det(self,obj):
        return [course.name for course in obj.course.all()]
    
class ShortsSerializer(serializers.ModelSerializer):
    vimeo_id = serializers.SerializerMethodField()
    views=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    isliked = serializers.SerializerMethodField()

    level_name=serializers.SerializerMethodField()

    class Meta:
        model = Shorts
        fields = '__all__'
    def get_level_name(self,obj):
        return obj.level.name
    
    def get_vimeo_id(self,obj):
        vimeo = obj.video_file
        urls = str(vimeo)
        print(urls)
        try:
            index = urls.index('.com/') + len('.com/')
        except:
            return None

        numbers = urls[index:]
        return numbers
    
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='SHORTS',liked_id=obj.id).count()
    
    def get_views(self,obj):
        return Views.objects.filter(view_assign='SHORTS',view_id=obj.id).count()
    
    def get_isliked(self,obj):
        user = self.context.get('user')

        return Likes.objects.filter(like_assign='SHORTS',liked_id=obj.id,user__id = user).exists()

class ShortsWatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortsWatched
        fields = '__all__'

    
    

class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = '__all__'
# from django.db.models.functions import Cast, DecimalField

class FacultyDashboardSerializer(serializers.ModelSerializer):
    total_completed_class = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    rateing = serializers.SerializerMethodField()
  
    class Meta:
        model = Faculty
        fields = ('name','total_completed_class','total_earnings','pending','rateing','modeofclasschoice','photo')


    def get_total_completed_class(self, obj):
        timetable= TimeTable.objects.filter(faculty=obj.user,topic__status="F").count()
        return timetable
    
    def get_total_earnings(self,obj):
        salary =FacultyAttendence.objects.filter(timetable__faculty=obj.user).aggregate(total_earning=Sum('paid_amount'))['total_earning']
        return salary
    
    def get_rateing(self,obj):
        rate= Rating.objects.filter(Q(rate_fac=obj) | Q(rating_on__faculty=obj.user) ).aggregate(rate=Avg('choice'))['rate']
        # salary =FacultyAttendence.objects.filter(timetable__faculty=obj.user).aggregate(pending_salary=Sum(F('current_salary')-F('paid_amount')))['pending_salary']
        return rate
    
    def get_pending(self,obj):
        salary =FacultyAttendence.objects.filter(timetable__faculty=obj.user).aggregate(pending_salary=Sum(F('current_salary')-F('paid_amount')))['pending_salary']
        return salary

from bs4 import BeautifulSoup

class QuizPoolUserViewsetSerializerNew(serializers.ModelSerializer):
    instruction = serializers.SerializerMethodField()
    class Meta:
        model=QuizPool
        fields=['id','name','description','instruction','duration','count','postive_mark','negative_mark']

    def get_instruction(self,obj):
        html_string=obj.instruction
        soup = BeautifulSoup(html_string, 'html.parser')
        li_elements = [li.get_text(strip=True) for li in soup.find_all('li')]
        return li_elements
    
class BatchPackagesSerializer(serializers.ModelSerializer):
    batch_name = serializers.SerializerMethodField()
    studymaterial = serializers.SerializerMethodField()
    questionbook = serializers.SerializerMethodField()
    publication = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    batch_fees = serializers.SerializerMethodField()
    class Meta:
        model = BatchPackages
        fields = '__all__'

    def get_batch_name(self,obj):
        return obj.batch.name
    
    def get_batch_fees(self,obj):
        return obj.batch.fees
    
    def get_publication(self, obj):
        publication_details = []
        for publication in obj.publications.all():
            publication_details.append({
                'book_id':publication.id,
                'bookname': publication.bookname,
                'book_price': publication.book_price
            })
        return publication_details
    
    def get_questionbook(self, obj):
        questionbook_details = []
        for questionbook in obj.question_book.all():
            questionbook_details.append({
                'book_id':questionbook.id,
                'bookname': questionbook.bookname,
                'book_price': questionbook.book_price
            })
        return questionbook_details
    
    def get_studymaterial(self, obj):
        studymaterial_details = []
        for studymaterial in obj.study_meterial.all():
            studymaterial_details.append({
                'book_id':studymaterial.id,
                'bookname': studymaterial.bookname,
                'book_price': studymaterial.book_price
            })
        return studymaterial_details
    
    def get_total_price(self, obj):
        total = 0
        for publication in obj.publications.all():
            total += publication.book_price
        for studymaterial in obj.study_meterial.all():
            total += studymaterial.book_price
        for questionbook in obj.question_book.all():
            total += questionbook.book_price
        return total


    



class QuizPoolUserStartSerializer(serializers.ModelSerializer):
    question= serializers.SerializerMethodField()
    class Meta:
        model = QuizPoolUserRoom
        fields=['id','quiz','user','question']
    
    def get_question(self,obj):
        queryset=obj.quiz.question.all()
        queryset=queryset.order_by('?')[:obj.quiz.count]
        ser=QuestionUserFirstSerializer(queryset, many=True)
        return ser.data


class QuizPoolAnswersUserStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizPoolAnswers
        fields=['id','room','question','question_copy','option_1','option_2','option_3','option_4','option_5','answer','index']

class BooksTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksType
        fields = '__all__'

class BooksSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    class Meta:
        model = Books
        fields = '__all__'
    def get_branch_name(self,obj):
        return obj.branch.name
    
    def get_type_name(self,obj):
        return obj.type.name


# class CartSerializer(serializers.ModelSerializer):
#     cart_items = serializers.SerializerMethodField()
#     class Meta:
#         model = Cart
#         fields = '__all__'

#     def get_cart_items(self,obj):
#         queryset= CartItem.objects.filter(cart=obj)
#         serializer= CartItemSerializer(queryset, many=True)
#         return serializer.data

class CartItemSerializer(serializers.ModelSerializer):
    publications=serializers.SerializerMethodField()
    totalprice=serializers.SerializerMethodField()
    class Meta:
        model = CartItems
        fields = '__all__'

    def get_publications(self, obj):
        queryset= Publications.objects.filter(id=obj.publication.id)
        serializer= PublicationSerializer(queryset, many=True)
        return serializer.data
    
    # def get_totalprice(self,obj):
    #     totalcart=CartItems.objects.filter(user=obj.user).values('publication')
    #     pub = Publications.objects.filter(id__in=totalcart).aggregate(total=Sum('book_price'))['total']
    #     return pub
    def get_totalprice(self, obj):
        total_price = CartItems.objects.filter(user=obj.user).aggregate(total=Sum(F('publication__book_price') * F('quantity')))['total']
        return total_price

class BatchStudentAppSerializer(serializers.ModelSerializer):
    branch_name=serializers.SerializerMethodField()
    timetable = serializers.SerializerMethodField()
    holidays = serializers.SerializerMethodField()
    class Meta:
        model = Batch
        fields = ['name','working_days','exam_days','branch_name','timetable','holidays']

    def get_branch_name(self,obj):
        return obj.branch.name
    
    def get_timetable(self,obj):
        queryset= TimeTable.objects.filter(batch=obj,faculty__isnull=False)
        ser= TimetableserializerStudent(queryset,many=True)
        return ser.data
    
    def get_holidays(self,obj):
        batch = obj
        ids = SpecialHoliday.objects.filter(Q(batches=batch)| Q(branches=batch.branch) | Q(levels=batch.course.course.level)).values('id')
        id = SpecialHoliday.objects.filter(Q(batches__isnull=True)| Q(branches__isnull=True) | Q(levels__isnull=True)).values('id')
        ik=[i['id'] for i in ids ]
        ip = [i['id'] for i in id]
        holidays = SpecialHoliday.objects.filter(id__in=ik+ip)
        serializer = BatchholidaysAppserializer(holidays, many=True)
        return serializer.data
    
class DailyClassSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    class_room = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = ['subject','faculty','class_room','date','status']
    
    def get_subject(self,obj):
        return obj.topic.module.subject.name
    

    def get_faculty(self,obj):
        try:
            return obj.faculty.name
        except:
            return None
        
    def get_class_room(self,obj):
        try:
            return  obj.room.room_no
        except:
            return None
    
    def get_status(self,obj):
        topic_choice = [("P", "PENDING"), ("S", "SCHEDULED"), ("B", "BOOKED"), ("F", "FINISHED")]
        status_mapping = {code: name for code, name in topic_choice}

        def get_status_name():
            return status_mapping.get(obj.topic.status, "UNKNOWN") 

        return get_status_name()
    
    def get_material(self,obj):
        try:
            queryset = MaterialReference.objects.filter(
                Q(materialupload__vstatus_research=True) | Q(materialupload__vstatus_faculty=True),
                    topic=obj.topic.topic.topic,
                    subtopic__topic=obj.topic.topic.topic,
                    materialupload__user=obj.faculty,
                    
                ).values('materialupload')
            
            ser=MaterialUploadsStudentSerializer(queryset,many=True)
                            
            return  ser.data
            pass
        except:
            return None
        

class MaterialUploadsStudentSerializer(serializers.Serializer):
    class Meta:
        model=MaterialUploads
        fields=['updated_file','name','user__username']
     







class BatchholidaysAppserializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialHoliday
        fields = ['date','name']

    

class TimetableserializerStudent(serializers.ModelSerializer):

    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()

    subtopic = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()
    class_status = serializers.SerializerMethodField()
    student_materials = serializers.SerializerMethodField()
    faculty_rating = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = ['id','date','branch_name','batch_name','course_name','topic_name','subtopic','faculty_name','class_status','student_materials','faculty_rating']

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.name

    def get_course_name(self, obj):
        return obj.course.name

    def get_subtopic(self,obj):
        subtopic=Subtopic_batch.objects.filter(topic=obj.topic)
        serilizer= SubtopicStudentSerializer(subtopic, many=True)
        return serilizer.data

    def get_faculty_name(self,obj):
        try:
            return Faculty.objects.get(user=obj.faculty).name
        except:
            obj.faculty.username

    def get_class_status(self,obj):
        return obj.topic.status
    
    def get_student_materials(self,obj):
        try:
            user=obj.faculty
            topic = obj.topic.topic.topic
            mat = ConvertedMaterials.objects.filter(user=user,topic=topic)
            material = ConvertedMaterialStudentSerializer(mat,many=True)
            return material.data
        except:
            return None
        

    def get_faculty_rating(self, obj):
        if obj.faculty:
            tim = TimeTable.objects.filter(faculty=obj.faculty.id).values('id')
            rating = Rating.objects.filter(
                rating_on__in=tim).aggregate(Avg('choice'))
            return rating['choice__avg']
        else:
            return None


class SubtopicStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic_batch
        fields = ['name']


class LibraryUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model = LibraryUser
        fields = ['id','user','branch','cardno','book_limit','username','branch_name']
        # fields = '__all__'
    def get_username(self,obj):
        return obj.user.username
    def get_branch_name(self,obj):
        return obj.branch.name

class StudentFeeCollectionSerializer(serializers.ModelSerializer):
    publications = serializers.SerializerMethodField()
    study_materials = serializers.SerializerMethodField()
    question_banks = serializers.SerializerMethodField()


    class Meta:
        model = StudentFeeCollection
        fields = '__all__' 

    def get_publications(self,obj):
        return [publications.bookname for publications in obj.publications.all()]    
    
    def get_study_materials(self,obj):
        return [study_materials.bookname for study_materials in obj.study_materials.all()]       
   
    def get_question_banks(self,obj):
        return [question_banks.bookname for question_banks in obj.question_banks.all()]    

class StudentFeeAfterAdmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudentFeeCollection
        fields = '__all__' 

    def get_publications(self,obj):
        return [publications.bookname for publications in obj.publications.all()]    
    
    def get_study_materials(self,obj):
        return [study_materials.bookname for study_materials in obj.study_materials.all()]       
   
    def get_question_banks(self,obj):
        return [question_banks.bookname for question_banks in obj.question_banks.all()]    
   

class GenralVideosSerializer(serializers.ModelSerializer):
    videolink=serializers.SerializerMethodField()
    category_name  = serializers.SerializerMethodField()
    category_id  = serializers.SerializerMethodField()
    videoobject_name  = serializers.SerializerMethodField()
    videocategory_id  = serializers.SerializerMethodField()
    level_name  = serializers.SerializerMethodField()

    class Meta:
        model = GeneralVideos
        exclude = ['is_delete']

    def get_videolink(self,obj):
        return obj.video.videolink
    
    def get_category_name(self,obj):
        try:
            return obj.category.name
        except:
            return None
    
    def get_category_id(self,obj):
        try:
            return obj.category.id
        except:
            return None
    
    def get_videoobject_name(self,obj):
        return obj.video.name
    
    def get_videocategory_id(self,obj):
        return obj.video.id
    
    def get_level_name(self,obj):
        return obj.level.name
    



class GeneralVideosCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralVideosCategory
        exclude = ['is_delete']


class GenralVideosUserSerializer(serializers.ModelSerializer):
    category_name=serializers.SerializerMethodField()
    video_link=serializers.SerializerMethodField()
    # vimeothumbnails=serializers.SerializerMethodField()
    videotype=serializers.SerializerMethodField()
    video_length=serializers.SerializerMethodField()
    views=serializers.SerializerMethodField()
    vimeo_id=serializers.SerializerMethodField()
    # vimeo_files=serializers.SerializerMethodField()
    class Meta:
        model = GeneralVideos
        exclude = ['is_delete','created_at']

    def get_category_name(self,obj):
        return obj.category.name
    
    def get_video_link(self,obj):
      
        data = url_encryption(obj.video)
        return  data
    
    def get_vimeothumbnails(self,obj):
    
            # print(get_vimeo_video_thumbnails(obj.video.vimeoid))
        return get_vimeo_video_thumbnail(obj.video.videolink.split('/')[-1])
        
    
    def get_videotype(self,obj):
        return "Vimeo"
    
    def get_video_length(self,obj):
        return obj.video.video_length
    
    def get_views(self,obj):
        return Views.objects.filter(view_id=obj.video.id,view_assign='VIDEOS').count()
    
    def get_vimeo_id(self,obj):
        return obj.video.videolink.split('/')[::-1][0]
    
    def get_vimeo_files(self,obj):
        return stream_vimeo_video(obj.video.videolink.split('/')[::-1][0])


def url_encryption(obj):

    cipher_suite = Fernet(ENCRYPTION_URL)
    low = cipher_suite.encrypt(obj.sd_240p.encode()) if obj.sd_240p else None
    middile = cipher_suite.encrypt(obj.sd_360p.encode()) if obj.sd_360p else None
    upper_middile = cipher_suite.encrypt(obj.sd_540p.encode()) if obj.sd_540p else None
    high =  cipher_suite.encrypt(obj.hd_720p.encode()) if obj.hd_720p else None
    hd = cipher_suite.encrypt(obj.hd_1080p.encode()) if obj.hd_1080p else None

    return [{'240':low},{'360':middile},{'540':upper_middile},{'720':high},{'1080':hd}]

    




    
import vimeo 
def get_vimeo_video_thumbnail(video_id):
    try:
        client = vimeo.VimeoClient(token='d9a01813f50cf7a68e966e285d557f36')
        video_response = client.get(f"/videos/{video_id}")

        if video_response.status_code == 200:
            video_data = video_response.json()
            thumbnail_url = video_data.get('pictures', {}).get('sizes', [])
            return thumbnail_url

        print(f"Error fetching Vimeo video data: {video_response.status_code} - {video_response.text}")
        return []

    except vimeo.exceptions.VideoNotFoundError as e:
        print(f"Vimeo video not found: {e}")
        return []
    except vimeo.exceptions.RequestError as e:
        print(f"Error fetching Vimeo video data: {e}")
        return []
def stream_vimeo_video( id):
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
    print(files,'files')
    
    return files

from cryptography.fernet import Fernet
from aceapp.settings.base import ENCRYPTION_URL


# Generate a symmetric encryption key only once
# key = Fernet.generate_key()
# print(key,"               keyyyyyyyyyy         ")
# cipher_suite = Fernet(ENCRYPTION_URL)

    
class GenralVideosUserRetriveSerializer(serializers.ModelSerializer):
    category_name=serializers.SerializerMethodField()
    video_link=serializers.SerializerMethodField()
    vimeothumbnails=serializers.SerializerMethodField()
    videotype=serializers.SerializerMethodField()
    video_length=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    liked=serializers.SerializerMethodField()
    vimeo_id=serializers.SerializerMethodField()
    views=serializers.SerializerMethodField()
    files=serializers.SerializerMethodField()
    class Meta:
        model = GeneralVideos
        exclude = ['is_delete']

    def get_category_name(self,obj):
        return obj.category.name
    
    def get_video_link(self,obj):
       
       data = url_encryption(obj.video)
       return  data
    
    def get_vimeothumbnails(self,obj):
        return get_vimeo_video_thumbnail(obj.video.videolink.split('/')[-1])
    
    def get_videotype(self,obj):
        return "Vimeo"
    
    def get_video_length(self,obj):
        return obj.video.video_length
    
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.video.id).count()
    
    def get_liked(self,obj):
        user = self.context.get('user')
        return Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.video.id,user__id=user).exists()
    
    def get_vimeo_id(self,obj):
        return obj.video.videolink.split('/')[::-1][0]
        
    def get_views(self,obj):
        return Views.objects.filter(view_id=obj.video.id,view_assign='VIDEOS').count()

        
    def get_files(self,obj):
        quryset=GeneralVideosMaterial.objects.filter(id__in=obj.files.values_list('id', flat=True))
        ser=GeneralVideosMaterialSerializer(quryset,many=True)
        return ser.data


class GeneralVideosCategoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralVideosCategory
        fields =['id','name']

from django.utils import timezone
class BookLendSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    book_fine = serializers.SerializerMethodField()
    current_date = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = BookLend
        fields = '__all__'
    def get_user_name(self,obj):
        return obj.user.user.username
    def get_branch_name(self,obj):
        return obj.user.branch.name
    def get_book_fine(self,obj):
        fine_instance = LibraryFine.objects.first()
        if fine_instance:
            set_fine = fine_instance.amount
        duedate = obj.duedate
        currentdate = timezone.now().date()
        difference = currentdate - duedate
        difference=int(difference.days)
        if difference>0:
            return difference * set_fine
        
        return None

    
class LibraryFineSerializer(serializers.ModelSerializer):
    class Meta:
        model= LibraryFine
        fields = '__all__'

class VideoReportSerializer(serializers.ModelSerializer):

    class  Meta:
        model = ReportFlag
        fields = '__all__'

class VideoReportUserSerializer(serializers.ModelSerializer):

    class  Meta:
        model = ReportFlag
        exclude = ['is_delete','created_at']
    

class QuizPoolUserRoomSubmitSerializer(serializers.ModelSerializer):
    correct_answers=serializers.SerializerMethodField()
    skipped=serializers.SerializerMethodField()
    time_taken=serializers.SerializerMethodField()
    incorrect_answer=serializers.SerializerMethodField()
    class Meta:
        model = QuizPoolUserRoom
        fields = '__all__'

    def get_correct_answers(self,obj):
        count=0
        qpa=QuizPoolAnswers.objects.filter(room=obj.id)
        for i in qpa:
            if i.crct_answer==i.answer:
                count+=1
        return count
    
    def get_skipped(self,obj):
        return QuizPoolAnswers.objects.filter(room=obj.id,answer__isnull=True).count()
    
    def get_time_taken(self,obj):
        time_difference = obj.end_time - obj.start_time
        minutes = time_difference.seconds // 60
        seconds = time_difference.seconds % 60
        return f"{minutes} minutes {seconds} seconds"
    
    def get_incorrect_answer(self,obj):
        count=0
        qpa=QuizPoolAnswers.objects.filter(room=obj.id,answer__isnull=False)
        for i in qpa:
            if i.crct_answer!=i.answer:
                count+=1
        return count
    


class QuizPoolUserRoomLeaderBoardSerializer(serializers.ModelSerializer):
    # rank = serializers.SerializerMethodField()
    # username = serializers.SerializerMethodField()

    class Meta:
        model = QuizPoolUserRoom
        fields = '__all__'

    # def get_rank(self, obj):
    #     return obj.rank

    # def get_username(self,obj):
    #     return obj.user.username
    
class CourseAppStudentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields =['id','name']
    
class StoriesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesCategory
        fields = '__all__'

class StoriesCreateSerializer(serializers.ModelSerializer):
    storycategory = serializers.SerializerMethodField()
    levelname = serializers.SerializerMethodField()
    level_category = serializers.SerializerMethodField()
    level_categoryid = serializers.SerializerMethodField()
    class Meta:
        model = Stories
        fields = '__all__'
    def get_storycategory(self, obj):
        return obj.category.name
    def get_levelname(self, obj):
        return obj.level.name
    def get_level_category(self, obj):
        return obj.level.category.name
    def get_level_categoryid(self, obj):
        return obj.level.category.id
    
class StoriesCategoryUserSerializer(serializers.ModelSerializer):
    stories = serializers.SerializerMethodField()
    class Meta:
        model = StoriesCategory
        fields = ['name','stories','image']
    
    def get_stories(self, obj):
        request = self.context['request']
        user = AuthHandlerIns.get_id(request=request)
        categories = StoriesCategory.objects.all()
        

        
        
        student = Student.objects.get(user=user)
        level = student.selected_course.level.id
    
        
        watched_stories = StoriesWatched.objects.filter(student=user, watched=True).values('stories__id')
        unwatched_videos = Stories.objects.filter(level=level, category__in=categories) \
            .exclude(id__in=Subquery(watched_stories))


        
        queryset = Stories.objects.filter(category__id = obj.id)
        if len(watched_stories) > 0:
            queryset = unwatched_videos
        serializer = StoriesSerializer(queryset,many=True)
        return serializer.data



class StoriesSerializer(serializers.ModelSerializer):
    # watched = serializers.SerializerMethodField()
    watched_count = serializers.SerializerMethodField()
    story_category = serializers.SerializerMethodField()
    # video_files_by_category = serializers.SerializerMethodField()
    class Meta:
        model = Stories
        # fields = '__all__'
        exclude = ['is_delete']

    def get_story_category(self,obj):
        return obj.category.name
    
    # def get_watched(self, obj):
    #     user = self.context['user']
    #     print(user,"FRM SERILIZER")
    #     if user:
    #         try:
    #             StoriesWatched.objects.get(student=user, stories=obj, watched=True)
    #             return True
    #         except StoriesWatched.DoesNotExist:
    #             return False
    #     else:
    #         return False
    def get_watched_count(self, obj):
        return StoriesWatched.objects.filter(stories=obj, watched=True).count()
    
    # def get_video_files_by_category(self, obj):
    #     user = self.context.get('user')
    #     if user:
    #         # Get the list of watched stories' IDs for the current user
    #         watched_stories_ids = StoriesWatched.objects.filter(student=user, watched=True).values_list('stories__id', flat=True)
    #         # Fetch unwatched stories for the given category that are not in the watched_stories_ids list
    #         unwatched_stories = Stories.objects.filter(category=obj.category, id__in=watched_stories_ids, watched=False)
    #     else:
    #         # If no user is available (guest user), simply fetch all unwatched stories for the category
    #         unwatched_stories = Stories.objects.filter(category=obj.category, watched=False)

    #     video_data = [{'id': story.id, 'video_file': story.video_file} for story in unwatched_stories]
    #     return video_data

class StoriesWatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesWatched
        fields = '__all__'


class ConvertedMaterialStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConvertedMaterials
        fields = ['id','file','name']


class CommentsAppSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    profile=serializers.SerializerMethodField()
    repli=serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    isliked = serializers.SerializerMethodField()
    class Meta:
        model= Comments
        fields = '__all__'

    def get_profile(self, obj):
        try:
            if obj.user.is_student:
                pic= Student.objects.get(user=obj.user)
                return pic.photo.url
            elif obj.user.is_faculty:
                pic=Faculty.objects.get(user=obj.user)
                return pic.photo.url
            return None
        except:
            return None
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_repli(self, obj):
        queryset=Comments.objects.filter(comment_assign='COMMENTS',commented_id=obj.id)
        ser=CommentsAppSerializer(queryset,many=True)
        return ser.data
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='COMMENTS',liked_id=obj.id).count()
    
    def get_isliked(self,obj):
        user=self.context.get('user')
        return Likes.objects.filter(like_assign='COMMENTS',liked_id=obj.id,user__id=user).exists()

class PackageMaterialsSerializer(serializers.ModelSerializer):

    class Meta:
        model=PackageMaterials
        fields='__all__'
class PackageMaterialSmall(serializers.ModelSerializer):
    
    class Meta:
        model=PackageMaterials
        fields=['id','name','file','description','status']

class QustionpoolNewSmall(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model=NewQuestionPool
        fields=('id','question_text','option_1','option_2','option_3','option_4','option_5','answer','type','answerhint')
class PackageQuestionPaperSerilizerSmall(serializers.ModelSerializer):
    questions=QustionpoolNewSmall(many=True)
    type = serializers.CharField(source='get_type_display')
    question_count=serializers.SerializerMethodField()
    attended=serializers.SerializerMethodField()
    attendcount=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    likecount=serializers.SerializerMethodField()
    class Meta:
        model=QuestionPaper 
        fields=('id','name','instruction','positivemark','negativemark','duration','type','questions','question_count','attended','attendcount','banner','description','likes','likecount','notes')    

    def get_question_count(self,obj):
        counts=obj.questions.count()
        return counts
    def get_attended(self,obj):
       id=self.context.get('id') 
       exampackageid=self.context.get('exampackageid')
       attend=QuestionpaperAttend.objects.filter(student=id,question_paper=obj.id,exampackage=exampackageid)
       print(attend,'addd')
       if attend:
            return True
       else:
            return False
    def get_attendcount(self,obj):
        id=self.context.get('id') 
        exampackageid=self.context.get('exampackageid')
        attend=QuestionpaperAttend.objects.filter(student=id,question_paper=obj.id,exampackage=exampackageid).count()
        if attend:
            return attend
        else:
            return 0
        
    def get_likes(self,obj):
        id=self.context.get('id') 
        if Likes.objects.filter(user=id,like_assign='QUESTION_PAPER',liked_id=obj.id):
            return True
        else:
            return False
    def get_likecount(self, obj):
        return Likes.objects.filter(like_assign='QUESTION_PAPER',liked_id=obj.id).count()    
    
class PackageQuestionPaperSerilizerNotpurchase(serializers.ModelSerializer):
    
    # questions=QustionpoolNewSmall(many=True)
    questions=serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display')
    question_count=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    likecount=serializers.SerializerMethodField()
    notes=serializers.SerializerMethodField()
    class Meta:
        model=QuestionPaper 
        # fields=('id','name','instruction','positivemark','negativemark','duration','type','questions','question_count')    
        fields=('id','name','type','questions','question_count','banner','description','likes','likecount','notes')    

    def get_question_count(self,obj):
        counts=obj.questions.count()
        return counts
    def get_questions(self,obj):
        id=self.context.get('id')
        purchase=PurchaseDetails.objects.filter(purchase_item='EXAM_PACKAGE',purchase_item_id=obj.id,user=id)  
        if purchase:
            questions=QustionpoolNewSmall(many=True)
        else:
            return None
    def get_likes(self,obj):
        id=self.context.get('id') 
        likes=Likes.objects.filter(user=id,like_assign='QUESTION_PAPER',liked_id=obj.id)
        if likes:
            return True
        else:
            return False
    def get_likecount(self, obj):
        return Likes.objects.filter(like_assign='QUESTION_PAPER',liked_id=obj.id).count()    
    
    def get_note(self,obj):
        return None
      
class VedioMeterialAndQuestionsSerializer(serializers.ModelSerializer):
    material=PackageMaterialSmall(many=True)
    questionpaper=PackageQuestionPaperSerilizerSmall(many=True)
    video=CommonVideoSerializer()
    materialids=serializers.SerializerMethodField()
    questionpaperids=serializers.SerializerMethodField()
    # video=AddVediotoStudioCourseSerializer()

    class Meta:
        model=VedioMeterialAndQuestions
        # fields='__all__'
        exclude=['created_at','created_by','is_delete']

    def get_materialids(self, obj):
        return list(obj.material.values_list('id', flat=True))
    
    def get_questionpaperids(self,obj):
        return list(obj.questionpaper.values_list('id',flat=True))


class VedioMeterialAndQuestionsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VedioMeterialAndQuestions
        exclude = ['created_at', 'created_by', 'is_delete']

class CategorySeriaizerSmall(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']
class LevelSeriaizerSmall(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields=['id','name']
class VedioPackageSerializer(serializers.ModelSerializer):
    videos=VedioMeterialAndQuestionsSerializer(many=True)
    videoids=serializers.SerializerMethodField()
    category=CategorySeriaizerSmall()
    level=LevelSeriaizerSmall()

    class Meta:
        model=VedioPackage
        exclude=['created_at','created_by','is_delete']

    def get_videoids(self,obj):
        return list(obj.videos.values_list('id',flat=True))
class CommonVideoSerializerNEW(serializers.ModelSerializer):
    # watched=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    likes_count=serializers.SerializerMethodField()
    vimeothumbnails=serializers.SerializerMethodField()
    views=serializers.SerializerMethodField()
    

    class Meta:
        model=StudioVideo
        fields=['id','name','description','video_length','editingstaff','videocontent','vimeoid','videolink','video_length','likes','likes_count','vimeothumbnails','views','sd_240p','sd_360p','sd_540p','hd_720p','hd_1080p']

    def get_likes(self,obj):
        id=self.context.get('id')
        Like=Likes.objects.filter(user__id=id,like_assign='VIDEOS',liked_id=obj.id)
        if Like:
            return True
        else:
            return False
    def get_likes_count(self,obj):
        id=self.context.get('id')
        likecount=Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.id).count()
        if likecount:
            return likecount
        else:
            return 0
        
    def get_vimeothumbnails(self,obj):
    
            # print(get_vimeo_video_thumbnails(obj.video.vimeoid))
        return get_vimeo_video_thumbnail(obj.videolink.split('/')[-1])
    
    def get_views(self,obj):
        return Views.objects.filter(view_assign='VIDEOS',view_id=obj.id).count()


class VedioMeterialAndQuestionsREadonlySerializer(serializers.ModelSerializer):
    material=PackageMaterialSmall(many=True)
    questionpaper=PackageQuestionPaperSerilizerSmall(many=True)
    # video=CommonVideoSerializerNEW()
    video=serializers.SerializerMethodField()
    video_question_paper_count=serializers.SerializerMethodField()
    video_material_count=serializers.SerializerMethodField()
    

    class Meta:
        model=VedioMeterialAndQuestions
        # fields='__all__'
        exclude=['created_at','created_by','is_delete']

    def get_video(self,obj):
        id = self.context.get('id')
        videoid=obj.video.id
        videos=StudioVideo.objects.filter(id=obj.video.id)
        print(videos,'kkk')
        serializers=CommonVideoSerializerNEW(videos,many=True,context={'id':id,'videoid':videoid})
        print("***")
        return serializers.data
    def get_video_question_paper_count(self,obj):
        return obj.questionpaper.count()

    def get_video_material_count(self,obj):
        return obj.material.count()

class VedioPackageREadonlySerializer(serializers.ModelSerializer):
    videos=VedioMeterialAndQuestionsREadonlySerializer(many=True)
    category=CategorySeriaizerSmall()
    level=LevelSeriaizerSmall()

    class Meta:
        model=VedioPackage
        exclude=['created_at','created_by','is_delete']

class VedioPackageDashboardREadonlySerializer(serializers.ModelSerializer):
    category=CategorySeriaizerSmall()
    level=LevelSeriaizerSmall()
    purchased=serializers.SerializerMethodField()


    class Meta:
        model=VedioPackage
        fields=['id','name','image','price','discount_price','banner','category','level','purchased']

    def get_purchased(self,obj):
        try:
            id =self.context.get("id")
            videos=PurchaseDetails.objects.filter(purchase_item='VIDEO_PACKAGE',purchase_item_id=obj.id,user=id)
            if videos:
                return True
            else:
                return False
        except:
            pass

class PackageMaterialSmallBeforePurchase(serializers.ModelSerializer):
    file=serializers.SerializerMethodField()
    class Meta:
        model=PackageMaterials
        fields=['id','name','file','description','status']

    def get_file(self,obj):
        return None

class PackageQuestionPaperSerilizerSmallBeforePurchase(serializers.ModelSerializer):
    
    # questions=QustionpoolNewSmall(many=True)
    type = serializers.CharField(source='get_type_display')
    question_count=serializers.SerializerMethodField()
    class Meta:
        model=QuestionPaper 
        fields=('id','name','instruction','positivemark','negativemark','duration','type','question_count')    

    def get_question_count(self,obj):
        counts=obj.questions.count()
        return counts
    
class CommonVideoSerializerNEWBeforePurchase(serializers.ModelSerializer):
    # watched=serializers.SerializerMethodField()
    videolink=serializers.SerializerMethodField()
    vimeoid=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    likes_count=serializers.SerializerMethodField()
    sd_240p=serializers.SerializerMethodField()
    sd_360p=serializers.SerializerMethodField()
    sd_540p=serializers.SerializerMethodField()
    hd_720p=serializers.SerializerMethodField()
    hd_1080p=serializers.SerializerMethodField()


    class Meta:
        model=StudioVideo
        fields=['id','name','description','video_length','editingstaff','videocontent','vimeoid','videolink','video_length','likes','likes_count','sd_240p','sd_360p','sd_540p','hd_720p','hd_1080p']
        

    def get_watched(self,obj):
        try:
            id=self.context.get("id")
            videoid=self.context.get("videoid")
            watch=Views.objects.filter(user=id,view_assign='VIDEOS',view_id=videoid)
            if watch:
                return True
            else:
                return False
        except:
            pass
    def get_videolink(self,obj):
        return None
    def get_vimeoid(self,obj):
        return None
    def get_likes(self,obj):
        id=self.context.get('id')
        Like=Likes.objects.filter(user__id=id,like_assign='VIDEOS',liked_id=obj.id)
        print(Like,'kkkk')
        if Like:
            return True
        else:
            return False
    def get_likes_count(self,obj):
        id=self.context.get('id')
        likecount=Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.id).count()
        if likecount:
            return likecount
        else:
            return 0
    def get_sd_240p(self, obj):
            return None

    def get_sd_360p(self, obj):
        return None

    def get_sd_540p(self, obj):
        return None

    def get_hd_720p(self, obj):
        return None

    def get_hd_1080p(self, obj):
        return None


class VedioMeterialAndQuestionsREadonlySerializerBerforePurchase(serializers.ModelSerializer):
    material=PackageMaterialSmallBeforePurchase(many=True)
    questionpaper=PackageQuestionPaperSerilizerSmallBeforePurchase(many=True)
    # video=CommonVideoSerializerNEWBeforePurchase()
    video=video=serializers.SerializerMethodField()
    video_question_paper_count=serializers.SerializerMethodField()
    video_material_count=serializers.SerializerMethodField()

    class Meta:
        model=VedioMeterialAndQuestions
        # fields='__all__'
        exclude=['created_at','created_by','is_delete']
    

    def get_video_question_paper_count(self,obj):
        return obj.questionpaper.count()

    def get_video_material_count(self,obj):
        return obj.material.count()
    
    def get_video(self,obj):
        id = self.context.get('id')
        print(id,"thsi is idddd")
        videoid=obj.video.id
        print(videoid,"thsi video id")
        videos=StudioVideo.objects.filter(id=obj.video.id)
        print(videos,'kkk')
        serializers=CommonVideoSerializerNEWBeforePurchase(videos,many=True,context={'id':id,'videoid':videoid})
        print("***")
        return serializers.data

class VideopacakgeviewdetialsSerializer(serializers.ModelSerializer):
    category=CategorySeriaizerSmall()
    level=LevelSeriaizerSmall()
    videos=serializers.SerializerMethodField()
    purchased=serializers.SerializerMethodField()
    question_paper_count=serializers.SerializerMethodField()
    material_count=serializers.SerializerMethodField()
    video_count=serializers.SerializerMethodField()
    class Meta:
        model=VedioPackage
        exclude=['created_by','is_delete']

    def get_videos(self,obj):
        try:
            id =self.context.get('id')
            print(obj.id,'idd')
            print(id,'id')
            videos=PurchaseDetails.objects.filter(purchase_item='VIDEO_PACKAGE',purchase_item_id=obj.id,user=id)
            if videos:
                print("***")
                videos_queryset = obj.videos.all()  # Retrieve the related videos queryset
                print(videos_queryset,'dd')
                serialized_videos = []  # List to store serialized video data
                for video in videos_queryset:
                    print(video,'video')
                    # Customize how each video is serialized here, e.g., use a separate serializer
                    serialized_video = VedioMeterialAndQuestionsREadonlySerializer(video,context={'id': id}).data
                    print(serialized_video,'serialized')
                    serialized_videos.append(serialized_video)
                return serialized_videos
            else:
                print("##")
                videos_queryset = obj.videos.all()  # Retrieve the related videos queryset
                print(videos_queryset,'dd')
                serialized_videos = []  # List to store serialized video data
                for video in videos_queryset:
                    print(video,'video')
                    # Customize how each video is serialized here, e.g., use a separate serializer
                    serialized_video = VedioMeterialAndQuestionsREadonlySerializerBerforePurchase(video,context={'id': id}).data
                    print(serialized_video,'serialized')
                    serialized_videos.append(serialized_video)
                return serialized_videos
                # return []
        except Exception as e:
            print(e,'this is error')
            pass

    def get_purchased(self,obj):
        try:
            id =self.context.get('id')
            videos=PurchaseDetails.objects.filter(purchase_item='VIDEO_PACKAGE',purchase_item_id=obj.id,user=id)
            if videos:
                return True
            else:
                return False
        except:
            pass
    def get_question_paper_count(self,obj):
        try:
            vediometerialandquestions=obj.videos.all()
            count=0
            for x in vediometerialandquestions:
                questionpaper=x.questionpaper.count()
                totalcount=count+questionpaper
                count=totalcount
            return totalcount
        except:
            pass

    def get_material_count(self,obj):
        try:
            vediometerialandquestions=obj.videos.all()
            count=0
            for x in vediometerialandquestions:
                materilcount=x.material.count()
                totalcount=count+materilcount
                count=totalcount
            return totalcount

        except:
            pass
    def get_video_count(self,obj):
        return obj.videos.count()

class VedioMeterialAndQuestionsREadonlySerializerWatched(serializers.ModelSerializer):
    material=PackageMaterialSmall(many=True)
    questionpaper=PackageQuestionPaperSerilizerSmall(many=True)
    # video=CommonVideoSerializerNEW()
    video=serializers.SerializerMethodField()
    video_question_paper_count=serializers.SerializerMethodField()
    video_material_count=serializers.SerializerMethodField()

    # video=AddVediotoStudioCourseSerializer()

    class Meta:
        model=VedioMeterialAndQuestions
        # fields='__all__'
        exclude=['created_at','created_by','is_delete']

    def get_video(self,obj):
        id = self.context.get('id')
        watchedvideo = self.context.get('watchedvideo', [])
        unwatchedvideo = self.context.get('unwatchedvideo', [])
        if watchedvideo:
            # videoid=obj.video.id
            videos=StudioVideo.objects.filter(id=obj.video.id)
            # videos=StudioVideo.objects.filter(id__in=watchedvideo)
            serializers=CommonVideoSerializerNEW(videos,many=True,context={"id":id})
            return serializers.data
        elif unwatchedvideo:    
            print("**********")
            # videos=VedioMeterialAndQuestions.objects.filter(video=obj.video)
            videos=StudioVideo.objects.filter(id=obj.video.id)
            # videos=StudioVideo.objects.filter(id__in=unwatchedvideo)
            print(videos,'blalblablabla')
            serializers=CommonVideoSerializerNEW(videos,many=True,context={"id":id})
            return serializers.data
        else:
            pass
    def get_video_question_paper_count(self,obj):
        return obj.questionpaper.count()

    def get_video_material_count(self,obj):
        return obj.material.count()


class VideopacakgeviewdetialsSerializerWatched(serializers.ModelSerializer):
    category=CategorySeriaizerSmall()
    level=LevelSeriaizerSmall()
    videos=serializers.SerializerMethodField()
    # videos=VedioMeterialAndQuestionsREadonlySerializerWatched(many=True)
    question_paper_count=serializers.SerializerMethodField()
    material_count=serializers.SerializerMethodField()
    video_count=serializers.SerializerMethodField()
    class Meta:
        model=VedioPackage
        exclude=['created_by','is_delete']

    def get_videos(self, instance):
        # Access watchedvideo from context
        watchedvideo = self.context.get('watchedvideo', [])
        unwatchedvideo = self.context.get('unwatchedvideo', [])
        id=self.context.get('id')
        if watchedvideo:
            studio_video_ids = StudioVideo.objects.filter(id__in=watchedvideo).values_list('id', flat=True)
            videos_queryset = instance.videos.filter(video__id__in=studio_video_ids)
            videos_serializer = VedioMeterialAndQuestionsREadonlySerializerWatched(
                videos_queryset, many=True, context={'watchedvideo': watchedvideo,'id':id}
            )

            return videos_serializer.data
        elif unwatchedvideo :
            studio_video_ids = StudioVideo.objects.filter(id__in=unwatchedvideo).values_list('id', flat=True)
            print(studio_video_ids,'jajaj')
            videos_queryset = instance.videos.filter(video__id__in=studio_video_ids)
            print(videos_queryset,'2nd')
            videos_serializer = VedioMeterialAndQuestionsREadonlySerializerWatched(
                videos_queryset, many=True, context={'unwatchedvideo': unwatchedvideo,'id':id}
            )
            return videos_serializer.data
        else:
            pass
    def get_question_paper_count(self,obj):
        try:
            vediometerialandquestions=obj.videos.all()
            count=0
            for x in vediometerialandquestions:
                questionpaper=x.questionpaper.count()
                totalcount=count+questionpaper
                count=totalcount
            return totalcount
        except:
            pass

    def get_material_count(self,obj):
        try:
            vediometerialandquestions=obj.videos.all()
            count=0
            for x in vediometerialandquestions:
                materilcount=x.material.count()
                totalcount=count+materilcount
                count=totalcount
            return totalcount

        except:
            pass

    def get_video_count(self,obj):
        return obj.videos.count()


class LikesAppSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()

    class Meta:
        model= Likes
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username
    

class QuizPoolAnswersUserSubmitSerializer(serializers.ModelSerializer):
    selected_answer_index=serializers.SerializerMethodField()
    selected_crctanswer_index=serializers.SerializerMethodField()
    class Meta:
        model = QuizPoolAnswers
        fields=['id','room','question','question_copy','option_1','option_2','option_3','option_4','option_5','answer','crct_answer','index','selected_answer_index','selected_crctanswer_index']

    def get_selected_answer_index(self,obj):
        try:
            return int(obj.answer.split("_")[1])
        except:
            return None
    
    def get_selected_crctanswer_index(self,obj):
        return int(obj.crct_answer.split("_")[1])
class ExampackageLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
class ExampackagebeforeSerializer(serializers.ModelSerializer):
    level=ExampackageLevelSerializer()
    exampaper_counts=serializers.SerializerMethodField()
    questions_count=serializers.SerializerMethodField()
    purchased=serializers.SerializerMethodField()
    class Meta:
        model=ExampaperPackage
        fields=['id','title','imagetitle','thumbnail','banner','description','price','discount_price','premium','status','level','exampaper_counts','questions_count','purchased']
    def get_exampaper_counts(self,obj):
        exmpprcount=obj.exampaper.count()
        return exmpprcount
    def get_questions_count(self, obj):
        total_question_count = 0
        
        for exampaper in obj.exampaper.all():
            total_question_count += exampaper.questions.count()
        
        return total_question_count
    
    def get_purchased(self,obj):
        id=self.context.get('id')
        if PurchaseDetails.objects.filter(user=id,purchase_item='EXAM_PACKAGE',purchase_item_id=obj.id):
            return True
        else:
            return False
    
class PackageQuestionPaperSerilizerSmallViewDeatils(serializers.ModelSerializer):
    question_count=serializers.SerializerMethodField()
    class Meta:
        model=QuestionPaper 
        fields=('id','name','question_count','duration')    

    def get_question_count(self,obj):
        counts=obj.questions.count()
        return counts
class ExampackageviewsDetialsSeriilaizer(serializers.ModelSerializer):
    exampaper=PackageQuestionPaperSerilizerSmallViewDeatils(many=True)
    exampaper_counts=serializers.SerializerMethodField()
    level=ExampackageLevelSerializer()
    class Meta:
        model=ExampaperPackage
        exclude=['created_at','created_by','is_delete']
    def get_exampaper_counts(self,obj):
        exmpprcount=obj.exampaper.count()
        return exmpprcount
class ExampaperpackageSerializer(serializers.ModelSerializer):
    # exampaper=PackageQuestionPaperSerilizerSmall(many=True)
    exampaper=serializers.SerializerMethodField()
    level=ExampackageLevelSerializer()
    exampaper_counts=serializers.SerializerMethodField()
    purchase=serializers.SerializerMethodField()
    

    class Meta:
        model=ExampaperPackage
        exclude=['created_at','created_by','is_delete']

    def get_exampaper_counts(self,obj):
        exmpprcount=obj.exampaper.count()
        return exmpprcount
    def get_exampaper(self,obj):
        id =self.context.get('id')
        attend=self.context.get('attend')
        notattend=self.context.get('notattend')
        exampackageid=obj.id
        purchase=PurchaseDetails.objects.filter(purchase_item='EXAM_PACKAGE',purchase_item_id=obj.id,user=id)
        if purchase and not attend and not notattend:
            exampapers = PackageQuestionPaperSerilizerSmall(obj.exampaper, many=True,context={'id':id,'exampackageid':exampackageid}).data
            return exampapers
        elif attend:
            attended=QuestionpaperAttend.objects.filter(student=id,exampackage=obj.id).values('question_paper')
            exampaperid = [x['question_paper'] for x in attended]
            print(exampaperid,'ddd')
            relevant_exampapers = obj.exampaper.filter(id__in=exampaperid)
            exampapers = PackageQuestionPaperSerilizerSmall(relevant_exampapers, many=True,context={'id':id,'exampackageid':exampackageid}).data
            return exampapers
        elif notattend:
            attended=QuestionpaperAttend.objects.filter(student=id,exampackage=obj.id).values('question_paper')
            exampaperid = [x['question_paper'] for x in attended]
            print(exampaperid,'ddd')
            relevant_exampapers = obj.exampaper.exclude(id__in=exampaperid)
            exampapers = PackageQuestionPaperSerilizerSmall(relevant_exampapers, many=True,context={'id':id,'exampackageid':exampackageid}).data
            return exampapers
        else:
            exampapers = PackageQuestionPaperSerilizerNotpurchase(obj.exampaper, many=True,context={'id':id,'exampackageid':exampackageid}).data
            return exampapers
            


        
    def get_purchase(self,obj):
        id =self.context.get('id')
        purchase=PurchaseDetails.objects.filter(purchase_item='EXAM_PACKAGE',purchase_item_id=obj.id,user=id)  
        if purchase:
            return True
        else:
            return False


        
class ExampackageCategorySerializerforadmin(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']
class ExampackageLevelSerializerforadmin(serializers.ModelSerializer):
    
    class Meta:
        model = Level
        fields = ['id', 'name' ]
class ExampaperpackageSerializerforAdmin(serializers.ModelSerializer):
    exampaper=PackageQuestionPaperSerilizerSmall(many=True)
    level=ExampackageLevelSerializerforadmin()
    category = serializers.SerializerMethodField()
  

    class Meta:
        model=ExampaperPackage
        exclude=['created_at','created_by','is_delete']

    def get_category(self, obj):
        level_instance = obj.level
        if level_instance is not None:
            category_instance = level_instance.category
            serializer = ExampackageCategorySerializerforadmin(category_instance)
            return serializer.data
        else:
            return None

class CurrentAffairsQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAffairsQuestions
        fields = '__all__'

class CurrentAffairsVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAffairsVideos
        fields = '__all__'

class DailyExamsSerializer(serializers.ModelSerializer):
    exampaper = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    class Meta:
        model = DailyExams
        exclude =['is_delete']
    def get_exampaper(self,obj):
        return obj.exampaper.name
    
    def get_level(self,obj):
        return obj.level.name
        
class CurrentAffairsVideosAssignSerializer(serializers.ModelSerializer):
    video_id = serializers.SerializerMethodField()
    video_name = serializers.SerializerMethodField()
    class Meta:
        model = CurrentAffairsVideosAssign
        exclude =['is_delete']

    def get_video_name(self,obj):
        return obj.video.name
    
    def get_video_id(self,obj):
        return obj.video.id

class  SpecialExamsCourseSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Course
        fields = ['id','name']
        
class SpecialExamsFacultySerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    class Meta:
        model=Faculty
        fields=['id','name','username']
    def get_username(self,obj):
        return obj.user.username

class SpecialExamsSerializer(serializers.ModelSerializer):
    course=SpecialExamsCourseSerializer()
    faculty=SpecialExamsFacultySerializer()
    exampaper=PackageQuestionPaperSerilizerSmall()
    class Meta:
        model=SpecialExams
        exclude=['created_at','created_by','is_delete'] 

class SpecialExamsPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model=SpecialExams
        exclude=['created_at','created_by','is_delete'] 


class GeneralVideosMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=GeneralVideosMaterial
        exclude=['is_delete'] 


class PreviousExamsSerializer(serializers.ModelSerializer):
    exampaper = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    class Meta:
        model = PreviousExams
        exclude =['is_delete']
    def get_exampaper(self,obj):
        return obj.exampaper.name
    
    def get_level(self,obj):
        return obj.level.name
    
class FacultyDetailsSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id','name','address','photo','qualification']


class PopularFacultySerializer(serializers.ModelSerializer):
    faculty = FacultyDetailsSerilaizer()
    course_name = serializers.SerializerMethodField()
    category_id =serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    level_id =serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    faculty_id = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()
    faculty_address = serializers.SerializerMethodField()
    faculty_photo = serializers.SerializerMethodField()
    faculty_qualification = serializers.SerializerMethodField()




    
    class Meta:
        model = PopularFaculty
        exclude =['is_delete']

    def get_faculty_id(self,obj):
        return obj.faculty.id
    def get_faculty_name(self,obj):
        return obj.faculty.name
    def get_faculty_address(self,obj):
        return obj.faculty.address
    def get_faculty_photo(self,obj):
        try:
            return obj.faculty.photo.url
        except:
            return None
    def get_faculty_qualification(self,obj):
        return obj.faculty.qualification
    def get_course_name(self,obj):
        return obj.course.name
    def get_category_name(self,obj):
        return obj.course.level.category.name
    def get_level_name(self,obj):
        return obj.course.level.name
    def get_category_id(self,obj):
        return obj.course.level.category.id
    def get_level_id(self,obj):
        return obj.course.level.id
    
class PopularFacultyCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    category_id =serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    level_id =serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = PopularFaculty
        # fields = ['course','created_at','course_name']
        exclude =['is_delete']

    
    def get_course_name(self,obj):
        return obj.course.name
    def get_course_id(self,obj):
        return obj.course.id
    def get_category_name(self,obj):
        return obj.course.level.category.name
    def get_level_name(self,obj):
        return obj.course.level.name
    def get_category_id(self,obj):
        return obj.course.level.category.id
    def get_level_id(self,obj):
        return obj.course.level.id
    def get_created_at(self,obj):
        try:
            return obj.created_at
        except:
            None
    
    

class GroupedPopularFacultySerializer(serializers.Serializer):
    course_name = serializers.CharField()
    details = serializers.CharField()
    faculty = serializers.ListField(child=FacultyDetailsSerilaizer())
    # popular = serializers.ListField(child=PopularFacultySerializer())
class ViewSerializeruser(serializers.ModelSerializer):
    class Meta:
        model = Views
        exclude =['is_delete']


class ScholarshipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipType
        exclude = ['is_delete']

class FacultyInfoSerializer(serializers.Serializer):
    faculty_id = serializers.IntegerField()
    faculty_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    # photo = serializers.ImageField()
    # class Meta:
    #     model = Faculty
    #     fields = ('faculty_id', 'faculty_name', 'email', 'mobile', 'photo')

class ScholarshipApprovalSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    approved_byname = serializers.SerializerMethodField()
    class Meta:
        model = ScholarshipApproval
        exclude = ['is_delete']

    def get_type(self,obj):
        # return [type.name for type in obj.type.all()]
        # return None
        return [{'name': type.name, 'id': type.id} for type in obj.type.all()]

    def get_student(self,obj):
        # return None
        return obj.student.name
    
    def get_student_id(self,obj):
        # return None
        return obj.student.id
    
    def get_approved_byname(self,obj):
        # return None
        return obj.approved_by.username
        
class LobyConnectSerializer(serializers.ModelSerializer):
    profilepic=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['username','profilepic','id']

    def get_profilepic(self,obj):
        s=Student.objects.get(user__id=obj.id)
        if s.photo:
            return s.photo.url
        return None
    

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

@receiver(post_save, sender=PollFightLobby)
def send_lobby_join(sender, instance, created, **kwargs):
    k=[instance.user1.id,instance.user2.id if instance.user2 else None]
    print(k,"kkkkkkkkkkkk")
    for i in k:
        if i:
            user_id=str(i)
            print(user_id)
            ser=LobyConnectSerializer(User.objects.filter(id__in=k),many=True)
            print(ser.data)
            channel_layer = get_channel_layer()
            print(channel_layer,"hhhhh")
            # data=json.dumps(ser.data)
            async_to_sync(channel_layer.group_send)(
                f"{user_id}",  # Use the recipient's group
                {"type": "group_message", "message": json.dumps({"action":"pollfight-connect","message":ser.data})}
            )


# @receiver(post_save, sender=PollFightSubmit)
# def send_submitted_details(sender, instance, created, **kwargs):
#     users=[instance.room.user1,instance.room.user2]
#     for i in users:
#         if i and i != instance.created_by.id:
#             user_id=str(i)
#             print(user_id)
#             ser=PollFightSubmitSerializer(instance)

#             channel_layer = get_channel_layer()
#             print(channel_layer,"hhhhh")
#             data=json.dumps(ser.data)
#             async_to_sync(channel_layer.group_send)(
#                 f"{user_id}",  # Use the recipient's group
#                 {"type": "group_message", "message": data}
#             )
import random
def poll_fight_bot(id,index):
    ins=PollFightLobby.objects.get(id=id)
    qins=PollFightSubmit.objects.filter(room=ins.id,index=index,created_by__isnull=True).first()
    choice=["option_1","option_2","option_3","option_4"]
    ans=[qins.crct_answer]*index
    final=choice+ans
    pp=random.choice(final)
    qins.answer=pp
    qins.save()
    return pp


@receiver(post_save, sender=PollFightSubmit)
def send_answer_poll(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        room=instance.room
        if not room.user2 and instance.created_by!=None:
            poll_fight_bot(room.id,instance.index)
        
        user=[room.user1.id,room.user2.id] if room.user2 else [room.user1.id]
        for i in user:
            try:
                if i != instance.created_by.id:
                    user_id=str(i)
                    channel_layer = get_channel_layer()
                    print(channel_layer,"hhhhh")
                    ser=PollFightSubmitSerializer(instance,many=False)
                    # data=json.dumps(ser.data)
                    async_to_sync(channel_layer.group_send)(
                        f"{user_id}",  # Use the recipient's group
                        {"type": "group_message", "message": json.dumps({"action":"pollfight-answer-submit","message":ser.data})}
                    )
            except:
                user_id=str(i)
                channel_layer = get_channel_layer()
                print(channel_layer,"hhhhh")
                ser=PollFightSubmitSerializer(instance,many=False)
                async_to_sync(channel_layer.group_send)(
                    f"{user_id}",  # Use the recipient's group
                    {"type": "group_message", "message": json.dumps({"action":"pollfight-answer-submit","message":ser.data})}
                )






class PollFightSubmitSerializer(serializers.ModelSerializer):
    ifcrct=serializers.SerializerMethodField()
    class Meta:
        model=PollFightSubmit
        exclude = ['is_delete']

    def get_ifcrct(self,obj):
        return obj.answer==obj.crct_answer

from student.serializers import StudentBatchSerializer
class StudentProfileSerializer(serializers.ModelSerializer):
       
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    joined_date = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class_details=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'

    def get_email(self, obj):
        return obj.user.email
    def get_mobile(self, obj):
        return obj.user.mobile
    def get_joined_date(self, obj):
        return obj.user.joined_date
    def get_user_id(self, obj):
        return obj.user.id
    def get_username(self,obj):
        return obj.user.username
    def get_class_details(self,obj):
        batch=StudentBatch.objects.filter(student=obj.id)
        serializers=StudentBatchSerializer(batch,many=True)
        return serializers.data
    def get_photo(self,obj):
        try:
            return obj.photo.url
        except:
            return None
        
class PollFightQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model =PollFightQuestion
        exclude=['is_delete']

    def validate(self, data):
        # Perform your custom validation here
        status = data.get('status', None)
        if status and PollFightQuestion.objects.filter(status=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("There can only be one instance with status=True.")
        
        return data


class PollFightQuestionRetrieveSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    class Meta:
        model =PollFightQuestion
        exclude=['is_delete']

    def get_question(self,obj):
        print("hhhhhh")
        id = self.context.get('ids')
        question_text = self.context.get('question_text')
        paginated = self.context.get('paginated')
        print(question_text,"id")
       
        queryset=NewQuestionPool.objects.filter(id__in=obj.question.all().values('id'))
        print(len(queryset))
        if id:
            queryset=queryset.filter(id=id)
        if question_text:
            queryset=queryset.filter(question_text__icontains=question_text)
        ser=QustionpoolNewSmall(queryset,many=True)
        page =paginated(queryset)
        if page is not None:
            serializer = QustionpoolNewSmall(page,many=True)
            # return self.get_paginated_response({"data": serializer.data})
        return ser.data
    
    def validate(self, data):
        # Perform your custom validation here
        status = data.get('status', None)
        if status and PollFightQuestion.objects.filter(status=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("There can only be one instance with status=True.")
        
        return data


# @receiver(pre_save, sender=PollFightLobby)
# def send_question_pollfight(sender, instance, **kwargs):
#     users=[instance.user1,instance.user2]
#     if instance.user1 and instance.user2 :
#         for i in users:
#             if i and i != instance.created_by.id:
#                 user_id=str(i)
#                 # print(user_id)
#                 ser=PollFightSubmitSerializer(instance)

#                 channel_layer = get_channel_layer()
#                 print(channel_layer,"hhhhh")
#                 data=json.dumps(ser.data)
#                 async_to_sync(channel_layer.group_send)(
#                     f"{user_id}",  # Use the recipient's group
#                     {"type": "group_message", "message": data}
#                 )

#     pass


class PollFightLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model= PollFightLobby
        exclude=[]

class TimeTableNewSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()
    approvals_user = serializers.SerializerMethodField()
    app_status=serializers.SerializerMethodField()
    class Meta:
        model=TimeTable
        exclude=[]

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.name

    def get_course_name(self, obj):
        return obj.course.name

    def get_status(self, obj):
        a = Approvals.objects.filter(faculty=AuthHandlerIns.get_id(
            request=self.context['request']), timetable=obj.id)
        if a:
            return True
        else:
            return False
    def get_subtopic(self,obj):
        subtopic=Subtopic_batch.objects.filter(topic=obj.topic)
        serilizer= Subtopic_batchSerializer(subtopic, many=True)
        return serilizer.data
    
    def get_approvals_user(self, obj):
        a = Approvals.objects.filter(faculty=AuthHandlerIns.get_id(
            request=self.context['request']), timetable=obj.id)
        
        ser = Approvalserializers(a, many=True)
        return ser.data
    
    def get_app_status(self,obj):
        key=''
        if not obj.faculty:
            key= "Available"
        if  Approvals.objects.filter(faculty=AuthHandlerIns.get_id(request=self.context['request']), timetable=obj.id).exists() and obj.faculty is None :
            key= "Applied"
        try:
            if obj.faculty.id ==AuthHandlerIns.get_id(request=self.context['request']) and obj.topic.status=='B':
                key= "Booked"
            if obj.faculty.id ==AuthHandlerIns.get_id(request=self.context['request']) and obj.topic.status=='F':
                key= "Finished"
        except:
            pass
        # key= "Other"
        return key


class ImageSerializerChat(serializers.ModelSerializer):
    class Meta:
        model=CommunityImage
        exclude=['is_delete']

    # def validate_image(self,data):
    #     return data
    
    # def is_valid(self, raise_exception=False):
    #     # Perform your custom validation logic here
    #     # You can access and validate the serializer's data and fields

    #     # Example: Check a specific condition
    #     # if not self.valid_condition():
    #     print("sssssssssssssssssssssssssssss",self.validators)
    #     #     self._errors['custom_field'] = ['Custom validation failed.']

    #     # Continue with the default is_valid method
    #     return super().is_valid(raise_exception=raise_exception)
    # def validate(self, attrs):
    #     print("ooooooooooooooooooooooooooooooooo")
    #     _, image_data = attrs.split(';base64,')
                
    #     # Decode the base64 data and create a ContentFile
    #     decoded_image = base64.b64decode(image_data)
    #     content_file = ContentFile(decoded_image, name='icon.png')

        
    #     return content_file
class PostsSerializer(serializers.ModelSerializer):
    images=ImageSerializerChat(many=True)
    class Meta:
        model=Posts
        exclude=[]

    def create(self, validated_data):
        # Extract data for related images
        images_data = validated_data.pop('images', [])
        post = Posts.objects.create(**validated_data)
        arr=[]
        # Create related images
        for image_data in images_data:
            arr.append(CommunityImage.objects.create(**image_data))

        post.images.set(arr)

        return post

  
        


class GroupMCQSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    class Meta:
        model=GroupMCQ
        exclude=['is_delete']
        
    def get_username(self,obj):
        if obj.created_by:
            return obj.created_by.username
        return None
class GroupChatSerializer1(serializers.ModelSerializer):
    post=PostsSerializer(read_only=True)
    mcq=GroupMCQSerializer(read_only=True)

    class Meta:
        model=GroupChat
        exclude=[]
class GroupChatSerializer(serializers.ModelSerializer):
    post=PostsSerializer()
    mcq=GroupMCQSerializer()
    # post=serializers.SerializerMethodField() 
    # mcq=serializers.SerializerMethodField()
    # test=serializers.SerializerMethodField()
    type=serializers.SerializerMethodField() 
    likes=serializers.SerializerMethodField()
    upvotes=serializers.SerializerMethodField()
    liked=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()

    class Meta:
        model=GroupChat
        exclude=[]

    def get_type(self,obj):
        return  "Mcq" if obj.mcq else "Post"
    
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='CHAT').count()
    
    def get_liked(self,obj):
        user_id = self.context['user']
        return Likes.objects.filter(like_assign='CHAT',liked_id=obj.id,user__id=user_id).exists()
    
    def get_comments(self,obj):
        return Comments.objects.filter(comment_assign='CHAT').count()
    
    def get_upvotes(self,obj):
        user_id = self.context['user']
        return UpVotes.objects.filter(user__id=user_id,chat=obj).count()



    # def get_post(self,obj):
    #     post=Posts.objects.get()
    #     ser=PostsSerializer()

    #     return

    # def get_test(self,obj):
    #     print(self.)
    #     return None

    # def create(self, validated_data):
    #     print(validated_data)
    #     # return
    #     # print(self.post)
    #     postser=PostsSerializer(data=validated_data['post'])
    #     mcqser=GroupMCQSerializer(data=validated_data['mcq'])
    #     data=''
    #     grpchatser=GroupChatSerializer(data={'group':validated_data['group'],'created_by':validated_data['created_by']})
    #     if grpchatser.is_valid(raise_exception=True):
    #         print("hhhhhhhhhhhhhhhhhhhhhhh")
    #     if  postser.is_valid(raise_exception=True):
    #         print("hellllllloooooooooooooo")
    #         pass
    #     else:
    #         mcqser.is_valid(raise_exception=True)



    #     return super().create(validated_data)

        
class GroupSerializer(serializers.ModelSerializer):
    course_name=serializers.SerializerMethodField()
    category_name=serializers.SerializerMethodField()
    level_name=serializers.SerializerMethodField()
    course_obj=serializers.SerializerMethodField()
    category_obj=serializers.SerializerMethodField()
    level_obj=serializers.SerializerMethodField()

    class Meta:
        model=Groups
        exclude=[]

    def get_course_name(self,obj):
        try:
            return obj.course.name
        except:
            return None
        
    def get_category_name(self,obj):
        try:
            return obj.category.name
        except:
            return None
        
    def get_level_name(self,obj):
        try:
            return obj.level.name
        except:
            return None
        
    def get_course_obj(self,obj):
        try:
            return CourseSerializer(Course.objects.get(id=obj.course.id) ,many=False).data
        except:

            return None
        
    def get_category_obj(self,obj):
        try:
            
            return CategorySeriaizerSmall(Category.objects.get(id=obj.category.id) ,many=False).data
        except:
            try:
                return CategorySeriaizerSmall(Category.objects.get(id=obj.level.category.id),many=False).data
            except:
                return CategorySeriaizerSmall(Category.objects.get(id=obj.course.level.category.id),many=False).data

            return None
        
    def get_level_obj(self,obj):
        try:
            return  LevelSeriaizerSmall(Level.objects.get(id=obj.level.id) ,many=False).data
            return obj.level.name
        except:
            try:
                return LevelSeriaizerSmall(Level.objects.get(id=obj.course.level.id),many=False).data
            except:
                return None
        

class GroupUserSerializer(serializers.ModelSerializer):
    members_count=serializers.SerializerMethodField()
    
    class Meta:
        model=Groups
        exclude=['is_delete','members','admins']

    def get_members_count(self,obj):
        return obj.members.all().count()
    
class UserSerializerLobbyList(serializers.ModelSerializer):
    photos=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['username','photos']

    def get_photos(self,obj):
        try:
            print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            stu=Student.objects.get(user__id=obj.id).photo
            return stu.url
        except Exception as e:
            print(e)
            return None


class UserSerializerGroupList(serializers.ModelSerializer):
    photos=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id','username','photos','email','mobile','is_student','is_staff','is_faculty','is_roleuser']

    def get_photos(self,obj):
        try:
            print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            stu=Student.objects.get(user__id=obj.id).photo
            return stu.url
        except Exception as e:
            print(e)
            try:
                return Faculty.objects.get(user__id=obj.id).photo.url
            except:
                pass
            return None

class FacultyTimetableAppDashboardSerializer(serializers.ModelSerializer):
    # date=serializers.SerializerMethodField()
    batch=serializers.SerializerMethodField()
    branch=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    room=serializers.SerializerMethodField()
    time=serializers.SerializerMethodField()
    strength=serializers.SerializerMethodField()
    class Meta:
        model = TimeTable
        exclude=['is_delete']

    def get_batch(self,obj):
        return obj.batch.name
    
    def get_branch(self,obj):
        return obj.batch.branch.name

    def get_course(self,obj):
        return obj.course.name
    
    def get_room(self,obj):
        if obj.room:
            return obj.room.name
        return None
    
    def get_time(self,obj):
        return "12:00:PM"
    
    def get_strength(self,obj):
        return obj.batch.strength
    # def get_date(self,obj):


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        exclude=[]
        
class FacultyFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyFeedback
        fields = '__all__'

class QuestionpaperattendSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuestionpaperAttend
        exclude=['is_delete']
from celery import shared_task

@shared_task
async def send_periodic_message():
    while True:
        channel_layer = get_channel_layer()
        print("newwww")
        # Send the message asynchronously using await
        await async_to_sync(channel_layer.group_send)(
            f"test",  # Use the recipient's group
            {"type": "group_message", "message": "hi"}
        )

        # Schedule the next message sending
        await asyncio.sleep(5)


class StudentFeeUpdationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeCollection
        fields = ['study_materials', 'publications', 'question_banks']

class StartPurchaseQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=PackageQuizPoolUserRoom
        fields=['id','question_paper','user','start_time','video_package','Exampaper_package','count']

class PurchaseQuizInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuestionPaper
        fields='__all__'


class QuestionGetQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model=PackageQuizPoolAnswers
        fields=['id','room','question_copy','option_1','option_2','option_3','option_4','option_5','answer']


class PurchaseQuizCompleteSerializer(serializers.ModelSerializer):
    end_time=serializers.SerializerMethodField()
    attendquestions=serializers.SerializerMethodField()
    skippedquestions=serializers.SerializerMethodField()
    total_score=serializers.SerializerMethodField()
    correct_answer=serializers.SerializerMethodField()
    wrong_answer=serializers.SerializerMethodField()
    timespent=serializers.SerializerMethodField()

    class Meta:
        model=PackageQuizPoolUserRoom
        fields=['id','question_paper','user','date','total_score','start_time','end_time','video_package','Exampaper_package','count','attendquestions','skippedquestions','correct_answer','wrong_answer','timespent']

    def get_end_time(self,obj):
        obj.end_time=datetime.now()
        return obj.end_time
    def get_attendquestions(self,obj):
        print(obj.id,'id')
        print(PackageQuizPoolAnswers.objects.filter(room=obj.id),'sss')
        attendquestions = PackageQuizPoolAnswers.objects.filter(room=obj.id).filter(answer__isnull=False).count()        
        return attendquestions
    def get_skippedquestions(self,obj):
        skippedquestions = PackageQuizPoolAnswers.objects.filter(room=obj.id).filter(answer__isnull=True).count()        
        return skippedquestions
    def get_correct_answer(self,obj):
        correct = PackageQuizPoolAnswers.objects.filter(room=obj.id, answer=F('crct_answer')).count()
        return correct
    def get_wrong_answer(self,obj):
        wrong=PackageQuizPoolAnswers.objects.filter(room=obj.id).exclude(answer=F('crct_answer')).count()
        return wrong
    def get_total_score(self,obj):
        mark=PackageQuizPoolUserRoom.objects.get(id=obj.id)
        postivemark=QuestionPaper.objects.get(id=mark.question_paper.id)
        total_score = (self.get_correct_answer(obj) * postivemark.positivemark) - (self.get_wrong_answer(obj) * postivemark.negativemark)
        mark.total_score=total_score
        mark.save()

        return total_score
    
    def get_timespent(self, obj):
        if obj.start_time and obj.end_time:
            start_time = obj.start_time
            end_time = obj.end_time

            # Ensure both start_time and end_time are timezone-aware
            if not start_time.tzinfo:
                start_time = timezone.make_aware(start_time, timezone.utc)
            if not end_time.tzinfo:
                end_time = timezone.make_aware(end_time, timezone.utc)

            # Calculate the time spent as a timedelta
            time_spent = end_time - start_time

            # Extract the total minutes from the timedelta
            total_seconds = time_spent.total_seconds() 
            total_minutes = round(total_seconds / 60, 2)

            return total_minutes

        return None 
        
    
    
class QuizInstructionSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model=QuestionPaper
        fields=['id','name','instruction','positivemark','negativemark','duration']

class AnswerKeySerializer(serializers.ModelSerializer):
    question= serializers.CharField(source='question.question_text', read_only=True)
    class Meta:
        model=PackageQuizPoolAnswers
        fields=['id','room','question','option_1','option_2','option_3','option_4','option_5','answer','crct_answer']

    def get_question(self,obj):
        questionext=NewQuestionPool.objects.get(id=obj.question.id)
        return questionext.question_text
class LeaderBoardSerializer(serializers.ModelSerializer):
    user=staffserializerSmall()
    leaderboard = serializers.SerializerMethodField()
    rank=serializers.SerializerMethodField()
    class Meta:
        model=PackageQuizPoolUserRoom
        fields=['id','total_score','user','leaderboard','rank']


    def get_leaderboard(self, instance):
        # Calculate the leaderboard position based on total_score
        max_score = PackageQuizPoolUserRoom.objects.aggregate(Max('total_score'))['total_score__max']
        return instance.total_score == max_score
    

    def get_rank(self, obj):
        user_id = obj.user_id
        rank = PackageQuizPoolUserRoom.objects.filter(
            Exampaper_package=obj.Exampaper_package,  # Filter by the same Exampaper_package
            total_score__gt=obj.total_score
        ).count() + 1  # +1 because ranks start from 1

        # Now, check if this record belongs to the authenticated user
        request_user_id = self.context['id']
        is_request_user = user_id == request_user_id

        return {
            'rank': rank,
            'is_request_user': is_request_user,
        }


class LeaderBoardSerializerUser(serializers.ModelSerializer):
    user=staffserializerSmall()
    leaderboard = serializers.SerializerMethodField()
    # rank=serializers.SerializerMethodField()
    class Meta:
        model=PackageQuizPoolUserRoom
        fields=['id','total_score','user','leaderboard']


    def get_leaderboard(self, instance):
        # Calculate the leaderboard position based on total_score
        max_score = PackageQuizPoolUserRoom.objects.aggregate(Max('total_score'))['total_score__max']
        return instance.total_score == max_score
class CoursePackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']
class CoursePackageLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields=['id','name']
class CoursePackageCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','name']
class CoursePackageSerializer(serializers.ModelSerializer):
    benifites = serializers.SerializerMethodField()
    category=serializers.SerializerMethodField()
    level=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()

    class Meta:
        model = OnlineCoursePackage
        fields = "__all__"

    def get_benifites(self, obj):
        # Split the comma-separated values into a list
        benifites_str = obj.benifites
        if benifites_str:
            return benifites_str.split(',')
        return []
    
    def get_course(self,obj):
        queryset=Course.objects.get(id=obj.course.id)
        serializers=CoursePackageCourseSerializer(queryset)
        return serializers.data
    
    def get_level(self,obj):
        queryset=Level.objects.get(id=obj.course.level.id)
        serializers=CoursePackageLevelSerializer(queryset)
        return serializers.data
    
    def get_category(self,obj):
        queryset=Category.objects.get(id=obj.course.level.category.id)
        serializers=CoursePackageCategorySerializer(queryset)
        return serializers.data
    

class CoursePackageSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = OnlineCoursePackage
        fields = "__all__"

class livezoomSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()

    class  Meta:
        model = ZoomMeetings
        fields = '__all__'

    def get_category(self,obj):
        try:
            return obj.category.name
        except:
            return None

    def get_level(self,obj):
        try:
            return obj.level.name
        except:
            return None
    def get_course(self,obj):
        try:
            return obj.course.name
        except:
            return None
        
    def get_subject(self,obj):
        try:
            return obj.subject.name
        except:
            return None
    def get_module(self,obj):
        try:
            return obj.module.name
        except:
            return None
    
    def get_topic(self,obj):
        try:
            return obj.topic.name
        except:
            return None


    def get_subtopic(self,obj):
        try:
            return obj.subtopic.name
        except:
            return None




class livezoomAppSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()

    class  Meta:
        model = ZoomMeetings
        exclude = ['is_delete','created_by','status']

    def get_category(self,obj):
        try:
            return obj.category.name
        except:
            return None

    def get_level(self,obj):
        try:
            return obj.level.name
        except:
            return None
    def get_course(self,obj):
        try:
            return obj.course.name
        except:
            return None
        
    def get_subject(self,obj):
        try:
            return obj.subject.name
        except:
            return None
    def get_module(self,obj):
        try:
            return obj.module.name
        except:
            return None
    
    def get_topic(self,obj):
        try:
            return obj.topic.name
        except:
            return None


    def get_subtopic(self,obj):
        try:
            return obj.subtopic.name
        except:
            return None



class NoticeBoardSerailizer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()


    class Meta:
        model = NoticeBoard
        exclude = ['is_delete']
    
    def get_branch_name(self,obj):
        try:

            return obj.branch.name
        except:
            return None

    def get_batch_name(self,obj):
        try:
            return obj.batch.name
        except:
            return None


class NoticeBoardUserSerailizer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()


    class Meta:
        model = NoticeBoard
        exclude = ['is_delete']
    
    def get_branch_name(self,obj):
        try:
            return obj.branch.name
        except:
            return None

    def get_batch_name(self,obj):
        try:
            return obj.batch.name
        except:
            return None

class VideoClassesBatchSerializer(serializers.ModelSerializer):
    video_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    subtopic_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = VideoClassesBatch
        exclude = ['is_delete']

    def get_video_name(self,obj):
        return obj.video.name
    
    def get_batch_name(self,obj):
        return obj.batch.name
    
    def get_subtopic_name(self,obj):
        
        return obj.subtopic.name
    
    def get_topic_name(self,obj):
        return obj.topic.name
    
    def get_module_name(self,obj):
        return obj.module.name
    
    def get_subject_name(self,obj):
        return obj.subject.name
    
class VideoClassesBatchUserSerializer(serializers.ModelSerializer):
    video_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    subtopic_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = VideoClassesBatch
        exclude = ['is_delete']

    def get_video_name(self,obj):
        return obj.video.name
    
    def get_batch_name(self,obj):
        return obj.batch.name
    
    def get_subtopic_name(self,obj):
        try:
            return obj.subtopic.name
        except:
            return None
    
    def get_topic_name(self,obj):
        try:
            return obj.topic.name
        except:
            return None
        
    def get_module_name(self,obj):
        try:
            return obj.module.name
        except:
            return None
        
    def get_subject_name(self,obj):
        try:
            return obj.subject.name
        except:
            return None
        
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.video.id).count()
    
    def get_liked(self,obj):
        return Likes.objects.filter(like_assign='VIDEOS',liked_id=obj.video.id).exists()
    
    def get_video_link(self,obj):
      
        data = url_encryption(obj.video)
        return  data
    
from django.db.models import DecimalField

class StudentFeeAppSerializer(serializers.ModelSerializer):

    batch=serializers.SerializerMethodField()
    branch=serializers.SerializerMethodField()
    batch_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    given_accessories=serializers.SerializerMethodField()
    

    class Meta:
        model = StudentBatch
        fields = ['id','batch', 'branch', 'batch_name', 'branch_name','student','given_accessories']

    def get_given_accessories(self,obj):
        print("         jjjjjjjjjjjjj        ")
        try:
            queryset=StudentFeeCollection.objects.filter(student=obj.student.user,batch_package__batch=obj.batch)
            batch_package =BatchPackages.objects.filter(batch__id=obj.batch.id).annotate(
                        total_study_material_price=Sum(F('study_meterial__book_price'), output_field=DecimalField()),
                        total_question_book_price=Sum(F('question_book__book_price'), output_field=DecimalField()),
                        total_publications_price=Sum(F('publications__book_price'), output_field=DecimalField())
                    ).annotate(grand_total=F('total_study_material_price')+F('total_question_book_price')+F('total_publications_price')+F('batch__fees'))
                
            grand_total = batch_package.first().grand_total
            total_fee_paid = queryset.aggregate(total = Sum('amountpaid'))
            balance_amount = grand_total - (total_fee_paid['total'] if total_fee_paid['total'] else 0)
            batchPAck=BatchPackages.objects.get(batch__id=obj.batch.id)
            total_publications=batchPAck.publications.all().values_list('id',flat=True)
            total_materials=batchPAck.study_meterial.all().values_list('id',flat=True)

            total_question=batchPAck.question_book.all().values_list('id',flat=True)
            print(total_publications.all().values_list('id',flat=True))
            data = {
                'batchPAckage':batchPAck.id,
                'total_fee_paid': total_fee_paid['total'],
                'publications':PublicationClassDetailSerializer(Publications.objects.filter(id__in=total_publications),many=True,context={"batch":obj.batch.id}).data,
                'materials':MaterialClassDetailSerializer(StudyMaterial.objects.filter(id__in=total_materials),many=True,context={"batch":obj.batch.id}).data,
                'question':QuestionBookClassDetailSerializer(QuestionBook.objects.filter(id__in=total_question),many=True,context={"batch":obj.batch.id}).data,
                'balance': balance_amount,
                'Total course fee':grand_total      
                          }

            return data
        except Exception as e:
            print(e,"    ::::::::::::::::::::;")
            return None
    def get_batch(self, obj):
        if obj.batch:
            return obj.batch.pk
        return None
    def get_branch(self, obj):
        if obj.branch:
            return obj.branch.pk
        return None
    def get_batch_name(self,obj):
        if obj.batch:
            return obj.batch.name
        return None
    def get_branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return None

class StudentTransactionSerializer(serializers.ModelSerializer):
    question_banks = serializers.SerializerMethodField()
    study_materials = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    class Meta:
        model = StudentFeeCollection
        fields = ['question_banks','study_materials','publications','amountpaid','created_at']
        

    def get_publications(self,obj):
        try:
            return PublicationsViewSerializer(obj.publications,many=True).data
        except:
            return None
    
    def get_study_materials(self,obj):
        try:
            return StudyMaterialViewSerializer(obj.study_materials,many=True).data
        except:
            return None
    
    def get_question_banks(self,obj):
        try:
            return QuestionBookViewSerializer(obj.question_banks,many=True).data
        except:
            return None
        
    
class UserLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
class PurchaseCoursepackageSerializer(serializers.ModelSerializer):
    class Meta:
        model=OnlineCoursePackage
        exclude=["created_at","created_by"]
class OnlineCoursePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineCoursePackage
        fields = ['id', 'name']  # Include the fields you want

class DayWiseOnlineCourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class DayWiseOnlineCourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    subject=serializers.SerializerMethodField()
    module=serializers.SerializerMethodField()
    class Meta:
        model = Topic
        fields = ['id', 'name','subject','module'] 

    def get_subject(self,obj):
        queryset=Subject.objects.get(id=obj.module.subject.id)
        serializer=DayWiseOnlineCourseSubjectSerializer(queryset)
        return serializer.data
    
    def get_module(self,obj):
        queryset=Module.objects.get(id=obj.module.id)
        serializer=DayWiseOnlineCourseModuleSerializer(queryset)
        return serializer.data
class DayWiseOnlineCourseSerializer(serializers.ModelSerializer):
    coursepackage  = OnlineCoursePackageSerializer(source="onlinecourse")  # Include the related OnlineCoursePackage
    topics = TopicSerializer(many=True)
    course=serializers.SerializerMethodField()
    
    class Meta:
        model=OnlineCourseOrder
        exclude=["created_at","is_delete"]

    def get_course(self,obj):
        online_course = obj.onlinecourse
        return {
            "id": online_course.course.id,
            "name": online_course.course.name
        }

    
class DayWiseOnlineCourseSerializerPost(serializers.ModelSerializer):
    class Meta:
        model=OnlineCourseOrder
        exclude=["created_at","is_delete"]


class StudentAttendanceGraphSerializer(serializers.ModelSerializer):
    subjects=serializers.SerializerMethodField()
    total=serializers.SerializerMethodField()
    attended=serializers.SerializerMethodField()
    skipped=serializers.SerializerMethodField()
    class Meta:
        model = Batch
        fields=['name','subjects','total','attended','skipped']

    def get_subjects(self,obj):
        subject=Subject_batch.objects.filter(batch=obj)
        user_id=self.context['user_id']
        serializer=SubjectBatchGraphSerializer(subject,many=True,context={'user_id':user_id})
        return serializer.data
    
    def get_total(self,obj):
        topics=Topic_batch.objects.filter(batch=obj)
        return topics.count()
    
    def get_attended(self,obj):
        user_id=self.context['user_id']
        attendance=StudentAttendance.objects.filter(timetable__batch=obj,student__id=user_id).distinct('timetable')
        return attendance.count()
    
    def get_skipped(self,obj):
        user_id=self.context['user_id']
        attendance=StudentAttendance.objects.filter(timetable__batch=obj,student__id=user_id).values_list('timetable',flat=True)
        timetable=TimeTable.objects.filter(batch=obj,topic__status='F').exclude(id__in=attendance)
        return timetable.count()


    

class SubjectBatchGraphSerializer(serializers.ModelSerializer):
    # percentage=serializers.SerializerMethodField()
    total_classes=serializers.SerializerMethodField()
    attended_classes=serializers.SerializerMethodField()
    skipped_classes=serializers.SerializerMethodField()
    class Meta:
        model = Subject_batch
        fields=['name','total_classes','attended_classes','skipped_classes']

    def get_total_classes(self,obj):
        # timetable=TimeTable.objects.filter(topic__module__subject=obj)
        topics=Topic_batch.objects.filter(module__subject=obj)
        return topics.count()

    def get_attended_classes(self,obj):
        timetable=TimeTable.objects.filter(topic__module__subject=obj).values_list('id',flat=True)
        user_id=self.context['user_id']
        student_attended=StudentAttendance.objects.filter(timetable__id__in=timetable,student__id=user_id).distinct('timetable')
        return student_attended.count()

    def get_skipped_classes(self,obj):
        user_id=self.context['user_id']
        student_attended=StudentAttendance.objects.filter(student__id=user_id).values_list('timetable',flat=True)
        timetable=TimeTable.objects.filter(topic__module__subject=obj,topic__status='F').exclude(id__in=student_attended)
        return timetable.count()


class OfflineExamSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExamQuestionPaper
        fields="__all__"


class ExamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ExamCategory
        exclude=["is_delete"]

class ExamQuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExamQuestionPaper
        exclude=['']


class UpVotesSerializerUser(serializers.ModelSerializer):
    class Meta:
        model=UpVotes
        exclude=['is_delete']


class SubjectBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject_batch
        exclude=['is_delete']