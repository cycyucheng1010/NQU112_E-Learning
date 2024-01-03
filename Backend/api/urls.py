from django.urls import path
from .views import ProjectViewset, UserViewset#,EnglishWordSearchAPIView
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset
from .views import SentenceAPIView, ImageAPIView


router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
#router.register('search',EnglishWordSearchAPIView,basename='search')
urlpatterns = router.urls

urlpatterns =[
    #path('chat/', chatgpt_request, name='chatgpt_request'),
    path('api/sentence/', SentenceAPIView.as_view(), name='api-sentence'),
    path('api/image/', ImageAPIView.as_view(), name='api-image'),
    #path('',home)
 ]