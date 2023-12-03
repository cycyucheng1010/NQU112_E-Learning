from django.contrib import admin
from .models import*

admin.site.register(Project)

# Register your models here.

from .models import(EnglishWord)
admin.site.register(EnglishWord)




