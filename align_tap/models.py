from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class BaseImage(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.CharField(max_length=32 )
    image = models.ImageField(upload_to='base/')
    pt1 = models.CharField(max_length=32)
    pt2 = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class ImageGroup(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.CharField(max_length=32 )

    def __str__(self):
        return self.name

class ProcessedImage(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    group = models.ForeignKey(ImageGroup,on_delete=models.CASCADE)
    base = models.ForeignKey(BaseImage, on_delete=models.SET_NULL, null=True )
    image = models.ImageField(upload_to='processed/')

    
