

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime
from datetime import timedelta
from django.forms import model_to_dict
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import JSONField
from django.core.validators import FileExtensionValidator
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from simple_history.models import HistoricalRecords
from aceapp.settings.base import AWS_STORAGE_BUCKET_NAME_PUBLIC
######### S3 BUCKET #########

class S3Storage(S3Boto3Storage):
    location = 'media'

######### S3 BUCKET ENDS #########
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_delete=True)

class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude()    


# Create your models here.###
class UserManager(BaseUserManager):
    def create_user(self, email, mobile=None, password=None, username=None, is_active=False, is_roleuser=False, is_superuser=False, is_faculty=False, is_staff=False, is_student=False):
        
        if not email:
            raise ValueError('Please Enter Email')
        if not password:
            raise ValueError('Please Enter Password')
        user = self.model(
            email=self.normalize_email(email),

        )
        user.mobile = mobile
        user.username = username
        user.is_active = is_active
        user.is_roleuser = is_roleuser
        user.is_superuser = is_superuser
        user.is_faculty = is_faculty
        user.is_staff = is_staff
        user.is_student= is_student
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_student(self, email, password, mobile, username):
        user = self.create_user(email=email, password=password, mobile=mobile,
                                username=username, is_active=True, is_student=True)
        return user

    def create_admin(self, email, password, mobile, username):
        user = self.create_user(email=email, password=password, mobile=mobile,
                                username=username, is_superuser=True, is_active=True, is_staff=True)

        return user

    def create_faculty(self, email, password, mobile, username):
        user = self.create_user(email=email, password=password, mobile=mobile,
                                username=username, is_active=True, is_faculty=True)
        return user

    def create_roleuser(self, email, password, mobile, username):
        user = self.create_user(email=email, password=password, mobile=mobile,
                                username=username, is_active=True, is_roleuser=True)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            is_staff=True

        )

        user.is_active = True
        user.is_roleuser = True
        user.is_superuser = True
        user.is_faculty = True
        user.is_staff = True
        user.is_student = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=10, unique=True, null=True)
    password = models.CharField(max_length=220, blank=False, null=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_roleuser = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    def get_date(self):
        time = datetime.now()
        if self.joined_date.day == time.day:
            return str(time.hour - self.joined_date.hour) + " hours ago"
        else:
            if self.joined_date.month == time.month:
                return str(time.day - self.joined_date.day) + " days ago"
            else:
                if self.joined_date.year == time.year:
                    return str(time.month - self.joined_date.month) + " months ago"
        return self.joined_date

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True

# ###########
# ############### AdditionEnds #################################



# from course.models import Level
class Faculty(models.Model):
    user = models.OneToOneField(
        User, unique=True, on_delete=models.CASCADE, null=True, related_name='user_profi')
    name=models.CharField(max_length=60,null=True)
    address = models.TextField(null=True)
    identity_card = models.FileField(null=True)
    photo = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    resume=models.FileField(null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    district = models.CharField(max_length=255, null=True)
    whatsapp_contact_number = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True)
    qualification = models.CharField(max_length=255, null=True)
    OFFLINE_ONLINE_CHOICES_exp = [
        ('1', 'Offline'),
        ('2', 'Online'),
        ('3','Both')
    ]
    modeofclasschoice = models.CharField(
        max_length=1, choices=OFFLINE_ONLINE_CHOICES_exp, blank=True, null=True)
    experiance_link = models.URLField(blank=True, null=True)
    pincode = models.IntegerField(null=True)
    # expected_salary = models.ManyToManyField('Faculty_Salary', related_name='faculties')
    # level = models.ForeignKey(Level, on_delete=models.CASCADE)
    # salary = models.CharField(max_length=6)
    # fixed_salary = models.CharField(max_length=7)
    # fixed_salary = models.IntegerField(null=True)
    # BATCH_CHOICES = (

    #     ('Mb', 'Morning Batch'),
    #     ('Rb', 'Regular Batch'),
    #     ('Eb', 'Evening Batch'),
    # )
    # availability = MultiSelectField(choices=BATCH_CHOICES, default=['Rb'], max_choices=3, validators=[MaxValueValidator(3)],null=True)
    photoverified=models.BooleanField(default=False)
    resumeverified=models.BooleanField(default=False)
    idverified=models.BooleanField(default=False)

    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    blockreason=models.TextField(null=True,blank=True)
    is_rejected=models.BooleanField(default=False)
    rejectreason=models.TextField(null=True,blank=True )
    inhouse_fac=models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True, blank=True)
    history = HistoricalRecords()
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

    def get_date(self):
        time = datetime.now()
        if self.joined_date.day == time.day:
            return str(time.hour - self.joined_date.hour) + " hours ago"
        else:
            if self.joined_date.month == time.month:
                return str(time.day - self.joined_date.day) + " days ago"
            else:
                if self.joined_date.year == time.year:
                    return str(time.month - self.joined_date.month) + " months ago"
        return self.joined_date


