from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('Order-Status',OrderStatus,basename=OrderStatus)
router.register('order-status-admin',OrderStatusAdmin,basename="orderstatusAdmin")
router.register('account-heads',HeadsCreateViewset,basename="account-heads")
router.register('account-transaction',TransactionCreateViewset,basename="account-transaction")
router.register('bank-accounts-create',BankAccountsCreateViewset,basename="bank-accounts-create")



urlpatterns = [
    path('', include(router.urls)),
    path('razorpaysuccess/',razorpaysuccess, name='razorpaysuccess')

    
]