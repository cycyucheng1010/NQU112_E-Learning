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
from ..models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber4,OptionalTopicNumber5, ExamPapers,StudentScores
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
import traceback
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
        if request.method == 'POST':
            try:
                data = request.data
                print(data)
                type = data.get('fromexamtype')
                fromexamnum = data.get('fromexamnum')

                # 检查 fromexamnum 是否为 None
                if fromexamnum is not None:
                    year = int(fromexamnum)
                    print(type)
                    print(year)

                    if type == '學測':
                        if 103 <= year <= 112:
                            response_data = test_paper(request, year)
                        return JsonResponse(response_data, safe=False)
                    else:
                        response_data = {"msg": "Invalid exam type"}
                else:
                    response_data = {"msg": "fromexamnum is None"}

            except:
                response_data = {"msg": "error"}

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
        

        group1 =  EnglishOptionalNumber1.objects.filter(year=f"{year}")

        list1 = []
        list1a =[]
        list1b =[]
        list1c = []
        list1d = []
        list1topic = []
        list1topicnumber = []

        for record in group1:
            topic_number = record.topic_number
            topic = record.topic
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            TOPIC_NUMBER = [
                f"topic_number: {topic_number}",
            ]
            TOPIC = [
                f"topic :{topic}",
            ]
            A = [
                f"answer_A: {answer_A}",
            ]
            B = [
                f"answer_B: {answer_B}",
            ]
            C = [
                f"answer_C: {answer_C}",
            ]
            D = [
                f"answer_D: {answer_D}",
            ]
            #list1 = [item.strip() for item in list1]
            list1a.extend(A)
            list1b.extend(B)
            list1c.extend(C)
            list1d.extend(D)
            list1topic.extend(TOPIC)
            list1topicnumber.extend(TOPIC_NUMBER)


        group2_1 =  OptionalTopicNumber2.objects.filter(year=f"{year}")

        list2topic  = []

        for record in group2_1 :
            
            topic = record.topic
            TOPIC = {
               
                f"topic :{topic}",
            }
            list2topic.extend(TOPIC)

        group2 =  EnglishOptionalNumber2.objects.filter(year=f"{year}")

        list2 = []
        list2a =[]
        list2b =[]
        list2c = []
        list2d = []
        list2topicnumber = []


        for record in group2:
            topic_number = record.topic_number
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            TOPIC_NUMBER = [
                f"topic_number: {topic_number}",
            ]
            A = [
                f"answer_A: {answer_A}",
            ]
            B = [
                f"answer_B: {answer_B}",
            ]
            C = [
                f"answer_C: {answer_C}",
            ]
            D = [
                f"answer_D: {answer_D}",
            ]
            list2a.extend(A)
            list2b.extend(B)
            list2c.extend(C)
            list2d.extend(D)
            list2topicnumber.extend(TOPIC_NUMBER)


        list3_1topic = []
        group3_1 = OptionalTopicNumber3.objects.filter(year=f"{year}")

        for record in group3_1:
            
            topic = record.topic
            TOPIC = {
                f"topic :{topic}",
            }
            list3_1topic.extend(TOPIC)

        group3 =  EnglishOptionalNumber3.objects.filter(year=f"{year}")

        list3 = []
        list3a = []
        list3b = []
        list3c = []
        list3d = []
        list3e = []
        list3f = []
        list3g = []
        list3h = []
        list3i = []
        list3j = []
        list3topic = []
        list3topicnumber = []

        for record in group3:
            topic_number = record.topic_number
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            answer_E = record.answer_E
            answer_F = record.answer_F
            answer_G = record.answer_G
            answer_H = record.answer_H
            answer_I = record.answer_I
            answer_J = record.answer_J
            TOPIC_NUMBER = [
                f"topic_number: {topic_number}",
            ]
            TOPIC = [
                f"topic :{topic}",
            ]
            A = [
                f"answer_A: {answer_A}",
            ]
            B = [
                f"answer_B: {answer_B}",
            ]
            C = [
                f"answer_C: {answer_C}",
            ]
            D = [
                f"answer_D: {answer_D}",
            ]
            E = [
                f"answer_E: {answer_E}",
            ]
            F = [
                f"answer_F: {answer_F}",
            ]
            G = [
                f"answer_G: {answer_G}",
            ]
            H = [
                f"answer_H: {answer_H}",
            ]
            I = [
                f"answer_I: {answer_I}",
            ]
            J = [
                f"answer_J: {answer_J}",
            ]

            list3a.extend(A)
            list3b.extend(B)
            list3c.extend(C)
            list3d.extend(D)
            list3e.extend(E)
            list3f.extend(F)
            list3g.extend(G)
            list3h.extend(H)
            list3i.extend(I)
            list3j.extend(J)
            list3topicnumber.extend(TOPIC_NUMBER)
            list3topic.extend(TOPIC)


        list4_1topic = []
        group4_1 = OptionalTopicNumber4.objects.filter(year=f"{year}")

        for record in group4_1:
           
            topic = record.topic
            TOPIC= {
               
                f"topic :{topic}",
            }
            list4_1topic.extend(TOPIC)

        list4 = []
        list4a = []
        list4b = []
        list4c = []
        list4d = []
        list4topicnumber = []
        list4topic =[]
        
        group4 = EnglishOptionalNumber4.objects.filter(year=f"{year}")
        for record in group4:
            topic_number = record.topic_number
            topic = record.topic
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            TOPIC_NUMBER = [
                f"topic_number: {topic_number}",
            ]
            TOPIC = [
                f"topic :{topic}",
            ]
            A = [
                f"answer_A: {answer_A}",
            ]
            B = [
                f"answer_B: {answer_B}",
            ]
            C = [
                f"answer_C: {answer_C}",
            ]
            D = [
                f"answer_D: {answer_D}",
            ]
            list4a.extend(A)
            list4b.extend(B)
            list4c.extend(C)
            list4d.extend(D)
            list4topicnumber.extend(TOPIC_NUMBER)
            list4topic.extend(TOPIC)

        list5_1topic = []
        group5_1 = OptionalTopicNumber5.objects.filter(year=f"{year}")

        for record in group5_1:
            
            topic = record.topic
            TOPIC = {
                
                f"topic :{topic}",
            }
            list5_1topic.extend(TOPIC )

        list5 = []
        list5a = []
        list5b = []
        list5c = []
        list5d = []
        list5topicnumber = []
        list5topic =[]

        group5 = EnglishOptionalNumber5.objects.filter(year=f"{year}")
        for record in group5:
            topic_number = record.topic_number
            topic = record.topic
            answer_A = record.answer_A
            answer_B = record.answer_B
            answer_C = record.answer_C
            answer_D = record.answer_D
            TOPIC_NUMBER = [
                f"topic_number: {topic_number}",
            ]
            TOPIC = [
                f"topic :{topic}",
            ]
            A = [
                f"answer_A: {answer_A}",
            ]
            B = [
                f"answer_B: {answer_B}",
            ]
            C = [
                f"answer_C: {answer_C}",
            ]
            D = [
                f"answer_D: {answer_D}",
            ]

            
            list5a.extend(A)
            list5b.extend(B)
            list5c.extend(C)
            list5d.extend(D)
            list5topicnumber.extend(TOPIC_NUMBER)
            list5topic.extend(TOPIC)

            list6 = []

        list7 = []
        list8 = []
        list9 = []
        list10 = []
        list11= []
        list12= []


        list7.extend(list3e)
        list8.extend(list3f)
        list9.extend(list3g)
        list10.extend(list3h)
        list11.extend(list3i)
        list12.extend(list3j)

        list1.extend(list1a)
        list1.extend(list2a)
        list1.extend(list3a)
        list1.extend(list4a)
        list1.extend(list5a)

        list2.extend(list1b)
        list2.extend(list2b)
        list2.extend(list3b)
        list2.extend(list4b)
        list2.extend(list5b)

        list3.extend(list1c)
        list3.extend(list2c)
        list3.extend(list3c)
        list3.extend(list4c)
        list3.extend(list5c)

        list4.extend(list1d)
        list4.extend(list2d)
        list4.extend(list3d)
        list4.extend(list4d)
        list4.extend(list5d)

        list5.extend(list1topic)
        list5.extend(list2topic)
        list5.extend(list3topic)
        list5.extend(list4topic)
        list5.extend(list5topic)
        list5.extend(list3_1topic)
        list5.extend(list4_1topic)
        list5.extend(list5_1topic)

        list6.extend(list1topicnumber)
        list6.extend(list2topicnumber)
        list6.extend(list3topicnumber)
        list6.extend(list4topicnumber)
        list6.extend(list5topicnumber)

        
        return { "list1": list1,"list2": list2,"list3": list3,"list4": list4,"list5": list5,"list6": list6,}
    
    except:
        traceback.print_exc() 

    return {"msg": "def error"}
'''

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


    
        examlist = []
        examlist.extend(list1)
        examlist.extend(list2_1)
        examlist.extend(list2)
        examlist.extend(list3_1)
        examlist.extend(list3)
        examlist.extend(list4_1)
        examlist.extend(list4)
        examlist.extend(list5_1)
        examlist.extend(list5)
'''
'''

'''
