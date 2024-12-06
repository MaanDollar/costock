from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Stock, StockCorrelation
import requests
import FinanceDataReader as fdr
import matplotlib
import matplotlib.pyplot as plt

import io

import base64
matplotlib.use('Agg')
def price(request, stock_code):
    # 주식 데이터를 동적으로 가져옴
    try:
        stock_df = fdr.DataReader(stock_code, '2023-06-01', '2024-07-26')
    except Exception as e:
        # 데이터를 가져오지 못했을 때 에러 처리
        context = {
            'error': f"Unable to fetch data for stock code: {stock_code}. Error: {str(e)}"
        }
        return render(request, 'ai/price_error.html', context)

    # Matplotlib 그래프 생성
    plt.figure(figsize=(10, 6))
    stock_df['Close'].plot(title=f'Stock Prices for {stock_code}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.tight_layout()

    # 그래프를 메모리에 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # 그래프를 base64로 인코딩
    graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'graph': graph_base64,
        'stock_code': stock_code
    }

    return render(request, 'ai/price.html', context)




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
