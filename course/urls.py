from django.urls import path, include

from accounts.api.views import *
from .views import *
from rest_framework.routers import DefaultRouter
# from views import CoursePdf


router = DefaultRouter(trailing_slash=True)
router.register(r'category', CategoryViewset, basename='category')
router.register(r'create-branch',BranchListCreateView, basename='branch' )
# router.register(r'branch-courses', BranchCourseView, basename='branch-courses')
router.register(r'timetableview', TimeTableViewSet)
router.register(r'batchviewset', BatchViewSet, basename='batchnew')
router.register(r'review-questions', ReviewQuestionsViewSet)
router.register(r'review-answers', ReviewViewSet)
router.register(r'get-review-questions', ReviewQuestionsGetViewSet)
router.register(r'timetable-review', TimeTableReViewSet)
router.register(r'faculty-attendance-on-timetable', FacultyAttendanceViewSet, basename='faculty-attendance-on-timetable')
router.register(r'timetable/attendance', TimeTableAttendanceViewSet, basename='faculty-attendance-on-timetable')
router.register(r'timetable/booked', TimeTableForBooked, basename='faculty-timetable-booked')
router.register(r'TimeTableMultipleDelete', TimeTableMultipleDelete, basename='TimeTableMultipleDelete')
router.register(r'timetable-by-date-of-branch', TimeTableByDateOfBranch, basename='timetable-by-date-of-branch')
# router.register(r'categories-topic-check', CategoryTopicExist, basename='categories-topic-check')
# router.register(r'course-level-check', CourseCheckViewSet, basename='course-level-check')
# router.register(r'subject-course-check', SubjectCheckViewSet, basename='subject-course-check')
# router.register(r'module-subject-check', ModuleCheckViewSet, basename='module-subject-check')
router.register(r'courses-content', CourseViewSet,basename = 'courses-content')
router.register(r'holiday-batch', HollidayForBatch,basename="holiday-batch")
router.register(r'CombinedBatchPercentage', CombinedBatchPercentage,basename="CombinedBatchPercentage")
router.register(r'BatchTopicOrderChange', BatchTopicOrderChange,basename="BatchTopicOrderChange")
router.register(r'faculyblockedlist', facultyblockedlist,basename="faculyblockedlist")
router.register(r'facultyrejecteddlist', facultyrejecteddlist,basename="faculyblockedlist")
router.register(r'facultyonlinelist', facultyonlinelist,basename="facultyonlinelist")
router.register(r'facultyofflinelist', facultyofflinelist,basename="facultyofflinelist")
router.register(r'CourseExcelAdd', CourseExcelAdd,basename="CourseExcelAdd")
router.register(r'notverifiedfacultiylist', FacultyListNotVerified,basename="notverifiedfacultiylist")
router.register(r'verifiedfacultiylist', FacultyList,basename="verifiedfacultiylist")
router.register(r'branchcourse', BranchCourseList,basename="branchcourse")
router.register(r'branchcoursebylevel', BranchCourseListByLevel,basename="branchcourse")
router.register(r'branchcoursebycategory', BranchCourseListByCategory,basename="branchcourse")
router.register(r'subtopic-batch-viewset', SubtopicBatchViewset,basename="subtopic-batch-viewset")
router.register(r'order-change-branch', OrderChangeBranch,basename="subtopic-batch-viewset")
router.register(r'order-change-branch-topic', BranchTopicOrderChange,basename="subtopic-batch-viewset")
router.register(r'onlinelevel', OnlineLevelVIewset,basename="level-for-app")
router.register(r'onlinecategory', OnlineCategoryVIewset,basename="category-for-app")
router.register(r'onlinecourse', OnlineCourseVIewset,basename="category-for-app")
router.register(r'review-on-faculty-based-student', ReviewListOfStudentBasedFaculty,basename="reviewfacultybasedstudent")
router.register(r'review-questions-on-choice', RatingQuestionsByChoice,basename="reviewonchoice")
router.register(r'timetable-viewset', TimeTableModelViewset,basename="timetableviewset")
router.register(r'category-list-fac', facultyCategorylist,basename="facultyCategorylist")
router.register(r'course-category-list-fac', facultyCourseCategorylist,basename="facultyCourseCategorylist")
router.register(r'course-list-fac', facultyCourselist,basename="facultyCourselist")
router.register(r'subject-list-fac', facultySubjectlist,basename="facultySubjectlist")
router.register(r'module-list-fac', facultyModulelist,basename="facultyModulelist")
router.register(r'topic-list-fac', facultyTopiclist,basename="facultyTopiclist")
router.register(r'crud-course', CourseViewSetNew,basename="course-excel-pagination")
router.register(r'courses', CourseCreateModelView,basename="course-permission")
router.register(r'coursebycategory', CourseByCategoryViewSet,basename="course-bycategory")
router.register(r'matertial-course-list-new-drag', MaterialNewCoureselist,basename="course-bycategory")
router.register(r'review-answer-view', ReviewAnswersViewSet,basename="review-answer-view")
router.register(r'review-answer-faculty-alltimetable', ReviewAllTimeTableFacultyViewSet,basename="review-answer-faculty-alltimetable")
router.register(r'rafachk', RatingOnFacultyViewSet,basename="rafachk")
router.register(r'review-count',ReviewCountFacultyWiseViewSet,basename="review-count")
router.register(r'approval-list-admin',ApprovalModelViewset,basename="approval-list-admin")
router.register(r'level-list-salary',LevelForSalaryViewset,basename="level-list-salary")
router.register(r'class-room-viewset',ClassRoomViewsets,basename="class-room-viewset")

