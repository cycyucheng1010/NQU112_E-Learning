from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class Project(models.Model):
    name = models.CharField(unique=True,max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.CharField(max_length=500,blank=True,null=True)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class EnglishWord(models.Model):
    word = models.TextField()
    phonetic_symbols = models.TextField()
    part_of_speech = models.TextField()
    explain = models.TextField()


    def __str__(self):
        return self.name
    
class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user
    
class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = mpdel.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects =AppUserManager()
    def __str__(self):
        return self.username
