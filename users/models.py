from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    firstName = models.CharField(null=True, blank=True)
    lastName = models.CharField(null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    isTeacher = models.BooleanField(null=True, blank=True)
    enrollmentDate = models.DateField(null=True, blank=True)
    hireDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username