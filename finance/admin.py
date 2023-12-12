from django.contrib import admin

# from finance.models import OnlineOrderPayment
from finance.models import *



# Register your models here.
admin.site.register(OnlineOrderPayment)
admin.site.register(Heads)
admin.site.register(BankAccounts)
admin.site.register(Transaction)