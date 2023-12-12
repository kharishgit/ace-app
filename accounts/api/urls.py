###
from django.urls import path,include
from . import views
from .views import update_faculty_photo, SalaryListCreateView, SalaryDetailView
from .views import *
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'updateinhousefac', FacultyViewSet, basename='faculty')
router.register(r'getquestionsbasedfaccoutop', QuestionPoolViewSet, basename='questions')
router.register(r'specialholidays', views.SpecialHolidayViewSet, basename='special-holidays'),
router.register(r'delete-faculty-reject-application',DeleteFacRejectApp,basename='DeleteFacRejectApp'),
router.register(r'faculties', QuestionPoolSearch)
router.register(r'check-user-exists', views.CheckUsernameExistsViewSet, basename='check-user-exists')
router.register(r'materials-get', MaterialViewSet,basename='materials-get')
router.register(r'questionimages', QuestionImageViewSet,basename='questionimages')
#new questionpaper
router.register('question-pool-all',QuestionPoolCreateNew)
router.register('question-paper-creation',QuestionPaperGeneration)
router.register(r'question-get-or-search', QuestionSearchView, basename='question-get-or-search')
router.register(r'question-get-based-all', QuestionViewSets, basename='QuestionViewSets')
router.register(r'question-get-based-published-all', QuestionViewSetsPublishedAll, basename='QuestionViewSets')
router.register(r'courselist-countquestions',QuestionCourseViewSet,basename='QuestionCourseViewSet')
# router.register(r'excel-add-questions',ExcelQuestionPoolCreate,basename='NewQuestionPoolViewSet')
router.register(r'excel-view-questions',ExcelQuestionget,basename='NewQuestionPoolViewSet')
router.register('publish-or-draft',PublishDraftQuestuion,basename='publish-or-draft')
router.register(r'deletequestions',DeleteQuestionAll,basename='DeleteQuestionAll')
router.register(r'excel-add-questions',ExcelQuestionPoolCreateNew,basename='NewQuestionPoolViewSet')
router.register('excel-add-dtp-sections',ExcelAddingDtpSections,basename="ExcelAddingDtpSections")
# router.register(r'subtopic-id-for-excel',Subtopicidforexcel,basename="Subtopicidforexcel")
router.register('categories-for-excel',CategoriesforExcel,basename='CategoriesforExcel')
router.register('level-for-excel',LevelforExcel,basename='LevelforExcel')
router.register('course-for-excel',CourseforExcel,basename='CourseforExcel')
router.register('subject-for-excel',SubjectforExcel,basename='SubjectforExcel')
router.register('module-for-excel',ModuleforExcel,basename='ModuleforExcel')
router.register('topic-for-excel',TopicforExcel,basename='TopicforExcel')
router.register('subtopic-for-excel',SubTopicforExcel,basename='SubTopicforExcel')






# router.register(r'studioapplicationapprove',StudioApplicationApprove,basename='StudioApplicationffApprove')




router.register(r'role-users', RoleUserViewSet)
router.register(r'passwordverify',PassWordVerify,basename="passwordverify")
router.register(r'passwordresetstaff',PasswordResetStaff,basename="passwordresetstaff")
#faculty file add
router.register(r'facultyimages', FacultyImageViewSet,basename='facultyimages')
router.register(r'facultyimagesbyadmin', FacultyImagesUpdateByadmin,basename='FacultyImagesUpdateByadmin')
router.register(r'approved-faculty-courses', FacultyApprovedCoursesViewSet, basename='faculty-approved-courses')
#inhouse facultylist
router.register(r'inhouse-faculty-list',InhouseFacultyList,basename='InhouseFacultyList')
router.register(r'materials-get', MaterialViewSet)
router.register(r'faculty-approved-topic', FacultyCourseAdditionViewSet, basename='faculty-course-additions')
router.register(r'faculty-approved-subject', FacultySubjectViewSet, basename='faculty-subject')
router.register(r'get-faultyon-subject', FacultyWithSubjectViewSet, basename='faculty-get-subject')
router.register(r'faculty-approved-course', FacultyCourseApprovedViewSet, basename='faculty-course-approved')
# router.register(r'faculty-approved-course-details', FacultyApprovedCourseDetailsViewSet, basename='faculty-course-apr-details')



