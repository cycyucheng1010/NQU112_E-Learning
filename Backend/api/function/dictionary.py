from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import assemblyai as aai
from rest_framework import viewsets,permissions
from rest_framework.response import Response 
from ..models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from ..models import EnglishWords

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
from api.models import Word_infos
import openai
import traceback
from openai import OpenAI
from django.http import JsonResponse
import requests


class EnglishWordSearchAPIView(viewsets.ViewSet):
    def list(self, request):
    # 从请求中获取搜索词
        search = request.GET.get('search_word', '').strip()  # 增加.strip()以移除可能的前后空格

        # 基于搜索词进行QuerySet过滤，只选择word字段，限制为前15个结果
        words = EnglishWords.objects.filter(
        Q(word__istartswith=search)
        ).values_list('word', flat=True)[:15]

        # 将结果转为列表，因为values_list返回的是QuerySet
        words_list = list(words)
        print(list(words))
        # 返回序列化后的数据
        print(search + "1")
        
        return JsonResponse(words_list, safe=False)

last_word = None
#畫面結果後端
class result(viewsets.ViewSet):
    #獲取查詢單字
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
    #把單字傳回前端顯示
    @action(methods=['GET'], url_path='get_last_word', detail=False)
    def get_last_word(self, request):
        # 返回存储的单词
        return JsonResponse({'status': 'success', 'word': last_word})
    #比對單字是否匹配
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
    #搜尋結果圖片
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
                    new_sentence = Word_infos(word=english_word, sentence=generated_sentence)
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
