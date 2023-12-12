from course.serializers import TopicFulldetails
from rest_framework import serializers
from accounts.models import Faculty_Salary, SalaryFixation, User, Faculty, Permissions, Experience, FacultyCourseAddition
from django.core.validators import RegexValidator
from django.utils import timezone
from accounts.models import Material
from course.models import Course
from course.serializers import *
from accounts.models import *
from django.db.models import Count
from django.db.models import Q
class PermissionSerializer(serializers.Serializer):
    class Meta:
        model = Permissions
        fields = ['__all__']


class ExperienceSerializer(serializers.ModelSerializer):
    # level = ClassLevelSerializer(many=True)
    # name = FacultySerializer()

    class Meta:
        model = Experience
        fields = '__all__'

class UsercheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class AdminUserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'password']
        # fileds = '__all__'

    def get_name(self, obj):
        name = obj.username
        return name

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        instance.is_superuser = True
        instance.is_faculty = True
        instance.is_roleuser = True

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'password']
        # fileds = '__all__'

    def get_name(self, obj):
        name = obj.username
        return name

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class FacultySerializer(serializers.ModelSerializer):
    # course = serializers.StringRelatedField(many=True)
    # topic = serializers.StringRelatedField(many=True)
    def validate_whatsapp_contact_number(self, value):
        print(value,)
        if Faculty.objects.filter(whatsapp_contact_number=value).exists():
            raise serializers.ValidationError(
                "Whatsapp contact number already exists")

        return value

    def validate_date_of_birth(self, value):
        """
        Check that the date of birth is at least 18 years before the current date.
        """
        today = timezone.now().date()
        min_age = 18
        min_birth_date = today - timedelta(days=(365.25 * min_age))
        if value and value > today:
            raise serializers.ValidationError(
                "Date of birth cannot be in the future.")
        elif value and value > min_birth_date:
            raise serializers.ValidationError(
                f"You must be at least {min_age} years old.")
        return value
    # name = serializers.CharField(max_length=30, required=True)
    whatsapp_contact_number = serializers.CharField(
        min_length=10, required=True)
    pincode = serializers.CharField(validators=[RegexValidator(
        '^[0-9]{6}$', 'Enter a valid 6-digit PIN code.')])
    qualification = serializers.CharField(required=True)
    district = serializers.CharField(required=True, min_length=4)
    # name_user = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ( 'id','address','identity_card','photo','resume','gender', 'district', 'whatsapp_contact_number', 'date_of_birth', 'qualification', 'experiance_link','pincode','name')        # fields = '__all__'

    # def get_name_user(self, obj):
    #     return obj.user.username


class MaterialSerializer(serializers.ModelSerializer):
    faculty_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subtopics = serializers.SerializerMethodField()
    

    class Meta:
        model = Material
        # fields = ('id', 'category', 'level', 'faculty', 'course',
        #           'subject', 'module', 'topic', 'file', 'topic_faculty')
        fields = '__all__'
    def get_faculty_name(self,obj):
        return obj.faculty.name
    def get_category_name(self,obj):
        return obj.category.name
    def get_level_name(self,obj):
        return obj.level.name
    def get_course_name(self,obj):
        return obj.course.name
    def get_subject_name(self,obj):
        return obj.subject.name
    def get_module_name(self,obj):
        return obj.module.name
    def get_file_name(self,obj):
        return obj.file.url
    def get_topic_name(self,obj):
        return obj.topic.name
    def get_subtopics(self,obj):
        return [subtopic.name for subtopic in obj.subtopic.all()]
    
    




class AdminFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyCourseAddition
        # fields = ('course', 'subject', 'module', 'topic')
        exclude=('is_approved','status','user')

from course.serializers import TopicFulldetails
# class TopicFulldetails(serializers.ModelSerializer):
#     class Meta:
#         model = Topic


class facultyprofileserializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(many=True)
    subject = serializers.StringRelatedField(many=True)
    module = serializers.StringRelatedField(many=True)
    # topic = serializers.StringRelatedField(many=True)
    # subtopic = serializers.StringRelatedField(many=True)
    topic = TopicFulldetails(many=True)
    user = UserSerializer()

    class Meta:
        model = Faculty
        fields = '__all__'


# Write editprofileserializer
# class UserSerializereditprofile(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'mobile']


# class FacultyEditProfileSerializer(serializers.ModelSerializer):
#     # course = serializers.StringRelatedField(many=True)
#     # subject = serializers.StringRelatedField(many=True)
#     # module = serializers.StringRelatedField(many=True)
#     # # topic = serializers.StringRelatedField(many=True)
#     # # subtopic = serializers.StringRelatedField(many=True)
#     # topic = TopicFulldetails(many=True)
#     # user = UserSerializer()
#     course = CourseSerializer(many=True)
#     subject = SubjectSerializer(many=True)
#     module = ModuleSerializer(many=True)
#     topic = TopicSerializer(many=True)

#     class Meta:
#         model = Faculty
#         fields = ['address', 'gender', 'district', 'gender', 'date_of_birth',
#                   'qualification', 'experiance_link', 'mode_of_class', 'pincode',
#                   'expected_salary','course', 'subject', 'module', 'topic']

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user', None)
    #     if user_data:
    #         user_serializer = UserSerializereditprofile(instance.user, data=user_data)
    #         if user_serializer.is_valid():
    #             user_serializer.save()
    #         else:
    #             raise serializers.ValidationError(user_serializer.errors)

    #     return super().update(instance, validated_data)

class FacultyEditProfileSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), many=True)
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True)
    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), many=True)
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), many=True)

    class Meta:
        model = Faculty
        fields = ['address', 'gender', 'district', 'gender', 'date_of_birth',
                  'qualification', 'experiance_link', 'mode_of_class', 'pincode',
                'course', 'subject', 'module', 'topic']





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile')

class UserNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FacultySerializerforisverifiedandNOT(serializers.ModelSerializer):
    course = serializers.StringRelatedField(many=True)
    subject = serializers.StringRelatedField(many=True)
    module = serializers.StringRelatedField(many=True)
    # topic = serializers.StringRelatedField(many=True)
    # subtopic = serializers.StringRelatedField(many=True)
    topic = TopicFulldetails(many=True)
    user = UserSerializer()

    class Meta:
        model = Faculty
        fields = '__all__'

# class FacultyCourseAdditionSerializer(serializers.ModelSerializer):
#     # faculty = FacultySerializer()
#     # category = CategorySerializer(many=True)
#     # level = LevelSerializer(many=True)
#     # course = CourseSerializer(many=True)
#     # subject = SubjectSerializer(many=True)
#     # module = ModuleSerializer(many=True)
#     # topic = TopicSerializer(many=True)

#     class Meta:
#         model = FacultyCourseAddition
#         fields = '__all__'

#     def validate(self, data):
#         faculty = data.get('faculty')
#         courses = data.get('course')
#         subjects = data.get('subject')
#         modules = data.get('module')
#         topics = data.get('topic')
#         # print(faculty)
#         if courses and self.instance is None:
#             # Check if any of the courses are already added for the same faculty
#             existing_courses = FacultyCourseAddition.objects.filter(faculty=faculty, course__in=courses)
#             if existing_courses.exists():
#                 raise serializers.ValidationError("Duplicate Course found")

#         if subjects and self.instance is None:
#             # Check if any of the subjects are already added for the same faculty
#             existing_subjects = FacultyCourseAddition.objects.filter(faculty=faculty, subject__in=subjects)
#             if existing_subjects.exists():
#                 raise serializers.ValidationError("Duplicate subject found")

#         if modules and self.instance is None:
#             # Check if any of the modules are already added for the same faculty
#             existing_modules = FacultyCourseAddition.objects.filter(faculty=faculty, module__in=modules)
#             if existing_modules.exists():
#                 raise serializers.ValidationError("Duplicate module found")

