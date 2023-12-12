from requests import Response
from rest_framework import serializers
from MobileApp.models import *
from MobileApp.serializers import *

from student.models import Publications
from .models import *

class PublicationSerializerOrderstatus(serializers.ModelSerializer):
    course_det = serializers.SerializerMethodField()
    class Meta: 
        model = Publications
        fields = ['bookname','icon','category','book_price','discount_price','no_of_pages','course','edition','publish_on','publish_on','description','course_det']
    def get_course_det(self,obj):
        return [course.name for course in obj.course.all()]
    
class VedioPackageSerializerOrderstatus(serializers.ModelSerializer):
    # videos=VedioMeterialAndQuestionsSerializer(many=True)

    class Meta:
        model=VedioPackage
        exclude=['created_at','created_by','is_delete']

class ExampaperpackageSerializerOrderstatus(serializers.ModelSerializer):
    # exampaper=PackageQuestionPaperSerilizerSmall(many=True)
    # level=ExampackageLevelSerializer()
    # exampaper_counts=serializers.SerializerMethodField()
    

    class Meta:
        model=ExampaperPackage
        exclude=['created_at','created_by','is_delete']

    def get_exampaper_counts(self,obj):
        exmpprcount=obj.exampaper.count()
        return exmpprcount
        
    
class OrderStatusSerializer(serializers.ModelSerializer):
    publication=serializers.SerializerMethodField()
    videopackages=serializers.SerializerMethodField()
    # subscription=serializers.SerializerMethodField()
    # question_paper=serializers.SerializerMethodField()
    exampackages=serializers.SerializerMethodField()
    class Meta:
        model=OnlineOrderPayment
        fields=['id','user','order_number','product','razor_id','total_amount','paid_amount','off_amount','payment_status','delivery_status','created_at','publication','exampackages','videopackages']

    def get_publication(self,obj):
        if obj.product=="publication":
            products=Publications.objects.filter(id=obj.product_id)
            publications=PublicationSerializerOrderstatus(products,many=True)
            return publications.data
        else:
            return None
        
    def get_videopackages(self,obj):
        if obj.product=="videopackages":
            videos=VedioPackage.objects.filter(id=obj.product_id)
            video=VedioPackageSerializerOrderstatus(videos,many=True)
            return video.data
        else:
            return None
        
    def get_exampackages(self,obj):
        if obj.product=="exampackages":
            exampaper=ExampaperPackage.objects.filter(id=obj.product_id)
            exampapers=ExampaperpackageSerializerOrderstatus(exampaper,many=True)
            return exampapers.data
        else:
            return None

class HeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heads
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    branch_name =serializers.SerializerMethodField()
    head_name = serializers.SerializerMethodField()
    acc_no_no =serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_branch_name(self,obj):
        return obj.branch.name

    def get_head_name(self,obj):
        return obj.head.name
    
    def get_acc_no_no(self,obj):
        try:
            return obj.acc_no.acc_no
        except:
            return None

        
        
class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=BankAccounts
        fields ='__all__'