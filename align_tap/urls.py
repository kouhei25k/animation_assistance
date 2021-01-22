
from rest_framework import routers
from .views import *
from django.urls import path, include
from . import views



router = routers.DefaultRouter()
router.register(r'base_image', BaseImageViewSet)
router.register(r'processed_image', ProcessedImageViewSet)
router.register(r'image_group', ImageGroupViewSet)
# router.register(r'download', DownloadViewSet)
# router.register(r'create_processed_image', CreateProcessedImageViewSet)
# router.register(r'user', UserDetailsView)



