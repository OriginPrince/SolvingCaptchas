from django.db import models

# Create your models here.
class picModel(models.Model):
    pic=models.ImageField(upload_to='media/test')