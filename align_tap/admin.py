from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(BaseImage)
admin.site.register(ProcessedImage)
admin.site.register(ProcessedImageGroup)

