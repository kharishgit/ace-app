from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()


router.register(r'quiz-pool', QuizPoolViewset, basename='QuizPoolViewset')
router.register(r'dailynews', DailyNewsViewset, basename='daily-news')
router.register(r'dailynews-viewonly', DailyNewsViewOnlyset, basename='daily-news-viewonly')

router.register(r'quiz-pool-user', QuizPoolAppView, basename='QuizPoolViewset')
router.register(r'quiz-pool-question', QuestionViewset, basename='QuestionViewset')
router.register(r'user-publication', PublicationsListViewset, basename='PublicationViewset')
router.register(r'success-stories', SuccessStoriesViewSet, basename='sucess-stories')
router.register(r'popular-faculty', PopularFacultyListView, basename='popular-faculty')
router.register(r'feedback-faculty-on-timetable', FeedBackForFacultyViewSet, basename='feedback-timetable')
router.register(r'banner-upload', BannerAddViewSet, basename='banner-upload')
router.register(r'feedback-all', FacultyBasedFeedBack, basename='feedback-all')
router.register(r'study-metrial-purchase', StudyMetrialPurchase, basename='study-metrial-purchase')
router.register(r'question-book-purchase', QuestionBookPurchase, basename='question-book-purchase')
# router.register(r'faculty-course-addition', CourseAppList, basename='CourseAppList')
router.register(r'shorts', ShortsViewSet, basename='shorts')
router.register(r'shorts-watched', ShortsWatchedViewset, basename='shortswatched')
router.register(r'question-category', QuestionCategoryViewSet, basename='question-category')

router.register(r'faculty-dashboard', FacultyDashboarViewset, basename='faculty-dashboard')
router.register(r'quiz-first-api', AppStudentQuiz, basename='quiz-first-api')
router.register(r'quiz-start-api', AppStudentStartQuiz, basename='quiz-start-api')
router.register(r'quiz-submit-answer-api', AppStudentSubmitAnswerQuiz, basename='quiz-start-api')
router.register(r'batch-packages', BatchPackagesViewSet, basename='batch-packages')
router.register(r'books-type', BookTypeViewSet, basename='typebooks')
router.register(r'library-books', LibraryBooksViewSet, basename='librarybooks')
router.register(r'batch-packages-get', BatchPackagesOnId, basename='batch-packages-get')
router.register(r'package-batches-on-branches', BatchPackagesOnBranchId, basename='package-batches-on-branches')
router.register(r'user-cart', CartItemViewset, basename='user-cart')
router.register(r'offline-student-batch', StudentBatchDetailsViewset, basename='offline-student-batch')
router.register(r'general-videos-admin', GeneralVideosViewset, basename='general-videos-admin')
router.register(r'general-videos-category-admin', GeneralVideosCategoryViewset, basename='general-videos-category-admin')
router.register(r'general-videos-user', GeneralVideosUserViewset, basename='general-videos-user')
router.register(r'general-videos-category-user', GeneralVideosCategoryUserViewset, basename='general-videos-category-user')
# router.register(r'offline-student-timetable', StudentBatchDetailsViewset, basename='offline-student-batch')
router.register(r'library-user', LibraryUserViewSet, basename='libraryuser')
router.register(r'book-lend', BookLendViewSet, basename='book-lend')
router.register(r'recent-course', RecentCourseViewset, basename='recent-course')
router.register(r'story-category', StoriesCategoryViewSet, basename='stories-category')
router.register(r'stories', StoriesViewSet, basename='stories')
router.register(r'comments', CommentsViewset, basename='comments')
router.register(r'likes', LikesViewset, basename='likes')
router.register(r'story-category-all-unwatched', StoriesAllCategoryViewSet, basename='story-category-all-unwatched')
router.register(r'story-watched', StoriesWatchedViewset, basename='story-watched')
router.register(r'ca-question', CurrentAffairsQuestionViewSet, basename='ca-questions')
router.register(r'ca-test', CurrentAffairsQuestionsDaySortedViewSet, basename='ca-test')
router.register(r'ca-video-create', CurrentAffairsVideosViewSet, basename='ca-video-create')
router.register(r'ca-video-view', CurrentAffairsVideosDaySortedViewSet, basename='ca-video-view')
router.register(r'ca-video-assaign', CurrentAffairsVideosAssaignViewSet, basename='ca-video-assign')
router.register(r'stories-app', StoriesUserAllCategoryViewSet, basename='stories-app')
router.register(r'daily-exam', DailyExamViewSet, basename='daily-exam')
router.register(r'daily-exam-app', DailyExamsAppView, basename='daily-exam-app')
router.register(r'general-video-material', GeneralVideosMaterialViewset, basename='general-video-material')
router.register(r'previous-exam-admin', PreviousExamViewSet, basename='previous-exam-admin')
router.register(r'previous-exam-app', PreviousExamsAppView, basename='previous-exam-app')
router.register(r'popular-fac', PopularFacultyEntryViewSet, basename='popular-fac')
router.register(r'views-user', Viewviewset, basename='views-user')
router.register(r'teachers-pouplar', PopularFacultyViewSet, basename='techers-popular')
router.register(r'scholarship-type', ScholarshipTypeViewset, basename='scholarship-type')
router.register(r'popular-faculty-admin-get', PopularFacultyEntryAdminGETViewSet, basename='popular-faculty-admin-get')
router.register(r'faculty-on-course', FacultyOnCourseViewSet, basename='faculty-on-course')
router.register(r'popularfaculty-on-course', PopularFacultyOnCourseGETViewSet, basename='popularfaculty-on-course')
router.register(r'course-popularfaculty', AvailableCoursesOnPopularFaculty, basename='course-popularfaculty')
router.register(r'scholarship-approval', ScholarshipApprovalViewSet, basename='scholarship-approval')
router.register(r'scholarship-type-wo-pagi', ScholarshipTypeViewsetReadOnly, basename='scholarship-type-wo-pagi')

