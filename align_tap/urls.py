
from rest_framework import routers
from .views import *
from django.urls import path, include
from . import views




router = routers.DefaultRouter()
router.register(r'base_image', BaseImageViewSet)
router.register(r'unprocessed_image', UnprocessedImageViewSet)
router.register(r'processed_image', ProcessedImageViewSet)



