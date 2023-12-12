from django.contrib import admin
from .models import  User,Faculty,Role,Permissions,Material,Experience,FacultyCourseAddition,QuestionPool,Question,NewQuestionPool,QuestionPaper
from .models import *
# Register your models here.
# class AdminQuestionPool(admin.ModelAdmin):
#     list_display=['facultys','categorys','levels','course','topic','file_type','type','questions']
class AdminQuestionPool(admin.ModelAdmin):
    list_display = ['facultys', 'categorys', 'levels', 'course','subject','topic', 'type', 'questions','publish']

    def questions(self, obj):
        return ', '.join([question.question_text for question in obj.questions.all()])

    questions.short_description = 'Questions'

class AdminNewQuestionPool(admin.ModelAdmin):
    list_display=['user','categorys','levels','topic','question_text','status','publish']

class AdminIncentive(admin.ModelAdmin):
    list_display=['name','rate','conditions','target_mandatory','status']

class AdminStaffIncentives(admin.ModelAdmin):
    list_display=['staff','status']

class AdminStaffSalary(admin.ModelAdmin):
    list_display=['staff','payment_status','paid_amount','payment_method','testimonial','current_salary','salary_date','advance_payment','status']

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Role)
admin.site.register(Permissions)
admin.site.register(Material)
admin.site.register(Experience)
# admin.site.register(QuestionPool,AdminQuestionPool)
admin.site.register(FacultyCourseAddition)
# admin.site.register(Question)
admin.site.register(SalaryFixation)
admin.site.register(Declaration)

#faculty reject
# admin.site.register(Users_Reject)
# admin.site.register(Faculty_Reject)
# admin.site.register(FacultyCourseAddition_Reject)
# admin.site.register(Experience_Reject)
admin.site.register(Faculty_Salary)
admin.site.register(NewQuestionPool,AdminNewQuestionPool)
admin.site.register(QuestionPaper)
admin.site.register(StudioCourse)
admin.site.register(StudioVideo)
admin.site.register(StudioNames)
admin.site.register(FacultyStudioApplication)
admin.site.register(StudioCourseAssign)
admin.site.register(MaterialUploads)
admin.site.register(MaterialReference)
admin.site.register(ConvertedMaterials)
admin.site.register(MaterialRating)
admin.site.register(OnlineSalary)
admin.site.register(Question)
admin.site.register(Incentives,AdminIncentive)
admin.site.register(StaffIncentives,AdminStaffIncentives)
admin.site.register(StaffSalary,AdminStaffSalary)
admin.site.register(StaffIncentiveAmount)




