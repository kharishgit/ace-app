from django.db import models
from course.models import *
from accounts.models import User

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_delete=True)
    
class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude()    

# Create your models here.



class OnlineOrderPayment(models.Model):
    user_ref=models.BigIntegerField()
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    order_number = models.CharField(max_length=20)
    OPTION_CHOICES = (
        ('publication', 'publication'),
        ('subscription', 'subscription'),
        ('question_paper', 'question paper'),
        ('exampackages', 'exampackages'),
        ('videopackages', 'videopackages'),
       
    )
    product=models.CharField(choices=OPTION_CHOICES,max_length=50)
    product_id=models.BigIntegerField()
    razor_id=models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2,default=0)
    off_amount = models.DecimalField(max_digits=15, decimal_places=2,default=0)
    OFFERS=(
        ('coupon', 'Coupon'),
        ('wallet', 'wallet'),
        ('none', 'None'),

    )
    offer_choice= models.CharField(choices=OFFERS, default='none', max_length=20)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        # Add more choices as per your requirement
    )
    payment_status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    Delivery_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        # Add more choices as per your requirement
    )
    delivery_status = models.CharField(choices=Delivery_CHOICES, default='pending', max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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

class Heads(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    category = models.BooleanField(default=True) # To check Expence or Liability
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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

class BankAccounts(models.Model):
    acc_no = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    is_delete = models.BooleanField(default=False)
    active=models.BooleanField(default=True)

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
                fields=['acc_no'],
                name=('unique_account_no'),
                condition=~Q(is_delete=True)
            )
        ]




class Transaction(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    head = models.ForeignKey(Heads, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    acc_no = models.ForeignKey(BankAccounts,blank=True, null=True,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
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