# history
router.register(r'history-branch',BranchHistoryView,basename="history-branch")
router.register(r'history-course',CourseHistory,basename="history-course")
router.register(r'history-subject',SubjectHistory,basename="history-subject")
router.register(r'history-subtopic',SubtopicHistory,basename="history-subtopic")
router.register(r'history-module',ModuleHistory,basename="history-module")
router.register(r'history-topic',TopicHistory,basename="history-topic")
router.register(r'history-faculty',FacultyHistory,basename="history-faculty")





#profile
router.register(r'profile',facultyprofile,basename='facultyprofile')
router.register(r'batchviewsetlist',BatchModelVieset,basename='batchviewsetlist')
router.register(r'faculty-limitation',FacultyLimitaionModelViewset,basename='faculty-limitation')
router.register(r'branchviewsetlist',BranchModelVieset,basename='branchviewsetlist')
router.register(r'approval-viewset',ApprovalModelviewset,basename='branchviewsetlist')
router.register(r'batch-crud',BatchModelViesetpatch,basename='batch-crud')
router.register(r'faculty-list-material',FacultyListMaterial,basename='faculty-list-material')
router.register(r'faculty-list-questions',FacultyListQuestions,basename='faculty-list-questions')

##permission add in level
router.register(r'level1',LevelListCreateViewsCopy, basename='create-level')
router.register(r'topic1',TopicCreateViewCopy, basename='create-level')
router.register(r'module1',ModuleCreateViewCopy, basename='create-level')
router.register(r'meterial-verified-fac-list',MeterialVerifiedFacultylist,basename="meterialverifiedfaclist")
router.register(r'timetable/attendance1', TimeTableAttendanceViewSetCopy, basename='faculty-attendance-on-timetable')
router.register(r'timetable1/',TimeTableViewSet,basename="timetablecopy")
router.register(r'faculty-history-view',FacultyHistoryViewSet,basename="facultyhistoryviewset")
router.register(r'subtopic-delete-batch',SubTopicBatchViewsetDelete,basename="subtopic-lis-delete-batch")
router.register(r'subject',SubjectCreation,basename="subject")
router.register(r'subtopic',SubtopicCreation,basename="subtopic")
router.register(r'module-creation',ModuleCreation,basename="module")
router.register(r'topic',TopicCreation,basename="topic")







