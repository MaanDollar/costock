from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=200)
    profile_image = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nickname
