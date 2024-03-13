from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import viewsets
import traceback
import re

class QuestionView(viewsets.ViewSet):
    @csrf_exempt
    @action(detail=False, methods=['POST'], url_path='reading_answer')
    def Question(self, request):
        if request.method == 'POST':
            try:
                data = request.data
                message_type = data.get('message_type')
                user_answer = data.get('user_answer')
                gpt_answer = data.get('gpt_answer')
                
                if message_type == 'correctanswer':
                    # 提取选项并格式化成与 user_answer 相同的格式
                    formatted_user_answer = self.format_answer(user_answer)
                    formatted_gpt_answer = self.format_answer(gpt_answer)

                    print(user_answer)
                    print(formatted_gpt_answer)

                    # 比较答案
                    comparison_result = self.compare_answers(formatted_user_answer, formatted_gpt_answer)

                    return JsonResponse({'comparison_result': comparison_result})
                else:
                    pass

            except Exception as e:
                traceback.print_exc()
                return JsonResponse({"error": str(e)})
        else:
            return JsonResponse({"error": "Invalid request method"})

    @staticmethod
    def extract_options(text):
        options = re.findall(r'\d+\.\s*([A-D])', text)
        return [option[-1] for option in options]

    @staticmethod
    def format_answer(answer):
        # 提取选项
        options = re.findall(r'\d+\.\s*([A-D])', answer)
        # 格式化成与 user_answer 相同的格式
        formatted_answer = ','.join(options)
        return formatted_answer

    @staticmethod
    def compare_answers(user_answer, gpt_answer):
        user_options = user_answer.split(',')
        gpt_options = gpt_answer.split(',')

        result = []
        for user_option, gpt_option in zip(user_options, gpt_options):
            if user_option == gpt_option:
                result.append(0)  # 选项匹配
            else:
                result.append(1)  # 选项不匹配
        
        print(result)
        return result