from django.urls import path
from .views import ProjectViewset, UserViewset
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
urlpatterns = router.urls

# urlpatterns =[
#    path('chat/', chatgpt_request, name='chatgpt_request'),
#     path('',home)
# ]