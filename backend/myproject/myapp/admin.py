from django.contrib import admin
from .models import User  # 導入你的模型

admin.site.register(User)  # 註冊模型
