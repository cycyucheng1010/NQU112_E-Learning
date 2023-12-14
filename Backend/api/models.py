from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

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


class EnglishOptional(models.Model):
    topic_number = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishOptionalNumber1(models.Model):
    topic_number = models.TextField()
    topic    = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishOptionalNumber2(models.Model):
    topic_number = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishOptionalNumber3(models.Model):
    topic_number = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer_E = models.TextField()
    answer_F = models.TextField()
    answer_G = models.TextField()
    answer_H = models.TextField()
    answer_I = models.TextField()
    answer_J = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishOptionalNumber4(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishOptionalNumber5(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishTopic(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    answer_A = models.TextField()
    answer_B = models.TextField()
    answer_C = models.TextField()
    answer_D = models.TextField()
    answer = models.CharField(max_length=255)
    year = models.IntegerField()

class EnglishWord(models.Model):
    word = models.TextField()
    phonetic_symbols = models.TextField()
    part_of_speech = models.TextField()
    explain = models.TextField()

class OptionalTopic(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    year = models.IntegerField()

class OptionalTopicNumber2(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    year = models.IntegerField()

class OptionalTopicNumber3(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    year = models.IntegerField()

class OptionalTopicNumber4(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    year = models.IntegerField()

class OptionalTopicNumber5(models.Model):
    topic_number = models.TextField()
    topic = models.TextField()
    year = models.IntegerField()

class ExamPaper(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    questions_optional_number1 = models.ManyToManyField(EnglishOptionalNumber1)
    questions_optional_number2 = models.ManyToManyField(EnglishOptionalNumber2)
    questions_optionaltopic_number2 = models.ManyToManyField(OptionalTopicNumber2)
    questions_optional_number3 = models.ManyToManyField(EnglishOptionalNumber3)
    questions_optionaltopic_number3 = models.ManyToManyField(OptionalTopicNumber3)
    questions_optional_number4 = models.ManyToManyField(EnglishOptionalNumber4)
    # questions_optionaltopic_number4 = models.ManyToManyField(OptionalTopicNumber4)
    questions_optional_number5 = models.ManyToManyField(EnglishOptionalNumber5)
    questions_optionaltopic_number5 = models.ManyToManyField(OptionalTopicNumber5)

class ExamPapers(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    questions_optional_number1 = models.ManyToManyField(EnglishOptionalNumber1)
    questions_optional_number2 = models.ManyToManyField(EnglishOptionalNumber2)
    questions_optionaltopic_number2 = models.ManyToManyField(OptionalTopicNumber2)
    questions_optional_number3 = models.ManyToManyField(EnglishOptionalNumber3)
    questions_optionaltopic_number3 = models.ManyToManyField(OptionalTopicNumber3)
    questions_optional_number4 = models.ManyToManyField(EnglishOptionalNumber4)
    # questions_optionaltopic_number4 = models.ManyToManyField(OptionalTopicNumber4)
    questions_optional_number5 = models.ManyToManyField(EnglishOptionalNumber5)
    questions_optionaltopic_number5 = models.ManyToManyField(OptionalTopicNumber5)

class student_scores(models.Model):
   
    subject = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=5, decimal_places=2)
 

