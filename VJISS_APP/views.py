import random
from django.shortcuts import render
from django.db.models import Q
from . models import Create_User
from . serializers import  Create_User_Serializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework import status
from rest_framework.response import Response
from . serializers import Login_User_Serializer

from django.contrib.auth import login
from django.utils.timezone import localtime
from .utils import get_tokens_for_user

from . serializers import Course_serializer,CouresWithSyllabus_serializer
from . models import Courses_Model
from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions

from . serializers import Syllabus_serializer
from . models import Syllabus_Model

from . serializers import InternshipOffers_serializer
from . models import InternshipOffers


from . serializers import Apply_Internship_serializer
from . models import Apply_Internship

from .models import Job_Notifications
from .serializers import Job_Notifications_serializer

from .models import About_Trainers
from .serializers import About_Trainers_serializer  

from .models import About_Company
from .serializers import About_Company_serializer

# email servers

from .mail_services.brevo_service import send_brevo_email
from django.conf import settings
from rest_framework.views import APIView




from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Create_User
from .serializers import Create_User_Serializer

from django.core.cache import cache


from . models import NewBatchs
from . serializers import NewBatchModel_serializer

from . models import Student_Enrollment
from . serializers import Student_Enrollment_serializer


from . models import Batch_Enrollment
from . serializers import Batch_Enrollment_serializer

#email serivices
from .mail_services import ApplyInternship,rejectinternship,selectedinternship,EnrollCourse,Batch_enrolled






