from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import django_filters
from rest_framework import viewsets, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from PIL import Image
import json
import os
from dj_rest_auth.views import UserDetailsView
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework import generics, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
# class UserDetailsView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class BaseImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BaseImage.objects.all()
    serializer_class = BaseImageSerializer

    def get_queryset(self):
        user = self.request.user
        return BaseImage.objects.filter(user=user)


class ProcessedImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImage.objects.all()
    serializer_class = ProcessedImageSerializer




class ImageList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImageGroup.objects.all()
    serializer_class = ProcessedImageGroupSerializer
    def get_queryset(self):
        user = self.request.user
        group_name = self.kwargs['group']
        # group = ProcessedImageGroup.objects.get(user=user, name=group_name)
        return ProcessedImageGroup.objects.filter(user=user, name=group_name)


class ProcessedImageGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImageGroup.objects.all()
    serializer_class = ProcessedImageGroupSerializer

    def get_queryset(self):
        user = self.request.user
        return ProcessedImageGroup.objects.filter(user=user)


class ImagesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImageGroup.objects.all()
    serializer_class = ImagesSerializer

    def get_queryset(self):
        user = self.request.user
        return ProcessedImageGroup.objects.filter(user=user)
    
    def create(self,request):

        base_id = request.POST.get('base')
        name = request.POST.get('name')
        image_group = ProcessedImageGroup.objects.create(user=request.user,base_id=base_id,name=name)
        image_group.save()

        base_image_objects = BaseImage.objects.get(pk=base_id)
        base_image = base_image_objects.image

        pt1 = base_image_objects.pt1.split(',')
        pt2 = base_image_objects.pt2.split(',')
        pt1 = [int(s) for s in pt1]
        pt2 = [int(s) for s in pt2]
        pt1 = tuple(pt1)
        pt2 = tuple(pt2)

    
        base = np.array(Image.open(f'media/{base_image}'), dtype=np.uint8)
        kp, des = get_keypoints(base, pt1, pt2)

        in_media_path = f'processed/{request.user.username}/{name}'
        absolute_path =f'media/{in_media_path}'
        if not os.path.isdir(absolute_path):
            os.makedirs(absolute_path)

        
        for image in request.FILES.getlist('images'):
            frame = np.array(Image.open(image), dtype=np.uint8)
            align = get_alignment_img(frame, kp, des)
            aligned_image = Image.fromarray(align)
            aligned_image.save(f'media/{in_media_path}/aligned_{image.name}', "JPEG")
            processed_image = ProcessedImage.objects.create(image=f'{in_media_path}/aligned_{image.name}')
            image_group.images.add(processed_image)


        return Response({'message': 'OK'})


