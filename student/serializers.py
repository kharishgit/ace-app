from rest_framework import serializers
from .models import *
from accounts.models import *
from course.models import *
from MobileApp.models import *
from course.serializers import *
from accounts.api.serializers import *
class studentlogin(serializers.ModelSerializer):
    def validate_mobile(self,value):
        if Student.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("mobile number already exists")
    
    mobile=serializers.IntegerField(required=True)
    class Meta:
        model=Student
        fields=('mobile',)
        
        
class offlineserializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        exclude = ('otp','is_active','admission_date')
        

class StudentForExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields = "__all__"


class StudentloginSeializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('mobile')

class StudentBathcSerializer(serializers.ModelSerializer):
    class Meta:
        model=Batch
        fields='__all__'
class StudetnBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields='__all__'




class StudentBatchSerialiazer(serializers.ModelSerializer):
    batch=StudentBathcSerializer()
    branch=StudetnBranchSerializer()
    class Meta:
        model=StudentBatch
        fields='__all__'



class StudentTimetableserializers(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subject_name=serializers.SerializerMethodField()
    subtopic_list = serializers.SerializerMethodField()
    topic_id = serializers.SerializerMethodField()
    student_materials = serializers.SerializerMethodField()
    faculty_details = serializers.SerializerMethodField()
    faculty_rating = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    combined = serializers.SerializerMethodField()
    studentbatches=serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField() 
    rating_status = serializers.SerializerMethodField()


    class Meta:
        model = TimeTable
        fields = '__all__'

    def get_topic_id(self,obj):
        return obj.topic.topic.topic.id

    def get_student_materials(self,obj):
        try:
            user=obj.faculty
            topic = obj.topic.topic.topic
            subtopics = SubTopic.objects.filter(topic=topic).values_list('id',flat=True)
            newmatref_ids = MaterialReference.objects.filter(subtopic__in=subtopics,user=user).values_list('materialupload',flat=True)
            new_material = MaterialUploads.objects.filter(id__in=newmatref_ids)
            new_material=new_material.filter(Q(vstatus_research=True)| Q(vstatus_faculty=True))
            material = MaterialForStudentsSerializer(new_material,many=True)
            return material.data
        except:
            return None
        
        

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.topic.topic.name

    def get_course_name(self, obj):
        return obj.course.course.course.name
    
    def get_subject_name(self,obj):
        courseid=obj.course.id
        subject=obj.topic.module.subject
        return subject.name


    def get_faculty_details(self, obj):
        if obj.faculty:
            fac = Faculty.objects.get(user=obj.faculty.id)
            facs = FacultySerializerssProfile(fac)
            return facs.data
        else:
            return None

    def get_faculty_rating(self, obj):
        if obj.faculty:
            tim = TimeTable.objects.filter(faculty=obj.faculty.id).values('id')
            rating = Rating.objects.filter(
                rating_on__in=tim).aggregate(Avg('choice'))
            return rating['choice__avg']
        else:
            return None

    def get_faculty_phone(self, obj):
        if obj.faculty:
            return obj.faculty.mobile
        else:
            return None


    def get_status(self, obj):
        return obj.topic.status
    
    def get_subtopic_list(self, obj):
        subtopic = Subtopic_batch.objects.filter(topic=obj.topic)
        serializer =Subtopic_batchSerializer(subtopic, many=True)
        return serializer.data

    def get_combined(self, obj):
        if obj.is_combined:
            timetable  = TimeTable.objects.filter(date=obj.date,batch__in=obj.combined_batch.all())
            serializer= TimetableserializersCombined(timetable, many=True)
            return serializer.data
        else:
            return None
        
    def get_studentbatches(self, obj):
        try:
            student_id = self.context.get('student_id')
            studentbatch = StudentBatch.objects.filter(student_id=student_id)
            serializer=StudentBatchSerializer(studentbatch,many=True)
            return serializer.data
        except :
            return None
 
    def get_rating(self,obj):
        return self.context['status'] 
    
    def get_rating_status(self,obj):
        student_id = self.context.get('student_id')
        studentuser = Student.objects.get(id=student_id)
        userid = studentuser.user.id
        rating = Rating.objects.filter(rating_on__id=obj.id,user=userid)
        if rating:
            return True
        else:
            return False
        

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class PublicationClassDetailSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    class Meta:
        model=Publications
        fields=['bookname','id','status']
    def get_status(self,obj):
        batch = self.context.get('batch')
        return StudentFeeCollection.objects.filter(publications=obj.id,batch_package__batch__id=batch).exists()
    
class MaterialClassDetailSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    class Meta:
        model=StudyMaterial
        fields=['bookname','id','status']
    def get_status(self,obj):
        batch = self.context.get('batch')
        return StudentFeeCollection.objects.filter(study_materials=obj.id,batch_package__batch__id=batch).exists()
    
class QuestionBookClassDetailSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    class Meta:
        model=QuestionBook
        fields=['bookname','id','status']
    def get_status(self,obj):
        batch = self.context.get('batch')
        return StudentFeeCollection.objects.filter(question_banks=obj.id,batch_package__batch__id=batch).exists()

from django.db.models import DecimalField
    
class StudentBatchSerializer(serializers.ModelSerializer):
    batch=serializers.SerializerMethodField()
    branch=serializers.SerializerMethodField()
    batch_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    given_accessories=serializers.SerializerMethodField()

    class Meta:
        model = StudentBatch
        fields = ['id','batch', 'branch', 'batch_name', 'branch_name','student','given_accessories']

    def get_given_accessories(self,obj):
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
                'balance': balance_amount       
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






class StudentSyllabusSerializer(serializers.ModelSerializer):
    batch=serializers.SerializerMethodField()
    branch=serializers.SerializerMethodField()
    batch_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    given_accessories=serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentBatch
        fields = ['id','batch', 'branch', 'batch_name', 'branch_name','student_name','given_accessories']

    def get_given_accessories(self,obj):
        try:
            queryset=StudentFeeCollection.objects.filter(student=obj.student.user,batch_package__batch=obj.batch)
            print("          qqq       ",queryset)
            batch_package =BatchPackages.objects.filter(batch__id=obj.batch.id).annotate(
                        total_study_material_price=Sum(F('study_meterial__book_price'), output_field=DecimalField()),
                        total_question_book_price=Sum(F('question_book__book_price'), output_field=DecimalField()),
                        total_publications_price=Sum(F('publications__book_price'), output_field=DecimalField())
                    ).annotate(grand_total=F('total_study_material_price')+F('total_question_book_price')+F('total_publications_price'))
            print("            package             ",batch_package)
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
                'balance': balance_amount       
                          }

            return data
        except Exception as e:
            print(e,"    ::::::::::::::::::::;")
            return None
    def get_batch(self, obj):
        if obj.batch:
            return obj.batch.pk
        return None
    
    def get_student_name(self,obj):
        return obj.student.name
    
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