#######Faculty Course Adding/Approving#########

from course.models import Course, Subject, Module, Topic, SubTopic, Batch, Branch,Category,Level,ClassLevel
class FacultyCourseAddition(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('blocked', 'Blocked'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_delete = models.BooleanField(default=False)
    history = HistoricalRecords()

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
                fields=['user', 'topic'],
                name='unique_faculty_topic',
                condition=~Q(is_delete=True)
            )
        ]
#######Faculty Course Adding/Approving ENDS#########





class Material(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='materials')
    subtopic=models.ManyToManyField(SubTopic,blank=True)
    topic_faculty = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'xlsx', 'docx', 'plg', 'png', 'jpeg'])], storage=S3Storage())
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_verified=models.BooleanField(default=False,null=True)
    updated_at = models.DateTimeField( auto_now=True)
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
from django.core.exceptions import ValidationError

class MaterialUploads(models.Model):
    file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'xlsx', 'docx', 'plg', 'png', 'jpeg'])], storage=S3Storage())
    name = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    published = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    updated_file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'xlsx', 'docx', 'plg', 'png', 'jpeg'])], storage=S3Storage(),null=True)
    reject_updated_file = models.BooleanField(default=False)
    reject_updated_file_fac = models.BooleanField(default=False)
    reject_updated_file_reason = models.TextField(null=True)
    reject_updated_file_reason_fac = models.TextField(null=True)
    vstatus_research = models.BooleanField(default=False)
    vstatus_faculty = models.BooleanField(default=False)
    edited_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="edited_user",null=True)
    edited_on_choice = [("SET", "SET"), ("TYPE", "TYPE")]
    edited_on = models.CharField(choices=edited_on_choice,default="TYPE",max_length=100,null=True)
    updated_at = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)

    # def clean(self):
    #     if self.user and not self.user.is_faculty:
    #         raise ValidationError("Material uploads can only be done by faculty users.")


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


class MaterialReference(models.Model):
    materialupload = models.ForeignKey(MaterialUploads,on_delete=models.CASCADE,null=True)
    category =models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,null=True,blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,blank=True)
    subtopic=models.ForeignKey(SubTopic,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
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

    class Meta:
        constraints=[
            models.CheckConstraint(
                check=(
                    (models.Q(category__isnull=False) & models.Q(level__isnull=True) & models.Q(course__isnull=True) & models.Q(module__isnull=True)& models.Q(subject__isnull=True)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=False) & models.Q(course__isnull=True) & models.Q(module__isnull=True)& models.Q(subject__isnull=True)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=False) & models.Q(module__isnull=True)& models.Q(subject__isnull=True)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=True) & models.Q(module__isnull=False)& models.Q(subject__isnull=True)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=True) & models.Q(module__isnull=True)& models.Q(subject__isnull=False)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=True) & models.Q(module__isnull=True)& models.Q(subject__isnull=True)& models.Q(topic__isnull=False)& models.Q(subtopic__isnull=True)) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=True) & models.Q(module__isnull=True)& models.Q(subject__isnull=True)& models.Q(topic__isnull=True)& models.Q(subtopic__isnull=False)) 
                ),
                name='only_one_field_non_null_constraint'
            )
        ]

    # def clean(self):
    #     fields = [
    #         self.category,
    #         self.level,
    #         self.course,
    #         self.subject,
    #         self.module,
    #         self.topic,
    #         self.subtopic,
    #     ]
    #     non_null_fields = [field for field in fields if field is not None]
    #     if len(non_null_fields) != 1:
    #         raise ValidationError('Only one field should be not null.')

    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Perform the validation before saving
    #     super().save(*args, **kwargs)
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user', 'topic'],
    #             name='unique_faculty_topic_material',
    #             condition=~Q(is_delete=True)
    #         ),models.UniqueConstraint(
    #             fields=['user', 'module'],
    #             name='unique_faculty_modul_material',
    #             condition=~Q(is_delete=True)
    #         ),models.UniqueConstraint(
    #             fields=['user', 'subtopic'],
    #             name='unique_faculty_subtopic_material',
    #             condition=~Q(is_delete=True)
    #         ),
    #     ]

    





