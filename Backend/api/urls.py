from django.urls import path, include  # 导入 include 模块
from rest_framework.routers import DefaultRouter
from .views import ProjectViewset, EnglishWordSearchAPIView, result, register, login  # 导入 register 和 login 视图函数

router = DefaultRouter()
router.register('project', ProjectViewset, basename='project')
router.register('search', EnglishWordSearchAPIView, basename='search')
router.register('result', result, basename='result')

urlpatterns = [
    path('api/', include(router.urls)),  # 将路由器的 URL 添加到 urlpatterns 中，并指定前缀为 'api/'
    path('api/register/', register, name='register'),  # 添加 register 视图函数的 URL
    path('api/login/', login, name='login'),  # 添加 login 视图函数的 URL
]