#studio
router.register(r'studio-course',views.StudioVideoCourse,basename='studio-courses')
router.register(r'studio-name',views.StudionNames,basename='studio-courses')
router.register('faculty-applications',views.FacultyApplicationsViews,basename='faculty-application')
router.register(r'add-vedio-in-studiovideo',AddVediotoStudioCourse,basename='AddVediotoStudioCourse')
router.register(r'Not-assign-vedio-topics',NotAssignVedioTopics,basename='NotAssignVedioTopics')
router.register(r'Count-of-application',CountofApplication,basename='CountofApplication')
router.register(r'video-Content-Details-based-course',CountofApplicationBased,basename='CountofApplication')
router.register(r'studio-application-approve',StudioApplicationApprove,basename='StudioApplicationApprove')
router.register(r'studio-with-faculty-assigned',AssignedFacultiesList,basename='NotassignedFaculties')
router.register(r'studio-without-faculty-assigned',NotassignedFaculties,basename='NotassignedFaculties')
router.register(r'studio-assigned-vedios',VedioAssignedStudio,basename='VedioAssignedStudio')
router.register(r'studio-applications-faculty-assigned',FacultyAssignedStudioCourseStudiouser,basename='studioapplctinfacultyassigned-not-vedios')
router.register(r'vedio-upload-vimeo-and-db',VidioaddingTovimeoandDb,basename='VidioaddingTovimeoandDb')
router.register(r'vedio-assign-for-course-etc',VideoAssigningForCourseEtc,basename=VideoAssigningForCourseEtc)
router.register('all-video-db',AllvideoDB,basename='AllvideoDB')
router.register(r'study-material-upload',MaterialUploadViewSet,basename='study-material-upload')
router.register(r'material-refernces',MaterialReferenceViewSet,basename='material-refernces')
router.register('Studio-Course-all-details',StudioCourseallDetails,basename='StudioCourseallDetails')
router.register('completed-studio-course-list',Completedstudiiocourselist,basename='Completedstudiiocourselist')
router.register('add-online-salary',CreateOnlineSalary,basename='CreateOnlineSalary')
#delte studiovideo in assigning video manually
router.register(r'delete-vidoe-from-manually-assigning',DeleteVideomanuallyAssigning,basename='DeleteVideomanuallyAssigning')
#common video add to vimeo 
router.register(r'add-video-to-vimeo-common',CommonVideoAdd,basename='CommonVideoAdd')
router.register(r'faculty-list-online',Facultylistonline,basename='Facultylistonline')
router.register(r'faculty-list-online-and-both',FacultylistonlineBoth,basename='FacultylistonlineBoth')
router.register(r'material-student-onfacultytopic',MaterialAllotedForStudents,basename='materialforstudent')
router.register(r'material-facultybased',MaterialUploadFacultyBasedViewSet,basename='materialfacultybased')
router.register(r'material-facultybaseduserid',MaterialUploadFacultyBasedUserIdViewSet,basename='materialfacultybasedid')
router.register(r'material-rating',MaterialRatingViewsSet,basename='materialrating')
router.register(r'popular-faculty',PopularFacultyViewSet,basename='popularfaculty')
# router.register(r'material-upload-view-admin',MaterialUploadAdminViewSet,basename='study-material-admin-view')
router.register(r'add-video-to-studio',AddVideoToStudioCourse,basename='AddVediotoStudioCourse')
router.register(r'all-faculty-material-view',AllFacultyMaterialAdminViewSet,basename='all-faculty-material-view')
router.register(r'all-pending-material-view',AllPendingMaterialAdminViewSet,basename='all-pending-material-view')
router.register(r'all-new-material-view',NewMaterialListViewSet,basename='all-new-material-view')
router.register(r'all-completed-material-view',AllCompletedMaterialAdminViewSet,basename='all-completed-material-view')
router.register(r'branch-history-view',BranchHistoryViewSet,basename='branch-history-view')