# Create your views here.
class Create_Users(GenericAPIView,CreateModelMixin):
    querset=Create_User.objects.all()
    serializer_class=Create_User_Serializer
    def post(self,request,*args,**kwargs):
        print("api is hiting")
        email=request.data.get('email')
        phone_number=request.data.get('phone_number')
        otp=str(request.data.get('otp'))
        # OTP validation
        cache_key = f"otp_{email}"
        cached_otp = cache.get(cache_key)
        print(email)
        print(phone_number)
        print(f"Cached OTP: {cached_otp}, Provided OTP: {otp}")  # Debugging line
        print(type(cached_otp), type(otp))  # Debugging line
        if Create_User.objects.filter(email=email).exists():
            return Response({'error':'User with this mail already exists  '},status=status.HTTP_400_BAD_REQUEST)
        elif cached_otp != otp:
            return Response({'error':'Invalid or expired OTP'},status=status.HTTP_400_BAD_REQUEST)
        elif Create_User.objects.filter(phone_number=phone_number).exists():
            return Response({'error':'User with this phone number already exists  '},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            response=self.create(request,*args,**kwargs)
            if response.status_code==status.HTTP_201_CREATED:
                print(request.data.get('password'))
                return Response({'message':'User Create Successfully '},status=status.HTTP_201_CREATED)
            cached_otp = cache.delete(cache_key)
            return response
# update user details
class Users_details(GenericAPIView,ListModelMixin):
    serializer_class=Create_User_Serializer
    queryset=Create_User.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class Update_Password(GenericAPIView, UpdateModelMixin):
    serializer_class = Create_User_Serializer
    queryset = Create_User.objects.all()

    def put(self, request, *args, **kwargs):
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        otp = str(request.data.get("otp"))
        new_password = request.data.get("new_password")

        # ---------- Validations ----------
        if not new_password:
            return Response({"error": "New password is required"}, status=400)

        if not email and not phone_number:
            return Response(
                {"error": "Email or phone number is required"},
                status=400
            )
        if not otp:
            return Response({"error": "OTP is required"}, status=400)

        # ---------- OTP Validation ----------
        cache_key = f"otp_{email }"
        cached_otp = cache.get(cache_key)
        print(f"Cached OTP: {cached_otp}, Provided OTP: {otp}")  # Debugging line
        print(type(cached_otp), type(otp))  # Debugging line
       
        if cached_otp != otp:
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------- User Fetch ----------
        try:
            user = Create_User.objects.get(
                Q(email=email) | Q(phone_number=phone_number)
            )
        except Create_User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ---------- Password Update ----------
        user.set_password(new_password)
        user.save()

        cache.delete(cache_key)  # clear OTP

        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
    serializer_class = Create_User_Serializer
    queryset = Create_User.objects.all()

        
class Login(GenericAPIView):
    serializer_class=Login_User_Serializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            login(request, user)
            tokens=get_tokens_for_user(user)

            return Response({'public_id':user.public_id,
                             'first_name':user.first_name,
                             'last_name':user.last_name,
                             'email':user.email,
                             'password':user.password,
                             'is_superuser':user.is_superuser,
                             'is_staff':user.is_staff,
                             'last_login': localtime(user.last_login),
                             'token':tokens['access'],
                             'refresh':tokens['refresh']
                             },status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
# add Course 

class AddCourse(GenericAPIView,CreateModelMixin):
    queryset=Courses_Model.objects.all()
    serializer_class=Course_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
   
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

#get courese
class Course_details(GenericAPIView,ListModelMixin):
    serializer_class=Course_serializer
    queryset=Courses_Model.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    

#get particular course details
class Course_particular_details(GenericAPIView,RetrieveModelMixin):
    serializer_class=CouresWithSyllabus_serializer
    queryset=Courses_Model.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)






    
#modifiy

class Course_modify(GenericAPIView,UpdateModelMixin):
    serializer_class=Course_serializer
    queryset=Courses_Model.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
        
#delete 

class Course_delete(GenericAPIView,DestroyModelMixin):
    serializer_class=Course_serializer
    queryset=Courses_Model.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
         self.destroy(request,*args,**kwargs)
         return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
    
#adding syllabus

class AddSyllabus(GenericAPIView,CreateModelMixin):
    queryset=Syllabus_Model.objects.all()
    serializer_class=Syllabus_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        course_id=request.data.get('course_id')
        if course_id is None:
            return Response({'error':'course_id is required/Invalid Course_id'},status=status.HTTP_400_BAD_REQUEST)
        syllabus=request.data.get('syllabus')
        if not syllabus or not isinstance(syllabus, list):
            return Response({'error':'Syllabus data must be a non-empty list'},status=status.HTTP_400_BAD_REQUEST)
        data=[
            {'course_id':course_id,
             'module':item.get('module'),
             'description':item.get('description')  
             }for item in syllabus
        ]
        print(data)
        serializer=self.get_serializer(data=data,many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message':'Syllabus added successfully'},status=status.HTTP_201_CREATED)
#get syllabus details
class Syllabus_details(GenericAPIView,ListModelMixin):
    serializer_class=Syllabus_serializer

    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = Syllabus_Model.objects.all()

        course_id = self.request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course_name__course_id=course_id)

        return queryset
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
#modify syllabus
class SyllabusModify(GenericAPIView,UpdateModelMixin):
    serializer_class=Syllabus_serializer
    queryset=Syllabus_Model.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

#delete syllabus
class SyllabusDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=Syllabus_serializer
    queryset=Syllabus_Model.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

# InternshipOffers can be added here similarly
class AddInternshipOffers(GenericAPIView,CreateModelMixin):
    queryset=InternshipOffers.objects.all()
    serializer_class=InternshipOffers_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


#retive internship offers can be implemented similarly
class InternshipOffers_details(GenericAPIView,ListModelMixin):
    serializer_class=InternshipOffers_serializer
    queryset=InternshipOffers.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
#modify internship offers
class InternshipOffers_modify(GenericAPIView,UpdateModelMixin):
    serializer_class=InternshipOffers_serializer
    queryset=InternshipOffers.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
#delete internship offers can be implemented similarly
class InternshipOffers_delete(GenericAPIView,DestroyModelMixin):
    serializer_class=InternshipOffers_serializer
    queryset=InternshipOffers.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

# internship application view

class InternshipApplication(GenericAPIView):
    serializer_class = Apply_Internship_serializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate request data
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        #  Save and get model instance
        application = serializer.save()

        # Access related objects safely
        user = application.student
        internship = application.internship_offers
        internship_name = internship.internship_name  # adjust if field differs

        # Prepare email
        html_message = ApplyInternship.internship_applied_template(
            student_name=f"{user.first_name} {user.last_name}",
            internship_title=internship_name
        )

        # Send email (HTML + CC)
        email =send_brevo_email(
    to_email=user.email,
    subject="🎉 Internship Application Successful",
    html_content=html_message,
    cc_mails=["hr@vjinnovative.co.in","vjinnovative123@gmail.com","venkateshjaripiti123@gmail.com"],
)
        email.content_subtype = "html"
        email.send(fail_silently=False)

        #  Return response
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


#view to see all applications (admin only)
class ViewApplications(GenericAPIView,ListModelMixin):
    serializer_class=Apply_Internship_serializer
    #permission_classes=[IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Apply_Internship.objects.select_related('student','internship_offers').order_by('-applied_on')
        print("Logged in email:", self.request.user.email)
        return Apply_Internship.objects.select_related('student','internship_offers').filter(student__email=self.request.user.email).order_by('-applied_on')
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    

#modify application
class ModifyApplication(GenericAPIView,UpdateModelMixin):
    serializer_class=Apply_Internship_serializer
    queryset=Apply_Internship.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]


    def perform_update(self, serializer):
        # 1️⃣ Get current object BEFORE update
        application = self.get_object()
        old_status = application.status
      
        # 2️⃣ Save updated object
        updated_application = serializer.save()
        new_status = updated_application.status

        print("PERFORM UPDATE")
        print("OLD:", old_status)
        print("NEW:", new_status)
        # 3️⃣ Send email ONLY if status changed
        if old_status != new_status:
            self.send_status_mail(updated_application)



    def send_status_mail(self, application):
        user = application.student
        internship = application.internship_offers
        student_name = f"{user.first_name} {user.last_name}"
        student_email = user.email
        student_ref_id = user.public_id

        # Rejected
        if application.status == "Rejected":
           
            html_message = rejectinternship.reject_internship_template(
                student_name=student_name,
                internship_title=internship.internship_name,
                application_id=application.application_id,
                applied_on=application.applied_on.strftime("%d %b %Y"),
            )
            subject = "❌ Internship Application Rejected - VJISS"

        # Accpeted
        elif application.status == "Accepted":
            html_message = selectedinternship.accept_internship_template(
                student_name=student_name,
                internship_title=internship.internship_name,
                application_id=application.application_id,
                applied_on=application.applied_on.strftime("%d %b %Y"),
            )
            subject = "🎉 Internship Application Selected - VJISS"

        else:
            return  # ⛔ No email for other statuses

        # 📧 Send email
        email = send_brevo_email(
    to_email=student_email,
    subject=subject,
    html_content=html_message,
    cc_mails=["hr@vjinnovative.co.in","vjinnovative123@gmail.com","venkateshjaripiti123@gmail.com"],
)

        email.content_subtype = "html"
        email.send(fail_silently=False)



    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs) 
    





  #delete application   
