from rest_framework import serializers

from .models import *
from .main import *
import numpy as np
from PIL import Image
from django.core.files.storage import default_storage
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User

# class UserSerializer(UserDetailsSerializer):
#     class Meta:
#         model = User
#         fields ='__all__'


class BaseImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BaseImage
        fields = ('user','name', 'image', 'pt1', 'pt2')

class ProcessedImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ProcessedImage
        fields = ('user','base', 'image')


class ImageGroupSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ImageGroup
        fields = ('user','name')



class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

class CreateProcessedImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = ImageSerializer(many=True)
    class Meta:
        model = ProcessedImage
        fields = ('user','base', 'image')


