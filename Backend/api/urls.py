from django.urls import path
from .views import ProjectViewset, UserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('project',ProjectViewset,basename='project')
router.register('user', UserViewset, basename='user')
urlpatterns = router.urls
# urlpatterns =[

#     path('',home)
# ]
