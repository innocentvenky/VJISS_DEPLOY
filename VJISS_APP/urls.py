from django.urls import path
from .views import Create_Users,Login
from .views import AddCourse
from .views import Course_details,Course_modify,Course_delete,Update_Password,Users_details, Course_particular_details
from .views import AddSyllabus,SyllabusModify,SyllabusDelete,Syllabus_details
from .views import InternshipOffers_modify,InternshipOffers_delete, AddInternshipOffers,InternshipOffers_details  
from .views import InternshipApplication,ViewApplications,ModifyApplication,DeleteApplication
from .views import AddJobNotification,JobNotificationDetails,JobNotificationModify,JobNotificationDelete
from .views import AddTrainers,TrainersDetails,TrainersModify,TrainersDelete
from .views import AddCompanyInfo,CompanyInfoDetails,CompanyInfoModify,CompanyInfoDelete
from . mail_services.opt import SendOtp
from . views import NewBacthAdding,BacthDetails,BatchUpdate,Batchdelete
from . views import StudentEnrollmentView,StudentEnrollment,StudentEnrollmentModify,StudentEnrollmentDelete
from . views import BatchEnrollment,BatchEnrollmentView,BatchEnrollmentModify,BatchEnrollmentDelete


from . import views

# endpoints URLS
urlpatterns=[
    path("VJISS/create_user/",Create_Users.as_view()),
    path("VJISS/users_details/",Users_details.as_view()),
    path('VJISS/send-otp/', SendOtp.as_view()),
    path("VJISS/update_password/",Update_Password.as_view()),
    path("VJISS/login/",Login.as_view()),


    path("VJISS/add_course/",AddCourse.as_view()),
    path("VJISS/course_particular_details/<str:pk>",Course_particular_details.as_view()),
    path("VJISS/course_details/",Course_details.as_view()),
    path("VJISS/modify_course/<str:pk>",Course_modify.as_view()),
    path("VJISS/delete_course/<str:pk>",Course_delete.as_view()),


    path("VJISS/add_syllabus/",AddSyllabus.as_view()),
    path("VJISS/syllabus_details/",Syllabus_details.as_view()),
    path("VJISS/modify_syllabus/<str:pk>",SyllabusModify.as_view()),
    path("VJISS/delete_syllabus/<str:pk>",SyllabusDelete.as_view()),


    path("VJISS/add_internship_offers/",AddInternshipOffers.as_view()),
    path("VJISS/internship_offers_details/",InternshipOffers_details.as_view()),
    path("VJISS/modify_internship_offers/<str:pk>",InternshipOffers_modify.as_view()),
    path("VJISS/delete_internship_offers/<str:pk>",InternshipOffers_delete.as_view()),


    path("VJISS/apply_internship/",InternshipApplication.as_view()),
    path("VJISS/view_applications/",ViewApplications.as_view()),
    path("VJISS/modify_application/<str:pk>",ModifyApplication.as_view()),
    path("VJISS/delete_application/<str:pk>",DeleteApplication.as_view()),


    path("VJISS/add_job_notification/",AddJobNotification.as_view()),
    path("VJISS/job_notification_details/",JobNotificationDetails.as_view()),
    path("VJISS/modify_job_notification/<str:pk>",JobNotificationModify.as_view()),
    path("VJISS/delete_job_notification/<str:pk>",JobNotificationDelete.as_view()),


    path("VJISS/add_trainer/",AddTrainers.as_view()),
    path("VJISS/trainer_details/",TrainersDetails.as_view()),
    path("VJISS/modify_trainer/<str:pk>",TrainersModify.as_view()),
    path("VJISS/delete_trainer/<str:pk>",TrainersDelete.as_view()),


    path("VJISS/add_company_info/",AddCompanyInfo.as_view()),
    path("VJISS/company_info_details/",CompanyInfoDetails.as_view()),
    path("VJISS/modify_company_info/<str:pk>",CompanyInfoModify.as_view()),
    path("VJISS/delete_company_info/<str:pk>",CompanyInfoDelete.as_view()),

    path("VJISS/newbatch/",NewBacthAdding.as_view()),
    path("VJISS/batch_details/",BacthDetails.as_view()),
    path("VJISS/update_batch/<str:pk>",BatchUpdate.as_view()),
    path("VJISS/delete_batch/<str:pk>",Batchdelete.as_view()),


    path("VJISS/student_enrollment/",StudentEnrollment.as_view()),
    path("VJISS/student_enrollment_details/",StudentEnrollmentView.as_view()),
    path("VJISS/modify_student_enrollment/<str:pk>",StudentEnrollmentModify.as_view()),
    path("VJISS/delete_student_enrollment/<str:pk>",StudentEnrollmentDelete.as_view()),

    path("VJISS/batch_enrollment/",BatchEnrollment.as_view()),
    path("VJISS/batch_enrollment_details/",BatchEnrollmentView.as_view()),
    path("VJISS/modify_batch_enrollment/<str:pk>",BatchEnrollmentModify.as_view()),
    path("VJISS/delete_batch_enrollment/<str:pk>",BatchEnrollmentDelete.as_view()),





]

        