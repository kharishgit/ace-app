from django.forms.models import model_to_dict
from django.db.models import Sum, F, Avg
from django.db import models
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from accounts.models import *
# from faculty import models  as fac
from simple_history.models import HistoricalRecords

from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from aceapp.settings.base import AWS_STORAGE_BUCKET_NAME_PUBLIC
# from aceapp.utils import MyS3Storage

from course.helper import branchcopycourse

from django.db.models.signals import pre_save, post_save
from django.db import transaction
from django.db.models import Q
from django.db.models import OuterRef, Subquery
# from aceapp.settings.base import STORAGES
from django.core.files.storage import get_storage_class
# Create your models here.

# new_storage_non_session = get_storage_class(STORAGES["public"]["BACKEND"])()
# new_storage_non_session = MyS3Storage(bucket_name='dev-aceapp-public')
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_delete=True)

class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude()    


class ClassLevel(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        

    objects = ActiveManager()
    newobjects = InActiveManager()
class Category(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category_entry',
                condition=~Q(is_delete=True)
            )
        ]


class Level(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField(null=False)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    
    objects = ActiveManager()
    newobjects = InActiveManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category','name'],
                name='unique_level_entry',
                condition=~Q(is_delete=True)
            )
        ]
    
class BatchType(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    
    objects = ActiveManager()
    newobjects = InActiveManager()
from storages.backends.s3boto3 import S3Boto3Storage
# 
class Course(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    description = models.TextField(null=True)
    batch_type = models.ForeignKey(BatchType, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    year = models.IntegerField(null=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    history = HistoricalRecords()

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['level','batch_type','name'],
                name='unique_course_entry',
                condition=~Q(is_delete=True)
            )
        ]




class Subject(models.Model):
    name = models.CharField(max_length=5000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    badge = models.TextField(default="Subject")
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name','course'], name='unique_subject_name_per_course'
    #         )
    #     ]
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course','name'],
                name='unique_subject_entry',
                condition=~Q(is_delete=True)
            )
        ]

    def _str_(self):
        return str(self.name) + "-" + str(self.course)
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()


class Module(models.Model):
    name = models.CharField(max_length=5000)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    badge = models.TextField(default="Module")
    active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name', 'subject'], name='unique_module_name_per_subject'
    #         )
    #     ]
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subject','name'],
                name='unique_module_entry',
                condition=~Q(is_delete=True)
            )
        ]

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

class Topic(models.Model):
    name = models.CharField(max_length=5000)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    active = models.BooleanField(default=True)
    day = models.IntegerField(default=None, null=True)
    order = models.IntegerField(null=True)
    time_needed = models.PositiveIntegerField(null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    video=models.ForeignKey('accounts.StudioVideo',on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name', 'module'], name='unique_topic_name_per_module'
    #         )
    #     ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['module','name'],
                name='unique_topic_entry',
                condition=~Q(is_delete=True)
            )
        ]

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()
    
    objects = ActiveManager()
    newobjects = InActiveManager()


class SubTopic(models.Model):
    name = models.CharField(max_length=5000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    time_needed = models.PositiveIntegerField(null=False)
    active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name', 'topic'], name='unique_subtopic_name_per_topic'
    #         )
    #     ]
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['topic','name'],
                name='unique_subtopic_entry',
                condition=~Q(is_delete=True)
            )
        ]

    def _str_(self):
        return str(self.name) + "-" + str(self.topic)


    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()
    
    objects = ActiveManager()
    newobjects = InActiveManager()


class Branch(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='branches_created')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='branches_updated', auto_created=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    updated_at = models.DateTimeField(default=timezone.now, auto_created=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    history = HistoricalRecords()
    description = models.TextField(null=True)
    user = models.ManyToManyField(User,null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    is_delete = models.BooleanField(default=False)

    def _str_(self):
        return self.name
    
    
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()
    


class Branch_courses(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'course'],
                name='unique_branch_course',
                condition=~Q(is_delete=True)
            )
        ]


