from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =('id','name','start_date','end_date','comments','status')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'