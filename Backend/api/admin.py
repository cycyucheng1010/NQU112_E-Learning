from django.contrib import admin
from .models import*
admin.site.register(Project)

from .models import EnglishOptional
admin.site.register(EnglishOptional)

from .models import EnglishOptionalNumber4
admin.site.register(EnglishOptionalNumber4)

from .models import EnglishOptionalNumber5
admin.site.register(EnglishOptionalNumber5)

from .models import OptionalTopic
admin.site.register(OptionalTopic)

from .models import EnglishTopic
admin.site.register(EnglishTopic)

from .models import EnglishOptionalNumber2
admin.site.register(EnglishOptionalNumber2)

from .models import (OptionalTopicNumber2)
admin.site.register(OptionalTopicNumber2)

from .models import(OptionalTopicNumber4)
admin.site.register(OptionalTopicNumber4)

from .models import(ExamPapers)
admin.site.register(ExamPapers)

from .models import(EnglishWord)
admin.site.register(EnglishWord)