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
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWord,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores

from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
import re  #比對刪除
import string #比對轉換大小寫
from rest_framework.parsers import MultiPartParser #用來處理傳送來的音檔
from django.core.files.storage import default_storage
from rest_framework.decorators import action
import os
from django.utils.crypto import get_random_string
from django.conf import settings
from django.http import JsonResponse

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
class EnglishWordSearchAPIView(viewsets.ViewSet):
    @action(methods=['POST'], detail=False)
    def VoiceToText(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"message": "没有文件上传"}, status=400)

        # 设置 AssemblyAI API 密钥
        aai.settings.api_key = "147cacab598c4c77b5cb4bb2d3ae295c"

        #tmp_dir = getattr(settings, 'TEMP_DIR', '/tmp/')
        #if not os.path.exists(tmp_dir):
            #os.makedirs(tmp_dir)
        import os
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'voice')
        file_name = get_random_string(length=12) + '.webm'
        #file_path = os.path.join(tmp_dir, file_name)
        file_path = os.path.join(desktop_dir, file_name)
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # 创建一个 AssemblyAI 转录器
            transcriber = aai.Transcriber()
            # 调用转录服务
            transcript = transcriber.transcribe(file_path)
            transcript_text = transcript.text
            print(transcript_text)
        except Exception as e:
            # 添加更多的错误处理逻辑
            return Response({"message": str(e)}, status=500)
        finally:
            # 清理临时文件
            if os.path.exists(file_path):
                os.remove(file_path)

        return Response({"transcript": transcript_text})
    def list(self, request):
    # 从请求中获取搜索词
        search = request.GET.get('search_word', '').strip()  # 增加.strip()以移除可能的前后空格

        # 基于搜索词进行QuerySet过滤，只选择word字段，限制为前15个结果
        words = EnglishWord.objects.filter(
        Q(word__istartswith=search)
        ).values_list('word', flat=True)[:15]

        # 将结果转为列表，因为values_list返回的是QuerySet
        words_list = list(words)
        print(list(words))
        # 返回序列化后的数据
        print(search + "1")
        
        return JsonResponse(words_list, safe=False)
    def generate_image(word, sentence, wordpic):
    # 1. 檢查是否已經生成過圖片
        
        image_filename = os.path.join(wordpic, f"{word}.png")
        if os.path.exists(image_filename):
            print(f"圖片 '{image_filename}' 已經存在，無需再次生成。")
            return

        # 2. 根據輸入的單字和句子生成 prompt
        prompt = f"{sentence.replace(word, f'((({word})))')}"

        url = "https://stablediffusionapi.com/api/v3/text2img"

        payload = json.dumps({
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
        })

        headers = {
            'Content-Type': 'application/json'
        }

        # 3. 發送 API 請求
        response = requests.request("POST", url, headers=headers, data=payload)

        # 4. 檢查狀態碼是否為成功
        if response.status_code == 200:
            response_data = response.json()
            image_url = response_data.get("output")[0]

        if image_url:
        # 5. 下載圖片到指定資料夾
            response_image = requests.get(image_url)
            with open(image_filename, 'wb') as img_file:
                img_file.write(response_image.content)

        print("Generated Image URL:", image_url)

last_word = None

class result(viewsets.ViewSet):
    
    @action(methods=['POST'], url_path='receive_word', detail=False)
    def receive_word(self, request):
        global last_word
        # 接收单词并存储
        last_word = request.data.get('word')
        if last_word is None or last_word.strip() == '':
            # 如果接收到的单词是None或空字符串，返回错误信息
            return JsonResponse({'status': 'error', 'message': 'No word provided'})
        # 如果单词有效，返回成功响应
        return JsonResponse({'status': 'success', 'message': 'Word received'})

    @action(methods=['GET'], url_path='get_last_word', detail=False)
    def get_last_word(self, request):
        # 返回存储的单词
        return JsonResponse({'status': 'success', 'word': last_word})

    @action(methods=['POST'], url_path='compare_word', detail=False)
    def compare_word(self, request):
        # Receive the file and word
        file = request.FILES.get('file')
        word = request.data.get('word')
        
        # Validate input
        if not file or not word:
            return JsonResponse({'status': 'error', 'message': '未提供文件或单词'}, status=400)

        # Set the file save path
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'voice')
        file_name = get_random_string(length=12) + '.webm'
        file_path = os.path.join(desktop_dir, file_name)

        # Transcription logic
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Set the AssemblyAI API key and transcribe
            aai.settings.api_key = "147cacab598c4c77b5cb4bb2d3ae295c"
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            transcript_text = transcript.text
            
         
            
            # Remove punctuation
            translator = str.maketrans('', '', string.punctuation)
            word_without_punctuation = word.translate(translator)
            word_cleaned = re.sub(r'[^a-zA-Z0-9]', '', word)
            transcript_text_cleaned = re.sub(r'[^a-zA-Z0-9]', '', transcript_text)
            transcript_text_without_punctuation = transcript_text.translate(translator)


            # Compare the word and transcript text (case insensitive)
            match = word_without_punctuation.lower() in transcript_text_without_punctuation.lower()
            
            # Log the transcript and word
            print(f"Transcript Text: {transcript_text}")
            print(f"Word: {word}")

            return JsonResponse({'status': 'success', 'word': word, 'transcript': transcript_text, 'match': match})
        except Exception as e:
            # Log the error
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        finally:
            # Clean up temporary files
            if os.path.exists(file_path):
                os.remove(file_path)