router.register(r'students-wo-scholarship', StudentlistForScholarship, basename='student-wo-scholarship')
router.register(r'pollfight-submit-answer', PollFightSubmitViewSet, basename='pollfight-submit-answer')
router.register(r'pollfight-question-admin', PollFightQuestionViewset, basename='pollfight-question-admin')
router.register(r'pollfight-user-question', PollFightSubmitUserViewset, basename='pollfight-user-question')
router.register(r'new-faculty-timetable', NewFacultyTimeTable, basename='new-faculty-timetable')
router.register(r'chat-viewset', ChatViewset, basename='chat-viewset')
router.register(r'group-user-viewset', GroupsUserViewsSet, basename='group-user-viewset')
router.register(r'group-admin-viewset', GroupsViewsSet, basename='group-admin-viewset')
router.register(r'group-admin-userlist-viewset', GroupWiseUserList, basename='group-admin-userlist-viewset')

router.register(r'student-fee-collection', StudentFeeCollectionViewSet, basename='student-fee-collection')
router.register(r'studentfee-afteradmission',StudentFeeAfterAdmission,basename = 'studentfee-afteradmission')
router.register(r'studentsyllabus-list',StudentSyllabusViewSet,basename = 'studentsyllabus-list')

router.register(r'student-attendance', StudentAttendanceViewset, basename='student-attendance')
router.register(r'student-attendance-user', StudentAttendanceViewsetUser, basename='student-attendance-user')

router.register(r'faculty-feedback', FacultyFeedBackOnTimeTableViewSet, basename='faculty-feedback')

router.register(r'student-publication-additions', StudentPublicationUpdateViewSet, basename='student-publication-additions')
router.register(r'read-book', ReadBookTypeViewSet, basename='read-book')
router.register(r'daily-class',DailyClassViewsets,basename='daily-class')
router.register(r'noticeboard-admin',NoticeBoardAdminViewset,basename='noticeboard-admin')
router.register(r'noticeboard-user',NoticeBoardUserViewset,basename='noticeboard-user')
router.register(r'videoclass-admin',VideoClassesBatchViewset,basename='videoclass-admin')
router.register(r'videoclass-user',VideoClassesBatchUserViewset,basename='videoclass-user')

router.register(r'studnet_appdeatils',StudnetDetaiApplView,basename='studnet_appdeatils')
router.register(r'student_transaction_View',StudentTransactionAppView,basename = 'student_transaction_View')

router.register(r'book-fine-libray', LibraryFineViewSet, basename='book-fine')
router.register(r'books-in-branch', BooksinBranch, basename='book-in-branch')

router.register(r'library-user-notexists', UserNotInLibraryUserViewSet, basename='library-user-notexists')
router.register(r'chat-upvotes-user', UpVotesViewset, basename='chat-upvotes-user')
router.register(r'subject-list-batch', SubjectBatchViewset, basename='subject-list-batch')

# live class
router.register(r'live-zoomclass',liveZoomclassViewset,basename = 'live-zoomclass')
router.register(r'liveZoom-App',liveZoomAppViewset,basename='liveZoom-App')


router.register(r'videoReport-Admin',VideoReportViewset,basename = 'videoReport-Admin')
router.register(r'videoReport-user',VideoReportUserViewset,basename='videoReport-user')