class Batch(models.Model):
    WEEKDAYS_CHOICES = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )

    name = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey('Course_branch', on_delete=models.CASCADE)
    description = models.TextField(null=True)
    strength = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    fees = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    installment_count= models.IntegerField(default=0)
    working_days = MultiSelectField(choices=WEEKDAYS_CHOICES, default=[
                                    'Mon'], max_choices=7, validators=[MaxValueValidator(7)])
    exam_days = MultiSelectField(choices=WEEKDAYS_CHOICES, default=[
                                 'Mon'], max_choices=7, validators=[MaxValueValidator(7)])
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_special = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)

    # hours = models.IntegerField(null=True)
    # history = HistoricalRecords()

    def _str_(self):
        return str(self.name) + " - " + str(self.course) + " - " + str(self.branch)
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_batch_name',
                condition=~Q(is_delete=True)
            )
        ]
    



class Course_batch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey('Course_branch', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)

        self.is_delete = True
        self.save()
    
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['batch','course'],
                name='unique_batch_course',
                condition=~Q(is_delete=True)
            )
        ]


class Subject_batch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_batch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    subject = models.ForeignKey('Subject_branch', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Module_batch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject_batch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    module = models.ForeignKey('Module_branch', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Topic_batch(models.Model):
    topic_choice = [("P", "PENDING"), ("S", "SCEDULED"),
                    ("B", "BOOKED"), ("F", "FINISED")]
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    module = models.ForeignKey(Module_batch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    topic = models.ForeignKey('Topic_branch', on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    status = models.CharField(choices=topic_choice,
                              max_length=200, default="P")
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()

    objects = ActiveManager()
    newobjects = InActiveManager()


class Subtopic_batch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic_batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    subtopic = models.ForeignKey('Subtopic_branch',null=True,on_delete=models.CASCADE)
    time_needed = models.PositiveIntegerField(null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


## Class Rooms

class ClassRooms(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    room_no=models.PositiveIntegerField()
    floor=models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_delete = models.BooleanField(default=False)
    

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()
    

################ TimeTable #################################
from django.core.exceptions import ValidationError


class TimeTable(models.Model):
    date = models.DateField(default=datetime.now)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic_batch, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course_batch, default=None, on_delete=models.CASCADE)
    # photo = models.ImageField(null=True)
    faculty = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_combined = models.BooleanField(default=False)
    combined_batch = models.ManyToManyField(Batch, blank=True, related_name='combined_batch')
    room=models.ForeignKey(ClassRooms,on_delete=models.CASCADE,null=True,blank=True)


    def _str_(self):
        return str(self.date) + ' - ' + str(self.batch) + ' - ' + str(self.branch) + ' - ' + str(self.course)
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'batch'],
                name='unique_timetable_entry',
                condition=~Q(is_delete=True)
            )
        ]

################ TimeTable #################################

################ Aprovals #################################


class Approvals(models.Model):
    timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['faculty', 'timetable'],
                name='unique_approval_entry',
                condition=~Q(is_delete=True)
            )
        ]


class FacultyAttendence(models.Model):
    method_choice = [("CASH", "CASH"), ("UPI", "UPI"),
                    ("NETBANKING", "NETBANKING")]
    status_choice = [("PAID", "PAID"), ("PARTIAL", "PARTIAL"),
                    ("PENDING", "PENDING")]
    timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    name = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    hours = models.PositiveIntegerField(default=0,null=True, blank=True)
    subtopics_covered = models.ManyToManyField(Subtopic_batch,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # new field for storing the time of last update
    payment_done = models.CharField(choices=status_choice,default="PENDING",max_length=100)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_method= models.CharField(choices=method_choice,max_length=100,default="CASH")
    testimonial  = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    current_salary=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    salary_date = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['timetable'],
                name='unique_timetable_attendance',
                condition=~Q(is_delete=True)
            )
        ]


