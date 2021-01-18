from rest_framework import serializers

from .models import *
from .main import *
import numpy as np
from PIL import Image
from django.core.files.storage import default_storage

class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseImage
        fields = ('name', 'image', 'pt1', 'pt2')


class UnprocessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnprocessedImage
        fields = ('image',)

    

class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = ('base', 'image')
