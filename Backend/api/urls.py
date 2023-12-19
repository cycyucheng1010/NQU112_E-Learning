from django.urls import path
from .views import ProjectViewset, UserViewset, ExamViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')
urlpatterns = router.urls
# urlpatterns =[

#     path('',home)
# ]