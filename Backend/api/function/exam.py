from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets,permissions
from ..serializers import ProjectSerializer,Project,UserSerializer,User,EnglishSerializer,ExamPaperSerializer
from rest_framework.response import Response 
from ..models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from ..models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
import traceback
#from gpt import gpt_process
#考試介面

class ExamViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    @action(methods=['GET'], url_path='gept', detail=False)
    #全民英檢
    def GEPT_exam(request, year):
        '''
        if request.method == 'POST':
            data = request.data
            fromexamtype = data.get('fromexamtype')
            fromexamnum = data.get('fromexamnum')

            if fromexamtype == '全民英檢':

                serializer = ExamPaperSerializer
                queryset = ExamPaper.objects.all()

            

            # 返回响应，可以是一个简单的成功消息
            return Response({"message": "User registered successfully."})
        else:
            # 如果不是 POST 请求，可以返回相应的错误消息
           return Response({"error": "Invalid request method."}, status=400)
        '''

    @csrf_exempt
    @action(detail=False, methods=['GET','POST'], url_path='gsat')
    #學測
    def GSAT_exam(self, request):
        response_data = {}
        if request.method =='POST':
            try:
                data = request.data 
                print(data)
                type = data.get('fromexamtype') # 等於寫法: type= data['fromexamtype']
                year = int(data.get('fromexamnum')) #由於讀近來的數字會是字串所以用int()轉成整數
                print(type)
                print(year)

                if type == '學測':
                    if 103<=year and year<=112:
                        response_data = test_paper(request, year)

                    return JsonResponse(response_data, safe=False)

            except:
                traceback.print_exc() 
                response_data = {"msg":"error"}

            return JsonResponse(response_data)
        
def test_paper(request, year):
    try:
        test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]


        for model_class, field_name in test_papers_models:

            #假设每个模型类都有一个方法用于获取数据
            model_data = model_class.objects.filter(year=year)

            exam_paper = ExamPapers.objects.create(
                name=f"Exam {year} ({field_name})", 
                description=f"Exam paper for the year {year}"
            )

            field = getattr(exam_paper, field_name)

            field.add(*model_data)
        

        group2_1 = EnglishOptionalNumber1.objects.filter(year=f"{year}")

        list1 = []

        for record in group2_1:
            topic_number = record.topic_number
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            data = [
                f"topic_number: {topic_number}",
                f"answer_A: {answer_A}",
                f"answer_B: {answer_B}",
                f"answer_C: {answer_C}",
                f"answer_D: {answer_D}"
            ]
            #list1 = [item.strip() for item in list1]
            list1.extend(data)
            
        print("hi")

        group2_2 = EnglishOptionalNumber2.objects.filter(year=f"{year}")

        list2 = []

        for record in group2_2:
            topic_number = record.topic_number
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            data = [
                f"topic_number: {topic_number}",
                f"answer_A: {answer_A}",
                f"answer_B: {answer_B}",
                f"answer_C: {answer_C}",
                f"answer_D: {answer_D}"
            ]
            list2.extend(data)
        
        print("bbb")

        list3 = []
        group3_1 = OptionalTopicNumber2.objects.filter(year=f"{year}")

        for record in group3_1:
            topic_number = record.topic_number
            topic = record.topic
            data = {
                f"topic_number: {topic_number}",
                f"topic :{topic}"
            }
            list3.extend(data)
        
        print("aaa")

        list4 = []
        group5_1 = OptionalTopicNumber5.objects.filter(year=f"{year}")

        for record in group5_1:
            topic_number = record.topic_number
            topic = record.topic
            data = {
                f"topic_number: {topic_number}",
                f"topic :{topic}"
            }
            list4.extend(data)
        
        print("ccc")

        list5 = []
        group5_2 = OptionalTopicNumber5.objects.filter(year=f"{year}")

        for record in group5_2:
            topic_number = record.topic_number
            topic = record.topic
            data = {
                f"topic_number: {topic_number}",
                f"topic :{topic}"
            }
            list5.extend(data)
        
        print("ddd")

        list6 = []
        group5_3 = OptionalTopicNumber5.objects.filter(year=f"{year}")

        for record in group5_3:
            topic_number = record.topic_number
            topic = record.topic
            data = {
                f"topic_number: {topic_number}",
                f"topic :{topic}"
            }
            list6.extend(data)
        
        print("eee")

        examlist = []
        examlist.extend(list1)
        examlist.extend(list2)
        examlist.extend(list3)
        examlist.extend(list4)
        examlist.extend(list5)
        examlist.extend(list6)

        return {"msg": "success", "examlist": examlist}
    
    except:
        traceback.print_exc() 

    return {"msg": "def error"}
'''
            # 获取该年份的考卷正确答案
            exam_paper = EnglishOptionalNumber1.objects.filter(year=year)
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



#保存學生成績
@csrf_exempt  
@action(detail=False, methods=['GET'], url_path='grade')
def save_grade(request):
    if request.method == 'GET':
        data = json.loads(request.body)

        stu_answers = data.get('stu_answers', '')
        question_number = data.get('question_number', '')
        correct_answers = data.get('correct_answers', '')
        stu_grade = data.get('stu_grade', '')
        message= {"abc":"hello"}
        return Response("message")

        # 在這裡進行保存成績的邏輯
        record_grade = StudentScores(
            subject=question_number,  
            score=stu_grade,
            timestamp=datetime.now(),
        )
        record_grade.save()

        return JsonResponse({'message': 'Grade saved successfully'})

    return JsonResponse({'error': 'Invalid request method'})
'''