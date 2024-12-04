from django.db import models

class Owned(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Recommended(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
