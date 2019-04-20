from django.db import models
# Create your models here.
class TrainResult(models.Model):
    username=models.CharField(max_length=32)
    train=models.CharField(max_length=32)
    result=models.CharField(max_length=256)