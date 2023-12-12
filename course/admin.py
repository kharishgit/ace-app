from django.contrib import admin
from .views import *


class Topic_batchAdmin(admin.ModelAdmin):
    model = Topic_batch
    list_display = ('batch', 'module', 'description',
                    'name', 'topic', 'status')
    # readonly_fields=('last_login','joined_date','password')
    # ordering=('joined_date',)


class adminhoidays(admin.ModelAdmin):
    model = Holidays
    list_display = ('date', 'name')


# Register your models here.
admin.site.register(Category)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Batch)
admin.site.register(TimeTable)
admin.site.register(Approvals)
admin.site.register(Course_batch)
admin.site.register(Subject_batch)
admin.site.register(Module_batch)
admin.site.register(Topic_batch, Topic_batchAdmin)
admin.site.register(Subtopic_batch)
admin.site.register(ExamSchedule)
admin.site.register(Level)
admin.site.register(ClassLevel)
admin.site.register(FacultyAttendence)
admin.site.register(Course_branch)
admin.site.register(Branch_courses)
admin.site.register(Holidays, adminhoidays)
admin.site.register(BatchType)
admin.site.register(Rating)
admin.site.register(Subject_branch)
admin.site.register(Subtopic_branch)
admin.site.register(Module_branch)
admin.site.register(Topic_branch)
admin.site.register(SpecialHoliday)
admin.site.register(Review)
admin.site.register(ReviewQuestions)
admin.site.register(FacultyLimitaion)
admin.site.register(ClassRooms)

