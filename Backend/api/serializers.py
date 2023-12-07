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


UserModel = get_user_model()

#註冊
class sign_upSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        def create(self, clean_data):
            user_obj = UserModel.objects.create_user(email=clean_data['email'],
                password=clean_data['passwortd'])
            user_obj.username = clean_data['username']
            user_obj.save()
            return user_obj
#登入
class sign_inSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(usernam=clean_data['email'], passwprd=clean_data['password'])
        if not user :
            raise ValueError('user not found')
        return user
#登出
class log_outSerializer(serializers.ModelSerializer):
    class Meat:
        models: UserModel
        fields = ('email','username')