#test api


#excelupdate
router.register('exceluploading',addexcels3,basename='addexcels3')

router.register(r'role',RolesViewSet,basename='RolesViewSet')
router.register(r'permission',PermissionViewSet,basename='RolesViewSet')
#faculty id photo verification
router.register(r'photo-id-resume-verifcation',Photoidresumeverification,basename='photoverifaction')
router.register(r'user-list-role',UserForRoles,basename='user-list-role')
router.register(r'branch-user',BranchUser,basename='branch-user')
router.register(r'branch-user-list',BranchUserlist,basename='branch-user-list')
router.register(r'BlockRoleUser',BlockRoleUser,basename='branch-user-list')
router.register(r'converted-materials',ConvertedMaterialViewSet,basename='converted-material')
router.register(r'uploaded-faculty-materials',UploadedMaterialsFacultyBased,basename='facultyuploaded-materials')
router.register(r'material-assigned-delete',MaterialReferenceDeleteViewSet,basename='delete-assignedmaterials')

#user patch detials
router.register(r'patch-user-details',ChangeUserDetails,basename='ChangeUserDetails')
#faculy online salary assign
router.register(r'online-offline-salary-assign',OfflineOnlineSalaryAssign,basename='OfflineOnlineSalaryAssign')
router.register(r'new-question-copy',NewQuestionPoolViewSetCopy,basename='new-question-copy')

#add permission
router.register('question-pool-all1',QuestionPoolCreateNewCopy,basename='questionpoolcreatenew')
router.register(r'study-material-upload1',MaterialUploadViewSetCopy,basename='study-material-upload')
router.register(r'topic-wise-faculty-list',FacultyListByTopicIdViewset,basename='topic-wise-faculty-list')
# router.register(r'branch-qr-scanner',branch_qr,basename='topic-wise-faculty-list')
#change specialholiday to modelviewset
router.register('specialholidays1',SpecialHolidaysViewsetCopy,basename="specialholidays")

#staff incentive salary
router.register('incentives',IncentivesViews,basename='incentives')
router.register('StaffIncentives',StaffIncentivesViews,basename='staffincentives')
router.register('staffsalary',StaffSalaryViews,basename='StaffSalary')
router.register('staffincentiveamount',StaffIncentiveAmount,basename='StaffIncentiveAmount')
router.register('staff-list',ActiveStafflist,basename="Activestafflist")
router.register('incentive-list-by-users',Incentiveslistbyusers,basename="Incentiveslistbyusers")
router.register('incentive-list-not-in-user',IncentivelistnotinUsers,basename="incentivelistnotin")


# history
router.register(r'history-facultycourse',FacultyCourseCreation,basename='history-facultycourse')
router.register(r'history-facultysalary',FacultySalaryCreation,basename='history-facultysalary')
router.register(r'history-facultyexperiance',FacultyExperianceCreation,basename='history-facultyexperiance')


router.register(r'facultycoursedelete',FacultyCourseDeletion,basename='facultycoursedelete')
router.register(r'salaries',SalaryCreation,basename='salary-list-create')
router.register(r'salaryfacultyfixations',salaryfacultychanging,basename='salaryfixation_detail')
router.register(r'experiences',ExperianceCreation,basename='experience-list-create')
router.register(r'updateinhousefac',InhouseFacultyCreation,basename = 'update-inhouse-fac')


