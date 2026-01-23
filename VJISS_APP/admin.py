from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Create_User, Courses_Model, Syllabus_Model
from .models import InternshipOffers
from . models import Apply_Internship
from . models import Job_Notifications  
from . models import About_Trainers
from . models import About_Company
from . models import NewBatchs

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Create_User
from . models import Student_Enrollment


@admin.register(Create_User)
class CustomUserAdmin(UserAdmin):
    model = Create_User

    list_display = [
        'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'is_active'
    ]
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    # EDIT USER PAGE
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'gender',
                'date_of_birth',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    # ADD USER PAGE
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'gender',
                    'date_of_birth',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_superuser',
                    'is_active',
                ),
            },
        ),
    )

class CourseAdmin(admin.ModelAdmin):
    list_display=['course_name','course_fee','course_level','course_duration',]

admin.site.register(Courses_Model,CourseAdmin)

class SyllabusAdmin(admin.ModelAdmin):
    list_display=['course_id','module','description']
admin.site.register(Syllabus_Model,SyllabusAdmin)

class InternshipOffersAdmin(admin.ModelAdmin):
    list_display=['internship_name','internship_description','technologies'] 
admin.site.register(InternshipOffers,InternshipOffersAdmin)

class Apply_InternshipAdmin(admin.ModelAdmin):
    list_display=['get_first_name','get_last_name','get_email','get_phone_number','get_internship_name','education','resume','applied_on','status','reason'] 
    def get_first_name(self, obj):
        return obj.student.first_name   
    def get_last_name(self, obj):
        return obj.student.last_name
    def get_email(self, obj):
        return obj.student.email
    def get_phone_number(self, obj):
        return obj.student.phone_number
    def get_internship_name(self, obj):
        return obj.internship_offers.internship_name
        
admin.site.register(Apply_Internship,Apply_InternshipAdmin)

class Job_NotificationsAdmin(admin.ModelAdmin):
    list_display=['job_title','company_logo','company_posted_date','posted_date','company_name','location','job_description','requirements','link'] 
admin.site.register(Job_Notifications,Job_NotificationsAdmin)

class About_TrainersAdmin(admin.ModelAdmin):
    list_display=['trainer_title','trainer_name','trainer_image','trainer_bio']  
admin.site.register(About_Trainers,About_TrainersAdmin)


class About_CompanyAdmin(admin.ModelAdmin):
    list_display=['company_id','company_name','company_logo','company_description']
admin.site.register(About_Company,About_CompanyAdmin)

class NewBatchAdmin(admin.ModelAdmin):
    list_display=['get_course_name','get_faculty_name','batch_id','start_date','end_date','timing','batch_type','status']
    def get_course_name(self, obj):
        return obj.course.course_name
    def get_faculty_name(self, obj):
        return obj.faculty.trainer_name
admin.site.register(NewBatchs,NewBatchAdmin)
class Student_EnrollmentAdmin(admin.ModelAdmin):
    list_display=['student_name','course_name','enrollment_date', 'status','phone_number','email']
    def student_name(self, obj):
        return obj.student.first_name + ' ' + obj.student.last_name
    def phone_number(self, obj):
        return obj.student.phone_number
    def email(self,obj):
        return obj.student.email
    def course_name(self, obj):
        return obj.course.course_name
admin.site.register(Student_Enrollment,Student_EnrollmentAdmin)