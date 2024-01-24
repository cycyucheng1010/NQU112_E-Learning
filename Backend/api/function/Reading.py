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
                print(data)

                article = data.get('article')
                question = data.get('question')



                print(data)

                # 根据消息类型选择发送的消息
                if message_type == 'article':
                    messages = [
                        {"role": "system", "content": "You are an English teacher. I am a student"},
                        {"role": "user", "content":  "Write a No subject limit 100-word article."},
                    ]
                    list_article = []
                    list_article.extend(messages)

                elif message_type == 'question':
                    messages = [
                        {"role": "system", "content": list_article},
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
            

            