@receiver(post_save, sender=FacultyAttendence)
def combinedbatch_attnedence_mark(sender, instance, **kwargs):
    if instance.timetable.is_combined:
        batch = instance.timetable.combined_batch.all()
        time = TimeTable.objects.filter(date = instance.timetable.date,batch__in=batch)
        for t in time:
            t.topic.status = 'F'
            t.topic.save()
        
    # Topic_batch.objects.filter(id=instance.topic.id).update(status="S")

############   EXAM MANAGEMENT #################
class ExamSchedule(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    invigilator_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exam_invigilator')
    discussion_staffs = models.ManyToManyField(
        User, related_name='exam_discussion_staffs')
    description = models.TextField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    # history = HistoricalRecords()

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    def _str_(self):
        return str(self.date) + ' - ' + str(self.batch) + ' - ' + str(self.branch) + ' - ' + str(self.course)

    objects = ActiveManager()
    newobjects = InActiveManager()

############   EXAM MANAGEMENT ENDS #################


@receiver(post_save, sender=TimeTable)
def timetable_status_update(sender, instance, **kwargs):
    Topic_batch.objects.filter(id=instance.topic.id).update(status="S")

@receiver(post_save, sender=TimeTable)
def timetable_status_update_all(sender, instance, **kwargs):
    Topic_batch.objects.filter(batch=instance.batch).exclude(id__in=TimeTable.objects.filter(batch=instance.batch).values('topic')).update(status="P")

@receiver(post_save, sender=TimeTable)
def timetable_status_update(sender, instance, **kwargs):
    if instance.faculty:
        topic_batch_id = instance.topic.id
        Topic_batch.objects.filter(id=topic_batch_id).update(status="B")


@receiver(post_save, sender=Branch_courses)
def branch_course_creater(sender, instance, **kwargs):
    branch = Branch.objects.get(id=instance.branch.id)
    c_copy = Course.objects.filter(id=instance.course.id)
    print(c_copy, "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    for course in c_copy:
        batch = instance
        course_batch = Course_branch.objects.create(
            name=course.name, branch=branch, description=course.description, course=course,branch_courses=instance)
        s_copy = Subject.objects.filter(course=course)

        for subject in s_copy:

            print(course_batch, "hhhhhhhhhhhhhhhhhhhhsws",
                  type(subject))
            try:
                subject_batch = Subject_branch.objects.create(
                    course=course_batch, name=subject.name, branch=branch, description=subject.description, subject=subject)
            except Exception as e:
                print(e, "kkkkkkksas")
                return

            print("yessssssssssssssssssssssssssssss")
            module_copy = Module.objects.filter(subject=subject)

            for module in module_copy:
                module_batch = Module_branch.objects.create(
                    subject=subject_batch, name=module.name, branch=branch, description=module.description, module=module)

                topic_copy = Topic.objects.filter(module=module)

                for topic in topic_copy:
                    topic_batch = Topic_branch.objects.create(
                        module=module_batch, name=topic.name, branch=branch, description=topic.description, topic=topic, order=topic.order)

                    subtopic_copy = SubTopic.objects.filter(topic=topic)

                    for sutopic in subtopic_copy:
                        subtopic_batch = Subtopic_branch.objects.create(
                            topic=topic_batch, name=sutopic.name, branch=instance.branch, subtopic=sutopic,description=sutopic.description,time_needed=sutopic.time_needed)


@receiver(post_save, sender=Batch)
def batch_course_creater(sender, instance,created, **kwargs):
    if not created:
        return
    c_copy = Course_branch.objects.filter(id=instance.course.id,branch=instance.branch)
    print(c_copy)
    for course in c_copy:
        batch = instance
        course_batch = Course_batch.objects.create(
            name=course.name, batch=batch, description=course.description, course=c_copy[0])
        s_copy = Subject_branch.objects.filter(course=course,branch=instance.branch)
        i = 0
        for subject in s_copy:

            print(course_batch)
            subject_batch = Subject_batch.objects.create(
                course=course_batch, name=subject.name, batch=batch, description=subject.description, subject=subject)

            module_copy = Module_branch.objects.filter(subject=subject,branch=instance.branch)

            for module in module_copy:
                module_batch = Module_batch.objects.create(
                    subject=subject_batch, name=module.name, batch=batch, description=module.description, module=module)

                topic_copy = Topic_branch.objects.filter(module=module,branch=instance.branch)

                for topic in topic_copy:
                    topic_batch = Topic_batch.objects.create(
                        module=module_batch, name=topic.name, batch=batch, description=topic.description, topic=topic, order=topic.order)

                    subtopic_copy = Subtopic_branch.objects.filter(topic=topic,branch=instance.branch)

                    for sutopic in subtopic_copy:
                        subtopic_batch = Subtopic_batch.objects.create(
                            topic=topic_batch, name=sutopic.name, batch=batch,subtopic=sutopic,description=sutopic.description,time_needed=sutopic.time_needed)

@receiver(post_save, sender=Subject)
@transaction.atomic
def set_priority(sender, instance, created, **kwargs):
    try:
        if not instance.pk:
            highest_priorty = Subject.objects.filter(course=instance.course).aggregate(
                models.Max('priority'))['priority__max']
        instance.priority = highest_priorty+1 if highest_priorty is not None else 1
    except:
        pass
    
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            course_batch = Course_branch.objects.filter(course=instance.course)
            for i in course_batch:
                highest_priorty = Subject_branch.objects.filter(course=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Subject_branch.objects.create(course = i, branch = i.branch,description=instance.description,name=instance.name,subject=instance,priority=priority)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass


@receiver(post_save, sender=Module)
@transaction.atomic
def set_priority(sender, instance, created, **kwargs):
    try:
        if not instance.pk:
            highest_priorty = Module.objects.filter(subject=instance.subject).aggregate(
                models.Max('priority'))['priority__max']
        instance.priority = highest_priorty+1 if highest_priorty is not None else 1
    except:
        pass

    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            subject_branch = Subject_branch.objects.filter(subject=instance.subject)
            for i in subject_branch:
                highest_priorty = Module_branch.objects.filter(subject=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Module_branch.objects.create(subject = i, branch = i.branch,description=instance.description,name=instance.name,module=instance,priority=priority)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass


@receiver(post_save, sender=Topic)
@transaction.atomic
def set_priority(sender, instance, created, **kwargs):
    try:
        if not instance.pk:
            highest_priorty = Topic.objects.filter(module=instance.module).aggregate(
                models.Max('priority'))['priority__max']
            subject_id = Subject.objects.filter(course=instance.module.subject.course.pk).values('id')
            module_id = Module.objects.filter(subject__in=subject_id).values('id')
            highest_order = Topic.objects.filter(module__in=module_id).aggregate(
                models.Max('order')
            )['order__max']
        
        instance.order = highest_order+1 if highest_order is not None else 1
        instance.priority = highest_priorty+1 if highest_priorty is not None else 1
    except Exception as e:
        print(e)
        pass
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            subject_branch = Module_branch.objects.filter(module=instance.module)
            for i in subject_branch:
                highest_priorty = Topic_branch.objects.filter(module=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Topic_branch.objects.create(module = i, branch = i.branch,description=instance.description,name=instance.name,topic=instance,priority=priority)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass


@receiver(post_save, sender=SubTopic)
@transaction.atomic
def set_priority(sender, instance, created, **kwargs):
    try:
        if not instance.pk:
            highest_priorty = SubTopic.objects.filter(topic=instance.topic).aggregate(
                models.Max('priority'))['priority__max']
        instance.priority = highest_priorty+1 if highest_priorty is not None else 1
    except:
        pass

    if created:
        try:
            print("huis")
            print(model_to_dict(instance),"ikujis")
            topic_branch = Topic_branch.objects.filter(topic=instance.topic)
            for i in topic_branch:
                highest_priorty = Subtopic_branch.objects.filter(topic=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Subtopic_branch.objects.create(topic = i, branch = i.branch,description=instance.description,name=instance.name,priority=priority,subtopic=instance,time_needed=instance.time_needed)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass





# ########  COURSE COPY BRANCHES  #########
class Course_branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    branch_courses = models.ForeignKey(Branch_courses, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch','course'],
                name='unique_course_branch',
                condition=~Q(is_delete=True)
            )
        ]


class Subject_branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_branch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Module_branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject_branch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Topic_branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    module = models.ForeignKey(Module_branch, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=5000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    clickStatus = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Subtopic_branch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic_branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    subtopic = models.ForeignKey(SubTopic,null=True,on_delete=models.CASCADE)
    time_needed = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    is_delete = models.BooleanField(default=False)

    def _str_(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    # description = models.TextField(null=True,blank=True)
    # status = models.BooleanField(default=False)
    # def _str_(self):
    #     return self.name


# ######### COURSE COPY ON BRANCHES

class Holidays(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=500)
    is_delete = models.BooleanField(default=False)
    

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


@receiver(post_save, sender=SubTopic)
def topic_time_update(sender, instance, **kwargs):
    print(instance.topic, "jjjjjjjjjjjjjj")
    k = SubTopic.objects.filter(topic=instance.topic).values('time_needed')
    print(k)
    s = sum([x['time_needed'] for x in k])
    print(s)
    t = Topic.objects.filter(id=instance.topic.id).update(time_needed=s)
    print(t, "jjjjjjjjjjjjjjjj")

class SpecialHoliday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    levels = models.ManyToManyField(Level, blank=True)
    batches = models.ManyToManyField(Batch, blank=True)
    branches = models.ManyToManyField(Branch, blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()


class Rating(models.Model):
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_on = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    choice = models.IntegerField(choices=CHOICES)
    rate_fac = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    choice = models.IntegerField(choices=CHOICES,null=True)
    on_question = models.ForeignKey('ReviewQuestions',on_delete=models.CASCADE,null=True)
    review_on = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    answer1 = models.TextField(blank=True, null=True)
    answer2 = models.TextField(blank=True, null=True)
    answer3 = models.TextField(blank=True, null=True)
    answer4 = models.TextField(blank=True, null=True)
    answer5 = models.TextField(blank=True, null=True) 
    feedback = models.TextField(blank=True, null=True) 
    is_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    def get_answers(self):
        return [self.answer1, self.answer2, self.answer3, self.answer4, self.answer5,self.feedback]
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
    objects = ActiveManager()
    newobjects = InActiveManager()

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['review_on', 'user'],
                name='unique_rateing_limitaion',
                condition=~Q(is_delete=True)
            )
        ]
    

    

class ReviewQuestions(models.Model):
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    choice = models.IntegerField(choices=CHOICES)
    question1 = models.TextField()
    question2 = models.TextField(blank=True, null=True)
    question3 = models.TextField(blank=True, null=True)
    question4 = models.TextField(blank=True, null=True)
    question5 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    class Meta:
        verbose_name_plural = "Review Questions"

    def _str_(self):
        return f"Questions for {self.get_choice_display()} reviews"

    def get_questions(self):
        return [self.question1, self.question2, self.question3, self.question4, self.question5]
    
class FacultyRating(models.Model):
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_on = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    choice = models.IntegerField(choices=CHOICES)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

@receiver(post_save, sender=Subject_branch)
@transaction.atomic
def add_copy_batch(sender, instance, created, **kwargs):
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            course_batch = Course_batch.objects.filter(course=instance.course)
            for i in course_batch:
                highest_priorty = Subject_batch.objects.filter(course=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Subject_batch.objects.create(subject = instance, course=i,batch = i.batch,description=instance.description,name=instance.name,priority=priority)
                print("here")
        except Exception as e: 
            print("error")
            print(e,"errr") 
            pass   

@receiver(post_save, sender=Module_branch)
@transaction.atomic
def add_copy_batch(sender, instance, created, **kwargs):
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            subject_batch = Subject_batch.objects.filter(subject=instance.subject)
            for i in subject_batch:
                highest_priorty = Module_batch.objects.filter(subject=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Module_batch.objects.create(module = instance, subject=i,batch = i.batch,description=instance.description,name=instance.name,priority=priority)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass

@receiver(post_save, sender=Topic_branch)
@transaction.atomic
def add_copy_batch(sender, instance, created, **kwargs):
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            module_batch = Module_batch.objects.filter(module=instance.module)
            for i in module_batch:
                highest_priorty = Topic_batch.objects.filter(module=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Topic_batch.objects.create(topic = instance, module=i,batch = i.batch,description=instance.description,name=instance.name,priority=priority)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass

@receiver(post_save, sender=Subtopic_branch)
@transaction.atomic
def add_copy_batch(sender, instance, created, **kwargs):
    if created:
        try:
            print("hui")
            print(model_to_dict(instance),"ikujis")
            topic_branch = Topic_batch.objects.filter(topic=instance.topic)
            for i in topic_branch:
                highest_priorty = Subtopic_batch.objects.filter(topic=i).aggregate(
                    models.Max('priority'))['priority__max']
                priority=highest_priorty+1 if highest_priorty is not None else 1
                Subtopic_batch.objects.create(topic = i, batch = i.batch,description=instance.description,name=instance.name,priority=priority,subtopic=instance,time_needed=instance.time_needed)
                print("here")
        except Exception as e:
            print("error")
            print(e,"errr") 
            pass


class PriceSetting(models.Model):
    package_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    offer_price = models.IntegerField(null=True)
    description = models.TextField(null=True) 
    benefits = models.TextField(null=True)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
        
    objects = ActiveManager()
    newobjects = InActiveManager()



class FacultyLimitaion(models.Model):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE , null=True, blank=True)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='faculty_limitaion_creator')
    max_class= models.IntegerField(null=True)
    current_count= models.IntegerField(null=True)
    is_admin= models.BooleanField(default=False)
    is_delete=models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()
        
    objects = ActiveManager()
    newobjects = InActiveManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'faculty'],
                name='unique_branch_faculty_limitaion',
                condition=~Q(is_delete=True)
            )
        ]

@receiver(pre_save, sender=Topic)
def pre_save_handler(sender, instance, **kwargs):
    if instance.pk is not None:
        # This block will execute when the instance is being updated
        topic = Topic_branch.objects.filter(topic_id=instance.pk)
        for i in topic:
            i.name= instance.name
            i.save()

        print("Editing instance...") 

@receiver(pre_save, sender=Topic_branch)
def pre_save_handler(sender, instance, **kwargs):
    if instance.pk is not None:
        # This block will execute when the instance is being updated
        topic = Topic_batch.objects.filter(topic_id=instance.pk)
        for i in topic:
            i.name= instance.name
            i.save()
            
        print("Editing instance...") 

@receiver(pre_save, sender=SubTopic)
def pre_save_handler(sender, instance, **kwargs):
    if instance.pk is not None:
        # This block will execute when the instance is being updated
        subtopic = Subtopic_branch.objects.filter(subtopic_id=instance.pk)
        for i in subtopic:
            i.name= instance.name
            i.save()
            
        print("Editing instance...") 

@receiver(pre_save, sender=Subtopic_branch)
def pre_save_handler(sender, instance, **kwargs):
    if instance.pk is not None:
        # This block will execute when the instance is being updated
        subtopic = Subtopic_batch.objects.filter(subtopic_id=instance.pk)
        for i in subtopic:
            i.name= instance.name
            i.save()
            
        print("Editing instance...") 

