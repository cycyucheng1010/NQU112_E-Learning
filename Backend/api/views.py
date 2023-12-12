from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from .models import *
from django.db.models import Q
import requests
from datetime import datetime


class ProjectViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    
    serializer_class = ProjectSerializer

    def list(self, request):
        queryset = Project.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project,data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        project.delete()
        return Response(status=204)

 #英文資料庫
class EnglishWordSearchAPIView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = EnglishSerializer

    def list(self, request):
        search = request.query_params.get('search','')

        #模糊搜尋
        queryset = EnglishWord.objects.filter(
            Q(wordicontains=search) | Q(explainicontains=search)
        )
        tag = "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/" + search
        print(tag)
        context = {
            'search': search,
            'english_words': queryset,
            'tag' : tag,
        }
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

#考試介面
class exam(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ExamSerializer

    def submit_exam(request):
        if request.method == 'POST':
            stu_answers = request.POST
            year = request.POST.get("year")
            now = datetime.now()
            correct_answers = {}
            stu_grade = 0

        # 获取该年份的考卷正确答案
            exam_paper = EnglishOptionalNumber1.objects.filter(year=year)#抓資料夾
            for question in exam_paper:
                correct_answers[question.id] = question.answer
        
        # 逐个比较学生答案和正确答案
            for question_id, stu_answer_list in stu_answers.items():
                if question_id.startswith("paper_"):  # 检查是否是问题答案字段
                    question_number = int(question_id.replace("paper_", ""))  # 获取问题编号
                    correct_answer = correct_answers.get(question_number)
   
                    if correct_answer and stu_answer_list:
                        stu_answer = stu_answer_list[0]  # 从列表中获取答案
                        if stu_answer == correct_answer:  # 比较答案
                            stu_grade += 1