#         if topics and self.instance is None:
#             # Check if any of the topics are already added for the same faculty
#             existing_topics = FacultyCourseAddition.objects.filter(faculty=faculty, topic__in=topics)
#             if existing_topics.exists():
#                 raise serializers.ValidationError("Duplicate topic found")

#         return data

# new faculty update in many to many


# class FacultyCourseAdditionSerializer(serializers.ModelSerializer):
#     # category = CategorySerializer(many=True)
#     # level = LevelSerializer(many=True)
#     # course = CourseSerializer(many=True)
#     # subject = SubjectSerializer(many=True)
#     # module = ModuleSerializer(many=True)
#     # topic = TopicSerializer(many=True)
#     # topic_name = serializers.Seri

#     class Meta:
#         model = FacultyCourseAddition
#         fields = ['id', 'user', 'category', 'level', 'course',
#                   'subject', 'module', 'topic', 'is_approved', 'status']


class FacultyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('photo', 'identity_card', 'resume')


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Question
#         fields=('question_text', 'option_1', 'option_2', 'option_3', 'option_4', 'option_5', 'answer')


# class QuestionPoolSerializer(serializers.ModelSerializer):
#     questions = QuestionSerializer(many=True)

#     class Meta:
#         model = QuestionPool
#         fields =('facultys', 'categorys', 'levels', 'course', 'topic', 'file_type', 'type', 'questions')

#     def create(self, validated_data):
#         questions_data = validated_data.pop('questions')
#         question_pool = QuestionPool.objects.create(**validated_data)
#         for question_data in questions_data:
#             Question.objects.create(question_pool=question_pool, **question_data)
#         return question_pool


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewQuestionPool
        fields = ('id', 'question_text', 'option_1', 'option_2',
                  'option_3', 'option_4', 'option_5', 'answer')


class QuestionPoolSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    categorysname=serializers.SerializerMethodField()
    levelsname=serializers.SerializerMethodField()
    coursename=serializers.SerializerMethodField()
    subjectname=serializers.SerializerMethodField()
    modulename=serializers.SerializerMethodField()
    topicname=serializers.SerializerMethodField()
    typename=serializers.SerializerMethodField()
    subtopicname=serializers.SerializerMethodField()
   

    class Meta:
        model = NewQuestionPool
        fields = '__all__'

    def get_username(self, obj):
        if obj.user is not None:
            return obj.user.username
        else:
            return None
        
    def get_categorysname(self, obj):
        if obj.categorys is not None:
            return obj.categorys.name
        else:
            return None
        
    def get_levelsname(self, obj):
        if obj.levels is not None:
            return obj.levels.name
        else:
            return None
        
    def get_coursename(self, obj):
        if obj.course is not None:
            return obj.course.name
        else:
            return None
        
    def get_subjectname(self, obj):
        if obj.subject is not None:
            return obj.subject.name
        else:
            return None

    
    def get_modulename(self,obj):
        if obj.module is not None:
                return obj.module.name
        else:
            return None
    
    def get_topicname(self,obj):
        if obj.topic is not None:
                return obj.topic.name
        else:
            return None
        

    def get_typename(self, obj):
        if obj.type:
            return dict(NewQuestionPool.TYPE).get(obj.type)
        else:
            return None
        
    
    def get_subtopicname(self,obj):
        if obj.subtopic:
            return obj.subtopic.name
        else:
            return None

# class UserSerializernew(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'mobile')

# class FacultyCourseAdditionSerializer(serializers.ModelSerializer):
#     # faculty=facultyviewDetails()
#     class Meta:
#         model = FacultyCourseAddition
#         fields = '__all__'


# class FacultyCourseAdditionsss(serializers.ModelSerializer):
    # class Meta:
    #     model=FacultyCourseAddition
    #     fields='__all__'

# class FacultyCourseAdditionsss(serializers.ModelSerializer):
#     category = CategorySerializer(many=True)
#     level = LevelSerializer(many=True)
#     course = CourseSerializer(many=True)
#     subject = SubjectSerializer(many=True)
#     module = ModuleSerializer(many=True)
#     topic = TopicSerializer(many=True)
#     faculty=facultyviewDetails()
#     class Meta:
#         model = FacultyCourseAddition
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)

#         # Convert IDs to names
#         data['category'] = [cat['name'] for cat in data['category']]
#         data['level'] = [lvl['name'] for lvl in data['level']]
#         data['course'] = [course['name'] for course in data['course']]
#         data['subject'] = [subj['name'] for subj in data['subject']]
#         data['module'] = [mod['name'] for mod in data['module']]
#         data['topic'] = [topic['name'] for topic in data['topic']]

#         return data
class FacultyCourseAdditionsss(serializers.ModelSerializer):
    # course = CourseSerializer()
    # category = CategorySerializer()
    # subject = SubjectSerializer()
    # module = ModuleSerializer()
    topic = TopicSerializer()
    batch_type_name=serializers.SerializerMethodField()
    # subtopic=serializers.SerializerMethodField()
    

    class Meta:
        model = FacultyCourseAddition
        fields = '__all__'

    def get_batch_type_name(self,obj):
        return obj.course.batch_type.name
    # def get_subtopic(self,obj):
    #     sub=Fa
    #     return obj.

# class FacultyCourseAdditionsss(serializers.ModelSerializer):
#     class Meta:
#         model=FacultyCourseAddition
#         fields='__all__'


class facultyviewDetails(serializers.ModelSerializer):
    user = UserSerializer()
    # faculty_course_addition = FacultyCourseAdditionsss(many=True)
    # courses = serializers.SerializerMethodField()
    # experiace = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_courses(self, obj):
        k = FacultyCourseAddition.objects.filter(user=obj.user.id).order_by('created_at')
        return FacultyCourseAdditionsss(k, many=True).data
    
    def get_pending(self,obj):
        return FacultyCourseAddition.objects.filter(user=obj.user.id,status="pending").count()

    def get_experiace(self, obj):
        exp = Experience.objects.filter(name=obj.id)
        return ExperienceSerializer(exp, many=True).data
    
    def get_rating(self, obj):
        rat = Rating.objects.filter(Q(rate_fac=obj) | Q(rating_on__faculty=obj.user )).values('choice')
        average_rating = rat.aggregate(avg_rating=Avg('choice'))['avg_rating']
        print(average_rating,"raaaaaaaaaaaaaaaaaaaaat")
        return average_rating
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     courses = representation['courses']
        
    #     sorted_courses = sorted(courses, key=lambda x: x['created_at'])
    #     representation['courses'] = sorted_courses
    #     return representation


class facultyviewDetailsProfile(serializers.ModelSerializer):
    user = UserSerializer()
    # faculty_course_addition = FacultyCourseAdditionsss(many=True)
    courses = serializers.SerializerMethodField()
    experiace = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_courses(self, obj):
        k = FacultyCourseAddition.objects.filter(user=obj.user.id).order_by('created_at')
        return FacultyCourseAdditionsss(k, many=True).data

    def get_experiace(self, obj):
        exp = Experience.objects.filter(name=obj.id)
        return ExperienceSerializer(exp, many=True).data
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     courses = representation['courses']
        
    #     sorted_courses = sorted(courses, key=lambda x: x['created_at'])
    #     representation['courses'] = sorted_courses
    #     return representation



