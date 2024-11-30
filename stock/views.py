from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Owned, Recommended
import requests

def add_owned(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        Owned.objects.create(
            name=name,
            quantity=int(quantity),
            price=float(price)
        )

    return render(request, 'accounts/login.html')

def modify_owned(request, stock_id):

    stock = get_object_or_404(Owned, id=stock_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        stock.name = name
        stock.quantity = int(quantity)
        stock.price = float(price)
        stock.save()

    return render(request, 'accounts/login.html', {'stock': stock})

def delete_owned(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        try:
            stock = Owned.objects.get(name=name, quantity=quantity, price=price)
            stock.delete()
            return redirect('stock_list')
        except Owned.DoesNotExist:

            error_message = "해당 종목을 찾을 수 없습니다."
            return render(request, 'delete_stock.html', {'error': error_message})

    return render(request, 'delete_stock.html')

def add_recommended(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        Recommended.objects.create(
            name=name,
            quantity=int(quantity),
            price=float(price)
        )

    return render(request, 'accounts/login.html')

def delete_recommended(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        try:
            stock = Recommended.objects.get(name=name, quantity=quantity, price=price)
            stock.delete()
            return redirect('stock_list')
        except Recommended.DoesNotExist:

            error_message = "해당 종목을 찾을 수 없습니다."
            return render(request, 'delete_stock.html', {'error': error_message})

    return render(request, 'accounts/login.html')

def modify_recommended(request, stock_id):

    stock = get_object_or_404(Recommended, id=stock_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        stock.name = name
        stock.quantity = int(quantity)
        stock.price = float(price)
        stock.save()

        return redirect('stock_list')

    return render(request, 'accounts/login.html')
