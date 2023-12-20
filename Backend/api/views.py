from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets,permissions
from .serializers import ProjectSerializer,Project,UserSerializer,User,EnglishSerializer,ExamPaperSerializer
from rest_framework.response import Response 
from .models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishWordSearch,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5, ExamPaper,StudentScores
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
import traceback
#from gpt import gpt_process

class ProjectViewset(viewsets.ViewSet):
    permission_classes =[permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
       queryset = self.queryset
       serializer = self.serializer_class(queryset,many =True)
       return Response(serializer.data)
 
    def create(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
            

    def retrieve(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer =self.serializer_class(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)

    def destroy(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        project.delete()

        return response(status=204)

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset =User.objects.all()

    @action(methods=['POST'],url_path = 'login',detail = False)
    def login(self,request):

        email = request.data.get('email')
        pwd = request.data.get('password')

        res ={
            'code':0,
            'msg' :'',
            'data':{}
        }
        if not all([email,pwd]):
            res['msg'] = '參數異常'
            return Response(res)
        print(request.data)
        try:
            user=User.objects.get(email=email,password=pwd)
        except:
            res['msg'] = '帳號或密碼錯誤請重新登入'
            return Response(res)
        if user.is_active !=1:
            res['msg'] = '用戶不可用，請重新登入'
        
        login(request,user)
        request.session['login'] =True
        request.session['FS_YWPT'] = True
        request.session.set_expiry(0)
        res['msg'] = '登入成功'
        res['code'] = 1
        res['data'] ={'email' :email}
        return Response(res)
    @action(methods=['POST'], url_path='register', detail=False)
    def register(self, request):
        '''
        注册
        :param request: 用于传参数，必要参数 email：邮箱   password：密码  username：用户名 
        :return:
        '''
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        if not all([email, password, username]):
            res['msg'] = '参数异常。'
            return Response(res)

        print([email, password, username])
        if User.objects.filter(username=username):
            res['msg'] = '用户已存在。'
            return Response(res)

        User.objects.create(password=password, is_superuser=0, username=username, email=email)
        res['code'] = 1
        res['data'] = [email, password, username]
        return Response(res)

#英文資料庫
class EnglishWordSearchAPIView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = EnglishSerializer
    queryset = EnglishWordSearch.objects.all()

    def list(self, request):
        search = request.query_params.get('search','')

        #模糊搜尋
        queryset = EnglishWordSearch.objects.filter(
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

                if type == 'abc':
                    if 103<=year and year<=112:
                        response_data = test_paper(request, year)

                    return JsonResponse(response_data, safe=False)

            except:
                traceback.print_exc() 
                response_data = {"msg":"error"}

            return JsonResponse(response_data)
        
def test_paper(request, year):
    try:
        print(year)

        test_paper_model = [
                    EnglishOptionalNumber1,
                    EnglishOptionalNumber2,
                    EnglishOptionalNumber3,
                    EnglishOptionalNumber4,
                    EnglishOptionalNumber5,
                    OptionalTopicNumber2,
                    OptionalTopicNumber3,
                    OptionalTopicNumber5,
                ]

        data_list = []


    except:
        traceback.print_exc() 
        response_data = {"msg":"def error"}

    return response_data

'''
        for model_class in test_paper_model:
            # 假设每个模型类都有一个 get_data 方法用于获取数据
            model_data = model_class.objects.get_data(year)

            options = [
                model_data.answer_A, model_data.answer_B, model_data.answer_C,
                model_data.answer_D, model_data.answer_E, model_data.answer_F,
                model_data.answer_G, model_data.answer_H, model_data.answer_I,
                model_data.answer_J
            ]

            if '題組' in model_data.topic_number:
                # 题组的处理方式
                group_data = {
                    '類別': '題組',
                    '題組': model_data.topic,
                    '題目列表': []
                }

                for i in range(1, 11):
                    # 题组中的每个题目的处理方式
                    question_data = {
                        '題號': str(i),
                        '題目': model_data.topic + str(i),
                        '選項1': 'a',
                        '選項2': 'b',
                        '選項3': 'c',
                        '選項4': 'd',
                    }

                    group_data['題目列表'].append(question_data)

                data_list.append(group_data)

            else:
                # 单选题的处理方式
                single_data = {
                    '類別': '單選',
                    '題號': model_data.topic_number,
                    '題目': model_data.topic,
                    '選項1': 'a',
                    '選項2': 'b',
                    '選項3': 'c',
                    '選項4': 'd',
                }

                data_list.append(single_data)
                
        # Return JSON response
        return data_list

    except:
        traceback.print_exc() 
        response_data = {"msg":"def error"}

    return response_data
'''
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

'''


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
'''