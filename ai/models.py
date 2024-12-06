from django.db import models

# Create your models here.
class Stock(models.Model):
    StockCode = models.CharField(max_length=10, primary_key=True)
    StockName = models.CharField(max_length=100)

class StockCorrelation(models.Model):
    StockCode = models.CharField(max_length=10, primary_key=True)
    RelatedStockCode = models.CharField(max_length=10)
    Correlation = models.DecimalField(max_digits=5, decimal_places=4)