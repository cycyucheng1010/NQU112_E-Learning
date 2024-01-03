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

#class GPTView(APIView): 
class GPTView(viewsets.ViewSet): 
    @csrf_exempt
    @action(detail=False, methods=['GET','POST'], url_path='gpt')
    def gpt (self, request):
        if request.method =='POST':
            try:
                list = []
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[
                        {"role": "system", "content": "You are a English teacher."},
                        {"role": "user", "content": "give me a english word"}
                    ],
                    max_tokens=50
                )
                
                data = response.choices[0].message.content
                list.append(data)
                
                return JsonResponse({"msg": "success","data": list})
                
            except Exception as e:
                traceback.print_exc() 
                return JsonResponse({"msg": "error"})

#gpt_view = GPTView.as_view()
