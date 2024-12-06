from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=200, unique=True)
    profile_image = models.URLField(max_length=500, blank=True, null=True)
