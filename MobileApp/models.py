from django.db import models
from accounts.models import *
from course.models import *
from student.models import * 
from decimal import Decimal
from finance.models import *
from accounts.models import ActiveManager,InActiveManager
# Create your models here.
class DailyNews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    file = models.FileField()
    VIDEO_UPLOAD_CHOICES = (
        ('V', 'VIMEO'),
        ('Y', 'YOUTUBE'),
    ) 
    video = models.CharField(choices=VIDEO_UPLOAD_CHOICES,max_length=200, default="V",null=True)
    url=models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    publish_on = models.DateField(null=True)
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



class QuizPool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    instruction = models.TextField(null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    duration = models.IntegerField(default=5)
    question = models.ManyToManyField(NewQuestionPool)
    count = models.IntegerField(null=True,blank=True)
    postive_mark=models.DecimalField(null=True,max_digits=8, decimal_places=2)
    negative_mark=models.DecimalField(null=True,max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    status = models.BooleanField(default=False)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['level'],
                name='unique_level_QuizPool',
                condition=~Q(is_delete=True)
            )
        ]



class SuccessStories(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    icon = models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    VIDEO_UPLOAD_CHOICES = (
        ('V', 'VIMEO'),
        ('Y', 'YOUTUBE'),
    ) 
    video = models.CharField(choices=VIDEO_UPLOAD_CHOICES,max_length=200, default="V",null=True)
    url=models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
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

class MobileBanner(models.Model):
    image = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    name = models.CharField(max_length=255)
    route=models.TextField(null=True)
    subroutes=models.TextField(null=True)
    width = models.CharField(max_length=4,null=True,blank=True)
    height = models.CharField(max_length=4,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    is_faculty=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
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


class QuestionCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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



class QuestionBook(models.Model):
    q_category = models.ForeignKey(QuestionCategory,on_delete=models.CASCADE,null=True)
    bookname = models.CharField(max_length=255)
    icon = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    category = models.CharField(max_length = 255,null = True)
    book_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
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


class StudyMaterial(models.Model):
    bookname = models.CharField(max_length=255)
    icon = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    category = models.CharField(max_length = 255,null = True)
    book_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
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


class BatchPackages(models.Model):
    name=models.CharField(max_length=255)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    study_meterial=models.ManyToManyField(StudyMaterial,blank=True)
    question_book=models.ManyToManyField(QuestionBook,blank=True)
    publications=models.ManyToManyField(Publications, blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['batch'],
                name='unique_batch_BatchPackages',
                condition=~Q(is_delete=True)
            )
        ]


class Shorts(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.URLField()
    # video_file = models.FileField(upload_to='shorts/')
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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


    

class ShortsWatched(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    shorts = models.ForeignKey(Shorts, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    LIKE_ASSIGN_CHOICES = (
        ('SHORTS','SHORTS'),
        ('CURRENT_AFFAIRS','CURRENT AFFAIRS'),
        ('STUDY_MATERIALS','STUDY MATERIALS'),
        ('QUESTION_PAPER','QUESTION PAPER'),
        ('VIDEOS','VIDEOS'),
        ('COMMENTS','COMMENTS'),
        ('STORIES','STORIES'),
        ('SUCCESS_STORIES','SUCCESS STORIES'),
        ('VIDEO_PACKAGE','VIDEO_PACKAGE'),
        ('EXAM_PACKAGE','EXAM_PACKAGE'),
        ('CHAT','CHAT'),
        ('ARTICAL','ARTICAL')
    ) 
    like_assign = models.CharField(choices=LIKE_ASSIGN_CHOICES,max_length=200, default="S",null=True)
    liked_id = models.BigIntegerField()
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    
    objects = ActiveManager()
    newobjects = InActiveManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','like_assign','liked_id'],
                name='unique_like_assign_constraints'
            )
        ]

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    COMMENTS_ASSIGN_CHOICES = (
        ('SHORTS','SHORTS'),
        ('CURRENT_AFFAIRS','CURRENT AFFAIRS'),
        ('STUDY_MATERIALS','STUDY MATERIALS'),
        ('QUESTION_PAPER','QUESTION PAPER'),
        ('VIDEOS','VIDEOS'),
        ('COMMENTS','COMMENTS'),
        ('STORIES','STORIES'),
        ('SUCCESS_STORIES','SUCCESS_STORIES'),
        ('VIDEO_PACKAGE','VIDEO_PACKAGE'),
        ('EXAM_PACKAGE','EXAM_PACKAGE'),
        ('CHAT','CHAT'),
        ('ARTICAL','ARTICAL')
    ) 
    comment_assign = models.CharField(choices=COMMENTS_ASSIGN_CHOICES,max_length=200, default="SHORTS",null=True)
    commented_id = models.BigIntegerField()
    comment=models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user','comment_assign'],
    #             name='unique_comment_assign_constraints'
    #         )
    #     ]



class BookStock(models.Model):
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    publication = models.ForeignKey(Publications, on_delete=models.CASCADE)
    publication_count = models.IntegerField(default=0)
    studymaterial = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE,null=True)
    studymaterial_count = models.IntegerField(default=0)
    questionbank = models.ForeignKey(QuestionBook, on_delete=models.CASCADE,null=True)
    questionbank_count = models.IntegerField(default=0)
    omr_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

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




class QuizPoolUserRoom(models.Model):
    quiz=models.ForeignKey(QuizPool,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    total_score=models.DecimalField(null=True,max_digits=8, decimal_places=2)
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(null=True)
    is_status = models.BooleanField(default=True)
    is_submited = models.BooleanField(default=False)
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

class QuizPoolAnswers(models.Model):
    room =models.ForeignKey(QuizPoolUserRoom,on_delete=models.CASCADE)
    question= models.ForeignKey(NewQuestionPool,on_delete=models.CASCADE,null=True)
    question_copy=models.TextField()
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
    crct_answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    index=models.IntegerField(default=0)
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
                fields=['room','index'],
                name='room_index_quiz_answer_submit',
                condition=~Q(is_delete=True)
            ),
              models.UniqueConstraint(
                fields=['room','question'],
                name='room_question_quiz_answer_submit',
                condition=~Q(is_delete=True)
            )
        ]




