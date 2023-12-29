from django.urls import path
from .views import ProjectViewset, UserViewset, ExamViewset,EnglishWordSearchAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
router.register('search',EnglishWordSearchAPIView,basename='search')
urlpatterns = router.urls
# urlpatterns =[

#     path('',home)
# ]