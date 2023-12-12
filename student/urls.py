from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'studentregistrationexcel', StudentExcelAdd, basename='StudentExcelAdd')
router.register(r'student-login',Studentlogin,basename='studentlogin')
router.register(r'otp-verification',Verifyotp,basename='Verifyotp')
router.register(r'student-details',Studentcoursedetails,basename='Studentdetails')
router.register(r'student-batch-details',StudentBatchDetails,basename='StudentBatchDetails')
router.register(r'student-register',StudentRegister,basename='StudentRegister')
router.register(r'student-profile', StudentViewSet,basename='StudentProfile')
router.register(r'userid-on-studentid', StudentUserViewSet, basename='useronstudent')
router.register(r'current-affairs',CurrentAffairsViewSet,basename='currentaffairs')
router.register(r'current-affairs-sorted',CurrentAffairsDaySortedViewSet,basename='currentaffairssorted')
##stdent temp new batchdetials
router.register(r'new-student-branch-details',NewStudentBatchDetials,basename="NewStudentBatchDetials")
router.register(r'student-list-temp',StudentlistTemp,basename='Studentlisttemp')
#edit studentbatch detials
router.register(r'edit-student-batch-details',EditStudentBatchDetials,basename='EditStudentDetials')



router.register(r'version', VersionViewSet,basename='VersionViewSet')

#####student original###
router.register(r'student-register-org',StudentRegisterOrg,basename='StudentRegisterOrg')
router.register(r'student-otp-verification1',StudentOtpVerificationOrg1,basename='StudentOtpVerificationorg')
router.register(r'student-email-verifacion',EmailVerifaction,basename='EmailVerifaction')
router.register(r'email-otp-verifacation',EmailOtpVerification,basename="EmailOtpVerification")
router.register(r'email-otp-verifacation1',EmailOtpVerification1,basename="EmailOtpVerification")
router.register(r'publication', PublicationViewSet,basename='publication')
router.register(r'student-update', StudentUserViewSet,basename='StudentUserViewSet')
router.register(r'student-apllication', StudentApplicationViewSet,basename='StudentApplicationViewSet')
router.register(r'student-reg-new', NewStudentRegister,basename='new-student-register')
router.register(r'studentReg-withoutAppilication',StudentRegWithoutApplication,basename='studentReg-withoutAppilication')
#dashboard profile
router.register('dashboard-profile',DashBoardProfile,basename="DashBoardProfile")
#delivery address
router.register(r'delivery-address',Deliveryaddress,basename='delivery-address')
router.register(r'publication-student',PublicationViewSetForStudent,basename='publication-student')
#declarations
router.register('student-declarations',studentDeclarationsViewSet,basename='studentDeclarationsViewSet')
router.register('student-ranklist',RankListViewSet,basename='student-ranklist')



urlpatterns = [
    path('', include(router.urls)),
    path('register/', Loginview.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    # path('offlineregister/',StudentRegistrationAPIView.as_view,name="offlinestudentregister")
    path('offlineregister/', StudentRegistrationAPIView.as_view(), name='offline_register'),
    path('deletestudent/', deletestudent, name='deletestudent'),

    # path('register/',views.FacultyRegisterView.as_view(),name="views"),
    # path('registerotp/',views.FacultyRegisterViewss.as_view(),name="views")

]

from django.urls import re_path


websocket_urlpatterns = [
    # re_path(r'ws/my-websocket/$', MyWebSocketConsumer.as_asgi()),
    # re_path(r'ws/new-sock/$', MyConsumer.as_asgi()),
    # re_path(r'ws/post/$', PostConsumer.as_asgi()),
]
