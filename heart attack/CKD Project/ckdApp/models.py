from django.db import models

# Create your models here.
class ckdModel(models.Model):

    age = models.FloatField()
    cp = models.FloatField()
    thalach = models.FloatField()
    exang = models.FloatField()
    oldpeak = models.FloatField()
    ca = models.FloatField()
