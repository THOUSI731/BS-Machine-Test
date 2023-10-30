from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Account(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self) -> str:
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE,related_name='profile')
    date_of_birth = models.DateField(null=True,blank=True)
    profile_picture = models.FileField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.user.email