# history
router.register(r'history-dailynews',DailyNewsHistory,basename='history-dailynews')
router.register(r'history-quizpool',QuestionPoolHistory,basename='history-quizpool')
router.register(r'history-success',SuccessStoriesHistory,basename='history-success')
router.register(r'history-banner',MobileBannerHistory,basename='history-banner')
router.register(r'history-questioncategory',QuestionCategoryHistory,basename='history-questioncategory')
router.register(r'history-questionbook',QuestionBookHistory,basename='history-questionbook')
router.register(r'history-studymaterial',StudyMaterialHistory,basename='history-studymaterial')
router.register(r'history-batchpackages',BatchPackagesHistory,basename='history-batchpackages')
router.register(r'history-shorts',ShortsHistory,basename='history-shorts')
router.register(r'history-generalvideo',GeneralVideoHistory,basename='history-generalvideo')


#video packages
router.register('video-package-materials',PackageMaterialsViewset,basename='PackageMaterialsViewset')
router.register('video-material-and-questions',VedioMeterialAndQuestionsViewset,basename='VedioMeterialAndQuestionsViewset')
router.register('video-package-admin',VedioPackageViewset,basename='VedioMeterialAndQuestionsViewset')
router.register('video-package',ReadonlyVideopPckage,basename='VedioMeterialAndQuestionsViewset')
router.register(r'verified-faculty-list-video-package', FacultyListforvideopackage,basename="verifiedfacultiylist")
router.register('video-package-purchase',VideoPackagePurchase,basename='VideoPackagePurchase')
router.register('video-package-dashboard',ReadonlyVideopPckageDashboard,basename="ReadonlyVideopPckage")
router.register('video-package-viewdetails',VideoPackageViewdetails,basename='VideoPackageViewdetails')
router.register('video-package-full-detials',VideoPackagefullDetils,basename="VideoPackagefullDetils")
#examp paper package
router.register('exam-package-before-purchase',Exampackagebeforepurchase,basename="Exampackagebeforepurchase")
router.register('exam-package-view-details',ExampackageviewsDetials,basename="exampackageviewdetials")
router.register('exam-paper-package',ReadOnlyExampaperpackageViewset,basename='Exampaperpackagefrontend')
router.register('exam-paper-packages',ExampaperpackageViewset,basename='Exampaperpackagebackend')
router.register('purcahse-exam-package',PurchaseExamPackages,basename="PurchasePackages")
#special exam practice
router.register('special-exam-practise',SpecialExamsViewset,basename='SpecialExamsviewset')
#attend
router.register('questionpaper-attend',QuestionPaperAttend,basename='questionpaperattend')
#purchase video/exampaper quiz
router.register('purchase-quiz-instructions',PurchaseQuizInstructions,basename='PurchaseQuizInstructions')
router.register('start-purchasequiz',StartPurchaseQuiz,basename='StartPurchaseQuiz')
router.register('question-get',QuestionGetinQuiz,basename="QuestionGetinQuiz")
router.register('quiz-complete',PurchaseQuizComplete,basename='PurchaseQuiz')
router.register('questionpaper-instructions',PurchaseQuizInstructions,basename='PurchaseQuizInstructions')
router.register('answer-keys',AnswerKeysPurchaseQuiz,basename="AnswerKeys")
router.register('leader-Board',LeaderBoardApi,basename="LeaderBoard")


#onlilne purchase course
router.register('course-package',CoursePackage,basename="coursepackage")
router.register('day-wise-online-course',DayWiseOnlineCourse,basename="DaywiseOnlineCourse")
router.register('purchase-course-package',PurchaseCoursepackage,basename="purchasecoursepackage")

#offline exams
router.register('exam-category-viewset',ExamCategoryViewset,basename="Examcategorycreation")
router.register('exam-question-paper-viewset',ExamQuestionPaperViewset,basename="ExamQuestionPaperViewset")
router.register("offline-exam-based-on-course",OfflineExamlist,basename="OfflineExamlistbasedonCourse")











urlpatterns = [
    path('', include(router.urls)),
    path('faculty-course-addition/',CourseAppList,name='CourseAppList'),
    path('stream_vimeo_video/<int:id>/',stream_vimeo_video,name='stream_vimeo_video'),
    path('stream_img_s3/<int:id>/',stream_s3_image,name='stream_vimeo_video'),
    path('getsocket/',get_socket,name='getsocket'),
    path('get_lobby/',get_lobby,name='get_lobby'),
    path('get_lobby_user/',get_lobby_user,name='get_lobby_user'),
    path('faculty-dashboard-timetable/',get_faculty_dashboard,name='get_faculty_dashboard'),
    path('poll-fight-submit/<int:id>/',poll_fight_submit,name='poll-fight-submit'),
    
]