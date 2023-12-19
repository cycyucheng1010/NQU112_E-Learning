from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets,permissions
from .serializers import ProjectSerializer,Project,UserSerializer,User
from rest_framework.response import Response 
from .models import Project
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
# Create your views here.

# def home(request):
#     return HttpResponse('this is the homepage')



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
    @action(detail=False, methods=['GET'], url_path='gsat')
    #學測
    def GSAT_exam(self, request):
    
        if request.method == 'GET':
            data = request.data
            fromexamtype = data.get('fromexamtype')
            year = data.get('fromexamnum')
            now = datetime.now()
            correct_answers = {}
            stu_answers = request.POST
            stu_grade = 0


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

            # 保存学生成绩记录
            record_grade = student_scores(subject=year, score=stu_grade, timestamp=now)
            record_grade.save()


            print(str(stu_answers) + "答案")
            print(question_number)
            print(correct_answers)
            print(stu_grade)




            if fromexamtype == '學測':
                if 103 <= year <= 112:

                    response_data = generate_test_paper(request, year)
                return JsonResponse(response_data)

        
def generate_test_paper(request, selected_year):



    test_papers_models = [
                        (EnglishOptionalNumber1, 'questions_optional_number1'),
                        (EnglishOptionalNumber2, 'questions_optional_number2'),
                        (EnglishOptionalNumber3, 'questions_optional_number3'),
                        (EnglishOptionalNumber4, 'questions_optional_number4'),
                        (EnglishOptionalNumber5, 'questions_optional_number5'),
                        (OptionalTopicNumber2, 'questions_optionaltopic_number2'),
                        (OptionalTopicNumber3, 'questions_optionaltopic_number3'),
                        (OptionalTopicNumber5, 'questions_optionaltopic_number5'),
    ]
    exam_testpaper_year = []

    for models, field_name in test_papers_models:
        years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()

        for year in years:
            questions = models.objects.filter(year=year)
            exam_paper = ExamPaper.objects.create(
            name=f"Exam {year} ({selected_year})",
            description=f"Exam paper for the year {year}"
            )
            field = getattr(exam_paper, field_name)
            field.add(*questions)
            exam_testpaper_year.append(exam_paper)

                    # Assuming you have other specific data for each group
            group2_1 = OptionalTopicNumber2.objects.get(topic_number=f"{selected_year}-1")
            group2_2 = OptionalTopicNumber2.objects.get(topic_number=f"{selected_year}-2")
            group3_1 = OptionalTopicNumber3.objects.get(topic_number=f"{selected_year}-1")
            group5_1 = OptionalTopicNumber5.objects.get(topic_number=f"{selected_year}-1")
            group5_2 = OptionalTopicNumber5.objects.get(topic_number=f"{selected_year}-2")
            group5_3 = OptionalTopicNumber5.objects.get(topic_number=f"{selected_year}-3")
                    # Prepare data to be sent as JSON
    data = {
                'exam_paper': {
                    'name': f"Exam {selected_year}",
                    'description': f"Exam paper for the year {selected_year}",
                    'questions': [question.serialize() for question in ExamPaper.objects.get(name=f"Exam {selected_year}").questions.all()]
            },
                    'exam_testpaper_year': [paper.serialize() for paper in exam_testpaper_year], 
                    'group2_1': group2_1.serialize(),
                    'group2_2': group2_2.serialize(),
                    'group3_1': group3_1.serialize(),
                    'group5_1': group5_1.serialize(),
                    'group5_2': group5_2.serialize(),
                    'group5_3': group5_3.serialize(),
                    'selected_year': selected_year,
                }

    # Return JSON response
    return JsonResponse(data)