@receiver(post_save, sender=QuizPoolAnswers)
def set_priority(sender, instance, created, **kwargs):
    if created:
        instance.crct_answer = instance.question.answer
        instance.save(update_fields=['crct_answer'])


class BooksType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
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


class Books(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(BooksType,on_delete=models.CASCADE)
    no_due_days = models.IntegerField(null=True)
    price = models.DecimalField(null=True,max_digits=8, decimal_places=2)
    description = models.TextField(null=True)
    purchased_on = models.DateField(null=True)
    subscription_upto = models.DateField(null=True)
    is_lend = models.BooleanField(default=True)
    qrcode = models.CharField(max_length=255,null=True,unique=True)
    ISBN = models.CharField(max_length=100,null=True)
    outsider_allowed = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
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



class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication=models.ForeignKey(Publications, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class LibraryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    cardno = models.CharField(max_length=100)
    book_limit  = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default = True)
    dues_completed = models.BooleanField(default=False)
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

class BookLend(models.Model):
    user = models.ForeignKey(LibraryUser,on_delete=models.CASCADE)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)
    borrowed_on = models.DateField()
    duedate = models.DateField()
    returned_on = models.DateField(null=True)
    description = models.TextField(null=True)
    fine = models.DecimalField(null=True,max_digits=8,decimal_places=2)
    lost = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
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

class LibraryFine(models.Model):
    amount = models.PositiveIntegerField(default=1)
    duedate = models.PositiveIntegerField(default=1)
    book_limit = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
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