class SalaryFixation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salaryscale = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    objects = ActiveManager()
    newobjects = InActiveManager()

    
    
    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()




class Faculty_Salary(models.Model):
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    exp_salary = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    fixed_salary = models.ForeignKey(SalaryFixation, on_delete=models.CASCADE,null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    is_online=models.BooleanField(default=False)
    history = HistoricalRecords()

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

@receiver(post_save, sender=FacultyCourseAddition)
def create_faculty_expected_salary_onlinecourse(sender, instance, created, **kwargs):
    if instance.course.is_online and not Faculty_Salary.objects.filter(level=instance.level,is_online=True).exists():
        user=Faculty.objects.get(user__id=instance.user.id)
        Faculty_Salary.objects.create(faculty=user,level=instance.level,is_online=True)

# @receiver(post_save, sender=Material)
# def update_material_upload_support(sender, instance, created, **kwargs):
#     if not created:
#         # Only update if Material object was not just created
#         material_upload_support = instance.materialuploadsupport
#         material_upload_support.faculty = instance.faculty
#         material_upload_support.topic = instance.topic
#         material_upload_support.is_uploaded = True
#         material_upload_support.file = instance.file
#         material_upload_support.save()





class Experience(models.Model):
    name = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
    inst_name = models.CharField(max_length=100,null=True)
    years = models.IntegerField(null=True)
    level =models.ManyToManyField(ClassLevel,blank=True)
    designation = models.CharField(max_length=100,null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    history = HistoricalRecords()

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

class Role(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)

    def __str__(self):
        return self.name
    
    # def delete(self, *args, **kwargs):
    #     for related_object in self._meta.related_objects:
    #         related_name = related_object.get_accessor_name()
    #         related_queryset = getattr(self, related_name).all()
    #         for related_instance in related_queryset:
    #             related_instance.delete(*args, **kwargs)
    #     self.is_delete = True
    #     self.save()
    objects = models.Manager()
    newobjects = InActiveManager()


def get_default():
    default={
    "Category": { 
            "create":True,
            "edit":True,
            "list":True,
            "delete":True,
            "Block":True,
            "PDF":True
        },
        "Level": { 
            "create":True,
            "edit":True,
            "list":True,
            "delete":True,
            "Block":True,
            "PDF":True
        },
        "Course": { 
            "create":True,
            "edit":True,
            "list":True,
            "delete":True,
            "Block":True,
            "PDF":True,
            "Order_change":True
        
        },
        "Subject": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Module": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Topic": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "SubTopic": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Faculty": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Branch": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Batch": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "TimeTable":{
            "create":False,
            "edit":False,
            "assignFaculty":False,
            "delete":False,
            "autoTimetable":False,
            "photo":False
        },
        "Holiday": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Material": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "Download":False,
            "AddVerified":False,
            "AssignMaterial":False
        },
        "QuestionPool": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "Block":False,
            "PDF":False
        },
        "Attendance": { 
            "create":False,
            "edit":False,
            "list":False,
            "delete":False,
            "PDF":False
        },
    }

    return default


