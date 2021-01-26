from rest_framework import serializers

from .models import *
from .main import *
import numpy as np
from PIL import Image
from django.core.files.storage import default_storage
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User


class BaseImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.ReadOnlyField()
    class Meta:
        model = BaseImage
        read_only_fields = ['id',]
        fields = ('id','user', 'name', 'image', 'pt1', 'pt2')

class ProcessedImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProcessedImage
        fields =  "__all__"

class ProcessedImageGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    base = BaseImageSerializer(read_only=True)
    images = ProcessedImageSerializer(many=True,read_only=True)
    class Meta:
        model = ProcessedImageGroup
        fields =  ('user','base', 'name', 'images')

class ImagesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = ProcessedImageSerializer(many=True)
    
    class Meta:
        model = ProcessedImageGroup
        fields = ['user','base', 'name', 'images']