class StudentFeeCollection(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    batch_package = models.ForeignKey(BatchPackages, on_delete=models.CASCADE)
    publications = models.ManyToManyField(Publications,blank=True)
    study_materials = models.ManyToManyField(StudyMaterial,blank=True)
    question_banks = models.ManyToManyField(QuestionBook,blank=True)
    amountpaid = models.DecimalField(null=True,max_digits=8,decimal_places=2)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='createby')
    created_at = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()
    updated_at = models.DateTimeField(null=True)

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

class GeneralVideosCategory(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(null=True)
    active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
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

class GeneralVideosMaterial(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(null=True)
    files=models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
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


class GeneralVideos(models.Model):
    video=models.ForeignKey(StudioVideo, on_delete=models.CASCADE)
    category=models.ForeignKey(GeneralVideosCategory,on_delete=models.CASCADE,null=True)
    level=models.ForeignKey(Level, on_delete=models.CASCADE)
    files=models.ManyToManyField(GeneralVideosMaterial,blank=True)
    thumbnails=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    title=models.CharField(max_length=100)
    description=models.TextField(null=True)
    active=models.BooleanField(default=True)
    priority=models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
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





@receiver(post_save, sender=QuizPoolUserRoom)
def set_priority(sender, instance, created, **kwargs):
    if created:
        pass
    elif instance.is_submited and instance.total_score==None:
        instance.end_time=datetime.now()
        instance.is_submited=True
        score = Decimal('0.0')
        qpa=QuizPoolAnswers.objects.filter(room=instance.id)
        for i in qpa:
            i.crct_answer=i.question.answer
            if i.answer==None:
                pass
            elif i.answer==i.question.answer:
                score+=instance.quiz.postive_mark
            elif i.answer!=i.question.answer:
                score-=instance.quiz.negative_mark

            i.save()
        

        

        instance.total_score=score
        instance.save()

class StoriesCategory(models.Model):
    name = models.CharField(max_length= 255)
    image=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
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

class Stories(models.Model):
    category = models.ForeignKey(StoriesCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    video_file = models.URLField(null = True)
    OPTION_CHOICES = (
        ('IMAGE', 'IMAGE'),
        ('VIDEO', 'VIDEO'),
    )
    type = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
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

class StoriesWatched(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    stories = models.ForeignKey(Stories, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
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


class PackageMaterials(models.Model):
    file = models.FileField(upload_to='materials/', validators=[FileExtensionValidator(['pdf', 'xlsx', 'docx', 'plg', 'png', 'jpeg'])], storage=S3Storage())
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
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

class VedioMeterialAndQuestions(models.Model):
    name=models.CharField(max_length=255,null=True)
    description = models.TextField(blank=True, null=True)
    video=models.ForeignKey(StudioVideo,on_delete=models.CASCADE,null=True)
    material=models.ManyToManyField(PackageMaterials,blank=True)
    questionpaper=models.ManyToManyField(QuestionPaper,blank=True)
    thumbnail=models.ImageField(null=True,blank=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
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

class VedioPackage(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    banner=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    level=models.ForeignKey(Level,on_delete=models.CASCADE,null=True,blank=True)
    videos=models.ManyToManyField(VedioMeterialAndQuestions,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    premium=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
    question_paper_attempt_limit=models.PositiveIntegerField(null=True)
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

class RecentWatched(models.Model):
    path=models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE)  
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


class CurrentAffairsQuestions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
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
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    is_delete = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    publish_on = models.DateField(null=True)

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
                fields=['user','question_text','option_1','option_2','option_3','option_4','answer'],
                name=('unique_question_answers'),
                condition=~Q(is_delete=True)
            )
        ]

class ExampaperPackage(models.Model):
    title=models.CharField(max_length=255)
    imagetitle=models.CharField(max_length=255,null=True)
    exampaper=models.ManyToManyField(QuestionPaper)
    level=models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    thumbnail=models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    banner=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    premium=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
    attend_count = models.PositiveIntegerField(default=4,null=True) 
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

class CurrentAffairsVideos(models.Model):
    name = models.CharField(max_length=255)
    url=models.URLField()
    published = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    publish_on = models.DateField(null=True)
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

class DailyExams(models.Model):
    title=models.CharField(max_length=255)
    imagetitle=models.CharField(max_length=255,null=True)
    exampaper=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE)
    level=models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    thumbnail=models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True)
    banner=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
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


class PreviousExams(models.Model):
    title=models.CharField(max_length=255)
    imagetitle=models.CharField(max_length=255,null=True)
    exampaper=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    thumbnail=models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    banner=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
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

class SpecialExams(models.Model):
    title=models.CharField(max_length=255)
    imagetitle=models.CharField(max_length=255,null=True)
    exampaper=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    thumbnail=models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    banner=models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    description=models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.BooleanField(default=True)
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

class CurrentAffairsVideosAssign(models.Model):
    video=models.ForeignKey(StudioVideo, on_delete=models.CASCADE)
    icon = models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
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

class PopularFaculty(models.Model):
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    priority = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    status = models.BooleanField(default=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['faculty','course','priority'],
                name='unique_faculty_course',
                condition=~Q(is_delete=True)
            )
        ]

class PaidSubscriptions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(OnlineOrderPayment, on_delete=models.CASCADE)
    OPTION_CHOICES = (
        ('publication', 'publication'),
        ('subscription', 'subscription'),
        ('question_paper', 'question paper'),
        ('exampackages', 'exampackages'),
        ('videopackages', 'videopackages'),
       
    )
    product=models.CharField(choices=OPTION_CHOICES,max_length=50)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    status = models.BooleanField(default=False)
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

class Views(models.Model):
    user = models.BigIntegerField()
    VIEW_ASSIGN_CHOICES = (
        ('SHORTS','SHORTS'),
        ('CURRENT_AFFAIRS','CURRENT AFFAIRS'),
        ('STUDY_MATERIALS','STUDY MATERIALS'),
        ('QUESTION_PAPER','QUESTION PAPER'),
        ('VIDEOS','VIDEOS'),
        ('COMMENTS','COMMENTS'),
        ('STORIES','STORIES'),
        ('SUCCESS_STORIES','SUCCESS STORIES'),
        ('VIDEO_PACKAGE','VIDEO_PACKAGE'),
        ('EXAM_PACKAGE','EXAM_PACKAGE')
    ) 
    view_assign = models.CharField(choices=VIEW_ASSIGN_CHOICES,max_length=200, default="S",null=True)
    view_id = models.BigIntegerField()
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    
    
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

class ScholarshipType(models.Model):
    name = models.CharField(max_length=255)
    discount_amount = models.DecimalField(null=True,max_digits=8,decimal_places=2)
    percentage = models.DecimalField(null=True,max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    status = models.BooleanField(default=True)
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

class ScholarshipApproval(models.Model):
    type = models.ManyToManyField(ScholarshipType)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    approved_on = models.DateField(null=True)
    status = models.BooleanField(default=True)
    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    description_request = models.TextField(null=True)
    description_approv_reject = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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



class PollFightLobby(models.Model):
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_1_lobby',null=True)
    user2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_2_lobby',null=True)
    winner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='winner_lobby',null=True)
    created_at=models.DateTimeField(default=timezone.now, editable=False)
    status = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=((models.Q(user1__isnull=True)) 
                       |( models.Q(user2__isnull=True)) 
                       | (~models.Q(user1=models.F('user2')))
                       ),
                name='user1_user2_not_same_constraint'
            )
        ]

