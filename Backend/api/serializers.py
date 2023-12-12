from rest_framework import serializers
from .models import Project
from .models import EnglishWord
from django.contrib.auth import get_user_model, authenticate

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =('id','name','start_date','end_date','comments','status')

class EnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ('word', 'phonetic_symbols', 'part_of_speech','explain')

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('','','','','')