#faculty questionpool app side
#faculty topics pass the course id
router.register('topic-based-on-fac-course',TopicBasedOnCourse,basename='TopicBasedOnCourse')
router.register('course-based-on-fac-category',CourseBasedOnCategory,basename='TopicBasedOnCourse')
router.register('faculty-category',FacultyCategory,basename='FacultyCategory')
router.register('pending-nonapprove-question',FacultyPendingQuestions,basename="FacultyPendingQuestions")
router.register('faculty-approve-button',FacultyApproveButton,basename="FacultyApproveButton")
router.register('faculty-reject-button',FacultyRejectButton,basename="FacultyRejectButton")
router.register('faculty-search-question',FacultyQuestionSearch,basename="FacultyRejectButton")

##not use
# router.register('faculty-dtp-approved-question',FacultySideDtpApprovedquestions,basename="FacultyPendingQuestions")

####DTP
router.register('fac-question-dtp-create-edit',FacappQuestinEdit,basename="FacappQuestinEdit")
router.register('faculty-new-added-questios',Facultynewaddedquestios,basename="Facultynewaddedquestios")
router.register('faculty-reject-questions',FacultyRejectQuestion,basename="Facultynewaddedquestios")
router.register('faculty-approved-questions',FacApprovedQuestions,basename="FacApprovedQuestions")