class PollFightQuestion(models.Model):
    question=models.ManyToManyField(NewQuestionPool,blank=True)
    status=models.BooleanField(default=True)
    points=models.IntegerField(default=0)
    count=models.IntegerField(default=0)
    duration=models.IntegerField(default=0)
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
from rest_framework.response import Response
@receiver(pre_save, sender=PollFightQuestion)
def enforce_unique_status(sender, instance, **kwargs):
    if instance.status and PollFightQuestion.objects.filter(status=True).exclude(pk=instance.pk).exists():
        raise ValidationError({"message":"There can only be one instance with status=True.","status_code": 409})
        # response_content = "There can only be one instance with status=True."
        # return Response(response_content, status=409) 


class PollFightSubmit(models.Model):
    room =models.ForeignKey(PollFightLobby,on_delete=models.CASCADE)
    question= models.ForeignKey(NewQuestionPool,on_delete=models.CASCADE,null=True)
    question_copy=models.TextField()
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
    crct_answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    index=models.IntegerField(default=0)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
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
                fields=['room','index','created_by'],
                name='unique_quiz_submit_for_user',
                condition=~Q(is_delete=True)
            )
        ]


class Groups(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE, null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True,blank=True)
    description = models.TextField(null=True)
    icon = models.ImageField(null=True,storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    members = models.ManyToManyField(User, related_name='members')
    admins = models.ManyToManyField(User, related_name='admins')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    is_open = models.BooleanField(default=False)   ## is_open = can user join freely or only admin can add
    is_admin_only = models.BooleanField(default=False)  ## is_admin_only = all user send msg or not
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

    class Meta:
        constraints=[
            models.CheckConstraint(
                check=(
                    (models.Q(category__isnull=False) & models.Q(level__isnull=True) & models.Q(course__isnull=True) ) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=False) & models.Q(course__isnull=True) ) |
                    (models.Q(category__isnull=True) & models.Q(level__isnull=True) & models.Q(course__isnull=False) ) 
                    
                ),
                name='only_one_field_non_null_constraint_for_group'
            )
        ]


