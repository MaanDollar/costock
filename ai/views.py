from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Stock, StockCorrelation
import requests
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

def price(request):
    naver_df = fdr.DataReader('035420', '2023-06-01', '2024-07-26')

    naver_df['Close'].plot(title='NAVER Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()



def add_ai(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        Stock.objects.create(
            name=name,
            quantity=int(quantity),
            price=float(price)
        )

    return render(request, 'accounts/login.html')

def modify_ai(request, stock_id):

    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        stock.name = name
        stock.quantity = int(quantity)
        stock.price = float(price)
        stock.save()

    return render(request, 'accounts/login.html', {'stock': stock})

def delete_ai(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        try:
            stock = Stock.objects.get(name=name, quantity=quantity, price=price)
            stock.delete()
            return redirect('stock_list')
        except Stock.DoesNotExist:

            error_message = "해당 종목을 찾을 수 없습니다."
            return render(request, 'delete_stock.html', {'error': error_message})

    return render(request, 'delete_stock.html')