class FacultyTopicsView(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_topics(self, obj):
        k = FacultyCourseAddition.objects.filter(user=obj.user.id)
        return FacultyCourseAdditionsss(k, many=True).data

# class FacultyTopicsView(serializers.ModelSerializer):
#     topics = serializers.SerializerMethodField()

#     class Meta:
#         model = Faculty
#         fields = '__all__'

#     def get_topics(self, obj):
#         # Get the faculty course addition details for the given faculty
#         faculty_course_additions = FacultyCourseAddition.objects.filter(user=obj.user.id)

#         # Serialize the faculty course additions
#         faculty_course_additions_data = FacultyCourseAdditionSerializer(faculty_course_additions, many=True).data

#         # Get the materials for the given faculty
#         materials = Material.objects.filter(faculty=obj.user.id)

#         # Serialize the materials
#         materials_data = MaterialSerializer(materials, many=True).data

#         # Combine the faculty course additions and materials data and return the final data
#         return faculty_course_additions_data + materials_data




class SalaryFixationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryFixation
        fields = '__all__'

class FacultySalarySerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    # fixed_salary = SalaryFixationSerializer() # Include nested serializer for fixed_salary

    class Meta:
        model = Faculty_Salary
        fields = '__all__'
    def get_level_name(self,obj):
        return obj.level.name
    def get_category_name(self,obj):
        return obj.level.category.name
    
class FacultySalaryFixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty_Salary
        fields = '__all__'

class FacultyList_AutoTimeTable_Topic_Serializer(serializers.ModelSerializer):
    faculty_rating = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    faculty_salary = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_faculty_rating(self, obj):
        if obj:
            tim = TimeTable.objects.filter(faculty=obj.id).values('id')
            rating = Rating.objects.filter(
                rating_on__in=tim).aggregate(Avg('choice'))
            return rating['choice__avg']
        else:
            return None
        
    def get_faculty_phone(self, obj):
        if obj:
            return obj.user.mobile
        else:
            return None
        
    def get_faculty_salary(self, obj):
        try:
            if obj:
                # fac = Faculty.objects.get(user=obj.user.id)
                fas=Faculty_Salary.objects.filter(faculty=obj,level=self.context['level'].id).first()
                print("kkkkkkkkkkkkkkkkkkkkkkk")
                if fas:
                    print(fas.fixed_salary)
                    return fas.fixed_salary.salaryscale
            return None
        except:
            return None

class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Declaration
        fields=('declaration',)
        

class FacultySerializerNew(serializers.ModelSerializer):
    
    # course = serializers.StringRelatedField(many=True)
    # topic = serializers.StringRelatedField(many=True)
    def validate_whatsapp_contact_number(self, value):
        print(value,)
        if Faculty.objects.filter(whatsapp_contact_number=value).exists():
            raise serializers.ValidationError("Whatsapp contact number already exists")

        return value

    def validate_date_of_birth(self, value):
        """
        Check that the date of birth is at least 18 years before the current date.
        """
        today = timezone.now().date()
        min_age = 18
        min_birth_date = today - timedelta(days=(365.25 * min_age))
        if value and value > today:
            raise serializers.ValidationError(
                "Date of birth cannot be in the future.")
        elif value and value > min_birth_date:
            raise serializers.ValidationError(
                f"You must be at least {min_age} years old.")
        return value
    # name = serializers.CharField(max_length=30, required=True)
    whatsapp_contact_number = serializers.CharField(
        min_length=10, required=True)
    pincode = serializers.CharField(validators=[RegexValidator(
        '^[0-9]{6}$', 'Enter a valid 6-digit PIN code.')])
    qualification = serializers.CharField(required=True)
    district = serializers.CharField(required=True, min_length=4)
    # name_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = ( 'id','address','gender', 'district', 'whatsapp_contact_number', 'date_of_birth', 'qualification', 'modeofclasschoice', 'experiance_link','pincode','name','user')


class NewFacultySalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty_Salary
        fields = [ 'faculty', 'level', 'exp_salary',]
        
class AdminsideFacultySerializerNew(serializers.ModelSerializer):
    
    # course = serializers.StringRelatedField(many=True)
    # topic = serializers.StringRelatedField(many=True)
    def validate_whatsapp_contact_number(self, value):
        print(value,)
        if Faculty.objects.filter(whatsapp_contact_number=value).exists():
            raise serializers.ValidationError("Whatsapp contact number already exists")

        return value

    def validate_date_of_birth(self, value):
        """
        Check that the date of birth is at least 18 years before the current date.
        """
        today = timezone.now().date()
        min_age = 18
        min_birth_date = today - timedelta(days=(365.25 * min_age))
        if value and value > today:
            raise serializers.ValidationError(
                "Date of birth cannot be in the future.")
        elif value and value > min_birth_date:
            raise serializers.ValidationError(
                f"You must be at least {min_age} years old.")
        return value
    # name = serializers.CharField(max_length=30, required=True)
    whatsapp_contact_number = serializers.CharField(
        min_length=10, required=True)
    pincode = serializers.CharField(validators=[RegexValidator(
        '^[0-9]{6}$', 'Enter a valid 6-digit PIN code.')])
    qualification = serializers.CharField(required=True)
    district = serializers.CharField(required=True, min_length=4)
    # name_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = ( 'id','address','gender', 'district', 'whatsapp_contact_number', 'date_of_birth', 'qualification', 'modeofclasschoice', 'experiance_link','pincode','name','user')


class FacultyCourseAdditionSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    # level = LevelSerializer(many=True)
    # course = CourseSerializer(many=True)
    # subject = serializers.SerializerMethodField()
    # # module = ModuleSerializer(many=True)
    # # topic = TopicSerializer(many=True)
    topic_name = serializers.SerializerMethodField()
    course_batch_type_name =serializers.SerializerMethodField()
    # facultyname = serializers.SerializerMethodField()
    # faculty_id = serializers.SerializerMethodField()
    class Meta:
        model = FacultyCourseAddition
        fields = '__all__'
        
    def get_topic_name(self, obj):
        return obj.topic.name
    def get_subject(self, obj):
        return obj.subject.name
    def get_facultyname(self,obj):
        return Faculty.objects.get(user=obj.user).name
    def get_faculty_id(self,obj):
        return Faculty.objects.get(user=obj.user).id
    
    def get_course_batch_type_name(self,obj):
        return obj.course.batch_type.name
       



class FacultyList_AutoTimeTable_Course_Serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()
    # user = UserSerializer()
    # course_adition = FacultyCourseAdditionSerializer()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_user(self, obj):
        userser=UserSerializer(User.objects.get(id=obj["user_id"])) 
        return userser.data
    
    def get_course(self, obj):
        fac=FacultyCourseAdditionSerializer(FacultyCourseAddition.objects.filter(user=obj["user_id"],course=self.context['course'].id), many=True)
        return fac.data
    
    def get_salary(self, obj):
        print(obj,"hellooo",self.context['level'].id)
        faculty_salary = Faculty_Salary.objects.filter(faculty=obj['id'],level=self.context['level'].id)
        if faculty_salary.exists():
            try:
                return faculty_salary[0].fixed_salary.salaryscale
            except:
                return "Not Fixed"
        else:
            return "Not Fixed"

class SpecialHolidaySerializer(serializers.ModelSerializer):
    batches = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all(), many=True)
    branches = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), many=True)
    levels = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), many=True)
    date=serializers.DateField(input_formats=["%d-%m-%Y"])

    class Meta:
        model = SpecialHoliday
        fields = ['id', 'name', 'date', 'batches','levels', 'branches']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        date_str = representation['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        representation['date'] = date_obj.strftime("%d-%m-%Y")
        return representation

class SpecialLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']

class SpecialBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']

class SpecialBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']


class GetSpecialHoliday(serializers.ModelSerializer):
    batches = SpecialBatchSerializer(many=True)
    branches = SpecialBranchSerializer(many=True)
    levels = SpecialLevelSerializer(many=True)
    date = serializers.DateField(input_formats=["%d-%m-%Y"])

    class Meta:
        model = SpecialHoliday
        fields = ['id', 'name', 'date', 'batches', 'levels', 'branches']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        date_str = representation['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        representation['date'] = date_obj.strftime("%d-%m-%Y")
        return representation
    
class UserSerializerQuestionSerch(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile')

class FacultyQuestionSerchserializer(serializers.ModelSerializer):
    user = UserSerializerQuestionSerch()

    class Meta:
        model = Faculty
        fields = ('id', 'user', 'name', 'photo')

class QuestionImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = QuestionImage
        fields = '__all__'

    def get_url(self, obj):
        return obj.questionimage.url
    
class QustionpoolNew(serializers.ModelSerializer):
    # published=serializers.SerializerMethodField()
    class Meta:
        model=NewQuestionPool
        fields=('id','user','categorys','levels','course','subject','module','topic','subtopic','question_text','option_1','option_2','option_3','option_4','option_5','answer','type','answerhint','status','publish')

    # def published(self,obj):

class QustionpoolNewone(serializers.ModelSerializer):
    # published=serializers.SerializerMethodField()
    class Meta:
        model=NewQuestionPool
        fields=('id','user','categorys','levels','course','subject','module','topic','subtopic','question_text','option_1','option_2','option_3','option_4','option_5','answer','type','answerhint','status','publish','add_user')


class QuestionPaperSerilizer(serializers.ModelSerializer):
    class Meta:
        model=QuestionPaper
        fields=('id','name','user','categorys','levels','course','subject','module','topic','instruction','positivemark','negativemark','duration','examtype','type','questions','banner','description','notes')

class GetQuestionPaperSerilizer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    categorys_name=serializers.SerializerMethodField()
    levels_name=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    subject_name=serializers.SerializerMethodField()
    module_name=serializers.SerializerMethodField()
    topic_name=serializers.SerializerMethodField()
    questions=QustionpoolNew(many=True)
    class Meta:
        model=QuestionPaper
        fields=('id','name','user','user_name','categorys','categorys_name','levels','levels_name','course','course_name','subject','subject_name','module','module_name','topic','topic_name','instruction','positivemark','negativemark','duration','examtype','type','questions','banner','description','notes')
    
    def get_user_name(self,obj):
        if obj.user:
            return obj.user.username
        return None

    def get_categorys_name(self,obj):
        if obj.categorys:                  
            return obj.categorys.name
        return None

    def get_levels_name(self,obj):   
        if obj.levels:              
             return obj.levels.name
        return None
    
    def get_course_name(self,obj):
        if obj.course:
            return obj.course.name
        return None

    def get_subject_name(self,obj):
        if obj.subject:
            return obj.subject.name
        return None

    def get_module_name(self,obj):
        if obj.module:
            return obj.module.name
        return None


    def get_topic_name(self,obj):
        if obj.topic:
            return obj.topic.name
        return None




class RoleUserSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    # branch = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    # def get_branch(self, obj):
    #     branch_qs = Branch.objects.filter(user=obj, is_delete=False)
    #     if branch_qs.exists():
    #         return BranchSerializer(branch_qs.first()).data
    #     return None
    def get_branch(self, obj):
        branch_qs = Branch.objects.filter(user=obj, is_delete=False)
        if branch_qs.exists():
            return BranchSerializer(branch_qs, many=True).data
        return []
    
class FacultyFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = QuestionFile
        fields = '__all__'

    def get_url(self, obj):
        return obj.facultyfile.url


class QuestionCourseSerializer(serializers.ModelSerializer):
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'level_id', 'category_id', 'level_name', 'category_name', 'batch_name', 'created_at', 'name', 'description', 'is_online', 'active', 'photo', 'year', 'is_delete', 'level', 'batch_type', 'question_count']

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            field_value = self.initial_data.get('batch_type')
            if Course.objects.filter(name__iexact=name,batch_type=field_value).exists():
                raise serializers.ValidationError(
                    "Course with this name already exists")
        return value

    def get_batch_name(self, obj):
        return obj.batch_type.name

    def get_level_id(self, obj):
        return obj.level.id

    def get_category_id(self, obj):
        return obj.level.category.id

    def get_level_id(self, obj):
        return obj.level.id

    def get_category_id(self, obj):
        return obj.level.category.id

    def get_level_name(self, obj):
        return obj.level.name

    def get_category_name(self, obj):
        return obj.level.category.name
    
    def get_question_count(self, obj):
        return NewQuestionPool.objects.filter(course=obj).count()
    

class MaterialUploadGetSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()
    class Meta:
        model = Material
        fields = '__all__'

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
        
    def get_level_id(self,obj):
        try:
            return obj.level.id
        except:
            return None
        
    def get_level_name(self,obj):
        try:
            return obj.level.name
        except:
            return None
    def get_course_name(self,obj):
        try:
            return obj.course.name
        except:
            return None
        
    def get_module_name(self,obj):
        try:
            return obj.module.name
        except:
            return None
        
    def get_topic_name(self,obj):
        try:
            return obj.topic.name
        except:
            return None
        
    def get_faculty_name(self,obj):
        try:
            return obj.faculty.user.username
        except:
            return None
        
# class MaterialTopicSerializer(serializers.ModelSerializer):
#     materials = MaterialSerializer(many=True, read_only=True)

#     module_id = serializers.SerializerMethodField()
#     subject_id = serializers.SerializerMethodField()
#     course_id = serializers.SerializerMethodField()
#     module_name = serializers.SerializerMethodField()
#     subject_name = serializers.SerializerMethodField()
#     course_name = serializers.SerializerMethodField()
#     level_id = serializers.SerializerMethodField()
#     category_id = serializers.SerializerMethodField()
#     level_name = serializers.SerializerMethodField()
#     category_name = serializers.SerializerMethodField()
#     subtopic = serializers.SerializerMethodField()


#     class Meta:
#         model = Topic
#         # fields = '__all__'
#         fields = ['id','subtopic','level_name','category_id','course_id','level_id','subject_id','module_id', 'name', 'module', 'description', 'priority', 'clickStatus', 'photo', 'active', 'day', 'order', 'time_needed', 'is_delete', 'created_at', 'materials','subject_name','category_name','module_name','course_name']


#     def validate_name(self, value):
#         """
#         Check that the name field doesn't already exist in the database
#         """
#         if self.context['request'].method == 'POST':
#             name = value.lower()
#             module = self.initial_data.get('module')

#             if Topic.objects.filter(name__iexact=name, module=module).exists():
#                 raise serializers.ValidationError(
#                     "Topic with this name already exists")
#         return value

#     def get_module_id(self, obj):
#         return obj.module.id

#     def get_subject_id(self, obj):
#         return obj.module.subject.id

#     def get_course_id(self, obj):
#         return obj.module.subject.course.id

#     def get_module_name(self, obj):
#         return obj.module.name

#     def get_subject_name(self, obj):
#         return obj.module.subject.name

#     def get_course_name(self, obj):
#         return obj.module.subject.course.name

#     def get_level_name(self, obj):
#         return obj.module.subject.course.level.name

#     def get_level_id(self, obj):
#         return obj.module.subject.course.level.id

#     def get_category_id(self, obj):
#         return obj.module.subject.course.level.category.id

#     def get_category_name(self, obj):
#         return obj.module.subject.course.level.category.name
    
#     def get_subtopic(self, topic):
#         try:
#             subtopic = topic.subtopic_set.filter()
#             ser = SubTopicSerializer(subtopic, many=True)
#             return ser.data
#         except SubTopic.DoesNotExist:
#             return None

class MaterialTopicSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    module_id = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    # Existing serializer fields
    class Meta:
        model = Topic
        fields = ['id', 'subtopic', 'level_name', 'category_id', 'course_id', 'level_id', 'subject_id', 'module_id', 'name', 'module', 'description', 'priority', 'clickStatus', 'photo', 'active', 'day', 'order', 'time_needed', 'is_delete', 'created_at', 'materials', 'subject_name', 'category_name', 'module_name', 'course_name']

    def get_subtopic(self, topic):
        try:
            subtopic = topic.subtopic_set.filter()
            ser = MaterialSubTopicSerializer(subtopic, many=True,context={'faculty':self.context.get('user')})
            return ser.data
        except SubTopic.DoesNotExist:
            return None

    def get_materials(self, topic):
        materials = topic.materials.all()
        serializer = MaterialSerializer(materials, many=True)
        return serializer.data
    
    def get_module_id(self, obj):
        return obj.module.id

    def get_subject_id(self, obj):
        return obj.module.subject.id

    def get_course_id(self, obj):
        return obj.module.subject.course.id

    def get_module_name(self, obj):
        return obj.module.name

    def get_subject_name(self, obj):
        return obj.module.subject.name

    def get_course_name(self, obj):
        return obj.module.subject.course.name

    def get_level_name(self, obj):
        return obj.module.subject.course.level.name

    def get_level_id(self, obj):
        return obj.module.subject.course.level.id

    def get_category_id(self, obj):
        return obj.module.subject.course.level.category.id

    def get_category_name(self, obj):
        return obj.module.subject.course.level.category.name


class StudioCourseSeializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    studioname = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    class Meta:
        model=StudioCourse
        # fields=('id','name',"topic","date","time","location","studioname")
        fields='__all__'

    def get_topic(self,obj):
          return [{'id': topic.id, 'name': topic.name} for topic in obj.topic.all()]
    
    def get_studioname(self, obj):
        studioname_instance = obj.studioname
        serializer = StudionameSerializer(studioname_instance)
        return serializer.data
    
    def get_status(self, obj):
        faculty_id = self.context['request']
        print(faculty_id,'**************')
        try:
            facapplication = FacultyStudioApplication.objects.get(studiocourse=obj.id, faculty=faculty_id)
            print(facapplication,'kkkk')
            if facapplication:
                print("+??++")
                try:
                    assign=StudioCourse.objects.get(id=obj.id,faculty=faculty_id)
                    if assign:
                        print("^^^^")
                        return 'assigned'
                except:
                        print("%%%")
                        return 'applied'

        except FacultyStudioApplication.DoesNotExist:
            print("####")
            return 'notapplied'


    
class StudionameSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioNames
        fields=('id','name','district','address','phonenumber')
    
class FacultyStudioApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacultyStudioApplication
        fields=('studiocourse','faculty','videourl')
    
class VideoAssignmentSerializer(serializers.ModelSerializer):
    # course_name = serializers.SerializerMethodField
    class Meta:
        model = StudioCourseAssign
        fields = '__all__'
    

class StudioApplicationApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioCourse
        # fields=('id','faculty','name',"topic","date","time","location","studioname")
        fields=('id','faculty')

class AddVediotoStudioCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioVideo
        fields='__all__'


# class TopicApplicationCountSerializer(serializers.Serializer):
#     topic = serializers.CharField(source='topic__name')
#     application_count = serializers.IntegerField()
# from rest_framework import serializers
class StudioCourseForApplicatioDetials(serializers.ModelSerializer):
    class Meta:
        model=StudioCourse
        fields='__all__'
class TopicApplicationCountSerializer(serializers.ModelSerializer):
    # studiocourse_name = serializers.CharField(source='name')
    # application_count = serializers.IntegerField()
    faculty=serializers.SerializerMethodField()
    studioname=serializers.SerializerMethodField()
    studiocourse=StudioCourseForApplicatioDetials()
    class Meta:
        model=FacultyStudioApplication
        fields='__all__'

    def get_faculty(self,obj):
            try:
                fac = Faculty.objects.get(user=obj.faculty)
                facser = facultyviewDetails(fac)
                return facser.data
            except :
                return None
    def get_studioname(self,obj):
        try:
            studioname=StudioCourse.objects.get(id=obj.studiocourse.id).studioname
            studioname=StudionameSerializer(studioname)
            return studioname.data
        except:
            pass
    


class StudioTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields=('id','name')


class StudiocoursebasedstudioSerializer(serializers.ModelSerializer):
    video=AddVediotoStudioCourseSerializer()
    studioname=StudionameSerializer()
    topic=StudioTopicSerializer(many=True)
    # faculty=facultyviewDetails(many=True)
    faculty=serializers.SerializerMethodField()

    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_studioname(self,obj):
        return obj.studioname.name
    
    def get_topic(self,obj):
        return obj.topic
    
    def get_vedio(self,obj):
        return obj.video
    
    def get_faculty(self,obj):
        try:
            fac = Faculty.objects.get(user=obj.faculty)
            facser = facultyviewDetails(fac)
            return facser.data
        except :
            return None
        
    
    
# class DupCourseNewDragSerializer(serializers.ModelSerializer):
#     subject = serializers.SerializerMethodField()

#     class Meta:
#         model = Course
#         fields = '__all__'  

    
#     def get_subject(self,obj):
#         subject = Subject.objects.filter(course=obj.id)
#         return DupSubjectNewDragSerializer(subject, many=True).data
    
# class DupSubjectNewDragSerializer(serializers.ModelSerializer):
#     modules = serializers.SerializerMethodField()

#     class Meta:
#         model = Subject
#         fields = '__all__'

    
#     def get_modules(self,obj):
#         subject = Module.objects.filter(subject=obj.id)
#         return DupModuleNewDragSerializer(subject, many=True).data
    

# class DupModuleNewDragSerializer(serializers.ModelSerializer):
#     topics = serializers.SerializerMethodField()

#     class Meta:
#         model = Module
#         fields = '__all__'

    
#     def get_topics(self,obj):
#         topic = Topic.objects.filter(module=obj.id)
#         return DupTopicNewDragSerializer(topic, many=True).data
    
# class DupTopicNewDragSerializer(serializers.ModelSerializer):
#       subtopic = serializers.SerializerMethodField()
#     # pending = serializers.BooleanField(default=True)
#     # scheduled=serializers.BooleanField(default=False)
#     # completed=serializers.BooleanField(default=False)
    

#     class Meta:
#         model = Topic
#         fields = '__all__'

    
#     def get_subtopic(self,obj):
#         subtopic = SubTopic.objects.filter(topic=obj.id)
#         return SubtopicNewDragSerializer(subtopic, many=True).data
    







# class DupTopicNewDragSerializer(serializers.ModelSerializer):
#     subtopic = SubtopicNewDragSerializer(many=True,source='subtopic_set')

#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = Topic
#         fields = '__all__'

#     def get_status(self, obj):
#         studiotopiccheck = StudioCourse.objects.filter(topic=obj)
#         if studiotopiccheck:
#             return 'Scheduled'
#         else:
#             return 'Pending'
class DupTopicNewDragSerializer(serializers.ModelSerializer):
    subtopic = SubtopicNewDragSerializer(many=True, source='subtopic_set')
    status = serializers.SerializerMethodField()
    vidodetails=serializers.SerializerMethodField()
    studiocourseid=serializers.SerializerMethodField() 
    applicationcount=serializers.SerializerMethodField()


    class Meta:
        model = Topic
        fields = '__all__'

    def get_status(self, obj):
        print(obj, 'YYYYYYYYYYYYYYYYYYY')
        if StudioCourse.objects.filter(topic=obj):
            studiotopiccheck = StudioCourse.objects.filter(topic=obj)
            print(studiotopiccheck, 'mmmmmmmm')
            if studiotopiccheck.exists():
                if studiotopiccheck.filter(video__isnull=False,faculty_id__isnull=False).exists():
                    print('dddddd')
                    return 'Completed'
                elif studiotopiccheck.filter(faculty_id__isnull=False,video__isnull=True).exists():
                    print("lllll")
                    return 'Faculty assigned'
                elif studiotopiccheck.filter(faculty_id__isnull=True,video__isnull=False).exists():
                    print("lllll")
                    return 'Faculty not assigned Video assigned'
                elif studiotopiccheck.filter(faculty_id__isnull=True,video__isnull=True).exists():
                    print("PPPP")
                    return 'Scheduled'
            else:
                pass
        elif StudioCourseAssign.objects.filter(topic=obj):
            return 'Completed'
        else:
            print("OOOOOOOOO")
            return 'Pending'
    def get_vidodetails(self,obj):

        if StudioCourseAssign.objects.filter(topic=obj):
            details=StudioCourseAssign.objects.filter(topic=obj)
            serializers=DragCourseVideoDetils(details,many=True)
            return serializers.data
        elif StudioCourse.objects.filter(topic=obj):
            details=StudioCourse.objects.filter(topic=obj)
            serializers=StudioCourseSeializerforlistingDrapandDrop(details,many=True)
            return serializers.data
        else:
            return None
    
    def get_studiocourseid(serlf,obj):
        if StudioCourse.objects.filter(topic=obj).values('id'):
            studiocourseid=StudioCourse.objects.filter(topic=obj).values('id')
            return studiocourseid
        else:
            return None

    def get_applicationcount(self,obj):
        if StudioCourse.objects.filter(topic=obj):
            studiotopiccheck = StudioCourse.objects.filter(topic=obj)
            print(studiotopiccheck, 'mmmmmmmm')
            if studiotopiccheck.exists():
                if studiotopiccheck.filter(faculty_id__isnull=True,video__isnull=True).exists():
                    count=FacultyStudioApplication.objects.filter(studiocourse__topic=obj).count()
                    return count
                else:
                    return None
            return None
        return None

class DupModuleNewDragSerializer(serializers.ModelSerializer):
    topics = DupTopicNewDragSerializer(many=True, source='topic_set')
    vidodetails=serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'
    
    def get_vidodetails(self,obj):
        details=StudioCourseAssign.objects.filter(module=obj)
        serializers=DragCourseVideoDetils(details,many=True)
        return serializers.data

class DupSubjectNewDragSerializer(serializers.ModelSerializer):
    modules = DupModuleNewDragSerializer(many=True, source='module_set')
    vidodetails=serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = '__all__'
    
    def get_vidodetails(self,obj):
        details=StudioCourseAssign.objects.filter(subject=obj)
        serializers=DragCourseVideoDetils(details,many=True)
        return serializers.data

class DupCourseNewDragSerializer(serializers.ModelSerializer):
    subjects = DupSubjectNewDragSerializer(many=True, source='subject_set')
    vidodetails=serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_vidodetails(self,obj):
        details=StudioCourseAssign.objects.filter(course=obj)
        serializers=DragCourseVideoDetils(details,many=True)
        return serializers.data


class RolesSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()
    userdetails = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'


    def get_permission(self,obj):
        perms = Permissions.objects.get(role=obj)
        return PermissionSerializer(perms).data
    
    def get_userdetails(self,obj):
        user= obj.user.all()
        return UserSerializer(user, many=True).data

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'

class FacultySubjectGetSerializer(serializers.ModelSerializer):
    #hiiiii
    subject = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    facultyname = serializers.SerializerMethodField()
    faculty_id = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    class Meta:
        model = FacultyCourseAddition
        fields = ['id', 'user', 'category', 'level', 'course',
                  'subject', 'module', 'topic', 'is_approved', 'status','topic_name','facultyname','faculty_id','faculty_phone']
        
    def get_topic_name(self, obj):
        return obj.topic.name
    def get_subject(self, obj):
        return obj.subject.name
    def get_facultyname(self,obj):
        return Faculty.objects.get(user=obj.user).name
    def get_faculty_id(self,obj):
        return Faculty.objects.get(user=obj.user).id
    def get_faculty_phone(self,obj):
        return obj.user.mobile



class StudioCourseSeializerforList(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    studionames = serializers.SerializerMethodField()


    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_topic(self,obj):
          return [{'id': topic.id, 'name': topic.name} for topic in obj.topic.all()]
    
    def get_studionames(self, obj):
        studioname_instance = obj.studioname
        serializer = StudionameSerializer(studioname_instance)
        return serializer.data
    

class StudioCourseSeializerforCrating(serializers.ModelSerializer):

    class Meta:
        model=StudioCourse
        fields='__all__'


class NotassignedFacultiesSerialilzer(serializers.ModelSerializer):
    studioname=StudionameSerializer()
    topic=StudioTopicSerializer(many=True)
    count=serializers.SerializerMethodField()
    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_count(self,obj):
        count=FacultyStudioApplication.objects.filter(studiocourse=obj.id).count()
        return count

class StudioassignedFacultiesSerialilzer(serializers.ModelSerializer):
    faculty=serializers.SerializerMethodField()
    studioname=StudionameSerializer()
    topic=StudioTopicSerializer(many=True)
    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_faculty(self,obj):
        try:
            fac = Faculty.objects.get(user=obj.faculty)
            facser = facultyviewDetails(fac)
            return facser.data
        except :
            return None
        
class vedioassignedStudioSerialilzer(serializers.ModelSerializer):
    studioname=StudionameSerializer()
    topic=StudioTopicSerializer(many=True)
    faculty=serializers.SerializerMethodField()
    video=AddVediotoStudioCourseSerializer()
    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_faculty(self,obj):
        try:
            fac = Faculty.objects.get(user=obj.faculty)
            facser = facultyviewDetails(fac)
            return facser.data
        except :
            return None
        


class VideoAssignForCourseetcSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudioCourseAssign
        fields = ('video', 'course', 'subject', 'module', 'topic', 'subtopic')

class MaterialUploadPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialUploads
        fields = '__all__'

class MaterialUploadSerializer(serializers.ModelSerializer):
    username =serializers.SerializerMethodField()
    materialreference=serializers.SerializerMethodField()
    uniqueid = serializers.SerializerMethodField()
    edited_user = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    file_format = serializers.SerializerMethodField()

    class Meta:
        model = MaterialUploads
        fields = '__all__'

    def get_file_format(self,obj):
        try:
            file_name = obj.file.name
            file_extension = file_name.split('.')[-1].lower()
            image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
            if file_extension in image_extensions:
                return True
            else:
                return False
        except:
            return False


    def get_completion_rate(self,obj):
        try:
            topic_ids_for_user = FacultyCourseAddition.objects.filter(user_id=obj.user.id).values_list('topic_id', flat=True).distinct()
            topic_ids_list = list(topic_ids_for_user)
            subtopic_count = SubTopic.objects.filter(topic_id__in=topic_ids_list).count()
            total_uploads = MaterialUploads.objects.filter(user=obj.user).count()
            if total_uploads == 0:
                return 0
            completion = (subtopic_count/total_uploads) / 100
            return completion
        except:
            return None








        

    def get_edited_user(self,obj):
        try:
            return obj.edited_user.username
        except:
            None
    
    def get_uniqueid(self,obj):
        userid = obj.user.id
        matid = obj.id
        return 'F'+str(userid)+str(matid)


    def get_username(self,obj):
        # print(obj.user)
        try:
            # facultyname = Faculty.objects.get(user__id = obj.user.id)
            facultyname = User.objects.get(id = obj.user.id)

            return facultyname.username
        except Exception as e:
         
            return None
        
    def get_materialreference(self,obj):
        mat=MaterialReference.objects.filter(materialupload=obj)
        ser=MaterialReferenceSerializer(mat,many=True)
        
        return ser.data

class MaterialReferenceSerializer(serializers.ModelSerializer):
    user_name =serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    class Meta:
        model = MaterialReference
        fields = '__all__'

    def get_user_name(self,obj):
        facultyname = Faculty.objects.get(user= obj.user)
        return facultyname.name
    def get_file(self,obj):
        return obj.materialupload.file.url
    def get_topic(self,obj):
        try:
          return obj.topic.name
        except:
            return None
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
    def get_subtopic(self,obj):
        try:
          return obj.subtopic.name
        except:
            return None
    def get_module(self,obj):
        try:
          return obj.module.name
        except:
            return None



class DragCourseVideoDetils(serializers.ModelSerializer):
    video=AddVediotoStudioCourseSerializer()
    class Meta:
        model=StudioCourseAssign
        fields='__all__'



class StudioCourseSeializerforlistingDrapandDrop(serializers.ModelSerializer):
    video=AddVediotoStudioCourseSerializer()
    class Meta:
        model=StudioCourse
        fields=('id',"video")

class studiocoursegetallsdetils(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    studioname = serializers.SerializerMethodField()
    faculty=serializers.SerializerMethodField()
    video=AddVediotoStudioCourseSerializer()
    count=serializers.SerializerMethodField()
    class Meta:
        model=StudioCourse
        fields='__all__'

    def get_topic(self,obj):
            return [{'id': topic.id, 'name': topic.name} for topic in obj.topic.all()]
    
    def get_studioname(self, obj):
        studioname_instance = obj.studioname
        serializer = StudionameSerializer(studioname_instance)
        return serializer.data

    def get_faculty(self,obj):
        try:
            fac = Faculty.objects.get(user=obj.faculty)
            facser = facultyviewDetails(fac)
            return facser.data
        except :
            return None
    def get_count(self,obj):
        try:
            count=FacultyStudioApplication.objects.filter(studiocourse=obj.id).count()
            return count 
        except:
            return None
    
        
class DeleteVideomanuallyAssigningSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioCourseAssign
        fields='__all__'

class MaterialForStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialUploads
        fields = ['id', 'updated_file','name']
class ConvertedMaterialSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    uploaded = serializers.SerializerMethodField()
    # batch = serializers.SerializerMethodField()
    class Meta:
        model = ConvertedMaterials
        fields = '__all__'

    def get_username(self,obj):
        try:
            user = Faculty.objects.get(user=obj.user)
            return user.name
        except :
            return None
        
    def get_uploaded(self, obj):
        material_references = obj.uploads.all()
        serializer = MaterialReferenceSerializer(material_references, many=True)
        return serializer.data
    # def get_batch(self, obj):
    #     return [batch.name for batch in obj.batch.all()]

class CommonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioVideo
        fields=['id','name','description','video_length','editingstaff','videocontent','vimeoid','videolink']



class facultyviewDetailsStudioClass(serializers.ModelSerializer):
    user = UserSerializer()
    rating=serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ['user','name','address','district','gender','rating']

    def get_rating(self,obj):
        return None
    
class MaterialRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialRating
        fields='__all__'


class FacultyNewonlineoffSalarySerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    modeofclass=serializers.SerializerMethodField()
    fixed_amount=serializers.SerializerMethodField()
    # fixed_salary = SalaryFixationSerializer() # Include nested serializer for fixed_salary

    class Meta:
        model = Faculty_Salary
        fields = '__all__'
    def get_level_name(self,obj):
        return obj.level.name
    def get_category_name(self,obj):
        return obj.level.category.name
    def get_modeofclass(self,obj):
        if obj.faculty.modeofclasschoice=='1':
            return 'offline'
        elif obj.faculty.modeofclasschoice=='2':
            return 'online'
        elif obj.faculty.modeofclasschoice=='3':
            return 'Both'
    def get_fixed_amount(self,obj):
        try:
            return obj.fixed_salary.salaryscale
        except:
            return None

        

class FixedSalarySerialzer(serializers.ModelSerializer):
    fixed_salary=serializers.SerializerMethodField()
    class Meta:
        model=Faculty_Salary
        fields=['fixed_salary']
    def get_fixed_salary(self,obj):
        if obj.fixed_salary.salaryscale:
            return obj.fixed_salary.salaryscale
        else:
            return None


        
class AssingSalaryStudioDetails(serializers.ModelSerializer):
    video=AddVediotoStudioCourseSerializer()
    studioname=StudionameSerializer()
    topic=StudioTopicSerializer(many=True)
    # faculty=facultyviewDetails(many=True)
    faculty=serializers.SerializerMethodField()
    fixedsalary=serializers.SerializerMethodField()
    salarydetails=serializers.SerializerMethodField()

    class Meta:
        model=StudioCourse
        # fields=['id','name','date','time','location','created_by','publish','assignvideo','fixedsalary','salarydetails','video','studioname','topic','faculty']
        fields='__all__'

    def get_studioname(self,obj):
        return obj.studioname.name
    
    def get_topic(self,obj):
        return obj.topic
    
    def get_vedio(self,obj):
        return obj.video
    
    def get_faculty(self,obj):
        fac = Faculty.objects.get(user=obj.faculty)
        print(fac,'fcc')
        facser = facultyviewDetailsStudioClass(fac)
        print(facser,'dddd')
        return facser.data
     
    def get_fixedsalary(self, obj):
            faculty = Faculty.objects.get(user=obj.faculty)
            print(faculty,'ddd')
            
            level =obj.topic.filter().values('module__subject__course__level').distinct()
            print(level,'level')
            level_id = level[0]['module__subject__course__level'] 
            print(level_id,'kkk')
            salary = Faculty_Salary.objects.filter(faculty=faculty.id,level=level_id,is_online=True).first()
            print(salary,'salary')
            serializers=FixedSalarySerialzer(salary)
            return serializers.data
    def get_salarydetails(self,obj):
        sal=OnlineSalary.objects.filter(studiocourse=obj.id)
        serializers=CreateOnlineSalarySerializerShrink(sal,many=True)
        return serializers.data
        

class PopularTeacherSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ('id', 'subject', 'address', 'identity_card', 'photo', 'resume', 'gender', 'district',
                  'whatsapp_contact_number', 'date_of_birth', 'qualification', 'experiance_link', 'pincode', 'name')

    def get_subject(self, obj):
        faculty_course_addition = FacultyCourseAddition.objects.filter(user=obj.user.id).first()
        if faculty_course_addition:
            return faculty_course_addition.subject.name
        return None
    
    def get_rating(self,obj):
        average_rating = Rating.objects.filter(rate_fac=obj).aggregate(Avg('choice'))['choice__avg']
        if average_rating is not None:
            return average_rating
        else:
            return 0
    def get_video_count(self,obj):
        count = StudioVideo.objects.filter(faculty=obj.user).count()
        return count
class CreateOnlineSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model=OnlineSalary
        fields='__all__'

class CreateOnlineSalarySerializerShrink(serializers.ModelSerializer):
    class Meta:
        model=OnlineSalary
        fields=['id','payment_status','paid_amount','testimonial','payment_method']



class facultyviewDetailsMaterial(serializers.ModelSerializer):
    user = UserSerializer()
    # faculty_course_addition = FacultyCourseAdditionsss(many=True)
    # courses = serializers.SerializerMethodField()
    # experiace = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_courses(self, obj):
        k = FacultyCourseAddition.objects.filter(user=obj.user.id).order_by('created_at')
        return FacultyCourseAdditionsss(k, many=True).data
    
    def get_pending(self,obj):
        um = len(MaterialReference.objects.filter(user=obj.user))
        cm = len(ConvertedMaterials.objects.filter(user=obj.user))

        return {
            "faculty-assigned-material":um,
            "converted-material":cm,
            "pending-count":um-cm
        }
    
    def get_notifications(self,obj):
        try:
            total_materials = MaterialUploads.objects.filter(user=obj.user).count()
            converted_materials = MaterialUploads.objects.filter(user=obj.user, updated_file__isnull=False).count()
            converted_materials_final = MaterialUploads.objects.filter(Q(user=obj.user) & (Q(vstatus_research=True) | Q(vstatus_faculty=True))).count()
            
            return {
                "NewMaterials":total_materials-converted_materials,
                "PendingMaterials":total_materials-converted_materials_final,
                "Completion Count":converted_materials_final,
                "TotalMaterial":total_materials
                
            }
        except:
            return None
    # def get_pending(self,obj):
    #     return FacultyCourseAddition.objects.filter(user=obj.user.id,status="pending").count()

    def get_experiace(self, obj):
        exp = Experience.objects.filter(name=obj.id)
        return ExperienceSerializer(exp, many=True).data
    
    def get_rating(self, obj):
        rat = Rating.objects.filter(Q(rate_fac=obj) | Q(rating_on__faculty=obj.user )).values('choice')
        average_rating = rat.aggregate(avg_rating=Avg('choice'))['avg_rating']
        print(average_rating,"raaaaaaaaaaaaaaaaaaaaat")
        return average_rating
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     courses = representation['courses']
        
    #     sorted_courses = sorted(courses, key=lambda x: x['created_at'])
    #     representation['courses'] = sorted_courses
    #     return representation

class MaterialUploadAdminViewSerializer(serializers.ModelSerializer):
    username =serializers.SerializerMethodField()
    materialreference=serializers.SerializerMethodField()

    class Meta:
        model = MaterialUploads
        fields = '__all__'

    def get_username(self,obj):
        # print(obj.user)
        try:
            facultyname = User.objects.get(id = obj.user.id)
            return facultyname.username
        except Exception as e:
         
            return None
        
    def get_materialreference(self,obj):
        mat=MaterialReference.objects.filter(materialupload=obj)
        ser=MaterialReferenceSerializer(mat,many=True)
        
        return ser.data
    
class IncentivesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Incentives
        fields='__all__'

class IncentiveSmall(serializers.ModelSerializer):
    class Meta:
        model=Incentives
        fields=['id','name','rate','types']
class staffserializerSmall(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','mobile']
class StaffIncentivesSerializer(serializers.ModelSerializer):
    incentives=IncentiveSmall()
    staff=staffserializerSmall()
    class Meta:
        model=StaffIncentives
        fields='__all__'

class StaffIncentivesSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model=StaffIncentives
        fields=['id','incentives','staff','target']


class incentiveSalarySerializersmall(serializers.ModelSerializer):
    incentives=IncentiveSmall()
    staff=staffserializerSmall()
    class Meta:
        model=StaffIncentives
        fields=['id','staff','incentives','target']

class StaffSalarySerializer(serializers.ModelSerializer):
    incentive_details = serializers.SerializerMethodField()
    class Meta:
        model=StaffSalary
        fields='__all__'

    def get_incentive_details(self, obj):
        # Here, you can retrieve the related StaffIncentives data and return it
        # You can customize this based on how you want to fetch and serialize the incentive details
        incentive_data = StaffIncentives.objects.filter(staff=obj.staff)  # Adjust the filter condition as needed
        serialized_incentive_data = incentiveSalarySerializersmall(incentive_data, many=True).data
        return serialized_incentive_data

class StaffIncentivesSerializerSmall(serializers.ModelSerializer):
    incentives=IncentiveSmall()
    class Meta:
        model=StaffIncentives
        fields=['incentives','staff','target','status']
class StaffIncentiveAmountSerializer(serializers.ModelSerializer):
    staffincetive=serializers.SerializerMethodField()
    users=serializers.SerializerMethodField()
    # user=staffserializerSmall()
    class Meta:
        model=StaffIncentiveAmount
        fields='__all__'

    def get_staffincetive(self,obj):
        incentives=StaffIncentives.objects.filter(staff=obj.user)
        serialiser=StaffIncentivesSerializerSmall(incentives,many=True)
        return serialiser.data
    def get_users(self,obj):
        users=User.objects.get(email=obj.user)
        print(users,'fusj')
        serializer=staffserializerSmall(users)
        return serializer.data

class staffbranchnameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields=['id','name','location']
class ActiveStafflistSerializer(serializers.ModelSerializer):
    branch=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id','username','email','mobile','mobile','is_active','is_roleuser','branch']

    def get_branch(self,obj):
        staffbranch=Branch.objects.filter(user=obj.id)
        serializers=staffbranchnameSerializer(staffbranch,many=True)
        return serializers.data

class AddVideoToStudioCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudioVideo
        fields='__all__'

class SubtopicforExcelSerializer(serializers.ModelSerializer):
    allapprove=serializers.SerializerMethodField()
    class Meta:
        model=SubTopic
        fields=['id','name','allapprove']

    def get_allapprove(self,obj):
        userid=self.context.get('userid')
        approved_question_count = NewQuestionPool.objects.filter(
            user=userid,
            subtopic=obj.id,
            admin_verify=True, dtp_verify=True, faculty_verify=True).count()
        
        total_question_count = NewQuestionPool.objects.filter(
            user=userid,
            subtopic=obj.id
        ).count()
        
        # Check if all questions are approved
        return approved_question_count == total_question_count
        
        

class CategoryforexcelSeriaizer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']


class AdminViewMaterialUploadSerializer(serializers.ModelSerializer):
    username =serializers.SerializerMethodField()
    # materialreference=serializers.SerializerMethodField()
    uniqueid = serializers.SerializerMethodField()
    edited_user = serializers.SerializerMethodField()
    class Meta:
        model = MaterialUploads
        fields = '__all__'

    def get_edited_user(self,obj):
        try:
            return obj.edited_user.username
        except:
            None
    
    def get_uniqueid(self,obj):
        userid = obj.user.id
        matid = obj.id
        return 'F'+str(userid)+str(matid)


    def get_username(self,obj):
        # print(obj.user)
        try:
            facultyname = Faculty.objects.get(user__id = obj.user.id)
            return facultyname.name
        except Exception as e:
         
            return None
        
    # def get_materialreference(self,obj):
    #     mat=MaterialReference.objects.filter(materialupload=obj)
    #     ser=MaterialReferenceSerializer(mat,many=True)
        
    #     return ser.data

class CategorySerializerAppSideQuestionPool(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class LevelSerializerAppSideQuestionPool(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']

class CourseSerializerAppSideQuestionPool(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']
class SubjectSerializerAppSideQuestionPool(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ModuelSerializerAppSideQuestionPool(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name']

class TopicBasedFacCourseSerilaizer(serializers.ModelSerializer):
    category=CategorySerializerAppSideQuestionPool(source='module.subject.course.level.category', read_only=True)
    level=CategorySerializerAppSideQuestionPool(source='module.subject.course.level', read_only=True)
    course=LevelSerializerAppSideQuestionPool(source='module.subject.course', read_only=True)
    subject=CourseSerializerAppSideQuestionPool(source='module.subject', read_only=True)
    module=ModuelSerializerAppSideQuestionPool(read_only=True)
    subtopics=serializers.SerializerMethodField()
    class Meta:
        model=Topic
        fields=['id','name','description','priority','active','category','level','course','subject','module','subtopics']

    def get_subtopics(self,obj):
        userid= self.context.get('user_id')
        subtopic=SubTopic.objects.filter(topic=obj.id).order_by('created_at')
        serializers=SubtopicforExcelSerializer(subtopic,many=True,context={"userid":userid})
        return serializers.data
    
class CoursebasedFacCourseSerializer(serializers.ModelSerializer):
    progress=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=['id','name','description','is_online','active','level','progress']

    def get_progress(self, obj):
        user_id = self.context.get('user_id')
        # Get the course ID from the current course object
        course_id = obj.id

        # Query for faculty's subtopics
        faculty_topics = FacultyCourseAddition.objects.filter(user=user_id, course=course_id,status="approved").values('topic')
        subtopics = SubTopic.objects.filter(topic__in=faculty_topics)
        subtopic_count = subtopics.count()

        # Count the number of questions for each faculty subtopic in the course and user
        subtopic_question_counts = NewQuestionPool.objects.filter(
            course_id=course_id,
            user=user_id,
            subtopic__in=subtopics
        ).values('subtopic_id').annotate(total_questions=Count('id'))

        # Calculate the total number of questions for faculty subtopics
        total_questions = sum(count['total_questions'] for count in subtopic_question_counts)

        # Calculate the percentage based on the conditions
        if subtopic_count == 0:
            return 0  # No faculty subtopics, so progress is 0%
        elif total_questions >= subtopic_count * 20:
            return 100  # All faculty subtopics have at least 20 questions, so progress is 100%
        else:
            percentage = (total_questions / (subtopic_count * 20)) * 100
            return round(percentage, 2) 


class facutlycategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','active']

class QustionpoolNewoneDtpCreate(serializers.ModelSerializer):
    class Meta:
        model=NewQuestionPool
        fields=('id','user','categorys','levels','course','subject','module','topic','subtopic','question_text','option_1','option_2','option_3','option_4','option_5','answer','type','answerhint','add_user','dtp_verify','dtp_edit')