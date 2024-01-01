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
from openai import OpenAI
from datetime import datetime
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores

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



# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-n2NyHG6Z2CUdEY3CeORAT3BlbkFJ2WbBGga2RuHTvGMZtVN")

# 定义文件路径
word_sentence_folder = "./function/wordsentence"
word_pic_folder = "./function/wordpic"

# 确保目录存在
os.makedirs(word_sentence_folder, exist_ok=True)
os.makedirs(word_pic_folder, exist_ok=True)

@csrf_exempt
@api_view(['POST'])
def generate_sentence(request):
    try:
        sentence_list = []

        # 从请求数据中获取单词和句子
        data = request.data
        word_input = data.get('word')
        sentence_input = data.get('sentence')

        # 使用 OpenAI API 生成句子
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an English teacher."},
                {"role": "user", "content": f"Craft a vivid sentence focusing on '{word_input}', ensuring a clear understanding of its meaning (within 15 words)."}
            ],
            max_tokens=30
        )
        
        generated_sentence = response.choices[0].message.content
        sentence_list.append(generated_sentence)

        # 保存生成的句子到文件
        sentence_filename = os.path.join(word_sentence_folder, f"{word_input}.txt")
        with open(sentence_filename, 'w') as file:
            file.write(generated_sentence)

        # 输出生成的句子并返回给前端
        print(f"Generated Sentence: {generated_sentence}")
        
        return JsonResponse({"status": "success", "sentence": generated_sentence})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "error"})


@api_view(['POST'])
def generate_image(request):
    try:
        data = json.loads(request.body)
        word_input = data.get('word')
        sentence_input = data.get('sentence')

        image_filename = os.path.join(word_pic_folder, f"{word_input}.png")

        if os.path.exists(image_filename):
            print(f"圖片 '{image_filename}' 已經存在，無需再次生成。")
            return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

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
        response = post(url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            image_url = response_data.get("output")[0] if "output" in response_data else None

            if image_url:
                # 直接在 generate_image 函數中下載圖片
                image_filename = os.path.join(word_pic_folder, f"{word_input}.png")
                response_image = get(image_url)

                with open(image_filename, 'wb') as img_file:
                    img_file.write(response_image.content)

                return JsonResponse({"status": "success", "image_url": f"{word_input}.png"})

        return JsonResponse({"status": "error", "message": "生成失敗"})