class Permissions(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    permissions = JSONField(default=get_default)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    def __str__(self) -> str:
        return self.role.name
    
    # def delete(self, *args, **kwargs):
    #     for related_object in self._meta.related_objects:
    #         related_name = related_object.get_accessor_name()
    #         related_queryset = getattr(self, related_name).all()
    #         for related_instance in related_queryset:
    #             related_instance.delete(*args, **kwargs)
    #     self.is_delete = True
    #     self.save()
    objects = models.Manager()
    newobjects = InActiveManager()



# print('ss')


class QuestionPool(models.Model):
    facultys=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    categorys=models.ForeignKey(Category,on_delete=models.CASCADE)
    levels=models.ForeignKey(Level,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)

    TYPE=[
        ('1','Practise test'),
        ('2','Question Paper'),
    ]
    type=models.CharField(
        max_length=1,choices=TYPE
    )
    questions=models.ManyToManyField('Question')

    @classmethod
    def get_questions(cls, faculty_id=None, course_id=None,subject_id=None, topic_id=None,type=None,category_id=None,level_id=None):
        """
        Returns a queryset of questions that match the given faculty, course, and topic IDs.
        """
        question_pool = QuestionPool.objects.all()
        if faculty_id:
            question_pool = question_pool.filter(facultys=faculty_id)
        if course_id:
            question_pool = question_pool.filter(course=course_id)
        if subject_id:
            question_pool=question_pool.filter(subject=subject_id)
        if topic_id:
            question_pool = question_pool.filter(topic=topic_id)
        if type:
            question_pool=question_pool.filter(type=type)
        if category_id:
            question_pool=question_pool.filter(categorys=category_id)
        if level_id:
            question_pool=question_pool.filter(levels=level_id)

        questions = []
        # question_pool = question_pool.order_by('-pk')
        for question_pool in question_pool:
            questions.extend(question_pool.questions.all().order_by('id'))
        return questions
    
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





class Question(models.Model):
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    option_5 = models.CharField(max_length=255, blank=True, null=True)
    OPTION_CHOICES = (
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
        ('option_3', 'Option 3'),
        ('option_4', 'Option 4'),
        ('option_5', 'Option 5'),
    )
    answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
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





class Declaration(models.Model):
    declaration=models.TextField()
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

class QuestionImage(models.Model):
    questionimage = models.ImageField()

class QuestionFile(models.Model):
    facultyfile = models.FileField()

class NewQuestionPool(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    categorys=models.ForeignKey(Category,on_delete=models.CASCADE)
    levels=models.ForeignKey(Level,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    subtopic=models.ForeignKey(SubTopic,on_delete=models.CASCADE,null=True)
    postive_mark=models.DecimalField(default=1,max_digits=8, decimal_places=2)
    negative_mark=models.DecimalField(default=0,max_digits=8, decimal_places=2)
    duration = models.IntegerField(null=True)
    is_delete = models.BooleanField(default=False)
    question_text = models.TextField(null=True)
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField()
    option_4 = models.TextField()
    option_5 = models.TextField(blank=True, null=True)
    OPTION_CHOICES = (
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
        ('option_3', 'Option 3'),
        ('option_4', 'Option 4'),
        ('option_5', 'Option 5'),
    )
    answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    answerhint=models.TextField(null=True,blank=True)
    TYPE=[
        ('1','Medium'),
        ('2','Simple'),
        ('3','Tough'),
        ('4','All'),
    ]
    type=models.CharField(
        max_length=1,choices=TYPE,null=True, blank=True
    )

    status=models.BooleanField(default=True)
    publish=models.BooleanField(default=False,null=True)
    admin_verify=models.BooleanField(default=False,null=True)
    dtp_verify=models.BooleanField(default=False,null=True)
    faculty_verify=models.BooleanField(default=False,null=True)
    faculty_reject=models.BooleanField(default=False,null=True)
    faculty_reject_reason=models.TextField(null=True,blank=True)
    dtp_edit=models.BooleanField(default=False,null=True)
    add_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='add_user')
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subtopic','question_text','option_1','option_2','option_3','option_4',],
                name='unique_sub_topic_question',
                condition=~Q(is_delete=True)
            )
        ]