from accounts.models import UserManager
class StudentRegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model = Student
        fields = ['id','user','name', 'photo','exam_number', 'admission_number', 'father_name', 'guardian',
                  'guardian_name', 'guardian_mobile', 'dob', 'gender', 'marital_status',
                  'religion', 'caste', 'address', 'pincode', 'qualification', 'description', 'admission_date','photo','is_online','is_offline','admission_enquiry','scholarship']


class StudentFeeCollectionNewSerializer(serializers.ModelSerializer):
    publications = serializers.SerializerMethodField()
    study_materials = serializers.SerializerMethodField()
    question_banks = serializers.SerializerMethodField()


    class Meta:
        model = StudentFeeCollection
        fields = '__all__' 

    def get_publications(self,obj):
        print("Getting")
        return [publications.bookname for publications in obj.publications.all()]    
    
    def get_study_materials(self,obj):
        return [study_materials.bookname for study_materials in obj.study_materials.all()]       
   
    def get_question_banks(self,obj):
        return [question_banks.bookname for question_banks in obj.question_banks.all()]       


class BatchPackagesNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchPackages
        fields = '__all__'

class StudyMaterialNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields='__all__'

class StudyMaterialViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields=['bookname']

class QuestionBookNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBook
        fields='__all__'

class QuestionBookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBook
        fields=['bookname']
class PublicationsNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields='__all__'

class PublicationsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields=['bookname']


class AccessoriesNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeCollection
        fields='__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
       
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    joined_date = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class_details=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()
    # publications = serializers.SerializerMethodField()
    # pub_assigned=serializers.SerializerMethodField()

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
        stdentbatch=StudentBatch.objects.filter(student=obj.id)
        serializers=StudentBatchSerializer(stdentbatch,many=True)
        return serializers.data
    
    # def get_publications(self,obj):
    #     print("getPublic")
    #     publication = StudentFeeCollection.objects.filter(student=obj.user.id)
    #     print(publication,"PUBLICATIONS")
    #     serializer=StudentFeeCollectionNewSerializer(publication,many=True)
    #     return serializer.data
    # # def get_pub_assigned(self,obj):
    # #     try:
    # #         student_batch = StudentBatch.objects.get(student =obj.id)
    # #         batch = student_batch.batch
    # #         print(batch.id)
    # #         packagematerial = BatchPackages.objects.filter(batch = batch)
    # #         print(packagematerial,"PACKAGEMATERIAL")
    # #         serializers = BatchPackagesNewSerializer(packagematerial,many=True)
    # #         return serializers.data
    # #     except StudentBatch.DoesNotExist:
    # #         batch = None
    # def get_pub_assigned(self, obj):
    #     try:
    #         # Get the student's batch
    #         student_batch = StudentBatch.objects.get(student=obj.id)
    #         batch = student_batch.batch
    #         # Get the BatchPackages assigned to the batch
    #         batch_packages = BatchPackages.objects.filter(batch=batch)
    #         # Get the StudentFeeCollection objects for the student and batch
    #         student_fee_collection = StudentFeeCollection.objects.filter(
    #             student=obj.user, batch_package=batch.id
    #         )
    #     #     # Find the difference between BatchPackages and StudentFeeCollection
    #     #     assigned_study_materials = batch_packages.values_list(
    #     #         'study_meterial', flat=True
    #     #     )
    #     #     assigned_question_banks = batch_packages.values_list(
    #     #         'question_book', flat=True
    #     #     )
    #     #     assigned_publications = batch_packages.values_list(
    #     #         'publications', flat=True
    #     #     )

    #     #     not_given_study_materials = StudyMaterial.objects.filter(
    #     #         id__in=assigned_study_materials
    #     #     ).exclude(id__in=student_fee_collection.values_list(
    #     #         'study_materials', flat=True
    #     #     ))

    #     #     not_given_question_banks = QuestionBook.objects.filter(
    #     #         id__in=assigned_question_banks
    #     #     ).exclude(id__in=student_fee_collection.values_list(
    #     #         'question_banks', flat=True
    #     #     ))

    #     #     not_given_publications = Publications.objects.filter(
    #     #         id__in=assigned_publications
    #     #     ).exclude(id__in=student_fee_collection.values_list(
    #     #         'publications', flat=True
    #     #     ))

    #     #     # Serialize the data
    #     #     study_materials_serializer = StudyMaterialNewSerializer(
    #     #         not_given_study_materials, many=True
    #     #     )
    #     #     question_banks_serializer = QuestionBookNewSerializer(
    #     #         not_given_question_banks, many=True
    #     #     )
    #     #     publications_serializer = PublicationsNewSerializer(
    #     #         not_given_publications, many=True
    #     #     )

    #     #     return {
    #     #         'study_meterial': study_materials_serializer.data,
    #     #         'question_banks': question_banks_serializer.data,
    #     #         'publications': publications_serializer.data,
    #     #     }

    #     # except StudentBatch.DoesNotExist:
    #     #     return None
           
        
    #         # Create dictionaries to store the given status for each item type
    #         study_meterial_status = {}
    #         question_banks_status = {}
    #         publications_status = {}

    #         # Loop through the BatchPackages to check each item's status
    #         for package in batch_packages:
    #             for study_material in package.study_meterial.all():
    #                 study_meterial_name = study_material.bookname  # Use the name as the key
    #                 study_meterial_status[study_meterial_name] = study_meterial_name in student_fee_collection.values_list(
    #                     'study_materials__bookname', flat=True
    #                 )

    #             for question_book in package.question_book.all():
    #                 question_banks_name = question_book.bookname  # Use the name as the key
    #                 question_banks_status[question_banks_name] = question_banks_name in student_fee_collection.values_list(
    #                     'question_banks__bookname', flat=True
    #                 )

    #             for publication in package.publications.all():
    #                 publications_name = publication.bookname  # Use the name as the key
    #                 publications_status[publications_name] = publications_name in student_fee_collection.values_list(
    #                     'publications__bookname', flat=True
    #                 )

    #         return {
    #             'study_meterial': study_meterial_status,
    #             'question_banks': question_banks_status,
    #             'publications': publications_status,
    #         }

    #     except StudentBatch.DoesNotExist:
    #         return None

    
    
class StudentSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    joined_date = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'

    def get_email(self, obj):
        return obj.user.email
    def get_mobile(self, obj):
        return obj.user.mobile
    def get_joined_date(self, obj):
        return obj.user.joined_date

class FeePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeePayment
        fields = '__all__'

