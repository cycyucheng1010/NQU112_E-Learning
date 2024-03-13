from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import viewsets
import traceback
import time

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

                # 根据消息类型选择调用相应的函数
                if message_type == 'article':
                    generated_text = generate_article()
                    list_articles.append(generated_text)
                elif message_type == 'question':
                    if not list_articles:
                        return JsonResponse({"error": "No article available for generating questions."})
                    generated_text = generate_question(list_articles[-1])
                    list_questions.append(generated_text)
                elif message_type == 'answer':
                    if not list_articles or not list_questions:
                        return JsonResponse({"error": "No article or questions available for generating answers."})
                    generated_text = generate_answer(list_articles[-1], list_questions[-1])

                return JsonResponse({"response": generated_text})

            except Exception as e:
                traceback.print_exc()
                return JsonResponse({"error": str(e)})

        return JsonResponse({"msg": "Invalid request method"})

def generate_article():
    messages = [
        {"role": "system", "content": "You are an English teacher. I am a student"},
        {"role": "user", "content": "Compose a 300-word reading comprehension passage suitable for the level of a standardized test, similar to the difficulty of a typical academic examination. The article should not be restricted to a specific subject and should align with the complexity typically found in such assessments."},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=600,
    )
    generated_text = response.choices[0].message.content
    if generated_text.strip():
        print("Generated article:", generated_text)
    else:
        print("Generated article is empty.")
    return generated_text

def generate_question(article):
    messages = [
        {"role": "system", "content": article},
        {"role": "user", "content": "Write 3 reading comprehension questions based on the above article and provide four options for each question "},
    ]
    time.sleep(2)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
    )
    generated_text = response.choices[0].message.content
    print("Generated question:", generated_text)
    return generated_text

def generate_answer(article, question):
    messages = [
        {"role": "system", "content": question},
        {"role": "user", "content": "Can you help me answer user questions? Provide the correct answer, and the format requires the only correct option and no content is required"},
    ]
    time.sleep(2)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
    )
    generated_text = response.choices[0].message.content
    print("Generated answer:", generated_text)
    return generated_text