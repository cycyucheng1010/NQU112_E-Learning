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
import time
import os

client = OpenAI(api_key="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")
list_articles = [] 
list_questions = [] 
list_answer  = []

class ReadingView(viewsets.ViewSet):
    @csrf_exempt
    @action(detail=False, methods=['POST'], url_path='reading_question')
    def gpt(self, request):
        global list_articles
        global list_questions

        if request.method == 'POST':

            try:

                data = request.data
                message_type = data.get('message_type')
                

                generated_text = ""

                # 根据消息类型选择发送的消息
                if message_type == 'article':

                    messages = [
                        {"role": "system", "content": "You are an English teacher. I am a student"},
                        {"role": "user", "content": "Compose a 300-word reading comprehension passage suitable for the level of a standardized test, similar to the difficulty of a typical academic examination. The article should not be restricted to a specific subject and should align with the complexity typically found in such assessments."},
                    ]

                    # 发送消息给 GPT
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=500,
                    )

                    # 获取生成的文本
                    generated_text = response.choices[0].message.content

                    # 检查生成的文本是否为空字符串
                    if generated_text.strip():

                        list_articles.append(generated_text)
                        print("Generated article:", generated_text)
                        print("List of articles:", list_articles)

                    else:

                        print("Generated article is empty. Skipping adding to list.")

                elif message_type == 'question':

                    if not list_articles:
                        print("No article available for generating questions.")
                        return JsonResponse({"error": "No article available for generating questions."})

                    # 取最新一篇文章生成問題
                    last_article = list_articles[-1]

                    messages = [
                        {"role": "system", "content": last_article},
                        {"role": "user", "content": "Write 3 reading comprehension questions based on the above article and provide four options for each question "},
                    ]

                    # 在這裡加入等待，給生成文章的請求足夠的時間
                    time.sleep(5)  

                    # 發送消息給 GPT
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=300,
                    )

                    # 獲取生成的文本
                    generated_text = response.choices[0].message.content

                    list_questions.append(generated_text)
                    print("Generated question:", generated_text)
                    print("List of questions:", list_questions)


                elif message_type == 'answer':
                    
                    last_article = list_articles[-1]
                    last_questions = list_questions[-1]

                    print(list_articles)
                    print(list_questions)

                    messages = [
                        {"role": "system", "content": last_questions},
                        {"role": "user", "content": "Can you help me answer the user's question? Provide the correct answer indicated in UPPERCASE."},
                    ]

                    # 在這裡加入等待，給生成文章的請求足夠的時間
                    time.sleep(5)  

                    # 發送消息給 GPT
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=300,
                    )

                    # 獲取生成的文本
                    generated_text = response.choices[0].message.content

                    list_answer.append(generated_text)


                # 返回生成的文本给前端
                return JsonResponse({"response": generated_text})

            except Exception as e:
                traceback.print_exc()
                return JsonResponse({"error": str(e)})

        return JsonResponse({"msg": "Invalid request method"})
            