urlpatterns = [
    path('', include(router.urls)),

#     path('create-branch/', BranchListCreateView, name='create-branch'),
    path('crud-branch/<int:pk>/',
         BranchRetrieveUpdateDestroyView.as_view(), name='crud-branch'),
    path('category/', CategoryListCreateView.as_view(), name='create-category'),
    path('crud-category/<int:pk>/',
         CategoryRetrieveUpdateDestroyView.as_view(), name='crud-category'),
    path('level/', LevelListCreateView.as_view(), name='create-level'),
    path('crud-level/<int:pk>/',
         LevelRetrieveUpdateDestroyView.as_view(), name='crud-level'),

#     path('courses/', CourseCreateView.as_view(), name='create-course'),
#     path('crud-course/<int:pk>/',
#          CourseRetrieveUpdateDestroyView.as_view(), name='crud-course'),
    path('batch/', BatchCreateView.as_view(), name='create-batch'),
    path('crud-batch/<int:pk>/',
         BatchRetrieveUpdateDestroyView.as_view(), name='crud-batch'),

#     path('subject/', SubjectCreateView.as_view(), name='create-subject'),

    path('crud-subject/<int:pk>/',
         SubjectRetrieveUpdateDestroyView.as_view(), name='crud-subject'),

#     path('module/', ModuleCreateView.as_view(), name='create-module'),

    path('crud-module/<int:pk>/',
         ModuleRetrieveUpdateDestroyView.as_view(), name='crud-topic'),

#     path('topic/', TopicCreateView.as_view(), name='create-topic'),

    path('crud-topic/<int:pk>/',
         TopicRetrieveUpdateDestroyView.as_view(), name='crud-topic'),

#     path('subtopic/', SubTopicCreateView.as_view(), name='create-topic'),

    path('crud-subtopic/<int:pk>/',
         SubTopicRetrieveUpdateDestroyView.as_view(), name='crud-subtopic'),
    path('classlevel/', CreateClassLevelView.as_view(), name='create-classlevel'),
    path('crud-classlevel/<int:pk>/',
         ClassLevelRetrieveUpdateDestroyView.as_view(), name='crud-classlevel'),
    path('getsubtopic/', getsubtopic, name='getsubtopic'),
    path('gettopic/', gettopic, name='gettopic'),
     path('gettopic/<int:id>/', gettopic, name='gettopic'),

    path('getmodule/', getmodule, name='getmodule'),
    path('getcourse/', getcourse, name='getcourse'),
    path('getbranch/', getbranch, name='getbranch'),
    path('getsubject/', getsubject, name='getsubject'),
    path('getbatch/', getbatch, name='getbatch'),


    path('getcategory/', getcategory, name='getcategory'),
    path('getlevel/', getlevel, name='getlevel'),
    path('level/<int:pk>/', LevelRetrieveUpdateDestroyView.as_view(), name="level-crud"),


    path('get/<id>/', getall, name='get'),
    path('getnew/<id>/', getallNew, name='getnew'),
    path('getcoursebatch/<id>/', getcourse_batch, name='getcourseofbatch'),
    path('timetable/', TimeTable_C.as_view(), name='time_table'),
    path('approve/', Approvals_c.as_view(), name='approve'),
    path('approve/<id>/', Approvals_c.as_view(), name='approve'),
    path('timetable-search/', TimeTableList.as_view(), name='timetable-search'),
    path('branches/<int:branch_id>/courses/',
         get_course_by_branch, name='get_course_by_branch'),
    path('topics/<int:topic_id>/subtopics/',
         get_subtopic_by_topic, name='get_subtopic_by_topic'),

    path('batches/<int:batch_id>/timetable/',
         get_timetable_by_batch, name='get_timetable_by_batch'),

    # path('approval/<int:timetable_id>/', get_faculty_timetablelist_by_each_class,
    #      name='get_faculty_timetablelist_by_each_class'),
    path('batches/<int:branch_id>/branches/',
         get_batch_in_branch, name='get_batch_in_branch'),

    path('fac-attendence-create/', FacultyAttendenceListCreateView.as_view(), name='fac-attendence-create'),
    path('fac-attendence-crud/<int:pk>/', FacultyAttendenceRetrieveUpdateDestroyView.as_view(), name='fac-attendence-crud'),
#     path('branches/<int:branch_id>/history/',
#          BranchHistoryView.as_view(), name='branch_history'),

     
     path('courses/<int:id>/history/',
         CourseHistoryView.as_view(), name='course_history'),

#     path('notverifiedfacultiylist/',
#          FacultyListNotVerified.as_view(), name='faculty_list'),
    path('batches/<int:branch_id>/branches/',
         get_batch_in_branch, name='get_batch_in_branch'),



    path('get/<id>/', getall, name='get'),
    path('getcoursebatch/<id>/', getcourse_batch, name='getcourseofbatch'),
    path('timetable/', TimeTable_C.as_view(), name='time_table'),
    path('approve/', Approvals_c.as_view(), name='approve'),
    path('approve/<id>/', Approvals_c.as_view(), name='approve'),
    path('timetable-search/', TimeTableList.as_view(), name='timetable-search'),
    path('branches/<int:branch_id>/courses/',
         get_course_by_branch, name='get_course_by_branch'),
    path('topics/<int:topic_id>/subtopics/',
         get_subtopic_by_topic, name='get_subtopic_by_topic'),

#     path('courses/', CourseCreateView.as_view(), name='create-course'),
    path('crud-course/<int:pk>/',
         CourseRetrieveUpdateDestroyView.as_view(), name='crud-course'),
    path('batch/', BatchCreateView.as_view(), name='create-batch'),
    path('crud-batch/<int:pk>/',
         BatchRetrieveUpdateDestroyView.as_view(), name='crud-batch'),
    path('subject/', SubjectCreateView.as_view(), name='create-subject'),
    path('crud-subject/<int:pk>/',
         SubjectRetrieveUpdateDestroyView.as_view(), name='crud-subject'),
    path('module/', ModuleCreateView.as_view(), name='create-module'),
    path('crud-module/<int:pk>/',
         ModuleRetrieveUpdateDestroyView.as_view(), name='crud-topic'),
    path('topic/', TopicCreateView.as_view(), name='create-topic'),
    path('crud-topic/<int:pk>/',
         TopicRetrieveUpdateDestroyView.as_view(), name='crud-topic'),
    path('subtopic/', SubTopicCreateView.as_view(), name='create-topic'),
    path('crud-subtopic/<int:pk>/',
         SubTopicRetrieveUpdateDestroyView.as_view(), name='crud-subtopic'),
    path('classlevel/', CreateClassLevelView.as_view(), name='create-classlevel'),
    path('crud-classlevel/<int:pk>/',
         ClassLevelRetrieveUpdateDestroyView.as_view(), name='crud-classlevel'),
    path('getsubtopic/', getsubtopic, name='getsubtopic'),
    path('gettopic/', gettopic, name='gettopic'),
    path('getmodule/', getmodule, name='getmodule'),
    path('getcourse/', getcourse, name='getcourse'),
    path('getbranch/', getbranch, name='getbranch'),
    path('getsubject/', getsubject, name='getsubject'),
    path('getbatch/', getbatch, name='getbatch'),
    path('get/<id>/', getall, name='get'),
    path('getcoursebatch/<id>/', getcourse_batch, name='getcourseofbatch'),
    path('timetable/', TimeTable_C.as_view(), name='time_table'),
    path('approve/', Approvals_c.as_view(), name='approve'),
    path('approve/<id>/', Approvals_c.as_view(), name='approve'),
    path('approvalsdetail/<id>/', Approval_c_p.as_view(), name='approve'),
    path('timetable-search/', TimeTableList.as_view(), name='timetable-search'),
    path('branches/<int:branch_id>/courses/',
         get_course_by_branch, name='get_course_by_branch'),
    path('topics/<int:topic_id>/subtopics/',
         get_subtopic_by_topic, name='get_subtopic_by_topic'),

    path('approval/<int:timetable_id>/', get_faculty_timetablelist_by_each_class,
         name='get_faculty_timetablelist_by_each_class'),
    path('batches/<int:branch_id>/branches/',
         get_batch_in_branch, name='get_batch_in_branch'),

    path('fac-attendence-create/', FacultyAttendenceListCreateView.as_view(), name='fac-attendence-create'),
    path('fac-attendence-crud/', FacultyAttendenceRetrieveUpdateDestroyView.as_view(), name='fac-attendence-crud'),
#     path('branches/<int:branch_id>/history/',
#          BranchHistoryView.as_view(), name='branch_history'),

    # path('fac-attendence-create/', FacultyAttendenceListCreateView.as_view(), name='fac-attendence-create'),
    # path('fac-attendence-crud/', FacultyAttendenceRetrieveUpdateDestroyView.as_view(), name='fac-attendence-crud'),
#     path('branches/<int:branch_id>/history/',
#          BranchHistoryView.as_view(), name='branch_history'),
#     path('notverifiedfacultiylist/',
#          FacultyListNotVerified.as_view(), name='faculty_list'),
    path('facblockandunblockfac/<int:fid>/', adminfacultyblockforverifiedfaculty.as_view(),
         name='adminfacultyblockforverifiedfaculty'),
#     path('faculyblockedlist/', facultyblockedlist.as_view(),
#          name='faucultyblocklit'),
#     path('facultyrejecteddlist/', facultyrejecteddlist.as_view(),
#          name='facultyrejecteddlist'),

    # faculty block with reason
    path('facultyblockwithreson/<int:id>/',
         faculyblockewdwithreason, name='faculyblockewdwithreason'),
    path('facultyrejectwithreson/<int:id>/',
         faculyrejectwithreason, name='faculyrejectwithreason'),

    path('batches/<int:branch_id>/branches/',
         get_batch_in_branch, name='get_batch_in_branch'),

    # path('verifiedfacultiylist/', FacultyList.as_view(), name='faculty_list'),
    # path('notverifiedfacultiylist/', FacultyListNotVerified.as_view(), name='faculty_list'),
    # path('batches/<int:branch_id>/branches/',get_batch_in_branch, name='get_batch_in_branch'),

    # faculty profile
    #     path('profile/<int:id>/',facultyprofile,name="faculty_profile"),
#     path('profile/<int:id>/', facultyprofile, name='faculty_profile'),
    path('profileedit/<pk>/', facultyupdateprofile.as_view(),
         name='edit faculty profile'),
    path('faculty_allappliedlist/<int:faculty_id>/',
         FacultyAppliedList.as_view()),
    path('faculty_allbookinglist/<int:faculty_id>/',
         Facultyallbookingdetils.as_view()),

    path('fac_topics/<int:id>/', FacultyTopics.as_view(), name='fac_topics'),




    path('order_change/', change_order, name='change_order'),


    path('examschedules/', ExamScheduleListCreateView.as_view(),
         name='examschedule-list'),
    path('examschedules/<int:pk>/',
         ExamScheduleRetrieveUpdateDestroyView.as_view(), name='examschedule-detail'),
    path('exam/<int:batch_id>/batch/', get_examschedule_by_batch,
         name='get_examschedule_by_batch'),
    path('examschedules/by-batch-and-branch/<int:batch_id>/<int:branch_id>/',
         get_examschedule_by_batch_and_branch, name='examschedule-by-batch-and-branch'),


    path('examschedules/', ExamScheduleListCreateView.as_view(),
         name='examschedule-list'),
    path('examschedules/<int:pk>/',
         ExamScheduleRetrieveUpdateDestroyView.as_view(), name='examschedule-detail'),
    path('exam/<int:batch_id>/batch/', get_examschedule_by_batch,
         name='get_examschedule_by_batch'),
    path('examschedules/by-batch-and-branch/<int:batch_id>/<int:branch_id>/',
         get_examschedule_by_batch_and_branch, name='examschedule-by-batch-and-branch'),
    path('getwhatyouwant/', getwhatyouwant, name='getwhatyouwant'),
    path('course/<int:level_id>/level/',
         get_course_by_level, name='get_course_by_level'),
    path('categories/<int:category_id>/courses/',
         CourseListByCategory.as_view(), name='course_list_by_category'),
    path('categories/', CategorySummaryList.as_view(), name='category_list'),
    path('levebycategory/<int:category_id>/',
         get_level_by_category, name="level_by_category"),
#     path('coursebycategory/<int:category_id>/',
#          get_course_by_category, name="course_by_category"),



    # create holidays
    path('createholidays/', CreateHolidays.as_view(), name='createholidays'),
    path('createholidays/<int:pk>/',
         CreateHolidays.as_view(), name='holiday-detail'),


    path('getclasslevel/', getclasslevel, name='getclasslevel'),
    path('subject/<int:course_id>/course/',
         subjectbycourse, name='subjectbycourse'),
    path('faculty_history/<int:faculty_id>/', FacultyHistoryView.as_view()),
     path('faculty_history/', FacultyHistoryAllView.as_view()),
     # path('faculty_history-with-date/<int:faculty_id>/', FacultyHistoryViewWithDate.as_view()),

    path('faculty_history-with-date/<int:faculty_id>/', FacultyHistoryViewWithDate, name='faculty_history_with_date'),

    path('module/<int:subject_id>/subject/',
         modulesbysubject, name='modulesbysubject'),
    path('topic/<int:module_id>/module/',
         topicsbymodule, name='topicsbymodule'),
    path('subtopics/', AllSubTopicsView.as_view(), name='all-subtopics'),

    # Status Change Active Inactive

    path('coursestatus/<int:id>/', statuschangecourse, name='coursestatus'),
    path('subjectstatus/<int:id>/', statuschangesubject, name='subjectstatus'),
    path('modulestatus/<int:id>/', statuschangemodule, name='modulestatus'),
    path('topicstatus/<int:id>/', statuschangetopic, name='topicstatus'),
    path('subtopicstatus/<int:id>/', statuschangesubtopic, name='subtopicstatus'),

    # End
    #     path('material-upload/', MaterialCreateAPIView.as_view(), name='material-upload'),
    #     path('materials/<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),

    path('batchcreate/', batchcreate, name='batchcreate'),

    path('timetable/<id>/', timetable_by_batch, name='timetable_by_batch'),
    path('batchtypes/', BatchTypeListCreateView.as_view(), name='batchtype-list'),
    path('batchtypes/<int:pk>/',
         BatchTypeRetrieveUpdateDestroyView.as_view(), name='batchtype-detail'),
    path('approvefaculty/<int:id>/',
         approve_faculty_timetable, name='approvefaculty'),
    path('addfaculty/<int:id>/<int:pk>/',
         add_faculty_timetable, name='addfaculty'),
    path('getsubjectonbatch/<int:id>/', get_subject_batch, name='get_subject'),

    path('ratings/', RatingListCreateView.as_view(), name='rating-list'),
    path('ratings/<int:pk>/', RatingRetrieveUpdateDestroyView.as_view(),
         name='rating-detail'),
    path('faculty/<int:faculty_id>/rating/',
         FacultyRatingView.as_view(), name='faculty_rating'),
    path('batchtype/', BatchTypeCreateView.as_view(), name='batchtype'),
    path('crud-batchtype/<int:pk>/',
         BatchTypeRetrieveUpdateDestroyView.as_view(), name='crud-batchtype'),
    path('getbatchtype/', batch_type_list, name='getbatchtype'),
    path('get-topic-by-order/<int:pk>/',
         TopicOrderGet.as_view({'get': 'list', 'patch': 'edit','post':'create'}), name='gettopicbyorder'),
    path('branch-courses/<int:pk>/',
         BranchCoursesView.as_view({'get': 'list'}), name='branch-courses'),
    path('batch-topic-list/<int:pk>/',
         BatchTopicListView.as_view({'get': 'list'}), name='batch-topic-list'),
     path('branch-courses-view/', BranchCourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='branch-course-list'),
     # path('branch-courses-view/<int:pk>/', BranchCourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='branch-course-detail'),
     # path('branch-courses-viewset/', CourseBranchViewSet.as_view({'get': 'list'}), name='branch-course-list'),
     path('branch-courses-viewset/<int:branch_id>/<int:course_id>/', CourseBranchViewSet.as_view({'delete': 'destroy'}), name='branch-course-detail'),
     path('branch-courses-det/<int:branch_id>/<int:course_id>/', crud_course_branch, name='branch-course-detail'),
     path('branch-courses-viewset/<int:branch_id>/', CourseBranchViewSet.as_view({'patch': 'partial_update'}), name='branch-course-detail'),
     path('topic-schedule-batch/<int:pk>/', TopicScheduleGet.as_view({'get': 'list'}), name='topic-schedule-batch'),
     path('faculty_availablity/<int:pk>/<date>/', FacultyAvailablity.as_view({'get': 'list'}), name='topic-schedule-batch'),
     path('schedule-auto-pending/<int:batch_id>/', AutoTimeSchedule.as_view({'post': 'create'}), name='schedule-remaining-timetable'),
     path('timetable/<int:timetable_id>/subtopics/', sutopic_based_on_timetable, name='subtopics'),
     path('subtopic_batch/<int:pk>/update_status/', FacultyAttendenceSubtopicBatchViewSet.as_view({'patch': 'partial_update'})),
     path('branch-admin-signup/',branchAdminSignup, name='branch-admin-signup'),
     path('categories-topic-check/', CategoryTopicExist.as_view({'get': 'list'}), name='category_topic_exist'),
     path('course-topic-check/<int:id>/', CourseTopicExist.as_view({'get': 'list'}), name='course_topic_exist'),
     path('subject-topic-check/<int:id>/', SubjectTopicExist.as_view({'get': 'list'}), name='subject_topic_exist'),
     path('module-topic-check/<int:id>/', ModuleTopicExist.as_view({'get': 'list'}), name='module_topic_exist'),
     path('level-topic-check/<int:id>/', LevelTopicExist.as_view({'get': 'list'}), name='level_topic_exist'),
     # path('categories-topic-check/<int:id>/', CategoryIdTopicExist.as_view({'get': 'list'}), name='category_topic_exist-id'),
#     path('deletefixdb',deletebugfix,name='bugfix-delete'),
#     path('deletefixdb2',deletebugfix2,name='bugfix-delete')
     path('get-batch-course/<int:id>/',getallNewBatch, name='get-batch-course'),
     path('get-material-course/',getallNewMaterial, name='get-batch-course'),
     path('get-calander/<int:id>/<int:month>/<int:year>/',getcalender_batch, name='get-calander')

]
