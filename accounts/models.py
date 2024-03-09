from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class Customuser(AbstractUser):
    ADMIN = 'Admin'
    MANAGER = 'Manager'
    TEACHER = 'Teacher'
    STUDENT = 'Student'
    HOD = 'Hod'
    
    ROLE_CHOICES =(
        (ADMIN,'Admin'),
        (MANAGER,'Manager'),
        (TEACHER,'Teacher'),
        (STUDENT,'Student'),
        (HOD,'Hod')
    )
    uuid = models.UUIDField(unique=True,editable=False,default=uuid.uuid4)
    username = models.CharField(max_length=50,blank=False,null=False)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES,blank=True,null=True,max_length=50)
    dob= models.CharField(max_length=20,null=True,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    class Meta:

        db_table = 'users_custom'