class CurrentAffairsSerializer(serializers.ModelSerializer):
    # course_name = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    class Meta:
        model = CurrentAffairs
        fields = ['id','title','description','file','vname','video','videolength','url','created_by','published','publish_on','created_at','icon','status','likes','liked']
    # def get_course_name(self, obj):
    #     return [course.name for course in obj.course.all()]
    def get_likes(self,obj):
        return Likes.objects.filter(like_assign='CURRENT_AFFAIRS',liked_id=obj.id).count()
    
    def get_liked(self,obj):
        user = self.context.get('user')
        return Likes.objects.filter(like_assign='CURRENT_AFFAIRS',liked_id=obj.id,user__id=user).exists()
    
class CurrentAffairsSerializerN(serializers.ModelSerializer):
    # course_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CurrentAffairs
        fields = ['id','title','description','file','vname','video','videolength','url','created_by','published','publish_on','created_at','icon','status']
    # def get_course_name(self, obj):
    #     return [course.name for course in obj.course.all()]
    

class StudentOrgerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()

    def get_userid(self, instance):
        return instance.user.id if instance.user else None

    studentotpid = serializers.SerializerMethodField()

    def get_studentotpid(self, instance):
        return None
    class Meta:
        model=Student
        fields=['userid','studentotpid']
    


class FirstregSerilizer(serializers.ModelSerializer):
    studentotpid = serializers.IntegerField(source='id')
    userid = serializers.SerializerMethodField(source='user')

    def get_userid(self, instance):
        return None

    class Meta:
        model = StudentOtp
        fields = ['userid','studentotpid']

class FirstregOtpSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    class Meta:
        model=StudentOtp
        fields='__all__'

    def get_user(self, obj):
        try:
            mobile = User.objects.get(mobile=obj.mobile)
            return True
        except User.DoesNotExist:
            return False


class OnllineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"


class StudentOTPBatchSerialiazer(serializers.ModelSerializer):
    # batch=StudentBathcSerializer()
    # branch=StudetnBranchSerializer()
    class Meta:
        model=StudentBatch
        fields='__all__'

class updateStudentBatchSerialiazer(serializers.ModelSerializer):
    batch=StudentBathcSerializer()
    branch=StudetnBranchSerializer()
    class Meta:
        model=StudentBatch
        fields='__all__'

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    course_det = serializers.SerializerMethodField()
    class Meta: 
        model = Publications
        fields = '__all__'
    def get_course_det(self,obj):
        return [course.name for course in obj.course.all()]

class FacutlyOrgerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()

    def get_userid(self, instance):
        return instance.user.id if instance.user else None

    studentotpid = serializers.SerializerMethodField()

    def get_studentotpid(self, instance):
        return None
    class Meta:
        model=Faculty
        fields=['userid','studentotpid']

class UserOrgerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()
    def get_userid(self, instance):
        return instance.id if instance.id else None
    
    studentotpid = serializers.SerializerMethodField()
    def get_studentotpid(self, instance):
        return None
    class Meta:
        model=User
        fields=['userid','studentotpid']

class EditStudentBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentBatch
        fields='__all__'


class StudentApplicationSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model= StudentApplicationOffline
        exclude=['is_delete']

    def get_branch_name(self, obj):
        return obj.branch.name
    
class dashboradserializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    selected_course = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    register_number = serializers.SerializerMethodField()
    coins = serializers.SerializerMethodField()
    level_id =  serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    


    class Meta:
        model = Student
        fields = ['id','name', 'photo','selected_course','course_id','level_id','category_id','username','user_id','user_email','mobile','exam_number','admission_number','register_number','coins']

    def get_username(self, obj):
        return obj.user.username

    def get_selected_course(self,obj):
        try:
            return obj.selected_course.name
        except:
            None
    def get_user_id(self,obj):
        return obj.user.id
    def get_user_email(self,obj):
        return obj.user.email
    def get_mobile(self,obj):
        return obj.user.mobile
    def get_course_id(self,obj):
        try:
            return obj.selected_course.id
        except:
            None  

    def get_category_id(self,obj):

        try:
            return obj.selected_course.level.category.id
        except:
            None

    def get_level_id(self,obj):
        try:
            return obj.selected_course.level.id
        except:
            None

    def get_register_number(self,obj):
        try:
            return obj.exam_number
        except:
            None     
    def get_coins(self,obj):
        try:
            return 0
        except:
            pass

class DeliveryaddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeliveryAddress
        exclude=['is_delete','created_at']



class Studentdeclarationserializer(serializers.ModelSerializer):
    class Meta:
        model=StudentDeclaration
        exclude=['is_delete','created_at']

class RankListSerializer(serializers.ModelSerializer):
    class Meta:
        model=RankList
        fields='__all__'
        
class AceRankHoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AceRankHolders
        fields = '__all__'