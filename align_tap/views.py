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


class ProcessedImageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImage.objects.all()
    serializer_class = ProcessedImageSerializer

    def get_queryset(self):
        user = self.request.user
        return ProcessedImage.objects.filter(user=user)


class ImageList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImage.objects.all()
    serializer_class = ProcessedImageSerializer

    def get_queryset(self):
        user = self.request.user
        group_name = self.kwargs['group']
        group = ImageGroup.objects.get(user=user, name=group_name)
        return ProcessedImage.objects.filter(user=user, group=group)


class ImageGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ImageGroup.objects.all()
    serializer_class = ImageGroupSerializer

    def get_queryset(self):
        user = self.request.user
        return ImageGroup.objects.filter(user=user)


class CreateProcessedImageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProcessedImage.objects.all()
    serializer_class = CreateProcessedImageSerializer

    def perform_create(self, serializer):
        image_list = []
        for upload_image in self.request.FILES.getlist('image'):
            image = upload_image
            image_name = upload_image.name
            image_list.append(image)

        folder_name = self.request.POST.get('folder')

        print(self.request.POST.get('folder'))
        if self.request.POST.get('folder'):
            print("ファイル名なし！")
            folder_name = image_list[0]
            print(folder_name)
        post_use_base = self.request.POST.get('base')
        base_image_objects = BaseImage.objects.get(id=post_use_base)
        base_image = base_image_objects.image

        pt1 = base_image_objects.pt1.split(',')
        pt2 = base_image_objects.pt2.split(',')
        pt1 = [int(s) for s in pt1]
        pt2 = [int(s) for s in pt2]
        pt1 = tuple(pt1)
        pt2 = tuple(pt2)

        base = np.array(Image.open(f'media/{base_image}'), dtype=np.uint8)
        kp, des = get_keypoints(base, pt1, pt2)

        if not os.path.isdir(f'media/processed/{folder_name}'):
            os.makedirs(f'media/processed/{folder_name}')

        for image in image_list:
            frame = np.array(Image.open(image), dtype=np.uint8)
            align = get_alignment_img(frame, kp, des)
            aligned_image = Image.fromarray(align)

            aligned_image.save(
                f'media/processed/{folder_name}/aligned_{image.name}', "JPEG")

            serializer.save(user=self.request.user,
                            base=base_image_objects,
                            image=f'processed/{folder_name}/aligned_{image.name}')


# @csrf_exempt
@api_view(['POST'])
def align_image(request):
    if request.method == "POST":
        print(request.FILES)
        image_list = []
        for upload_image in request.FILES.getlist('image'):
            image = upload_image
            image_name = upload_image.name
            image_list.append(image)

        if request.POST.get('folder') == "undefined":
            folder_name = image_list[0]
        else:
            folder_name = request.POST.get('folder')[1:]

        post_use_base = request.POST.get('base')
        base_image_objects = BaseImage.objects.get(name=post_use_base)
        base_image = base_image_objects.image

        pt1 = base_image_objects.pt1.split(',')
        pt2 = base_image_objects.pt2.split(',')
        pt1 = [int(s) for s in pt1]
        pt2 = [int(s) for s in pt2]
        pt1 = tuple(pt1)
        pt2 = tuple(pt2)

        print(pt2)
        base = np.array(Image.open(f'media/{base_image}'), dtype=np.uint8)
        kp, des = get_keypoints(base, pt1, pt2)

        if not os.path.isdir(f'media/processed/{request.user.username}/{folder_name}'):
            os.makedirs(
                f'media/processed/{request.user.username}/{folder_name}')

        image_group = ImageGroup(
            user=request.user,
            name=folder_name
        )
        image_group.save()
        for image in image_list:
            frame = np.array(Image.open(image), dtype=np.uint8)
            align = get_alignment_img(frame, kp, des)
            aligned_image = Image.fromarray(align)

            aligned_image.save(
                f'media/processed/{request.user.username}/{folder_name}/aligned_{image.name}', "JPEG")

            processed_image = ProcessedImage(
                user=request.user,
                group=image_group,
                base=base_image_objects,
                image=f'processed/{request.user.username}/{folder_name}/aligned_{image.name}'
            )

            processed_image.save()

    return HttpResponse("成功")


class ZipfileRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class DownloadList(generics.ListAPIView):
    
    def get():
        # <input type="checkbox" name="zip"のnameに対応
    # file_pks = request.POST.getlist('zip')
        file_names = ["",""]
        queryset = ProcessedImageSerializer.objects.filter(base=3)
        print(upload_files)
        response = HttpResponse(content_type='application/zip')
        file_zip = zipfile.ZipFile(response, 'w')
        for upload_file in upload_files:
            file_zip.writestr(upload_file.file.name, upload_file.file.read())

    # Content-Dispositionでダウンロードの強制
        response['Content-Disposition'] = 'attachment; filename="files.zip"'

        return response