class CommunityImage(models.Model):
    image=models.ImageField(upload_to='community/')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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




class Posts(models.Model):
    # group = models.ForeignKey(Groups,on_delete=models.CASCADE)
    title=models.TextField()
    description = models.TextField(null=True)
    location = models.CharField(null=True,max_length=200)
    images = models.ManyToManyField(CommunityImage,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    is_delete = models.BooleanField(default=False)

    def clean(self):
        # Specify the minimum number of related objects (keys) required
        max_key_count = 3  # Change this to your desired minimum count

        # Check the number of related objects
        key_count = self.images.count()

        # Perform the validation
        if key_count > max_key_count:
            raise ValidationError(
                 f"Up to {max_key_count} keys are allowed, but {key_count} were selected."
    
            )

    def save(self, *args, **kwargs):
        # Call the clean method to perform validation before saving
        # self.clean()

        # Call the parent class's save method to save the object
        super(Posts, self).save(*args, **kwargs)

   
    
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
            models.CheckConstraint(
                check=((models.Q(title__isnull=False))),
                name='posts-chat-required'
            )
        ]


class GroupMCQ(models.Model):
    question=models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255, blank=True, null=True)
    option_4 = models.CharField(max_length=255, blank=True, null=True)
    option_5 = models.CharField(max_length=255, blank=True, null=True)
    OPTION_CHOICES = (
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
        ('option_3', 'Option 3'),
        ('option_4', 'Option 4'),
        ('option_5', 'Option 5'),
    )
    answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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
            models.CheckConstraint(
                check=((models.Q(question__isnull=False)) 
                       &( models.Q(option_1__isnull=False)) 
                       &( models.Q(option_2__isnull=False)) 
                       ),
                name='question-chat-required'
            )
        ]


