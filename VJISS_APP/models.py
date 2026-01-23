from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

class Create_User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False
                                    , validators=[RegexValidator(r'^[6-9][0-9]{9}$', 'Enter a valid 10-digit phone number.')])


    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    date_of_birth = models.DateField()
    
    # ALL REQUIRED FIELDS 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # ← REQUIRED BY PermissionsMixin
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Fix related_name conflicts
    groups = models.ManyToManyField(Group, related_name='vjiss_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='vjiss_users', blank=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number', 'date_of_birth']

    def __str__(self):
        return f"{self.email}\t ({self.public_id})"



    
class Courses_Model(models.Model):
    course_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    course_name=models.CharField(max_length=100)
    course_logo=models.ImageField(upload_to='course_logos/')
    course_duration=models.CharField(max_length=50)
    course_fee=models.IntegerField()
    course_description=models.TextField()
    level_choices=[('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')]
    course_level=models.CharField(max_length=20,choices=level_choices,default='Beginner')
    def __str__(self):
        return  f"{self.course_name}\t ({self.course_id})"
class Syllabus_Model(models.Model):
    syllabus_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    course_id=models.ForeignKey(Courses_Model,on_delete=models.CASCADE,related_name='syllabus_courses')
    module=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self):
        return f"{self.module}\t ({self.syllabus_id})"
    




#Specializations Model

class InternshipOffers(models.Model):
    internship_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    internship_name=models.CharField(max_length=100)
    internship_description=models.TextField()
    technologies=models.CharField(max_length=200)
    def __str__(self):
        return f"{self.internship_name}\t ({self.internship_id})"

#intership model 
class Apply_Internship(models.Model):
    application_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student=models.ForeignKey(Create_User,on_delete=models.CASCADE,related_name='internship_applicants')
    internship_offers=models.ForeignKey(InternshipOffers,on_delete=models.CASCADE,related_name='internship_offers')
    education_choices=[('Diploma', 'Diploma'),('UG', 'Under Graduate'),('PG', 'Post Graduate'),('PhD', 'PhD'),]
    education=models.CharField(max_length=200,choices=education_choices)
    resume=models.FileField(upload_to='resumes/')
    applied_on=models.DateField(auto_now_add=True)
    status_choices=[('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')]
    status=models.CharField(max_length=20,choices=status_choices,default='Pending')
    reason=models.TextField(blank=True,null=True)
    def __str__(self):
        return f'{self.student.email}\t({self.application_id}) '

#job notifications model
class Job_Notifications(models.Model):
    notification_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    company_logo=models.ImageField(upload_to='company_logos/')
    job_title=models.CharField(max_length=200)
    company_name=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    company_posted_date=models.DateField(null=True, blank=True,default=None)
    posted_date=models.DateField(default=None,null=True, blank=True)
    job_description=models.TextField()
    requirements=models.TextField()
    link=models.URLField()
    def __str__(self):
        return f'{self.company_name}\t({self.notification_id}) '

#about trainers
class About_Trainers(models.Model):
    trainer_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    trainer_title=models.CharField(max_length=200)
    trainer_name=models.CharField(max_length=200)
    trainer_image=models.ImageField(upload_to='trainer_images/')
    trainer_bio=models.TextField()
    def __str__(self):
        return f'{self.trainer_name}\t({self.trainer_id}) '
class About_Company(models.Model):
    company_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    company_name=models.CharField(max_length=200)
    company_logo=models.ImageField(upload_to='company_logos/')
    company_description=models.TextField()
    office_address=models.TextField()
    contact_email=models.EmailField(max_length=200)   
    contact_phone=models.CharField(max_length=15)
    google_map_link=models.URLField(blank=True,null=True ,max_length=500)
    def __str__(self):
        return str(self.company_id) 



class NewBatchs(models.Model):
    batch_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    course=models.ForeignKey(Courses_Model,on_delete=models.CASCADE,related_name='batch_courses')
    faculty=models.ForeignKey(About_Trainers,on_delete=models.CASCADE,related_name='faculty_name')
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    timing=models.TimeField(blank=True,null=True)
    mode_choices=[('Online','Online'),('Offline','Offline')]
    mode=models.CharField(max_length=20,choices=mode_choices,default='Offline')
    quafication_requirements=models.CharField(max_length=100)
    course_duration=models.CharField(max_length=50)
    batch_choices=[('Weekdays','Weekdays'),('Weekends','Weekends')]
    batch_type=models.CharField(max_length=20,choices=batch_choices,default='Weekdays')
    choices=[('started','started'),('upcoming','upcoming'),('completed','completed')]
    status=models.CharField(max_length=20,choices=choices,default='upcoming')
    def __str__(self):
        return f'{self.course.course_name}\t({self.faculty.trainer_name}) \t ({self.batch_id}) '



#student enrollment.
class Student_Enrollment(models.Model):
    enrollment_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student=models.ForeignKey(Create_User,on_delete=models.CASCADE,related_name='enrolled_students')
    course=models.ForeignKey(Courses_Model,on_delete=models.CASCADE,related_name='enrolled_courses')
    enrollment_date=models.DateField(auto_now_add=True)
    status_choices=[('Interested','Interested'),('NotInterested','NotInterested'),('Pending','Pending')]
    status=models.CharField(max_length=20,choices=status_choices,default="Pending")
    def __str__(self):
        return str(self.enrollment_id)