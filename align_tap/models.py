from django.db import models

# Create your models here.


class BaseImage(models.Model):
    name = models.CharField(max_length=32 )
    image = models.ImageField(upload_to='base/')
    pt1 = models.CharField(max_length=32)
    pt2 = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class UnprocessedImage(models.Model):
    image = models.ImageField(upload_to='unprocessed/')

   
class ProcessedImage(models.Model):
    base = models.ForeignKey(BaseImage, on_delete=models.SET_NULL, null=True )
    image = models.ImageField(upload_to='processed/')

    