class QuestionPaper(models.Model):
    name=models.CharField(max_length=225,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    categorys=models.ForeignKey(Category,on_delete=models.CASCADE)
    levels=models.ForeignKey(Level,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,null=True)
    notes=models.FileField(null=True,blank=True)
    instruction=models.TextField(null=True)
    positivemark=models.FloatField(null=True)
    negativemark=models.FloatField(null=True)
    duration=models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    TYPES=[
            ('1','Course'),
            ('2','Subject'),
            ('3','Module'),
            ('4','Topic'),
            ('5','Model')
        ]
    examtype=models.CharField(
            max_length=1,choices=TYPES,null=True
        )


    TYPE=[
        ('1','Free'),
        ('2','Premium'),
    ]
    type=models.CharField(
        max_length=1,choices=TYPE
    )


    status=models.BooleanField(default=False)
    questions=models.ManyToManyField(NewQuestionPool)
    banner=models.ImageField(null=True,blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True,blank=True)
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


class StudioCourse(models.Model):
    faculty=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='faculty_studio')
    name=models.TextField(null=True)
    topic=models.ManyToManyField(Topic)
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=122)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey('StudioVideo',on_delete=models.CASCADE,null=True,blank=True)
    studioname=models.ForeignKey('StudioNames',on_delete=models.CASCADE)
    publish=models.BooleanField(default=False)
    assignvideo=models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    coverdtopic=models.ManyToManyField(Topic,blank=True,related_name='covered_topics')

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


