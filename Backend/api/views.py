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
#句子圖片模型
from api.models import WordInfos
import openai
import traceback
from openai import OpenAI
from django.http import JsonResponse
import requests

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
            transcript_text = transcript.text.lower()
            transcript_words = transcript_text.split()
            transcript_words = transcript_text.replace('.', '').split()
            transcript_text = transcript_words[0]
            
            
            # Remove punctuation
            translator = str.maketrans('', '', string.punctuation)
            word_without_punctuation = word.translate(translator)
            word_cleaned = re.sub(r'[^a-zA-Z0-9]', '', word)
            transcript_text_cleaned = re.sub(r'[^a-zA-Z0-9]', '', transcript_text)
            transcript_text_without_punctuation = transcript_text.translate(translator)
            
            

            # Compare the word and transcript text (case insensitive)
            match = word_cleaned in transcript_text_cleaned
            
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
    
    @action(methods=['POST'], url_path='sentence', detail=False)
    def word_sentence(self, request):
        word_text = last_word.strip()  # 从请求中获取并清理单词文本
        english_word = EnglishWord.objects.filter(word=word_text).first()
        
        if english_word:
            word_info = WordInfos.objects.filter(word=english_word).first()
            if word_info:
                # 单词信息存在，可以进行后续操作
                sentence = word_info.sentence
                image_url = word_info.image_url if word_info.image_url else None
                print(f"单词 '{word_text}' 的相关句子是: {sentence}")
                print(image_url)
                
                # 返回找到的句子和图片URL
                return JsonResponse({
                    "msg": "success", 
                    "existing_sentence": sentence if sentence else "No sentence available.",
                    "existing_image": image_url if image_url else "No image available."
                })
            else:
                # 单词信息不存在，使用 GPT-3 生成句子
                client = OpenAI(api_key="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")  # 替换为你的OpenAI API密钥注意會一直換
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        messages=[
                            {"role": "system", "content": "You are an English teacher."},
                            {"role": "user", "content": f"give me a sentence for the word '{word_text}'"}
                        ],
                        max_tokens=50
                    )
                    
                    generated_sentence = response.choices[0].message.content
                    print(f"没有找到与单词 '{word_text}' 相关的句子。生成的句子是: {generated_sentence}")
                    
                    # 将生成的句子存储到数据库
                    new_sentence = WordInfos(word=english_word, sentence=generated_sentence)
                    new_sentence.save()

                    # 使用Stable Diffusion API生成图片
                    prompt = f"{generated_sentence.replace(word_text, f'((({word_text})))')}"
                

                    url = "https://modelslab.com/api/v6/realtime/text2img"

                    payload = json.dumps({
                            "key" :"0nntsJq4X9NgNJUUZ0CCziE4NfQZdcNv2I0ulMa7tRjHJF0oqSsBONUa1S1e",
                            "prompt": prompt,
                            "width": "512",
                            "height": "512",
                            "num_inference_steps": "20",
                            "seed": 0,
                            "sample":1,
                            "guidance_scale": 7.5, 
                            "webhook": None,
                            "track_id": None
                            })
                    headers = {'Content-Type': 'application/json'}
                    response = requests.request("POST", url, headers=headers, data=payload)

                    if response.status_code == 200:
                        response_data = response.json()
                        print(response_data)
                        image_url = response_data.get("output")[0]
                        if image_url:
                            # 更新WordInfo实例的image字段为图片URL
                            new_sentence.image_url = image_url
                            new_sentence.save()
                            print("Generated Image URL:", image_url)
                            return JsonResponse({"msg": "success", "generated_sentence": generated_sentence, "generated_image_url": image_url})
                        else:
                            print("未能获取图片 URL。")
                    else:
                        print("Error:", response.status_code, response.text)
                    return JsonResponse({"msg": "error", "error_details": "Failed to generate image."})
                except Exception as e:
                    traceback.print_exc()
                    return JsonResponse({"msg": "error", "error_details": str(e)})
        else:
            # 如果没有找到对应的 EnglishWord 实例
            return JsonResponse({"msg": "error", "error_details": f"Word '{word_text}' not found."})
