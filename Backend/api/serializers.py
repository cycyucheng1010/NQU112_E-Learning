from rest_framework import serializers
from .models import Project
from .models import EnglishWordSearch
#from .models import ExamUI
from django.contrib.auth.models import User
from .models import ExamPaper, EnglishOptionalNumber1, EnglishOptionalNumber2, OptionalTopicNumber2, EnglishOptionalNumber3, OptionalTopicNumber3, EnglishOptionalNumber4

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =('id','name','start_date','end_date','comments','status')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EnglishSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishWordSearch
        fields = ('word', 'phonetic_symbols', 'part_of_speech','explain')

class ExamPaperSerializer(serializers.ModelSerializer):
    questions_optional_number1 = serializers.PrimaryKeyRelatedField(many=True, queryset=EnglishOptionalNumber1.objects.all())
    questions_optional_number2 = serializers.PrimaryKeyRelatedField(many=True, queryset=EnglishOptionalNumber2.objects.all())
    questions_optionaltopic_number2 = serializers.PrimaryKeyRelatedField(many=True, queryset=OptionalTopicNumber2.objects.all())
    questions_optional_number3 = serializers.PrimaryKeyRelatedField(many=True, queryset=EnglishOptionalNumber3.objects.all())
    questions_optionaltopic_number3 = serializers.PrimaryKeyRelatedField(many=True, queryset=OptionalTopicNumber3.objects.all())
    questions_optional_number4 = serializers.PrimaryKeyRelatedField(many=True, queryset=EnglishOptionalNumber4.objects.all())
    class Meta:
        model = ExamPaper
        fields = '__all__'
