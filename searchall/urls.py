from django.urls import path
from django.conf.urls import include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter
# from views import CoursePdf


router = DefaultRouter(trailing_slash=True)
router.register(r'generate-pdf', GeneratePdfViewset, basename='gen-pdf')
# router.register(r'special-holidays', SpecialHolidayViewSet)

urlpatterns = [
    path('', include(router.urls)),

    #accoutn app tabels pagintion,searhing and ordering
    path('courseslist/', views.CoursePagination.as_view(), name='coursesoagination'),
    path('subjectsslist/',views.SubjectPagination.as_view(),name='subjectpagination'),
    path('moduleslist/',views.ModulePagination.as_view(),name='modulepagination'),
    path('topicslist/',views.TopicPagination.as_view(),name='topicpagination'),
    path('subtopicslist/',views.SubtopicPagination.as_view(),name='subtopicpagination'),
    path('batchlist/',views.BatchPagination.as_view(),name='batchpagination'),
    path('branchlist/',views.BranchPagination.as_view(),name='branchpagination'),
    # path('branchadminlist/',views.BranchadminPagination.as_view(),name='brachadminpagination'),
    path('superadminlist/',views.SuperadminPagination.as_view(),name='SuperadminPagination'),
    path('serachfacultylist/',views.FacultyListView.as_view(),name='SuperadminPagination'),
    # path('serachfacultylistss/',views.FacultyListViewss.as_view(),name='SuperadminPagination'),


    #course table data to excel
    # path('export_to_excel/', views.export_data_to_excel, name='export_to_excel'),
    # path('export/courses/', views.export_COURSE_to_excel, name='export_courses'),
    # path('export/batches/', views.export_BATCH_to_excel, name='export_batches'),
    # path('export/subjects/', views.export_SUBJECT_to_excel, name='export_subject_to_excel'),
    # path('export/module/', views.export_MODULE_to_excel, name='export_module_to_excel'),
    # path('export/topic/', views.export_TOPIC_to_excel, name='export_topic_to_excel'),
    # path('export/subtopic/', views.export_SUBTOPIC_to_excel, name='export_subtopic_to_excel'),
    # path('export/branch/', views.export_BRANCH_to_excel, name='export_subtopic_to_excel'),
    # # path('export/branch/', views.export_BRANCHADMIN_to_excel, name='export_subtopic_to_excel'),
    # path('export/branch/', views.export_SUPERADMIN_to_excel, name='export_subtopic_to_excel'),
    # path('export/faculty/', views.export_FACAULTY_to_excel, name='export_subtopic_to_excel'),

    #common url of this one
    path('export/<str:resource_class>/',views. export_to_excel, name='export_to_excel'),




    # path('courses/pdf/', views.CoursePdf.as_view(), name='course_pdf'),
    path('courses/pdf/', views.export_courses_pdf, name='courses_pdf'),
    path('batches/pdf/', views.export_batch_pdf, name='courses_pdf'),
    path('subject/pdf/', views.export_subject_pdf, name='courses_pdf'),
    path('module/pdf/', views.export_MODULE_pdf, name='module_pdf'),
    path('topic/pdf/', views.export_TOPIC_pdf, name='module_pdf'),
    path('subtopic/pdf/', views.export_SUBTOPIC_pdf, name='module_pdf'),
    path('branch/pdf/', views.export_BRANCH_pdf, name='module_pdf'),
    # path('branchAdmin/pdf/', views.export_BRANCHADMIN_pdf, name='module_pdf'),
    path('superAdmin/pdf/', views.export_SUPERADMIN_pdf, name='module_pdf'),
    #common url of  pdf file
    path('common/<str:model_name>/', views.common_pdf_formate, name='common colour pdf'),
    #anoopsir pdf
    # path('all-courses-pdf/', views.generate_course_pdf, name='all_courses_pdf'),

    path('commonss/<str:model_name>/', views.common_pdf_formate, name='common colour pdf'),
    path('convert_to_excel/', convert_to_excel, name='convert_to_excel'),

    path('table_to_pdf/<str:model_name>/', views.table_to_pdf, name='table_to_pdf'),

    path('export-blocked-faculties/', export_blocked_faculties_to_excel),
    path('export-rejected-faculties/', export_rejected_faculties_to_excel),
    path('export-active-faculties/', export_active_faculties_to_excel),
    path('export-applied-faculties/', export_applied_faculties_to_excel),
    path('export-holiday-list/', export_holiday_list),
    path('courses/<int:course_id>/excel/', views.generate_excel_for_course, name='generate_excel_for_course'),
    path('export-excel-query/', export_to_excel),
    path('export-pdf-query/', export_to_pdf),
    path('export-inhouse-faculty/',export_inhouse_faculties_to_excel),
    path('export-offline-faculty/',export_offline_faculties_to_excel),
    path('export-online-faculty/',export_online_faculties_to_excel),









]
# from django.urls import path
# from .views import export_data_to_excel
# # export_data_to_pdf

# urlpatterns = [
#     path('export_to_excel/', export_data_to_excel, name='export_to_excel'),
#     # path('export_to_pdf/', export_data_to_pdf, name='export_to_pdf'),
# ]
