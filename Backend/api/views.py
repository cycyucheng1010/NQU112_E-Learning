from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import assemblyai as aai
from rest_framework import viewsets,permissions
from .serializers import ProjectSerializer,Project,UserSerializer,User,EnglishSerializer,ExamPaperSerializer
from rest_framework.response import Response 
from .models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores

from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt

#from .importfile.AssemblyAI import VoiceToText
from rest_framework.parsers import MultiPartParser #用來處理傳送來的音檔
from django.core.files.storage import default_storage
from rest_framework.decorators import action
import os
from django.utils.crypto import get_random_string
from django.conf import settings


class ProjectViewset(viewsets.ViewSet):
    permission_classes =[permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
       queryset = self.queryset
       serializer = self.serializer_class(queryset,many =True)
       return Response(serializer.data)
 
    def create(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
            

    def retrieve(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer =self.serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)

    def destroy(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        project.delete()

        return response(status=204)

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset =User.objects.all()

    @action(methods=['POST'],url_path = 'login',detail = False)
    def login(self,request):

        email = request.data.get('email')
        pwd = request.data.get('password')

        res ={
            'code':0,
            'msg' :'',
            'data':{}
        }
        if not all([email,pwd]):
            res['msg'] = '參數異常'
            return Response(res)
        print(request.data)
        try:
            user=User.objects.get(email=email,password=pwd)
        except:
            res['msg'] = '帳號或密碼錯誤請重新登入'
            return Response(res)
        if user.is_active !=1:
            res['msg'] = '用戶不可用，請重新登入'
        
        login(request,user)
        request.session['login'] =True
        request.session['FS_YWPT'] = True
        request.session.set_expiry(0)
        res['msg'] = '登入成功'
        res['code'] = 1
        res['data'] ={'email' :email}
        return Response(res)
    @action(methods=['POST'], url_path='register', detail=False)
    def register(self, request):
        '''
        注册
        :param request: 用于传参数，必要参数 email：邮箱   password：密码  username：用户名 
        :return:
        '''
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        if not all([email, password, username]):
            res['msg'] = '参数异常。'
            return Response(res)

        print([email, password, username])
        if User.objects.filter(username=username):
            res['msg'] = '用户已存在。'
            return Response(res)

        User.objects.create(password=password, is_superuser=0, username=username, email=email)
        res['code'] = 1
        res['data'] = [email, password, username]
        return Response(res)

英文資料庫
#class EnglishWordSearchAPIView(viewsets.ViewSet):
#    parser_classes = (MultiPartParser,)
#
#    @action(methods=['POST'], detail=False)
#    def VoiceToText(self, request, *args, **kwargs):
#        file = request.FILES.get('file')
#        if not file:
#            return Response({"message": "没有文件上传"}, status=400)#
#
        # 设置 AssemblyAI API 密钥
#        aai.settings.api_key = "147cacab598c4c77b5cb4bb2d3ae295c"

        #tmp_dir = getattr(settings, 'TEMP_DIR', '/tmp/')
        #if not os.path.exists(tmp_dir):
            #os.makedirs(tmp_dir)
#        import os
#        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'voice')
#        file_name = get_random_string(length=12) + '.webm'
#        #file_path = os.path.join(tmp_dir, file_name)
#        file_path = os.path.join(desktop_dir, file_name)
#        try:
#            with open(file_path, 'wb+') as destination:
#                for chunk in file.chunks():
#                    destination.write(chunk)

            # 创建一个 AssemblyAI 转录器
#            transcriber = aai.Transcriber()
            # 调用转录服务
#            transcript = transcriber.transcribe(file_path)
#            transcript_text = transcript.text
#            print(transcript_text)
#       except Exception as e:
            # 添加更多的错误处理逻辑
#            return Response({"message": str(e)}, status=500)
#        finally:
#            # 清理临时文件
#            if os.path.exists(file_path):
#                os.remove(file_path)
#
#        return Response({"transcript": transcript_text})



