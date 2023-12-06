from rest_framework import serializers
from .models import Project
from .models import EnglishWord

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =('id','name','start_date','end_date','comments','status')

class Englishproject(serializers.ModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ('word', 'phonetic_symbols', 'part_of_speech','explain')

class Accountproject(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields =('user','gmail','password')
