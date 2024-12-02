from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100)  # 종목명
    quantity = models.IntegerField()  # 수량
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 매입 단가

    def __str__(self):
        return self.name