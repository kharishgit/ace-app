from django.db import models
from accounts.models import Batch,Branch, S3Storage
from datetime import datetime,timezone
from accounts.models import User
from course.models import PriceSetting
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from storages.backends.s3boto3 import S3Boto3Storage
from course.models import *
# Create your models here.

class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude()    


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_delete=True)
    


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
    name = models.CharField(max_length=255)
    exam_number = models.IntegerField(null=True, blank=True)
    admission_number = models.CharField(max_length=255,null=True, blank=True)
    father_name = models.CharField(max_length=255,null=True,blank=True)
    guardian = models.CharField(max_length=255,null=True,blank=True)
    guardian_name = models.CharField(max_length=255,null=True,blank=True)
    guardian_mobile = models.CharField(max_length=10, null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ] 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    MARITAL_STATUS=[
        ('1','Single'),
        ('2','Married')
    ]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS,null=True)

    religion = models.CharField(max_length=255,null=True)
    caste = models.CharField(max_length=255,null=True)
    address = models.TextField(null=True)
    pincode = models.IntegerField(null=True)
    qualification = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    otp = models.CharField(max_length=6, null=True,blank=True) 
    is_online = models.BooleanField(default=False)
    is_offline = models.BooleanField(default=False)
    admission_enquiry = models.BooleanField(default=False)
    photo = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    admission_date = models.DateTimeField(null=True,blank=True)
    emailverified = models.BooleanField(default=False)
    status =models.BooleanField(default=False)
    selected_course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    added_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='added_students')
    scholarship = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()

    # def __str__(self) -> str:
    #     return self.student.user
    objects = ActiveManager()
    newobjects = InActiveManager()
    
    def get_date(self):
        time = datetime.now()
        if self.admission_date.day == time.day:
            return str(time.hour - self.admission_date.hour) + " hours ago"
        else:
            if self.admission_date.month == time.month:
                return str(time.day - self.admission_date.day) + " days ago"
            else:
                if self.admission_date.year == time.year:
                    return str(time.month - self.admission_date.month) + " months ago"
        return self.admission_date
   
    
    def is_otp_valid(self):

        """
        Check if the OTP is valid.
        """
        if (timezone.now() - self.admission_date).seconds > 300000000:
            # OTP is expired
            return False
        return True
    
    # def __str__(self) -> str:
    #     return self.user 
   
class StudentBatch(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True,blank=True)
    batch_name = models.CharField(max_length=250,null=True,blank=True)
    branch_name = models.CharField(max_length=250, null=True,blank=True)
    is_delete = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_queryset = getattr(self, related_name).all()
            for related_instance in related_queryset:
                related_instance.delete(*args, **kwargs)
        self.is_delete = True
        self.save()

    # def __str__(self) -> str:
    #     return self.student.user
    objects = ActiveManager()
    newobjects = InActiveManager()




class FeePayment(models.Model):
    method_choice = [("CASH", "CASH"), ("UPI", "UPI"),
                    ("NETBANKING", "NETBANKING")]
    package_choosed = models.ForeignKey(PriceSetting,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_started_on = models.DateTimeField()
    paid_amount = models.CharField(max_length=20)
    pending_amount = models.CharField(max_length=20)
    payment_method= models.CharField(choices=method_choice,max_length=255,default="CASH")
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


class OnlineStudent(models.Model):
    mobile_number = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6, null=True)  # allow null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile_number

    def is_otp_valid(self):
        
        """
        Check if the OTP is valid.
        """
        if (timezone.now() - self.created_at).seconds > 300000000:
            # OTP is expired
            return False
        return True
    


class CurrentAffairs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    file = models.FileField(null=True)
    VIDEO_UPLOAD_CHOICES = (
        ('V', 'VIMEO'),
        ('Y', 'YOUTUBE'),
    ) 
    vname = models.CharField(max_length=255,null=True, blank=True)
    icon = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    vimeoid = models.CharField(max_length=20,null=True, blank=True)
    videolength = models.CharField(max_length=10,null=True, blank=True)
    video = models.CharField(choices=VIDEO_UPLOAD_CHOICES,max_length=200, default="V",null=True)
    url=models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    publish_on = models.DateField(null=True)
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

class StudentOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    mobile = models.CharField(max_length=12,null=True, blank=True)
    otp = models.CharField(max_length=4,null=True, blank=True)
    isverified = models.BooleanField(default=False)
    createdat = models.DateTimeField(default=timezone.now, auto_created=True)


class Version(models.Model):
    version_code = models.CharField(max_length=10)
    name = models.CharField(max_length=50,null=True)
    released_date = models.DateField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.version_code
    



class Publications(models.Model):
    bookname = models.CharField(max_length=255)
    icon = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    category = models.CharField(max_length = 255,null = True)
    book_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    offlinebook_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    no_of_pages = models.IntegerField(null=True)
    course = models.ManyToManyField(Course,blank=True)
    edition = models.CharField(max_length=100,null=True)
    stock = models.IntegerField(default=1)
    is_online = models.BooleanField(default=False)
    medium = models.CharField(max_length=255,null=True)
    order_count = models.IntegerField(null=True)
    paperback = models.BooleanField(default=True)
    publish_on = models.DateField(null=True)
    admission_time_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    old_student = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    outsider = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    description = models.TextField(null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
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


class StudentApplicationOffline(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,default=0)
    father_name = models.CharField(max_length=255,null=True,blank=True)
    guardian = models.CharField(max_length=255,null=True,blank=True)
    guardian_name = models.CharField(max_length=255,null=True,blank=True)
    guardian_mobile = models.CharField(max_length=10, null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    email = models.EmailField(max_length=100,null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ] 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    MARITAL_STATUS=[
        ('1','Single'),
        ('2','Married')
    ]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS,null=True)
    photo=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')

    religion = models.CharField(max_length=255,null=True)
    caste = models.CharField(max_length=255,null=True)
    address = models.TextField(null=True)
    pincode = models.IntegerField(null=True)
    qualification = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status =models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
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



class DeliveryAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255)
    mobile_number=models.CharField(max_length=10)
    pincode=models.CharField(max_length=6)
    locality=models.CharField(max_length=255)
    address=models.TextField()
    district=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    landmark=models.CharField(max_length=255,null=True)
    alternate_mobilenum=models.CharField(max_length=10,null=True)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
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


class StudentDeclaration(models.Model):
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

class RankList(models.Model):
    exam_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='ranklist/', validators=[FileExtensionValidator(['xlsx'])], storage=S3Storage())
    is_delete = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
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

class AceRankHolders(models.Model):
    exam = models.ForeignKey(RankList,on_delete=models.CASCADE)
    rank = models.IntegerField()
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_user')
    is_delete = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by_rank')

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

