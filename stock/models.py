from django.db import models

class Owned(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    price = models.IntegerField()

class Recommended(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    price = models.IntegerField()