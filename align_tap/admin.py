from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(BaseImage)
admin.site.register(UnprocessedImage)
admin.site.register(ProcessedImage)
