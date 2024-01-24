from django.urls import path
from .views import ProjectViewset, UserViewset
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset
from .function.gpt import GPTView
from .function.score import ScoreViewset
from .function.Reading import ReadingView


router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
router.register('chatgpt', GPTView, basename='chatgpt')
router.register('score', ScoreViewset, basename='score')
router.register('reading', ReadingView, basename='reading')
urlpatterns = router.urls

#urlpatterns =[
#     path('',home)
# ]