class DeleteApplication(GenericAPIView,DestroyModelMixin):
    serializer_class=Apply_Internship_serializer
    queryset=Apply_Internship.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

# job notifications can be added here similarly
class AddJobNotification(GenericAPIView,CreateModelMixin):
    queryset=Job_Notifications.objects.all()
    serializer_class=Job_Notifications_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
#job notification view can be added here similarly
class JobNotificationDetails(GenericAPIView,ListModelMixin):
    serializer_class=Job_Notifications_serializer
    queryset=Job_Notifications.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
#jon notification modify 
class JobNotificationModify(GenericAPIView,UpdateModelMixin):
    serializer_class=Job_Notifications_serializer
    queryset=Job_Notifications.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

#job notification delete can be implemented similarly
class JobNotificationDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=Job_Notifications_serializer
    queryset=Job_Notifications.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
#adding trainers 
class AddTrainers(GenericAPIView,CreateModelMixin):
    queryset=About_Trainers.objects.all()
    serializer_class=About_Trainers_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class TrainersDetails(GenericAPIView,ListModelMixin):
    serializer_class=About_Trainers_serializer
    queryset=About_Trainers.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class TrainersModify(GenericAPIView,UpdateModelMixin):
    serializer_class=About_Trainers_serializer
    queryset=About_Trainers.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
class TrainersDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=About_Trainers_serializer
    queryset=About_Trainers.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)


class AddCompanyInfo(GenericAPIView,CreateModelMixin):
    queryset=About_Company.objects.all()
    serializer_class=About_Company_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class CompanyInfoDetails(GenericAPIView,ListModelMixin):
    serializer_class=About_Company_serializer
    queryset=About_Company.objects.all()
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    

class CompanyInfoModify(GenericAPIView,UpdateModelMixin):
    serializer_class=About_Company_serializer
    queryset=About_Company.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
class CompanyInfoDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=About_Company_serializer
    queryset=About_Company.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

#New Batchs


class NewBacthAdding(GenericAPIView,CreateModelMixin):
    queryset=NewBatchs.objects.all()
    serializer_class=NewBatchModel_serializer
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class BacthDetails(GenericAPIView,ListModelMixin):
    serializer_class=NewBatchModel_serializer
    queryset=NewBatchs.objects.all()
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class BatchUpdate(GenericAPIView,UpdateModelMixin):
    serializer_class=NewBatchModel_serializer
    queryset=NewBatchs.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def put(self,request,*args,**kwargs):
        self.update(request,*args,**kwargs)
        return Response({"Message":"Successfully Updated "},status.HTTP_200_OK)
    def patch(self,request,*args,**kwargs):
        self.update(request,*args,**kwargs)
        return Response({"Message":"Successfully Updated "},status.HTTP_200_OK)

class Batchdelete(GenericAPIView,DestroyModelMixin):
    serializer_class=NewBatchModel_serializer
    queryset=NewBatchs.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwars):
        self.destroy(request,*args,**kwars)
        return Response({"Message":"Successfully Deleted"},status.HTTP_200_OK)


class StudentEnrollment(GenericAPIView,CreateModelMixin):
    queryset=Student_Enrollment.objects.all()
    serializer_class=Student_Enrollment_serializer
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        application=serializer.save()
        user=application.student
        course=application.course
        course_name=course.course_name
           
        #prepare email
        html_message=EnrollCourse.course_enrolled_template(
            student_name=f"{user.first_name} {user.last_name}",
            course_name=course_name
        )
        email=send_brevo_email(
    to_email=user.email,
    subject="🎉 Course Enrollment Successful",
    html_content=html_message,
    cc_mails=["hr@vjinnovative.co.in","vjinnovative123@gmail.com","venkateshjaripiti123@gmail.com"],
)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class StudentEnrollmentView(GenericAPIView,ListModelMixin):
    serializer_class=Student_Enrollment_serializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Student_Enrollment.objects.select_related('student','course').order_by('-enrollment_date')
        print("Logged in email:", self.request.user.email)
        return Student_Enrollment.objects.select_related('student','course').filter(student__email=self.request.user.email).order_by('-enrollment_date')
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class StudentEnrollmentModify(GenericAPIView,UpdateModelMixin):
    serializer_class=Student_Enrollment_serializer
    queryset=Student_Enrollment.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions,IsAuthenticated]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
class StudentEnrollmentDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=Student_Enrollment_serializer
    queryset=Student_Enrollment.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
    



class BatchEnrollment(GenericAPIView,CreateModelMixin):
    queryset=Batch_Enrollment.objects.all()
    serializer_class=Batch_Enrollment_serializer
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        application=serializer.save()
        user=application.student
        batch=application.batch
        batch_type=batch.batch_type
        course_name=batch.course.course_name
           
        #prepare email
        html_message=Batch_enrolled.batch_enrolled_template(
            student_name=f"{user.first_name} {user.last_name}",
            batch_type=batch_type,
            course_name=course_name
        )
        email=send_brevo_email(
    to_email=user.email,
    subject="🎉 Course Enrollment Successful",
    html_content=html_message,
    cc_mails=["hr@vjinnovative.co.in","vjinnovative123@gmail.com","venkateshjaripiti123@gmail.com"],
)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class BatchEnrollmentView(GenericAPIView,ListModelMixin):
    serializer_class=Batch_Enrollment_serializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Batch_Enrollment.objects.select_related('student','batch').order_by('-enrollment_date')
        print("Logged in email:", self.request.user.email)
        return Batch_Enrollment.objects.select_related('student','batch').filter(student__email=self.request.user.email).order_by('-enrollment_date')
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
class BatchEnrollmentModify(GenericAPIView,UpdateModelMixin):
    serializer_class=Batch_Enrollment_serializer
    queryset=Batch_Enrollment.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions,IsAuthenticated]
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
class BatchEnrollmentDelete(GenericAPIView,DestroyModelMixin):
    serializer_class=Batch_Enrollment_serializer
    queryset=Batch_Enrollment.objects.all()
    permission_classes=[IsAdminUser,DjangoModelPermissions]
    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)
        return Response({'message':"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)