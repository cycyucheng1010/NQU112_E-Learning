from django.urls import path
from .views import ProjectViewset, UserViewset, SentenceAPIView, ImageAPIView
from rest_framework.routers import DefaultRouter
from .function.exam import ExamViewset

router = DefaultRouter()
router.register('project', ProjectViewset, basename='project')
router.register('user', UserViewset, basename='user')
router.register('exam', ExamViewset, basename='exam')

urlpatterns = router.urls

# 使用 += 運算符將新的路徑添加到現有的 urlpatterns 列表
urlpatterns += [
    path('api/sentence/', SentenceAPIView.as_view(), name='api-sentence'),
    path('api/image/', ImageAPIView.as_view(), name='api-image'),
    # 可以在這裡添加其他路徑
    # path('your_path/', YourView.as_view(), name='your-view-name'),
]

#router.register('search',EnglishWordSearchAPIView,basename='search')