class GroupChat(models.Model):
    group = models.ForeignKey(Groups,on_delete=models.CASCADE,null=True)
    post = models.OneToOneField(Posts,on_delete=models.CASCADE,null=True)
    mcq = models.OneToOneField(GroupMCQ,on_delete=models.CASCADE,null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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
            models.CheckConstraint(
                check=((models.Q(post__isnull=True)) 
                       &( models.Q(mcq__isnull=False)) 
                       |( models.Q(post__isnull=False)) 
                       &( models.Q(mcq__isnull=True)) 
                       ),
                name='question-chat-required-or-mcq'
            ),
            models.CheckConstraint(
                check=(
                       ( models.Q(group__isnull=False)) 
                       ),
                name='group-chat-required-group'
            )
        ]


class PurchaseDetails(models.Model):
    user = models.BigIntegerField()
    PURCHASE_CHOICES = (
        ('EXAM_PACKAGE','EXAM_PACKAGE'),
        ('PUBLICATION','PUBLICATION'),
        ('STUDY_MATERIALS','STUDY MATERIALS'),
        ('QUESTION_PAPER','QUESTION PAPER'),
        ('VIDEO_PACKAGE','VIDEO_PACKAGE'),
        ('COURSE_PURCHASE','COURSE_PURCHASE'),
    ) 
    purchase_item = models.CharField(choices=PURCHASE_CHOICES,max_length=200)
    purchase_item_id = models.BigIntegerField()
    purchase_amount=models.BigIntegerField()
    history = HistoricalRecords()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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


@receiver(post_save, sender=OnlineOrderPayment)
def create_purchase_details(sender, instance, created, **kwargs):
    if instance.payment_status=="success":
        try:
            # Define a mapping from OnlineOrderPayment product to PurchaseDetails purchase_item
            product_to_purchase_mapping = {
                'publication': 'PUBLICATION',
                'subscription': 'COURSE_PURCHASE',
                'question paper': 'QUESTION_PAPER',
                'exampackages': 'EXAM_PACKAGE',
                'videopackages': 'VIDEO_PACKAGE',
            }
            
            # Get the corresponding purchase_item from the mapping
            purchase_item = product_to_purchase_mapping.get(instance.product, 'UNKNOWN')

            # Use a database transaction for atomicity
            with transaction.atomic():
                # Create a PurchaseDetails instance with relevant information
                PurchaseDetails.objects.create(
                    user=instance.user_ref,
                    purchase_item=purchase_item,
                    purchase_item_id=instance.product_id,
                    purchase_amount=instance.paid_amount,
                    # Add other fields as needed
                )
        except Exception as e:
            # Handle any exceptions that might occur during creation
            print(f"Error creating PurchaseDetails: {str(e)}")

# Connect the signal handler to the post_save signal of OnlineOrderPayment
post_save.connect(create_purchase_details, sender=OnlineOrderPayment)
    



class PackageQuizPoolUserRoom(models.Model):
    question_paper=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    total_score=models.DecimalField(null=True,max_digits=8, decimal_places=2)
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(null=True)
    video_package=models.ForeignKey(VedioPackage,on_delete=models.CASCADE,null=True)
    Exampaper_package=models.ForeignKey(ExampaperPackage,on_delete=models.CASCADE,null=True)
    count = models.IntegerField(null=True)
    is_status = models.BooleanField(default=True)
    is_submited = models.BooleanField(default=False)
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

@receiver(post_save, sender=PackageQuizPoolUserRoom)
def create_answers_for_room(sender, instance, created, **kwargs):
    print(instance,'instancee')
    if created:
        # Check if 'question_paper' and 'question_id' are present in instance's data
            question_paper_id = instance.question_paper.id
            print(question_paper_id,'ddd')
            # Retrieve the QuestionPaper and NewQuestionPool instances
            question_paper = QuestionPaper.objects.filter(id=question_paper_id).values('questions')
            print(question_paper,'dd')
            for x in question_paper:
                print(x['questions'],'sdds')
                qs=NewQuestionPool.objects.get(id=x['questions'])
                answers = PackageQuizPoolAnswers.objects.create(
                    room=instance,
                    question=qs,
                    question_copy=qs.question_text, 
                    option_1=qs.option_1,
                    option_2=qs.option_2,
                    option_3=qs.option_3,
                    option_4=qs.option_4,
                    option_5=qs.option_5,
                    crct_answer=qs.answer
            )

