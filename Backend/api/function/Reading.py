from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import action
import traceback
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
import os

client = OpenAI(api_key="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")

class ReadingView(viewsets.ViewSet): 
    @csrf_exempt
    @action(detail=False, methods=['GET','POST'], url_path='reading_question')
    def gpt (self, request):
        if request.method =='POST':
            try:

                data = request.data
                message_type = data.get('article','question')

                print(data)

                # 根据消息类型选择发送的消息
                if message_type == 'article':
                    messages = [
                        {"role": "system", "content": "You are an English teacher. I am a student"},
                        {"role": "user", "content":  "Write a No subject limit 100-word article."},
                    ]

                elif message_type == 'question':
                    messages = [
                        {"role": "system", "content": "You are an English teacher."},
                        {"role": "user", "content": "And write 1 reading comprehension question based on the above article."},
                    ]
                else:
                    return JsonResponse({"error": "Invalid message type"})

                # 发送消息给 GPT
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=150
                )

                # 獲取生成的文本
                generated_text = response.choices[0].message.content

                # 返回生成的文本給前端
                return JsonResponse({"response": generated_text})
                
            except Exception as e:
                traceback.print_exc() 
                return JsonResponse({"msg": "error"})
            

            