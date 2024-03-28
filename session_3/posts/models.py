from django.db import models

# Create your models here.

class CodeReviewer(models.Model):
    name = models.CharField(max_length=5)
    age = models.IntegerField()
    major = models.CharField(max_length=20)
    gitHub = models.CharField(max_length=20)