class PackageQuizPoolAnswers(models.Model):
    room =models.ForeignKey(PackageQuizPoolUserRoom,on_delete=models.CASCADE)
    question= models.ForeignKey(NewQuestionPool,on_delete=models.CASCADE,null=True)
    question_copy=models.TextField()
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
    crct_answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    index=models.IntegerField(default=0)
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

class StudentAttendance(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    timetable=models.ForeignKey(TimeTable,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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

class FacultyFeedback(models.Model):
    CHOICES = (
        (1, 'One star'),
        (2, 'Two stars'),
        (3, 'Three stars'),
        (4, 'Four stars'),
        (5, 'Five stars'),
    )
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)
    choice = models.IntegerField(choices=CHOICES)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
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



class QuestionpaperAttend(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    exampackage=models.ForeignKey(ExampaperPackage,on_delete=models.CASCADE,null=True)
    videopackage=models.ForeignKey(VedioPackage,on_delete=models.CASCADE,null=True)
    attend= models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
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


class Wallet(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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

class TransactionsWallet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_choice=(
        ('QUIZ','QUIZ'),
        ('POLL','POLL'),
    ) 
    source = models.CharField(choices=source_choice,max_length=200)
    source_id = models.BigIntegerField()
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


class ExamCategory(models.Model):
    name=models.CharField(max_length=250)
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

class ExamQuestionPaper(models.Model):
    name=models.CharField(max_length=225)
    code=models.CharField(max_length=225)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    notes=models.FileField(upload_to='materials/',null=True,blank=True)
    instruction=models.TextField(null=True)
    positivemark=models.FloatField(null=True)
    negativemark=models.FloatField(null=True)
    duration=models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    questions=models.ManyToManyField(NewQuestionPool)
    category=models.ForeignKey(ExamCategory,on_delete=models.CASCADE)
    description=models.TextField(null=True,blank=True)
    is_qr=models.BooleanField(default=False)
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



class OnlineCoursePackage(models.Model):
    name=models.CharField(max_length=225)
    descriptions=models.TextField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    validity=models.IntegerField(default=0)
    benifites=models.TextField()
    prize=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    strike_prize=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    PAYMENT_CHOICES = (
        ('fullpayment', 'fullpayment'),
        ('installment', 'installment')

    )
    payment_type = models.CharField(max_length=255, choices=PAYMENT_CHOICES,default='fullpayment')
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True,null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
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



class NoticeBoard(models.Model):
    date=models.DateField()
    content=models.TextField()
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
    is_status= models.BooleanField(default=False)
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


class VideoClassesBatch(models.Model):
    video=models.ForeignKey(StudioVideo,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    subtopic=models.ForeignKey(SubTopic,on_delete=models.CASCADE,null=True,blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,blank=True)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    is_status= models.BooleanField(default=False)
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


class ReportFlag(models.Model):
    REPORT_ASSIGN_CHOICES = (
        ('SHORTS','SHORTS'),
        ('CURRENT_AFFAIRS','CURRENT AFFAIRS'),
        ('STUDY_MATERIALS','STUDY MATERIALS'),
        ('QUESTION_PAPER','QUESTION PAPER'),
        ('VIDEOS','VIDEOS'),
        ('COMMENTS','COMMENTS'),
        ('STORIES','STORIES'),
        ('SUCCESS_STORIES','SUCCESS STORIES'),
        ('VIDEO_PACKAGE','VIDEO_PACKAGE'),
        ('EXAM_PACKAGE','EXAM_PACKAGE'),
        ('CHAT','CHAT'),
        ('ARTICAL','ARTICAL')
    ) 
    REPORT_CATEGORY  = (
    ("SEXUAL_CONTENT", "Sexual content"),
    ("VIOLENT_OR_REPULSIVE_CONTENT", "Violent or repulsive content"),
    ("HATEFUL_OR_ABUSIVE_CONTENT", "Hateful or abusive content"),
    ("HARASSMENT_OR_BULLYING", "Harassment or bullying"),
    ("HARMFUL_OR_DANGEROUS_ACTS", "Harmful or dangerous acts"),
    ("MISINFORMATION", "Misinformation"),
    ("CHILD_ABUSE", "Child abuse"),
    ("PROMOTES_TERRORISM", "Promotes terrorism"),
    ("SPAM_OR_MISLEADING", "Spam or misleading"),
    ("LEGAL_ISSUE", "Legal issue"),
    ("CAPTIONS_ISSUE", "Captions issue"),
    ("NONE_OF_THESE_ARE_MY_ISSUE", "None of these are my issue")
    )
    report_assign = models.CharField(choices=REPORT_ASSIGN_CHOICES,max_length=200, default="S",null=True)
    report_id = models.BigIntegerField()
    category=models.CharField(choices=REPORT_CATEGORY,max_length=200)
    content=models.TextField()
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
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



class OnlineCourseOrder(models.Model):
    onlinecourse=models.ForeignKey(OnlineCoursePackage,on_delete=models.CASCADE)
    topics=models.ManyToManyField(Topic)
    day = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
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

class ZoomMeetings(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(Module,on_delete=models.CASCADE,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,null=True)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, auto_created=True)
    meeting_id = models.BigIntegerField()
    password = models.CharField(max_length=10)
    image = models.ImageField(storage=S3Boto3Storage(
            bucket_name=AWS_STORAGE_BUCKET_NAME_PUBLIC,  # Specify the bucket for this field
            default_acl='public-read',
            querystring_auth=False
        ),upload_to='Images/')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    reminder = models.IntegerField(default=0)
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







class OfflineExamQuizPoolUserRoom(models.Model):
    question_paper=models.ForeignKey(ExamQuestionPaper,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    total_score=models.DecimalField(null=True,max_digits=8, decimal_places=2)
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(null=True)
    count = models.IntegerField(null=True)
    is_status = models.BooleanField(default=True)
    is_submited = models.BooleanField(default=False)
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

# @receiver(post_save, sender=PackageQuizPoolUserRoom)
# def create_answers_for_room(sender, instance, created, **kwargs):
#     print(instance,'instancee')
#     if created:
#         # Check if 'question_paper' and 'question_id' are present in instance's data
#             question_paper_id = instance.question_paper.id
#             print(question_paper_id,'ddd')
#             # Retrieve the QuestionPaper and NewQuestionPool instances
#             question_paper = QuestionPaper.objects.filter(id=question_paper_id).values('questions')
#             print(question_paper,'dd')
#             for x in question_paper:
#                 print(x['questions'],'sdds')
#                 qs=NewQuestionPool.objects.get(id=x['questions'])
#                 answers = PackageQuizPoolAnswers.objects.create(
#                     room=instance,
#                     question=qs,
#                     question_copy=qs.question_text, 
#                     option_1=qs.option_1,
#                     option_2=qs.option_2,
#                     option_3=qs.option_3,
#                     option_4=qs.option_4,
#                     option_5=qs.option_5,
#                     crct_answer=qs.answer
#             )

class OfflineExamQuizPoolAnswers(models.Model):
    room =models.ForeignKey(OfflineExamQuizPoolUserRoom,on_delete=models.CASCADE)
    question= models.ForeignKey(NewQuestionPool,on_delete=models.CASCADE,null=True)
    question_copy=models.TextField()
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
    crct_answer = models.CharField(max_length=255, choices=OPTION_CHOICES,null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    index=models.IntegerField(default=0)
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

class UpVotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(GroupChat,on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

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