urlpatterns = [
    path('', include(router.urls)),
    path('Topic-Status/<int:pk>/',
         TopicStatusVedioCourse.as_view(actions={'get': 'retrieve'}), name='TopicStatusVedioCourse'),
     # path('api/topic-application-count/', TopicApplicationCountViewSet.as_view({'get': 'list'}), name='topic-application-count'),
    path('question-pool/topic-question-count/', NewQuestionPoolViewSet.as_view({'get': 'topic_question_count'}), name='topic-question-count'),
#     path('updateinhousefac/<int:facultyid>/', FacultyViewSet.as_view({'patch': 'partial_update'}), name='update_inhouse_fac'),
    path('faculties/search_by_username/', QuestionPoolSearch.as_view({'get': 'search_by_username'}), name='faculty_search_by_username'),
    path('admin-sgp/', Admin_signup, name='Admin_signup'),
    path('faculty-sgp/', Faculty_signup, name='Faculty_signup'),
    path('role-sgp/', Roleuser_signup, name='Roleuser_signup'),
    path('login-a/', Login_single, name='Login_all'),
    path('adminfacultymessagewhatsap/<int:id>/',
         views.adminfacultyverificationwithWhatsapp.as_view()),
    path('facultyforgotpassword/',
         views.facultyforgotpassword.as_view(), name="facultylogin"),
    # path('adminfaculty-sgp/', AdminFaculty_signup, name='Faculty_signup'),
    # path('crud-faculty/<int:pk>/',
    #         FacultyRetrieveUpdateDestroyView.as_view(), name='crud-faculty'),
    path('faclist/', faculty_list, name='faculrt_list'),
    path('material-upload/', MaterialCreateAPIView.as_view(), name='material-upload'),
#     path('experiences/', ExperienceListCreateView.as_view(),
#          name='experience-list-create'),
    path('experiences/<int:pk>/', ExperienceDetailView.as_view(),
         name='experience-detail'),
    path('faculty_course_additions/', FacultyCourseAdditionListCreateView.as_view(),
         name='faculty_course_addition_list_create'),
    # path('faculty_course_additions/<int:pk>/', FacultyCourseAdditionRetrieveUpdateDestroyView.as_view(), name='faculty_course_addition_retrieve_update_destroy'),
    path('faculty/<int:faculty_id>/update-photo/',
         update_faculty_photo, name='update-faculty-photo'),
    path('faculty-course-additions/<int:user_id>/',
         FacultyCourseAdditionView.as_view(), name='faculty-course-additions'),
    path('FacultyCourseAdditionPendingtoapprove/<int:pk>/',
         FacultyCourseAdditionPendingtoapprove.as_view(), name='faculty-course-additions'),
    path('FacultyCourseAdditionPendingtoBlock/<int:pk>/',
         FacultyCourseAdditionPendingtoBlock.as_view(), name='faculty-course-additions'),


    # question pool
    path('question-pools/', QuestionPoolCreateView, name='question-pool-create'),
    path('questionpoolall/', QuestionPoolget.as_view(),
         name='question-pool-create'),
    path('questions/', Questionget.as_view(), name='questions'),
    path('materials/<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
    path('faculty-course-additions/<int:user_id>/',
         FacultyCourseAdditionView.as_view(), name='faculty-course-additions'),
    path('check-email/', views.CheckEmailExists.as_view(), name='check-email'),
    path('check-mobile/', views.CheckMobileExists.as_view(), name='check-mobile'),
    path('faculty-sgp-experiences/', faculty_signup_and_experience,
         name='faculty_signup_and_experience'),
    path('check-whatsapp/', views.CheckWhatsappExists.as_view(),
         name='check-whatsapp'),
#     path('salaries/', SalaryListCreateView.as_view(), name='salary-list-create'),
    path('salaries/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),
    path('salaryfixations/', SalaryFixationListCreateView.as_view(),
         name='salaryfixation_list_create'),
    path('salaryfixations/<int:pk>/', SalaryFixationDetailView.as_view(),
         name='salaryfixation_detail'),


    path('facultylistforauto/<int:pk>/',
         facultyList_AutoTimeTable_Course, name='facultylistforauto'),
    path('facultylistfortopic/<int:pk>/',
         facultyList_AutoTimeTable_Topic, name='facultylistfortopic'),
    # declaration
    path('createdeclaration/', DeclarationCreation.as_view(),
         name='createdeclaration'),
    path('updatedeclarations/<int:pk>/',
         DeclarationCreation.as_view(), name='declaration-update'),
    path('faculty/<int:faculty_id>/salary/',
         get_salarydetails_by_faculty, name='faculty_salary'),

    path('facultysignup/', faculty_signup_new, name='facultylistfortopic'),
    path('adminfaculty-sgp/', AdminFaculty_signup, name='Faculty_signup'),
    path('changefacultypassword/<int:pk>/',
         AdmincangefacPassword, name='AdmincangefacPassword'),
#     path('salaryfacultyfixations/<int:pk>/',
#          SalaryFixDetailView.as_view(), name='salaryfixation_detail'),
    path('salarydetail/', get_salary_list, name='salary-list'),
    path('internal-faculty/',
         InternalFaculty.as_view(actions={'get': 'list'}), name='faculty-list'),
    path('internal-faculty/<int:pk>/',
         InternalFacultyByTopic.as_view(actions={'get': 'retrieve'}), name='faculty-topic-list'),
    path('getfacultyonuserid/<int:user_id>/',getfacultyonuserid, name='get-faculty-id'),
    #faculty change password
    path('faculty/updatepassword/', views.facultychangepassword.as_view({'patch': 'update_password'}), name='faculty-update-password'),
    path('approved-faculties-history/', ApprovedFacultiesListForHistory.as_view(), name='approved-faculties-history'),
    #faculty file add 
     path('faculty/<int:faculty_id>/update-file/',
         Update_Faculty_File, name='update-faculty-photo'),
     # path('facultycoursedelete/<int:pk>/',FacultyCourseAdditionDelete.as_view(),name='FacultyCourseAdditionDelete'),
     path('materials-get/<int:faculty_id>/<int:topic_id>/', MaterialViewSet.as_view({'get': 'list'}), name='material-list'),

     path('material-crud/<int:pk>/', MaterialCRUDView.as_view(),
         name='material-crud'),
     path('online-course-assign/', views.OnlineCourseAssign.as_view({'post': 'create'}), name='online-course-assign'),
     #test vimeo vedios
     path('api/videos/<str:video_id>/', VideoAPIView.as_view(), name='get_video'),
     path('getallvedio/', GetAllVideoAPIViews.as_view(), name='post_video'),
     path('batch-letters/<int:id>/', getbranchletters, name='batch-letters'),
     path('getavailablity/<int:id>/', getavailablity, name='getavailablity'),
     path('branch-qr-scanner/<int:id>/',branch_qr,name='branch-qr-scanner')
 

     









]
