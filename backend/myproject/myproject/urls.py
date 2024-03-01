from django.contrib import admin
from django.urls import path
from myapp.views import test_view, register, login, home  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/test/', test_view, name='test'),
    path('', home, name='home'),  
]
