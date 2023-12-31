from django.urls import path
from .views import ProjectViewset, UserViewset
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset
from .function.gpt import GPTView

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
router.register('chatgpt', GPTView, basename='chatgpt')
urlpatterns = router.urls

#urlpatterns =[
#     path('',home)
# ]
'''
urlpatterns = router.urls + [
    path('gpt/', GPTView.as_view(), name='gpt'),
    
]'''