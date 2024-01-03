from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,permissions
from .serializers import ProjectSerializer,Project,UserSerializer,User,EnglishSerializer,ExamPaperSerializer
from rest_framework.response import Response 
from .models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from openai import OpenAI
from datetime import datetime
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores
from .models import WordSentence,WordImage
from .serializers import SentenceSerializer, ImageSerializer

from rest_framework.decorators import api_view
from rest_framework.views import APIView
import traceback
import json
from django.views.decorators.csrf import csrf_exempt

#from .importfile.AssemblyAI import VoiceToText
from rest_framework.parsers import MultiPartParser #用來處理傳送來的音檔
from django.core.files.storage import default_storage
from rest_framework.decorators import action
import os
from django.utils.crypto import get_random_string
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
import requests
from requests import post, get




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

        return Response(status=204)

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

#英文資料庫
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



# 封裝 OpenAI 相關操作
class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_sentence(self, word_input):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an English teacher."},
                {"role": "user", "content": f"Craft a vivid sentence focusing on '{word_input}', ensuring a clear understanding of its meaning (within 15 words)."}
            ],
            max_tokens=30
        )
        
        return response
# 初始化 OpenAI 客户端
openai_client = OpenAIClient(api_key="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")

class SentenceAPIView(APIView):
    def post(self, request):
        serializer = SentenceSerializer(data=request.data)
        if serializer.is_valid():
            word_input = serializer.validated_data['word']

            # 檢查資料庫中是否已存在句子
            try:
                word_sentence = WordSentence.objects.get(word=word_input)
                generated_sentence = word_sentence.sentence
                print(f"句子 '{generated_sentence}' 已經存在，無需再次生成。")
                serializer = SentenceSerializer(word_sentence)
                return Response({"status": "success", "sentence": serializer.data})
            except WordSentence.DoesNotExist:
                pass

            # 使用 OpenAI API 生成句子
            response = openai_client.generate_sentence(word_input)
            generated_sentence = response.choices[0].message.content

            # 保存生成的句子到資料庫
            WordSentence.objects.create(word=word_input, sentence=generated_sentence)
            print(f"Generated Sentence: {generated_sentence}")

            serializer = SentenceSerializer({'word': word_input, 'sentence': generated_sentence})
        
            return Response({"status": "success", "sentence": serializer.data})
        else:
            return Response({"status": "error", "message": serializer.errors}, status=400)

class ImageAPIView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            word_input = serializer.validated_data['word']
            sentence_input = serializer.validated_data['sentence']

            # 檢查資料庫中是否已存在圖片
            try:
                word_image = WordImage.objects.get(word=word_input)
                image_url = word_image.image.name
                print(f"圖片 '{image_url}' 已經存在，無需再次生成。")
                serializer = ImageSerializer(word_image)
                return Response({"status": "success", "image": serializer.data})
            except WordImage.DoesNotExist:
                pass

            # 使用外部 API 生成圖片
            prompt = f"{sentence_input.replace(word_input, f'((({word_input})))')}"
            url = "https://stablediffusionapi.com/api/v3/text2img"
            payload = {
                "key": "kRdhAtCe7TqcTgUkpoBeWB569nwAO7UnvR3BGvVGBj2zJtKbsapxWka0sPQ2",
                "prompt": prompt,
                "width": "512",
                "height": "512",
                "samples": "1",
                "num_inference_steps": "20",
                "guidance_scale": 7.5,
                "safety_checker": "yes",
                "multi_lingual": "no",
                "panorama": "no",
                "self_attention": "no",
                "upscale": "no",
                "embeddings_model": None,
                "webhook": None,
                "track_id": None
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            image_url = response_data.get("output")[0] if "output" in response_data else None

            if image_url:
                # 保存到資料庫
                WordImage.objects.create(word=word_input, image=f'word_images/{word_input}.png')
                serializer = ImageSerializer({'word': word_input, 'image': f'word_images/{word_input}.png'})
                return Response({"status": "success", "image": serializer.data})
            else:
                return Response({"status": "error", "message": "生成失敗"})
        else:
            return Response({"status": "error", "message": serializer.errors}, status=400)