class StudioVideo(models.Model):
    name=models.CharField(max_length=225)
    vimeoid = models.CharField(max_length=255,null=True, blank=True)
    video_length = models.CharField(max_length=10,null=True, blank=True)
    faculty = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='faculty_studio_video')
    description=models.TextField(null=True,blank=True)
    shootingdaytime=models.DateTimeField(null=True,blank=True)
    shootingenddaytime=models.DateTimeField(null=True,blank=True)
    editingdaytime=models.DateTimeField(null=True,blank=True)
    editingenddaytime=models.DateTimeField(null=True,blank=True)
    editingstaff=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    videolink=models.TextField(null=True,blank=True)
    is_delete = models.BooleanField(default=False)
    existing = models.BooleanField(default=True)
    videocontent = models.TextField(null=True, blank=True)
    adminverify = models.BooleanField(default=False)
    totalhours=models.FloatField(null=True,blank=True)
    intro=models.BooleanField(default=False)
    sd_240p=models.TextField(null=True,blank=True)
    sd_360p=models.TextField(null=True,blank=True)
    sd_540p=models.TextField(null=True,blank=True)
    hd_720p=models.TextField(null=True,blank=True)
    hd_1080p=models.TextField(null=True,blank=True)
    thumbnail=models.ImageField(null=True,blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
 

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



class StudioNames(models.Model):
    name=models.CharField(max_length=225)
    district=models.CharField(max_length=225)
    address=models.TextField()
    phonenumber=models.CharField(max_length=10,null=True)
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

class FacultyStudioApplication(models.Model):
    studiocourse=models.ForeignKey(StudioCourse,on_delete=models.CASCADE,null=True)
    faculty=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_approved=models.BooleanField(default=False)
    videourl=models.URLField(null=True,blank=True)
    description=models.TextField(null=True)
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

class StudioCourseAssign(models.Model):
    video=models.ForeignKey(StudioVideo,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,null=True,blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,blank=True)
    subtopic=models.ForeignKey(SubTopic,on_delete=models.CASCADE,null=True,blank=True)
    public=models.BooleanField(default=False)
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

@receiver(post_save, sender=Role)
def add_permission_for_role(sender, instance, created, **kwargs):
    Permissions.objects.get_or_create(role=instance)
    return True



class ConvertedMaterials(models.Model):
    file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'xlsx', 'docx', 'plg', 'png', 'jpeg'])], storage=S3Storage())
    name = models.CharField(max_length=255,null= True, blank=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    uploads = models.ManyToManyField(MaterialReference)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    topic = models.ManyToManyField(Topic,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdby',null=True)
    active = models.BooleanField(default=False)
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


from course.models import TimeTable
class MaterialRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    material = models.ForeignKey(ConvertedMaterials, on_delete=models.CASCADE)
    like = models.BooleanField()
    dislike = models.BooleanField()
    feedback = models.TextField(null=True, blank=True)
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


class CommentOnMaterial(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_on = models.ForeignKey(ConvertedMaterials, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    comments = models.TextField(null = True, blank=True)
   


class OnlineSalary(models.Model):
    studiocourse=models.ForeignKey(StudioCourse,on_delete=models.CASCADE)
    method_choice = [("CASH", "CASH"), ("UPI", "UPI"),
                    ("NETBANKING", "NETBANKING")]
    status_choice = [("PAID", "PAID"), ("PARTIAL", "PARTIAL"),
                    ("PENDING", "PENDING")]
    topics_covered = models.ManyToManyField(Topic,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # new field for storing the time of last update
    payment_status = models.CharField(choices=status_choice,default="PENDING",max_length=100)
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


class Incentives(models.Model):
    name=models.CharField(max_length=255)
    rate=models.DecimalField(max_digits=10,decimal_places=2,default=0)    
    conditions=models.TextField(null=True)
    target_mandatory=models.BooleanField(default=False)
    status_choice = [("ADMISSION_WISE", "ADMISSION WISE"), 
                    ("SINGLE_PAYMENT_ENCOURAGE_WISE", "SINGLE PAYMENT ENCOURAGE WISE"),
                    ("PHOTO_COLLECTION ", "PHOTO COLLECTION "),
                    ("ENQIUREES_WISE", "ENQIUREES WISE"),
                    ("FOLLOW_UP", "FOLLOW UP"),
                    ("SOCIAL_MEDIA ", "SOCIAL MEDIA "),
                    ("CLASS_COMMUNICATION", "CLASS COMMUNICATION"),
                    ("FEE_COLLECTION_WISE", "FEE COLLECTION WISE"),
                    ("OTHERS", "OTHERS")]
    types = models.CharField(choices=status_choice,default="OTHERS",max_length=255)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    status = models.BooleanField(default=True)
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
   

class StaffIncentives(models.Model):
    incentives=models.ForeignKey(Incentives,on_delete=models.CASCADE,null=True)
    staff=models.ForeignKey(User,on_delete=models.CASCADE)
    target=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    status = models.BooleanField(default=True)
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

class StaffIncentiveAmount(models.Model):
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    staffincetive=models.ForeignKey(StaffIncentives,on_delete=models.CASCADE,null=True,blank=True)
    achieved_target=models.DecimalField(max_digits=10,decimal_places=2,default=0,null=True,blank=True)
    method_choice = [("CASH", "CASH"), ("UPI", "UPI"),
                    ("NETBANKING", "NETBANKING")]
    status_choice = [("PAID", "PAID"), ("PARTIAL", "PARTIAL"),
                    ("PENDING", "PENDING")]
    payment_status = models.CharField(choices=status_choice,default="PENDING",max_length=100,null=True)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,null=True)
    payment_method= models.CharField(choices=method_choice,max_length=100,default="CASH",null=True)
    payment_date = models.DateField(null=True,blank=True)
    incentive_message = models.TextField(null=True)
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
    objects = ActiveManager 


class StaffSalary(models.Model):
    staff=models.ForeignKey(User,on_delete=models.CASCADE)
    method_choice = [("CASH", "CASH"), ("UPI", "UPI"),
                    ("NETBANKING", "NETBANKING")]
    status_choice = [("PAID", "PAID"), ("PARTIAL", "PARTIAL"),
                    ("PENDING", "PENDING")]
    updated = models.DateTimeField(auto_now=True)  # new field for storing the time of last update
    payment_status = models.CharField(choices=status_choice,default="PENDING",max_length=100)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_method= models.CharField(choices=method_choice,max_length=100,default="CASH")
    testimonial  = models.TextField(null=True)
    current_salary=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    salary_date = models.DateField(null=True,blank=True)
    advance_payment=models.DecimalField(max_digits=10,decimal_places=2,default=0,null=True)
    adv_payment_date=models.DateTimeField(null=True)
    salary_message=models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

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

