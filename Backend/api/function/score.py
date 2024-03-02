from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,permissions
from rest_framework.response import Response 
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from ..models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPapers,StudentScores,EnglishTopic
from django.views.decorators.csrf import csrf_exempt
import traceback
import json


#計算分數 計分方式用 XX (做答對的分數) / 100(總題數假設100)
#一題用一分的方式計算
class ScoreViewset(viewsets.ViewSet):
    
    @csrf_exempt
    @action(methods=['POST'], url_path='user_score', detail = False)
    def score_process(self, request):

        Score_data = {}

        if request.method == 'POST' :
            try :

                data = request.data
                print(data)
                
                user_answer = data.get('useranswer') #後端接收到使用者的作答
                year = int(data.get('fromexamnum'))#抓該年分的答案

                #測試
                print(year)
                print(user_answer)

                #將總分塞到data
                if 103<=year and year<=112:
                    Score_data = answer_process(request ,user_answer, year)
                #回傳分數給前端
                return JsonResponse(Score_data, safe=False)

            except :
                traceback.print_exc() 
                response_data = {"msg":"error"}
            
            return Response(response_data)

def process_list5(year):

    if year == 110:
        return False
    if year == 111:
        return False
    if year == 112:
        return False

    return True

def list5_processing_logic():
    pass        
#對答案 然後抓寫正確的題數        
def answer_process(request ,user_answer, year):

    try : 
        #將原本生成題目方式改成生成答案
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

        for record in group1:
            answer = record.answer
            data = [
                f"answer: {answer}",
            ]
            list1.extend(data)

        group2 =  EnglishOptionalNumber2.objects.filter(year=f"{year}")
        list2 = []

        for record in group2:
            answer = record.answer
            data = [
                f"answer: {answer}",
            ]
            list2.extend(data)

        group3 =  EnglishOptionalNumber3.objects.filter(year=f"{year}")
        list3 = []

        for record in group3:
            answer = record.answer
            data = [
                f"answer: {answer}",
            ]
            list3.extend(data)

        group4 =  EnglishOptionalNumber4.objects.filter(year=f"{year}")
        list4 = []

        for record in group4:
            answer = record.answer
            data = [
                f"answer: {answer}",
            ]
            list4.extend(data)

        group5 =  EnglishOptionalNumber5.objects.filter(year=f"{year}")
        list5 = []

        for record in group5:
            answer = record.answer
            data = [
                f"answer: {answer}",
            ]
            list5.extend(data)

        #輸出正確答案
        correct_answer = []
        correct_answer.extend(list1)
        correct_answer.extend(list2)
        correct_answer.extend(list3)
        correct_answer.extend(list4)
        correct_answer.extend(list5)

        #記錄每大題得分
        l1 = 0
        l2 = 0
        l3 = 0 
        l4 = 0
        l5 = 0

        #記錄每大題的總分
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0

        for item1, item2 in zip(user_answer, list1):
            if item1 == item2:
                l1 += 1
        for item1, item2 in zip(user_answer, list2):
            if item1 == item2:
                l2 += 1
        for item1, item2 in zip(user_answer, list3):
            if item1 == item2:
                l3 += 1
        for item1, item2 in zip(user_answer, list4):
            if item1 == item2:
                l4 += 2
        if list5:
            for item1, item2 in zip(user_answer, list5):
                if item1 == item2:
                    l5 += 2
        #得分
        user_score = l1 + l2 +l3 +l4 +l5

        for item1, item2 in zip(list1, list1):
            if item1 == item2:
                s1 += 1
        for item1, item2 in zip(list2, list2):
            if item1 == item2:
                s2 += 1
        for item1, item2 in zip(list3, list3):
            if item1 == item2:
                s3 += 1
        for item1, item2 in zip(list4, list4):
            if item1 == item2:
                s4 += 2
        if list5:
            for item1, item2 in zip(list5, list5):
                if item1 == item2:
                    s5 += 2
        #總分
        total_score = s1 + s2 +s3 +s4 +s5

        response_data = {
            "user score": user_score,
            "total score": total_score,
            "correct answer": correct_answer,
        }
        return response_data
    except:
        traceback.print_exc() 
        response_data = {"msg":"answer_error"}

    return response_data

'''

        while index < len(user_answer) and index < len(examlist):
            item1 = user_answer[index].split(" ")[-1]  # 只取最後一個字元
            item2 = examlist[index].split(" ")[-1]  # 只取最後一個字元

            print(f"item1: {item1}, item2: {item2}")

            if item1 == item2:
                matches += 1
                print(matches)
                if item2 in list4 or item2 in list5:
                    # 如果答案在list4或list5中，且答案與解答相同，加 1 分
                    matches += 2
                    print(matches)
            else:
                mismatches += 1

            index += 1
'''