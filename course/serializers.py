from rest_framework import serializers
# from accounts.api.serializers import *
# from accounts.api.serializers import *
from .models import *
from accounts.models import Faculty_Salary , Material,MaterialReference,ConvertedMaterials
from .serializers import *
from accounts.api.authhandle import AuthHandlerIns
from django.db.models import Avg

class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    # subjects = serializers.SerializerMethodField()
    # module = serializers.SerializerMethodField()
    # topic = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            if Category.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError(
                    "Category with this name already exists")
        return value

    def get_level(self, category):
        try:
            level = category.level_set.filter()
            ser = LevelSerializer(level, many=True)
            return ser.data
        except Level.DoesNotExist:
            return None

    def get_courses(self, obj):
        courses = Course.objects.filter(level__category=obj)
        serializer = CourseSerializer(courses, many=True)
        return serializer.data
    
    # def get_subjects(self, obj):
    #     subjects = Subject.objects.filter(course__level__category=obj)
    #     serializer = SubjectSerializer(subjects, many=True)
    #     return serializer.data
    
    # def get_module(self, obj):
    #     modules = Module.objects.filter(subject__course__level__category=obj)
    #     serializer = ModuleSerializer(modules, many=True)
    #     return serializer.data
    
    # def get_topic(self, obj):
    #     topic = Topic.objects.filter(module__subject__course__level__category=obj)
    #     serializer = TopicSerializer(topic, many=True)
    #     return serializer.data


# class CourseDetailSerializer(serializers.ModelSerializer):
#     subjects = SubjectSerializer(many=True, read_only=True)

#     # subject = serializers.SerializerMethodField()
#     # module = serializers.SerializerMethodField()
#     # topic = serializers.SerializerMethodField()
#     class Meta:
#         model = Course
#         fields = '__all__'

#     def get_subject(self, course):
#         try:
#             subject = course.subject_set.filter()
#             ser = SubjectSerializer(subject, many=True)
#             return ser.data
#         except Subject.DoesNotExist:
#             return None
        
#     def get_module(self, obj):
#         module = Module.objects.filter(subject__course=obj)
#         serializer = ModuleSerializer(module, many=True)
#         return serializer.data
    
#     def get_topic(self, obj):
#         topic = Topic.objects.filter(module__subject__course=obj)
#         serializer = TopicSerializer(topic, many=True)
#         return serializer.data



class LevelSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            if Level.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError(
                    "Level with this name already exists")
        return value

    def get_category_id(self, obj):
        return obj.category.id


class BatchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchType
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            if BatchType.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError(
                    "BatchType with this name already exists")
        return value


class CourseSerializer(serializers.ModelSerializer):
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

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


class CategorySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'active', 'photo']


class BranchCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = Branch_courses
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_branch_name(self, obj):
        return obj.branch.name
    
class BranchCourseAdditionalSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch_courses
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_branch_name(self, obj):
        return obj.branch.name
    
    def create(self, validated_data):
        print(validated_data,"llllllllllllllllllllllllllllllllllllllllllllllllll")
        return super().create(validated_data)
    


class Branch_coursesSerializer(serializers.ModelSerializer):
    batch_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = Branch_courses
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name
    def get_batch_name(self, obj):
        return obj.course.batch_type.name
    
    def get_year(self,obj):
        return obj.course.year

# class BranchCreateSerializer(serializers.ModelSerializer):
#     courses = serializers.ListField(child=serializers.IntegerField())
#     class Meta:
#         model = Branch
#         fields = '__all__'

#     def create(self, validated_data):
#         courses_data= validated_data.pop('courses')
#         branch = Branch.objects.create(**validated_data)
#         for course_id in courses_data:
#             try:
#                 course = Course.objects.get(id=course_id)
#                 Branch_courses.objects.create(branch=branch,course=course)
#                 # course.save()
#             except Course.DoesNotExist:
#                 # Handle case where course ID is invalid or does not exist
#                 pass
#         return branch


class BranchCreateSerializer(serializers.ModelSerializer):
    courses = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    course = serializers.SerializerMethodField(read_only=True)
    course_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            if Branch.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError(
                    "Branch with this name already exists")
        return value

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        branch = Branch.objects.create(**validated_data)
        for course_id in courses_data:
            try:
                course = Course.objects.get(id=course_id)
                Branch_courses.objects.create(branch=branch, course=course)
            except Course.DoesNotExist:
                pass
        return branch

    def get_course(self, obj):
        ans = []
        courses = Branch_courses.objects.filter(branch=obj.id).values('course')
        print(courses,'courseserializer')
        return [x['course'] for x in courses]

    # def get_course_details(self, obj):
    #     courses = Branch_courses.objects.filter(branch=obj.id).values('course')
    #     print(courses)
    #     ans = [x['course'] for x in courses]
    #     return [Course.objects.filter(id=x).values('id', 'name')[0] for x in ans]
    
    def get_course_details(self, obj):
        print("ddd")
        courses = Branch_courses.objects.filter(branch=obj.id).values('course')
        print(courses)
        ans = [x['course'] for x in courses]
        courses= Course.objects.filter(id__in=ans)
        ser = CourseSerializer(courses, many=True)
        print(ser.data,'serilizercoursedetails')
        return ser.data


class BranchCreateSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['name', 'location']

    # def save(self, **kwargs):
    #     instance = self.instance
    #     email = AuthHandlerIns.get_mail(request=self.context['request'])
    #     user = User.objects.get(email=email)
    #     instance._history_user = user
    #     instance.save(**kwargs)
    #     return instance
    
    def validate_name(self, value):
        """
        Check that the name field doesn't already exist for the same Branch
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            course = self.initial_data.get('course')
            if Course.objects.filter(name__iexact=name, course=course).exists():
                raise serializers.ValidationError(
                    "Course with this name already exists for this Branch")
        return value

class BranchSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), many=True, write_only=True)
    courses_details = CourseSerializer(
        many=True, read_only=True, source='courses')

    class Meta:
        model = Branch
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist for the same Branch
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            course = self.initial_data.get('course')
            if Course.objects.filter(name__iexact=name, course=course).exists():
                raise serializers.ValidationError(
                    "Course with this name already exists for this Branch")
        return value

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        branch = Branch.objects.create(**validated_data)
        for course in courses_data:
            branch.courses.add(course)
        return branch


class BatchSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    Branch_name = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    course_details = serializers.SerializerMethodField()


    class Meta:
        model = Batch
        fields = '__all__'
        # depth = 1

    def get_course_name(self, obj):
        return obj.course.name

    def get_Branch_name(self, obj):
        return obj.branch.name
    
    def get_application_count(self, obj):
        topic = Topic_batch.objects.filter(batch=obj.id,status="S").values('id')
        timetable = TimeTable.objects.filter(topic__in=topic).values('id')
        approvals = Approvals.objects.filter(timetable__in=timetable)
        return approvals.count()
    
    def get_course_details(self,obj):
        course = Course.objects.get(id=obj.course.course.id)
        ser = CourseSerializer(course)
        return ser.data
    
    

class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist for the same course
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            course = self.initial_data.get('course')
            if Subject.objects.filter(name__iexact=name, course=course).exists():
                raise serializers.ValidationError(
                    "Subject with this name already exists for this course")
        return value

    def get_course_id(self, obj):
        return obj.course.id

    def get_course_name(self, obj):
        return obj.course.name

    def get_level_name(self, obj):
        return obj.course.level.name

    def get_level_id(self, obj):
        return obj.course.level.id

    def get_category_id(self, obj):
        return obj.course.level.category.id

    def get_category_name(self, obj):
        return obj.course.level.category.name
    
    

    


class ModuleSerializer(serializers.ModelSerializer):
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            subject = self.initial_data.get('subject')

            if Module.objects.filter(name__iexact=name, subject=subject).exists():
                raise serializers.ValidationError(
                    "Module with this name already exists")
        return value

    def get_subject_id(self, obj):
        return obj.subject.id

    def get_course_id(self, obj):
        return obj.subject.course.id

    def get_subject_name(self, obj):
        return obj.subject.name

    def get_course_name(self, obj):
        return obj.subject.course.name

    def get_level_name(self, obj):
        return obj.subject.course.level.name

    def get_level_id(self, obj):
        return obj.subject.course.level.id

    def get_category_id(self, obj):
        return obj.subject.course.level.category.id

    def get_category_name(self, obj):
        return obj.subject.course.level.category.name
    
    


class TopicSerializer(serializers.ModelSerializer):

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
    subtopic = serializers.SerializerMethodField()


    class Meta:
        model = Topic
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            module = self.initial_data.get('module')

            if Topic.objects.filter(name__iexact=name, module=module).exists():
                raise serializers.ValidationError(
                    "Topic with this name already exists")
        return value

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
    
    def get_subtopic(self, topic):
        try:
            subtopic = topic.subtopic_set.filter()
            ser = SubTopicSerializer(subtopic, many=True)
            return ser.data
        except SubTopic.DoesNotExist:
            return None
class SubTopicSerializerforexcel(serializers.ModelSerializer):
    
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



    class Meta:
        model = SubTopic
        fields = '__all__'

    def get_module_id(self, obj):
        return obj.topic.module.id

    def get_subject_id(self, obj):
        return obj.topic.module.subject.id

    def get_course_id(self, obj):
        return obj.topic.module.subject.course.id

    def get_module_name(self, obj):
        return obj.topic.module.name

    def get_subject_name(self, obj):
        return obj.topic.module.subject.name

    def get_course_name(self, obj):
        return obj.topic.module.subject.course.name

    def get_level_name(self, obj):
        return obj.topic.module.subject.course.level.name

    def get_level_id(self, obj):
        return obj.topic.module.subject.course.level.id

    def get_category_id(self, obj):
        return obj.topic.module.subject.course.level.category.id

    def get_category_name(self, obj):
        return obj.topic.module.subject.course.level.category.name
# description


class SubTopicSerializer(serializers.ModelSerializer):
    topic_id = serializers.SerializerMethodField()
    module_id = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        fields = '__all__'
        # fields = ['id', 'name', 'topic_name', 'module_name', 'subject_name', 'course_name']

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            topic = self.initial_data.get('topic')

            if SubTopic.objects.filter(name__iexact=name, topic=topic).exists():
                raise serializers.ValidationError(
                    "SubTopic with this name already exists")
        return value

    def get_topic_id(self, obj):
        return obj.topic.id

    def get_module_id(self, obj):
        return obj.topic.module.id

    def get_subject_id(self, obj):
        return obj.topic.module.subject.id

    def get_course_id(self, obj):
        return obj.topic.module.subject.course.id

    def get_topic_name(self, obj):
        return obj.topic.name

    def get_module_name(self, obj):
        return obj.topic.module.name

    def get_subject_name(self, obj):
        return obj.topic.module.subject.name

    def get_course_name(self, obj):
        return obj.topic.module.subject.course.name

    def get_level_name(self, obj):
        return obj.topic.module.subject.course.level.name

    def get_level_id(self, obj):
        return obj.topic.module.subject.course.level.id

    def get_category_id(self, obj):
        return obj.topic.module.subject.course.level.category.id

    def get_category_name(self, obj):
        return obj.topic.module.subject.course.level.category.name


class TopicSerializerWithSubTopics(TopicSerializer):
    subtopics = SubTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'


class SubjectFullSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Subject
        fields = '__all__'


class ModuleFullSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Module
        fields = '__all__'


class TopicFulldetails(serializers.ModelSerializer):
    module = ModuleFullSerializer()

    class Meta:
        model = Topic
        fields = '__all__'


class Timetableserializersnew(serializers.ModelSerializer):

    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()
    approvals_user = serializers.SerializerMethodField()
    app_status=serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = '__all__'

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
       
        if obj.id in self.context['available'] :
            key= "Available"
        if  obj.id in self.context['approvals'] :
            key= "Applied"
        try:
            if obj.id in self.context['booked']:
                key= "Booked"
            if obj.id in self.context['history']:
                key= "Finished"
        except:
            pass
        # key= "Other"
        return key


class Timetableserializersnew1(serializers.ModelSerializer):

    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = '__all__'

    def get_day(self, obj):
        k = list((str(obj.date)))[-2:]
        return str(k[0]+k[1])

    def get_year(self, obj):
        k = list((str(obj.date)))[:4]
        return str(k[0]+k[1]+k[2]+k[3])

    def get_month(self, obj):
        k = list((str(obj.date)))[5:8]
        return str(k[0]+k[1])

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


class Timetableserializers(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subtopic_list = serializers.SerializerMethodField()

    faculty_list = serializers.SerializerMethodField()
    faculty_details = serializers.SerializerMethodField()
    faculty_rating = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    faculty_salary = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    combined = serializers.SerializerMethodField()


    class Meta:
        model = TimeTable
        fields = '__all__'

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.topic.topic.name

    def get_course_name(self, obj):
        return obj.course.course.course.name

    def get_faculty_list(self, obj):
        app = Approvals.objects.filter(timetable=obj.id)
        # print(app, "appppppspapspaps")
        serializer = Approvalserializers(app, many=True)
        # print(serializer)
        return serializer.data

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

    def get_faculty_salary(self, obj):
        try:
            if obj.faculty:
                fac = Faculty.objects.get(user=obj.faculty.id)
                fas = Faculty_Salary.objects.filter(
                    faculty=fac, level=obj.course.course.course.level).first()
                # print("kkkkkkkkkkkkkkkkkkkkkkk")
                if fas:
                   
                    return fas.fixed_salary.salaryscale
            return None
        except:
            return None

    def get_day(self, obj):
        k = list((str(obj.date)))[-2:]
        return str(k[0]+k[1])

    def get_year(self, obj):
        k = list((str(obj.date)))[:4]
        return str(k[0]+k[1]+k[2]+k[3])

    def get_month(self, obj):
        k = list((str(obj.date)))[5:8]
        return str(k[0]+k[1])

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
        
class TimetableserializersCombined(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subtopic_list = serializers.SerializerMethodField()

    faculty_list = serializers.SerializerMethodField()
    faculty_details = serializers.SerializerMethodField()
    faculty_rating = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    faculty_salary = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    class Meta:
        model = TimeTable
        fields = '__all__'

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.topic.topic.name

    def get_course_name(self, obj):
        return obj.course.course.course.name

    def get_faculty_list(self, obj):
        app = Approvals.objects.filter(timetable=obj.id)
        print(app, "appppppspapspaps")
        serializer = Approvalserializers(app, many=True)
        print(serializer)
        return serializer.data

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

    def get_faculty_salary(self, obj):
        try:
            if obj.faculty:
                fac = Faculty.objects.get(user=obj.faculty.id)
                fas = Faculty_Salary.objects.filter(
                    faculty=fac, level=obj.course.course.course.level).first()
                print("kkkkkkkkkkkkkkkkkkkkkkk")
                if fas:
                    print(fas.fixed_salary)
                    return fas.fixed_salary.salaryscale
            return None
        except:
            return None

    def get_day(self, obj):
        k = list((str(obj.date)))[-2:]
        return str(k[0]+k[1])

    def get_year(self, obj):
        k = list((str(obj.date)))[:4]
        return str(k[0]+k[1]+k[2]+k[3])

    def get_month(self, obj):
        k = list((str(obj.date)))[5:8]
        return str(k[0]+k[1])

    def get_status(self, obj):
        return obj.topic.status
    
    def get_subtopic_list(self, obj):
        subtopic = Subtopic_batch.objects.filter(topic=obj.topic)
        serializer =Subtopic_batchSerializer(subtopic, many=True)
        return serializer.data

        



class Timetableserializersdate(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['date']


class FacultySerializerss(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class FacultySerializerssProfile(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class Approvalserializers(serializers.ModelSerializer):
    user = FacultySerializerss(read_only=True)
    # faculty = FacultySerializerssProfile(read_only=True)
    topic = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    faculty_place = serializers.SerializerMethodField()
    faculty_salary = serializers.SerializerMethodField()
    faculty_id = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()
    engaged = serializers.SerializerMethodField()

    class Meta:
        model = Approvals
        fields = '__all__'

    def get_topic(self, obj):
        return obj.timetable.topic.pk

    def get_topic_name(self, obj):
        return obj.timetable.topic.name

    def get_faculty_phone(self, obj):
        print("objsasdddddddddddddddddddddddddddddddddd")
        return obj.faculty.mobile

    def get_faculty_place(self, obj):
        fac = Faculty.objects.get(user=obj.faculty)
        return fac.district

    def get_faculty_id(self, obj):
        fac = Faculty.objects.get(user=obj.faculty)
        return fac.pk

    def get_faculty_name(self, obj):
        fac = Faculty.objects.get(user=obj.faculty)
        return fac.name

    def get_rating(self, obj):
        fac = Faculty.objects.get(user=obj.faculty)
        tim = TimeTable.objects.filter(faculty=obj.faculty).values('id')
        rating = Rating.objects.filter(
            rating_on__in=tim).aggregate(Avg('choice'))
        print(rating['choice__avg'])
        return rating['choice__avg']

    def get_faculty_salary(self, obj):

        fac = Faculty.objects.get(user=obj.faculty.id)
        print(type(obj.timetable.course.course.course), "ajith")
        fas = Faculty_Salary.objects.filter(
            faculty=fac, level=obj.timetable.course.course.course.level).first()
        if fas:
            try:
                # print(fas.fixed_salary.salaryscale)
                return fas.fixed_salary.salaryscale
            except:
                return None
        return None

    def get_engaged(self,obj):
        return TimeTable.objects.filter(date=obj.timetable.date,faculty=obj.timetable.faculty).exists()


class Approvalserializers_get(serializers.ModelSerializer):
    # user = FacultySerializerss(read_only=True )
    faculty_name = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    # faculty_ = serializers.SerializerMethodField()

    class Meta:
        model = Approvals
        fields = '__all__'

    def get_faculty_name(self, obj):
        return Faculty.objects.get(user=obj.faculty).name

    def get_faculty_phone(self, obj):
        return obj.faculty.mobile


class Approvalserializerspost(serializers.ModelSerializer):
    # faculty = FacultySerializerss()
    class Meta:
        model = Approvals
        fields = '__all__'


class TimeTableSearchSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        # fields = ('id', 'date', 'branch', 'batch', 'topic', 'course',  'faculty')
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.name


# class FacultyAttendenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FacultyAttendence
#         fields = '__all__'


class ExamScheduleSerializer(serializers.ModelSerializer):
    # invigilator_name = UserSerializer()
    # discussion_staffs = UserSerializer(many=True)
    # batch = BatchSerializer()

    class Meta:
        model = ExamSchedule
        fields = '__all__'


class TimeTableSearchSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        # # fields = ('id', 'date', 'branch', 'batch',
        #           'topic', 'course',  'faculty')
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.name


# class FacultyAttendenceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = FacultyAttendence
#         fields = '__all__'

#     def create(self, validated_data):
#         print("From Create")
#         Topic_batch.objects.filter(id=validated_data["subtopics_covered"][0].topic.id).update(status="F")
#         subtopic_covered = validated_data.pop('subtopics_covered')
#         faculty = FacultyAttendence(**validated_data)
#         faculty.save()
#         faculty.subtopics_covered.set(subtopic_covered)
#         subtopic_ids = [subtopic.id for subtopic in subtopic_covered]
#         Subtopic_batch.objects.filter(id__in=subtopic_ids).update(status=True)
#         return faculty
    
#     def update(self, instance, validated_data):
#         print("Updating")
#         Topic_batch.objects.filter(id=validated_data["subtopics_covered"][0].topic.id).update(status="F")
#         subtopic_covered = validated_data.pop('subtopics_covered')
#         instance = super().update(instance, validated_data)
#         instance.subtopics_covered.set(subtopic_covered)
#         subtopic_ids = [subtopic.id for subtopic in subtopic_covered]
#         Subtopic_batch.objects.filter(id__in=subtopic_ids).update(status=False)
#         return instance

class FacultyAttendenceSerializer(serializers.ModelSerializer):
    combinedwith = serializers.SerializerMethodField()
    
    class Meta:
        model = FacultyAttendence
        fields = '__all__'
    def get_combinedwith(self, obj):
        if obj.timetable.is_combined:
            timetable = obj.timetable
            combined_batches = timetable.combined_batch.all()
            return [batch.name for batch in combined_batches]
        else:
            return ([])

    def create(self, validated_data):
        print("From Create")
        tt=TimeTable.objects.get(id=validated_data["timetable"].id).topic.id
        print("TT")
        print(tt)
        Topic_batch.objects.filter(id=tt).update(status="F")
        subtopic_covered = validated_data.pop('subtopics_covered')
        faculty = FacultyAttendence(**validated_data)
        faculty.save()
        faculty.subtopics_covered.set(subtopic_covered)
        subtopic_ids = [subtopic.id for subtopic in subtopic_covered]
        sub=Subtopic_batch.objects.filter(id__in=subtopic_ids)
        for i in sub:
            i.status=True
            i.save()
        return faculty
    
    def update(self, instance, validated_data):
        print("Updating")
        if validated_data.get("subtopics_covered"):
            Topic_batch.objects.filter(id=validated_data["subtopics_covered"][0].topic.id).update(status="F")
            subtopic_covered = validated_data.pop('subtopics_covered')
            instance = super().update(instance, validated_data)
            instance.subtopics_covered.set(subtopic_covered)
            subtopic_ids = [subtopic.id for subtopic in subtopic_covered]
            Subtopic_batch.objects.filter(id__in=subtopic_ids).update(status=True)
        else:
            instance = super().update(instance, validated_data)
        return instance


class ExamScheduleSerializer(serializers.ModelSerializer):
    # invigilator_name = UserSerializer()
    # discussion_staffs = UserSerializer(many=True)
    # batch = BatchSerializer()

    class Meta:
        model = ExamSchedule
        fields = '__all__'


def validate_year(value):
    if value < 2023 or value > 2100:
        raise serializers.ValidationError("Year must be between 2023 and 2100")
    elif len(str(value)) != 4:
        raise serializers.ValidationError("Year must be a 4-digit integer")


class holidaysserializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = ('id', 'date', 'name')


# facultyblockwithreson
class facultyblockwithreson(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'blockreason')


class facultyrejectwithreson(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'is_rejected')


class Subject_batchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject_batch

        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    choice = serializers.ChoiceField(choices=CHOICES)
    user_det = serializers.SerializerMethodField()
    rating_det = serializers.SerializerMethodField()
    choice_det = serializers.SerializerMethodField()
    
    class Meta:
        model = Rating
        # fields = ['id', 'user', 'rating_on', 'choice']
        fields = '__all__'
    def create(self, validated_data):
        choice = validated_data.pop('choice')
        rating = Rating.objects.create(**validated_data, choice=choice)
        return rating
    def get_user_det(self, obj):
        return obj.user.username  
    def get_choice_det(self, obj):
        return obj.choice 
    def get_rating_det(self, obj):
        return obj.rating_on.branch.name


class TopicBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic_batch
        fields = '__all__'


class TimeTableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['faculty', 'topic']

    def update(self, instance, validated_data):
        if instance.is_combined:
            timetables = TimeTable.objects.filter(date=instance.date,batch__in=instance.combined_batch.values('id'))
            for timetable in timetables:
                timetable.faculty=validated_data.get('faculty', instance.faculty)
                timetable.save()
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.save()
        return instance

    def delete(self, instance):
        # Get the related topic instance
        print("hellooooo22222222222")
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
            # Update the status of the topic instance
            topic.status = 'P'
            topic.save()
            # Delete the timetable instance
            instance.delete()


class BatchViewsetSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    original_course = serializers.SerializerMethodField()
    batch_course= serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = '__all__'

    def get_course_name(self, obj):
        return obj.course.name

    def get_branch_name(self, obj):
        return obj.branch.name
    
    def get_original_course(self, obj):
        try:
            return obj.course.course.id
        except:
            return None
    
    def get_batch_course(self, obj):
        return Course_batch.objects.get(batch=obj).id

class TopicBatchSerializerNew(serializers.ModelSerializer):
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
    subtopic = serializers.SerializerMethodField()


    class Meta:
        model = Topic_batch
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            module = self.initial_data.get('module')

            if Topic.objects.filter(name__iexact=name, module=module).exists():
                raise serializers.ValidationError(
                    "Topic with this name already exists")
        return value

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
        return obj.module.subject.course.course.course.level.name

    def get_level_id(self, obj):
        return obj.module.subject.course.course.course.level.id

    def get_category_id(self, obj):
        return obj.module.subject.course.course.course.level.category.id

    def get_category_name(self, obj):
        return obj.module.subject.course.course.course.level.category.name
    
    def get_subtopic(self,obj):
        subtopic = Subtopic_batch.objects.filter(topic=obj.id)
        return Subtopic_batchSerializer(subtopic, many=True).data
    
class SubtopicBranchNewDragSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtopic_branch
        fields = '__all__'

class SubtopicNewDragSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopic
        fields = '__all__'

class TopicBranchNewDragSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    time_needed = serializers.SerializerMethodField()
    class Meta:
        model = Topic_branch
        fields = '__all__'

    
    def get_subtopic(self,obj):
        subtopic = Subtopic_branch.objects.filter(topic=obj.id).order_by('priority')
        return SubtopicBranchNewDragSerializer(subtopic, many=True).data
    
    def get_time_needed(self,obj):
        return obj.topic.time_needed
    
class TopicNewDragSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    
    def get_subtopic(self,obj):
        subtopic = SubTopic.objects.filter(topic=obj.id).order_by('priority')
        return SubtopicNewDragSerializer(subtopic, many=True).data


class ModuleBranchNewDragSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()

    class Meta:
        model = Module_branch
        fields = '__all__'

    
    def get_topics(self,obj):
        topic = Topic_branch.objects.filter(module=obj.id).order_by('priority')
        return TopicBranchNewDragSerializer(topic, many=True).data
    
    def get_badge(self,obj):
        return obj.module.badge

class ModuleNewDragSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'

    
    def get_topics(self,obj):
        topic = Topic.objects.filter(module=obj.id).order_by('priority')
        return TopicNewDragSerializer(topic, many=True).data

class SubjectBranchNewDragSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()

    class Meta:
        model = Subject_branch
        fields = '__all__'

    
    def get_modules(self,obj):
        subject = Module_branch.objects.filter(subject=obj.id).order_by('priority')
        return ModuleBranchNewDragSerializer(subject, many=True).data
    
    def get_badge(self,obj):
        return obj.subject.badge
    
class SubjectNewDragSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    
    def get_modules(self,obj):
        subject = Module.objects.filter(subject=obj.id).order_by('priority')
        return ModuleNewDragSerializer(subject, many=True).data

class CourseBranchNewDragSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    class Meta:
        model = Course_branch
        fields = '__all__'

    
    def get_subject(self,obj):
        print("yesas")
        subject = Subject_branch.objects.filter(course=obj.id).order_by('priority')
        return SubjectBranchNewDragSerializer(subject, many=True).data
    

class CourseNewDragSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    
    def get_subject(self,obj):
        subject = Subject.objects.filter(course=obj.id).order_by('priority')
        return SubjectNewDragSerializer(subject, many=True).data
    
    
class ReviewQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewQuestions
        fields = ('id', 'choice', 'question1', 'question2', 'question3', 'question4', 'question5')

class ReviewSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    # on_question = ReviewQuestionsSerializer()

    class Meta:

        model = Review
        # fields = ['id', 'user','choice','question_on', 'review_on', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5','feedback','users']
        fields = '__all__'
    def get_users(self,obj):
        return obj.user.username
    
    
    

# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'on_question', 'review_on', 'choice', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'feedback']

#     def get_user(self, obj):
#         return obj.user.username

#     def validate(self, data):
#         # Check if required fields are present and not null
#         required_fields = ['choice', 'user', 'review_on', 'on_question']
#         for field in required_fields:
#             if field not in data or data[field] is None:
#                 raise serializers.ValidationError({field: [f"{field} field is required and should not be null."]})

#         # Check uniqueness constraint
#         user = data['user']
#         review_on = data['review_on']
#         if Review.objects.filter(user=user, review_on=review_on, is_delete=False).exists():
#             raise serializers.ValidationError({"non_field_errors": ["Review for this user and review_on already exists."]})

#         return data
    
class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['id', 'date', 'branch', 'batch', 'topic', 'course', 'faculty', 'description']

    def create(self, validated_data):
        return TimeTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.branch = validated_data.get('branch', instance.branch)
        instance.batch = validated_data.get('batch', instance.batch)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.course = validated_data.get('course', instance.course)
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    


class Subtopic_batchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic_batch
        fields = '__all__'

class TimetableAttendanceSerializer(serializers.ModelSerializer):
    branch_name=serializers.SerializerMethodField()
    batch_name =serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subtopic_name = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    payment_done = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    # subtopics_covered = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    faculty_attendenceid = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    testimonial = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = TimeTable
        fields = '__all__'

    

    def get_branch_name(self,obj):
        return obj.branch.name
    
    def get_batch_name(self,obj):
        return obj.batch.name

    def get_course_name(self,obj):
        return obj.course.name
    
    def get_topic_name(self,obj):
        return obj.topic.name
    
    def get_subtopic_name(self,obj):
        subtopic= Subtopic_batch.objects.filter(topic=obj.topic)
        serializer=Subtopic_batchSerializer(subtopic, many=True)
        return serializer.data
    
    def get_faculty_attendenceid(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.id
        except:
            return None
        
    def get_testimonial(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.testimonial
        except:
            return None
    def get_status(self, obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.status
        except:
            return None
    
    def get_cost(self,obj):
        try:
            if obj.faculty:
                salary = Faculty_Salary.objects.get(faculty=Faculty.objects.get(user=obj.faculty),level = obj.course.course.course.level,is_online=False)
                return salary.fixed_salary.salaryscale
        except Exception as e:
            return None
    # def get_attendance(self,obj):
    #     faculty_attendance = FacultyAttendence.objects.filter(timetable=obj.id)
    #     serializer = FacultyAttendenceSerializer(faculty_attendance)
    #     return serializer.data
    def get_rating(self, obj):
        if obj.faculty:
            tim = TimeTable.objects.filter(faculty=obj.faculty.id).values('id')
            rating = Rating.objects.filter(
                rating_on__in=tim).aggregate(Avg('choice'))
            return rating['choice__avg']
        else:
            return None

    def get_amount_paid(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.paid_amount
        except:
            return None
        
    def get_payment_method(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.payment_method
        except:
            return None
        
    def get_payment_done(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.payment_done
        except:
            return None
        
    def get_start_time(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.start_time
        except:
            return None
        
    def get_end_time(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.end_time
        except:
            return None
        
    def get_hours(self,obj):
        try:
            facultyattendance=FacultyAttendence.objects.get(timetable=obj.id)
            return facultyattendance.hours
        except:
            return None
        
    # def get_subtopics_covered(self,obj):
    #     try:
    #         facultyattendance = FacultyAttendence.objects.get(timetable=obj.id)
    #         subtopics = facultyattendance.subtopics_covered.all()
    #         serializer= Subtopic_batchSerializer(subtopics, many=True)
    #         return serializer.data
    #     except:
    #         return None
        
    def get_name(self,obj):
        try:
            return obj.faculty.username
        except:
            return None
        # try:
        #     facultyattendance=TimeTable.objects.get(id=obj.id)
        #     return facultyattendance.faculty.username
        # except:
        #     return None
        
 
class FacultyAttendenceSubtopicBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic_batch
        fields = ['status']


    
class BookedTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

    

class Batchholidaysserializer(serializers.ModelSerializer):

    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = SpecialHoliday
        fields = '__all__'


    def get_day(self, obj):
        day = list((str(obj.date)))[-2:]
        return str(day[0]+day[1])

    def get_year(self, obj):
        year = list((str(obj.date)))[:4]
        return str(year[0]+year[1]+year[2]+year[3])

    def get_month(self, obj):
        month = list((str(obj.date)))[5:8]
        return str(month[0]+month[1])
    

class SubjectDetailSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name','modules']

    def get_modules(self, subject):
        modules = subject.module_set.all()
        serializer = ModuleDetailSerializer(modules, many=True)
        return serializer.data
    
class ModuleDetailSerializer(serializers.Serializer):
    topic = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'name','topic']

    def get_topic(self, module):
        try:
            topic = module.topic_set.filter()
            ser = TopicSerializer(topic, many=True)
            return ser.data
        except Topic.DoesNotExist:
            return None
        


    

class CourseDetailSerializer(serializers.ModelSerializer):
    # subjects = SubjectDetailSerializer(many=True, read_only=True)
    # modules = ModuleSerializer(many=True, read_only=True)
    # topic = TopicSerializer(many=True, read_only=True)
    subject = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id','name','subject','module','topic']

    def get_subject(self, course):
        try:
            subject = course.subject_set.filter()
            ser = SubjectSerializer(subject, many=True)
            return ser.data
        except Subject.DoesNotExist:
            return None
    
    # def get_subject(self, obj):
    #     subject = Subject.objects.filter(course=obj)
    #     serializer = SubjectSerializer(subject, many=True)
    #     return serializer.data
        
        
    def get_module(self, obj):
        module = Module.objects.filter(subject__course=obj)
        serializer = ModuleSerializer(module, many=True)
        return serializer.data
    
    def get_topic(self, obj):
        topic = Topic.objects.filter(module__subject__course=obj)
        serializer = TopicSerializer(topic, many=True)
        return serializer.data
    


class TimetableCombinedPercentageSerializers(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    course_name = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    subtopic_list = serializers.SerializerMethodField()

    faculty_list = serializers.SerializerMethodField()
    faculty_details = serializers.SerializerMethodField()
    faculty_rating = serializers.SerializerMethodField()
    faculty_phone = serializers.SerializerMethodField()
    faculty_salary = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    combined = serializers.SerializerMethodField()
    topic_percentage = serializers.SerializerMethodField()


    class Meta:
        model = TimeTable
        fields = '__all__'

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_topic_name(self, obj):
        return obj.topic.topic.topic.name

    def get_course_name(self, obj):
        return obj.course.course.course.name

    def get_faculty_list(self, obj):
        app = Approvals.objects.filter(timetable=obj.id)
        serializer = Approvalserializers(app, many=True)
        return serializer.data

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

    def get_faculty_salary(self, obj):
        try:
            if obj.faculty:
                fac = Faculty.objects.get(user=obj.faculty.id)
                fas = Faculty_Salary.objects.filter(
                    faculty=fac, level=obj.course.course.course.level).first()
                if fas:
                    return fas.fixed_salary.salaryscale
            return None
        except:
            return None

    def get_day(self, obj):
        k = list((str(obj.date)))[-2:]
        return str(k[0]+k[1])

    def get_year(self, obj):
        k = list((str(obj.date)))[:4]
        return str(k[0]+k[1]+k[2]+k[3])

    def get_month(self, obj):
        k = list((str(obj.date)))[5:8]
        return str(k[0]+k[1])

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
        

    def get_topic_percentage(self, obj):
        timetable = self.context.get('timetable')
        # subtopic1 = Subtopic_batch.objects.filter(topic=timetable.topic).order_by('name')
        # subtopic2 =Subtopic_batch.objects.filter(topic=obj.topic).order_by('name')
        # similarity={}
        # for i in range(0,min(len(subtopic1),len(subtopic2))):
            
        #     similarity[subtopic1[i].name]={subtopic2[i].name:calculate_similarity(subtopic2[i].name,subtopic1[i].name)}

        # return similarity
        return calculate_similarity(timetable.topic.name,obj.topic.name) 
       


def calculate_similarity(string1, string2):
    set1 = set(string1.lower())
    set2 = set(string2.lower())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection) / len(union)
    similarity_percentage = similarity * 100
    return similarity_percentage      




class BatchTopicSerializer(serializers.ModelSerializer):

    module_id = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    subtopic = serializers.SerializerMethodField()


    class Meta:
        model = Topic_batch
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            module = self.initial_data.get('module')

            if Topic_batch.objects.filter(name__iexact=name, module=module).exists():
                raise serializers.ValidationError(
                    "Topic with this name already exists")
        return value

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
    
    def get_subtopic(self, obj):
        try:
            # subtopic = topic.subtopic_set.filter()
            subtopic= Subtopic_batch.objects.filter(topic__id=obj.id)
            ser = Subtopic_batchSerializer(subtopic, many=True)
            return ser.data
        except SubTopic.DoesNotExist:
            return None


class MaterialSubTopicSerializer(serializers.ModelSerializer):
    topic_id = serializers.SerializerMethodField()
    module_id = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        fields = '__all__'
        # fields = ['id', 'name', 'topic_name', 'module_name', 'subject_name', 'course_name']

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            topic = self.initial_data.get('topic')

            if SubTopic.objects.filter(name__iexact=name, topic=topic).exists():
                raise serializers.ValidationError(
                    "SubTopic with this name already exists")
        return value
    
    def get_status(self, obj):
        user = self.context.get('faculty')
        faculty = Faculty.objects.get(user=user)
        if Material.objects.filter(subtopic__in=[obj.id],faculty=faculty).exists():
            return True
        return False

    def get_topic_id(self, obj):
        return obj.topic.id

    def get_module_id(self, obj):
        return obj.topic.module.id

    def get_subject_id(self, obj):
        return obj.topic.module.subject.id

    def get_course_id(self, obj):
        return obj.topic.module.subject.course.id

    def get_topic_name(self, obj):
        return obj.topic.name

    def get_module_name(self, obj):
        return obj.topic.module.name

    def get_subject_name(self, obj):
        return obj.topic.module.subject.name

    def get_course_name(self, obj):
        return obj.topic.module.subject.course.name

    def get_level_name(self, obj):
        return obj.topic.module.subject.course.level.name

    def get_level_id(self, obj):
        return obj.topic.module.subject.course.level.id

    def get_category_id(self, obj):
        return obj.topic.module.subject.course.level.category.id

    def get_category_name(self, obj):
        return obj.topic.module.subject.course.level.category.name


class CourseBranchSerilizer(serializers.ModelSerializer):

    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()


    class Meta:
        model = Course_branch
        fields = '__all__'

    def get_batch_name(self, obj):
        return obj.course.batch_type.name

    def get_level_id(self, obj):
        return obj.course.level.id

    def get_category_id(self, obj):
        return obj.course.level.category.id

    def get_level_id(self, obj):
        return obj.course.level.id

    def get_category_id(self, obj):
        return obj.course.level.category.id

    def get_level_name(self, obj):
        return obj.course.level.name

    def get_category_name(self, obj):
        return obj.course.level.category.name
    
    def get_year(self, obj):
        return obj.course.year
    
    def get_photo(self, obj):
        return obj.course.photo.url if obj.course.photo else None
    

class BranchTopicSerializer(serializers.ModelSerializer):

    module_id = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()


    class Meta:
        model = Topic_branch
        fields = '__all__'

    def validate_name(self, value):
        """
        Check that the name field doesn't already exist in the database
        """
        if self.context['request'].method == 'POST':
            name = value.lower()
            module = self.initial_data.get('module')

            if Topic.objects.filter(name__iexact=name, module=module).exists():
                raise serializers.ValidationError(
                    "Topic with this name already exists")
        return value

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
    
    def get_subtopic(self, topic):
        try:
            subtopic = topic.subtopic_set.filter()
            ser = SubTopicSerializer(subtopic, many=True)
            return ser.data
        except SubTopic.DoesNotExist:
            return None



class OnlineCategorySerializer(serializers.ModelSerializer):

    # level = serializers.SerializerMethodField()
    # courses = serializers.SerializerMethodField()
    # subjects = serializers.SerializerMethodField()
    # module = serializers.SerializerMethodField()
    # topic = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

        
class OnlineLevelSerializer(serializers.ModelSerializer):

    # level = serializers.SerializerMethodField()
    # courses = serializers.SerializerMethodField()
    # subjects = serializers.SerializerMethodField()
    # module = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    class Meta:
        model = Level
        fields = '__all__'

    def get_course_count(self, obj):
        return len(Course.objects.filter(level__id=obj.id,is_online=True))



class CourseOnlineSerializer(serializers.ModelSerializer):
    # level_id = serializers.SerializerMethodField()
    # category_id = serializers.SerializerMethodField()
    # level_name = serializers.SerializerMethodField()
    # category_name = serializers.SerializerMethodField()
    subject_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_subject_count(self, obj):
        return len(Subject.objects.filter(course__id=obj.id))


class CourseApproveNewSerializer(serializers.ModelSerializer):
    level_id = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    batch_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

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
    

from collections import OrderedDict

class CourseNewMaterialSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()
    batch_type_name=serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    
    def get_subject(self, obj):
        print("subject")
        fac = self.context.get('fac')
        print(obj,"jkjjjjjj",fac,fac['subject'])

        subject = Subject.objects.filter(course=obj.id, id__in=fac['subject']).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        ser=SubjectNewMatSerializer(subject, many=True, context={"fac": fac})
        return ser.data

    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(course = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data
    
    def get_batch_type_name(self,obj):
        return obj.batch_type.name
    
    
        

class SubjectNewMatSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    
    def get_modules(self,obj):
        print("get_modules")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # mid=[i.module.id for i in fac]
        subject = Module.objects.filter(subject=obj.id,id__in=fac['module']).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        mod=ModuleNewMatSerializer(subject, many=True,context={"fac":fac})
        return mod.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(subject = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data


class ModuleNewMatSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'

    
    def get_topics(self,obj):
        print("get_topics")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # tid=[i.topic.id for i in fac]
        topic = Topic.objects.filter(module=obj.id,id__in=fac['topic']).order_by('priority')
        print(topic.values('id'),"hhhhhhhhhhhhhh")
        ser=TopicNewMatSerializer(topic, many=True,context={"fac":fac})
        return ser.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(module = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data
    
class TopicNewMatSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    
    def get_subtopic(self,obj):
        print("get_subtopic")
        # fac=self.context.get('fac')
        # print(fac,"TIp")
        # tid=[i.topic.id for i in fac]
        subtopic = SubTopic.objects.filter(topic=obj.id).order_by('priority')
        ser=SubtopicNewMatSerializer(subtopic, many=True)
        return ser.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(topic = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data

class MaterialReferenceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    user_name =serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = MaterialReference
        fields = '__all__'

    def get_user_name(self,obj):
        facultyname = Faculty.objects.get(user = obj.user)
        return facultyname.name
    def get_file(self,obj):
        return obj.materialupload.file.url 
    def get_created_date(self,obj):
        return obj.materialupload.created_at 
    def get_name(self,obj):
        return obj.materialupload.name 

class SubtopicNewMatSerializer(serializers.ModelSerializer):
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        fields = '__all__'
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(subtopic = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data


class CourseBatchNewDragSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    class Meta:
        model = Course_batch
        fields = '__all__'

    
    def get_subject(self,obj):
        subject = Subject_batch.objects.filter(course=obj.id).order_by('priority')
        return SubjectBatchNewDragSerializer(subject, many=True).data
    

class SubjectBatchNewDragSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()

    class Meta:
        model = Subject_batch
        fields = '__all__'

    
    def get_modules(self,obj):
        subject = Module_batch.objects.filter(subject=obj.id).order_by('priority')
        return ModuleBatchNewDragSerializer(subject, many=True).data
    
    def get_badge(self,obj):
        return obj.subject.subject.badge
    

class ModuleBatchNewDragSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()

    class Meta:
        model = Module_batch
        fields = '__all__'

    
    def get_topics(self,obj):
        topic = Topic_batch.objects.filter(module=obj.id).order_by('priority')
        return TopicBranchNewDragSerializer(topic, many=True).data
    
    def get_badge(self,obj):
        return obj.module.module.badge
    
class TopicBranchNewDragSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    time_needed = serializers.SerializerMethodField()
    class Meta:
        model = Topic_batch
        fields = '__all__'

    
    def get_subtopic(self,obj):
        subtopic = Subtopic_batch.objects.filter(topic=obj.id).order_by('priority')
        return SubtopicBatchNewDragSerializer(subtopic, many=True).data
    
    def get_time_needed(self,obj):
        return obj.topic.topic.time_needed
    
class SubtopicBatchNewDragSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtopic_batch
        fields = '__all__'



class FacultyLimitaionSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model = FacultyLimitaion
        fields = '__all__'

    def get_branch_name(self,obj):
        if obj.branch:
            return obj.branch.name
        


class CourseNewMaterialAdminSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    
    def get_subject(self, obj):
        print("subject")
        fac = self.context.get('fac')
        print(obj,"jkjjjjjj",fac,fac['subject'])

        subject = Subject.objects.filter(course=obj.id, id__in=fac['subject']).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        ser=SubjectNewMatAdminSerializer(subject, many=True, context={"fac": fac})
        return ser.data

    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(course = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data
    
class SubjectNewMatAdminSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    
    def get_modules(self,obj):
        print("get_modules")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # mid=[i.module.id for i in fac]
        subject = Module.objects.filter(subject=obj.id,id__in=fac['module']).order_by('priority')
        print(subject.values('id'),"hhhhhhhhhhhhhh")
        mod=ModuleNewMatAdminSerializer(subject, many=True,context={"fac":fac})
        return mod.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(subject = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data



class ModuleNewMatAdminSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'

    
    def get_topics(self,obj):
        print("get_topics")
        fac=self.context.get('fac')
        print(obj,"jkjjjjjj",fac)
        # tid=[i.topic.id for i in fac]
        topic = Topic.objects.filter(module=obj.id,id__in=fac['topic']).order_by('priority')
        print(topic.values('id'),"hhhhhhhhhhhhhh")
        ser=TopicNewMatAdminSerializer(topic, many=True,context={"fac":fac})
        return ser.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(module = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data
    
class TopicNewMatAdminSerializer(serializers.ModelSerializer):
    subtopic = serializers.SerializerMethodField()
    meterial =serializers.SerializerMethodField()
    approved_metrial = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    
    def get_subtopic(self,obj):
        print("get_subtopic")
        # fac=self.context.get('fac')
        # print(fac,"TIp")
        # tid=[i.topic.id for i in fac]
        subtopic = SubTopic.objects.filter(topic=obj.id).order_by('priority')
        ser=SubtopicNewMatSerializer(subtopic, many=True)
        return ser.data
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(topic = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data
    
    def get_approved_metrial(self, obj):
        approved = ConvertedMaterials.objects.filter(topic=obj.id)
        ser = ConvertedMaterialsSerializer(approved, many=True)
        return ser.data



class SubtopicNewMatAdminSerializer(serializers.ModelSerializer):
    meterial =serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        fields = '__all__'
    
    def get_meterial(self, obj):
        mat = MaterialReference.objects.filter(subtopic = obj.id)
        return MaterialReferenceSerializer(mat,many=True).data



class ConvertedMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model= ConvertedMaterials
        fields= '__all__'

class FacultyHistorySerializer(serializers.Serializer):
    date = serializers.DateField()
    time_from = serializers.TimeField()
    time_to = serializers.TimeField()
    hours = serializers.IntegerField()
    branch = serializers.CharField()
    batch = serializers.CharField()
    level = serializers.CharField()
    course = serializers.CharField()
    topic = serializers.CharField()
    payment = serializers.CharField()
    paidamount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField()
    faculty_name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    fixed_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_salary = serializers.CharField()
    average_rating = serializers.FloatField()


class ApprovalModelViewsetSerializer(serializers.ModelSerializer):
    batch_name=serializers.SerializerMethodField()
    branch_name=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    topic_name=serializers.SerializerMethodField()
    user_name=serializers.SerializerMethodField()
    faculty_name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    date=serializers.SerializerMethodField()
    engaged=serializers.SerializerMethodField()
    class Meta:
        model=Approvals
        exclude=['is_delete']

    def get_batch_name(self,obj):
        return obj.timetable.batch.name
    
    def get_branch_name(self,obj):
        return obj.timetable.branch.name
    
    def get_course_name(self,obj):
        return obj.timetable.course.name
    
    def get_topic_name(self,obj):
        return obj.timetable.topic.name
    
    def get_user_name(self,obj):
        return obj.faculty.username
    
    def get_faculty_name(self,obj):
        return Faculty.objects.get(user=obj.faculty).name
    
    def get_mobile(self,obj):
        return obj.faculty.mobile
    
    def get_date(self,obj):
        return obj.timetable.date
    
    def get_engaged(self,obj):
        return TimeTable.objects.filter(date=obj.timetable.date,faculty=obj.timetable.faculty).exists()
    
class HistorySerializer(serializers.Serializer):
    history_change = serializers.SerializerMethodField()
    history_date = serializers.CharField()
    history_id = serializers.CharField()
    history_type = serializers.SerializerMethodField()
    history_user_email = serializers.CharField(source='history_user')
    history_user_id = serializers.CharField()
    id = serializers.CharField()
    instance_name =  serializers.SerializerMethodField()
    historical_user = serializers.SerializerMethodField()
    # branch_details = BranchSerializer(source='instance', read_only=True)

    def get_instance_name(self, obj):
        return obj.name
    
    def get_historical_user(self, obj):
        # h_user = HistoricalRecords.history.get(id=obj.id)
        try:
            return obj.history_user.id
        except:
            return None

    def get_history_type(self, obj):
        if obj.history_type == '+':
            return 'Create'
        elif obj.history_type == '-':
            return 'Delete'
        # elif obj.history_type == '~':
        #     return 'Update'
        elif obj.history_type == '~':
            if getattr(obj, 'is_delete', False):
                return 'Delete'  # Change history_type to 'Delete' if is_delete is True
            return 'Update'
        return 'Unknown'

    def get_history_change(self, obj):
        changes = {}

        if obj.history_type == '~':
            prev_records = obj.instance.history.filter(history_date__lt=obj.history_date)
            if prev_records.exists():
                prev_record = prev_records.latest('history_date')
                original_instance = prev_record.instance
                for field in original_instance._meta.fields:
                    old_value = getattr(prev_record, field.attname)
                    new_value = getattr(obj, field.attname)
                    if old_value != new_value:
                        changes[field.verbose_name] = {
                            'old': old_value,
                            'new': new_value,
                        }
                if 'is delete' in changes and changes['is delete']['new'] == True:
                    # return {'is_deleted': True, 'id': obj.instance.id}

                    return 'Deleted instance'
        return changes
    
class HistoryCourseSerializer(serializers.Serializer):
    history_change = serializers.SerializerMethodField()
    history_date = serializers.CharField()
    history_id = serializers.CharField()
    history_type = serializers.SerializerMethodField()
    history_user_email = serializers.CharField(source='history_user')
    history_user_id = serializers.CharField()
    id = serializers.CharField()
    historical_user = serializers.SerializerMethodField()
    # branch_details = BranchSerializer(source='instance', read_only=True)

    
    
    def get_historical_user(self, obj):
        # h_user = HistoricalRecords.history.get(id=obj.id)
        try:
            return obj.history_user.id
        except:
            return None

    def get_history_type(self, obj):
        if obj.history_type == '+':
            return 'Create'
        elif obj.history_type == '-':
            return 'Delete'
        # elif obj.history_type == '~':
        #     return 'Update'
        elif obj.history_type == '~':
            if getattr(obj, 'is_delete', False):
                return 'Delete'  # Change history_type to 'Delete' if is_delete is True
            return 'Update'
        return 'Unknown'

    def get_history_change(self, obj):
        changes = {}

        if obj.history_type == '~':
            prev_records = obj.instance.history.filter(history_date__lt=obj.history_date)
            if prev_records.exists():
                prev_record = prev_records.latest('history_date')
                original_instance = prev_record.instance
                for field in original_instance._meta.fields:
                    old_value = getattr(prev_record, field.attname)
                    new_value = getattr(obj, field.attname)
                    if old_value != new_value:
                        changes[field.verbose_name] = {
                            'old': old_value,
                            'new': new_value,
                        }
                if 'is delete' in changes and changes['is delete']['new'] == True:
                    # return {'is_deleted': True, 'id': obj.instance.id}

                    return 'Deleted instance'
        return changes
    

class ClassRoomSerializer(serializers.ModelSerializer):
    branch_name=serializers.SerializerMethodField()
    class Meta:
        model=ClassRooms
        exclude=['is_delete']

    def get_branch_name(self,obj):
        return obj.branch.name