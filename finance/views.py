from django.shortcuts import render
from rest_framework.decorators import api_view
from MobileApp.models import CartItems
from accounts.api.authhandle import AuthHandlerIns
from course.views import SinglePagination

from finance.models import OnlineOrderPayment
from permissions.permissions import *
from .razorpay import razorpay_client
from rest_framework.response import Response
# Create your views here.
import razorpay
from rest_framework import viewsets
from .serializers import *
from rest_framework import status


@api_view(['POST'])
def razorpaysuccess(request):
#    \
    res = request.data
    params_dict = {
        'razorpay_payment_id' : res['razorpay_payment_id'],
        'razorpay_order_id' : res['razorpay_order_id'],
        'razorpay_signature' : res['razorpay_signature']
    }

    # verifying the signature
    try:
        res = razorpay_client.utility.verify_payment_signature(params_dict)
        print(res)
        if res == True:
            razorpay_order_id=params_dict['razorpay_order_id']
            product=OnlineOrderPayment.objects.filter(razor_id=razorpay_order_id)
            amounts=OnlineOrderPayment.objects.filter(razor_id=razorpay_order_id).values('total_amount')
            print(amounts)
            total_sum = 0
            for amount in amounts:
                total_sum += amount['total_amount']

            print(total_sum)
            for x in product:
                x.paid_amount=total_sum
                x.payment_status="success"
                x.save()

            return Response({'status':'Payment Successful'})
        return Response({'status':'Payment Faileddd'})
    except Exception as e:
        error_message = str(e) if str(e) else 'Payment Failed'
        return Response({'status': error_message}, status=status.HTTP_400_BAD_REQUEST)

   
from rest_framework.response import Response

class OrderStatus(viewsets.ReadOnlyModelViewSet): 
    serializer_class = OrderStatusSerializer
    permission_classes = [StudentPermission]

    def get_queryset(self):
        student = AuthHandlerIns.get_id(request=self.request)
        return OnlineOrderPayment.objects.filter(user=student).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class OrderStatusAdmin(viewsets.ModelViewSet):
    serializer_class = OrderStatusSerializer
    queryset = OnlineOrderPayment.objects.all().order_by('-created_at')
    permission_classes = [AdminAndRolePermission]
    pagination_class = SinglePagination


    def get_queryset(self):
        queryset=OnlineOrderPayment.objects.all().order_by('-created_at')
        id = self.request.query_params.get('id')
        username = self.request.query_params.get('username')
        email = self.request.query_params.get('email')
        mobile = self.request.query_params.get('mobile')
        order_number = self.request.query_params.get('order_number')
        product = self.request.query_params.get('product')
        delivery_status = self.request.query_params.get('delivery_status')
        payment_status = self.request.query_params.get('payment_status')
        razor_id = self.request.query_params.get('razor_id')
        if id:
            queryset=queryset.filter(id=id)
        if username:
            queryset=queryset.filter(user__username__icontains=username)
        if email:
            queryset=queryset.filter(user__email__icontains=email)
        if mobile:
            queryset=queryset.filter(user__mobile__startswith=mobile)
        if order_number:
            queryset=queryset.filter(order_number__icontains=order_number)
        if product:
            queryset=queryset.filter(product__publication=product)
        if delivery_status:
            queryset=queryset.filter(delivery_status=delivery_status)
        if payment_status:
            queryset=queryset.filter(payment_status=payment_status)
        if razor_id:
            queryset=queryset.filter(delivery_status__icontains=razor_id)
        return queryset



class HeadsCreateViewset(viewsets.ModelViewSet):
    queryset=Heads.objects.all().order_by('-created_at')
    pagination_class=SinglePagination
    permission_classes=[AdminAndRolePermission]
    serializer_class=HeadsSerializer

class TransactionCreateViewset(viewsets.ModelViewSet):
    queryset=Transaction.objects.all()
    pagination_class=SinglePagination
    permission_classes=[AdminAndRolePermission]
    serializer_class=TransactionSerializer

class BankAccountsCreateViewset(viewsets.ModelViewSet):
    queryset=BankAccounts.objects.all()
    pagination_class=SinglePagination
    permission_classes=[AdminAndRolePermission]
    serializer_class=BankAccountSerializer