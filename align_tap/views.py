from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import django_filters
from rest_framework import viewsets, filters
from .serializer import *
from PIL import Image
import json
import os
# Create your views here.


def index(request):
    base_image_list = BaseImage.objects.all()
    context = {'base_image_list': base_image_list}
    output = "hello"
    return render(request, 'index.html', context)


class BaseImageViewSet(viewsets.ModelViewSet):
    queryset = BaseImage.objects.all()
    serializer_class = BaseImageSerializer


class UnprocessedImageViewSet(viewsets.ModelViewSet):
    queryset = UnprocessedImage.objects.all()
    serializer_class = UnprocessedImageSerializer

    
class ProcessedImageViewSet(viewsets.ModelViewSet):
    queryset = ProcessedImage.objects.all()
    serializer_class = ProcessedImageSerializer

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def align_image(request):
    if request.method == "POST":
        print(request.FILES)
        image_list=[]
        for upload_image in request.FILES.getlist('image'):
            image = upload_image
            image_name = upload_image.name
            image_list.append(image)

        folder_name = request.POST.get('folder')
        post_use_base = request.POST.get('base')
        base_image_objects=BaseImage.objects.get(name=post_use_base)
        base_image=base_image_objects.image

        pt1 = base_image_objects.pt1.split(',')
        pt2 = base_image_objects.pt2.split(',')
        pt1=[int(s) for s in pt1]
        pt2=[int(s) for s in pt2]
        pt1=tuple(pt1)
        pt2=tuple(pt2)
       
        base = np.array(Image.open(f'media/{base_image}'), dtype=np.uint8)
        kp, des = get_keypoints(base, pt1, pt2)
        

        if not os.path.isdir(f'media/processed/{folder_name}'):
            os.makedirs(f'media/processed/{folder_name}')


        for image in image_list:
            frame = np.array(Image.open(image), dtype=np.uint8)
            align = get_alignment_img(frame, kp, des)
            aligned_image = Image.fromarray(align)

            aligned_image.save(f'media/processed/{folder_name}/aligned_{image.name}', "JPEG")

            processed_image = ProcessedImage(
                base = base_image_objects,
                image = f'processed/{folder_name}/aligned_{image.name}'
            )
        
            processed_image.save()

    return HttpResponse("成功")