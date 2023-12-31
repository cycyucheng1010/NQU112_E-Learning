from django.urls import path
from .views import ProjectViewset, UserViewset#,EnglishWordSearchAPIView
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset
#from .views import generate_sentence, generate_image

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
#router.register('search',EnglishWordSearchAPIView,basename='search')
urlpatterns = router.urls

# urlpatterns =[
#    path('chat/', chatgpt_request, name='chatgpt_request'),
#    path('generate/sentence/', generate_sentence, name='generate_sentence'),
#    path('generate/image/', generate_image, name='generate_image'),
#     path('',home)
# ]