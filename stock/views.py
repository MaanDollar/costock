from django.http import JsonResponse
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
    return JsonResponse({'status': 'success', 'message': 'success'})


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

    return JsonResponse({'status': 'success', 'message': 'success'})

def delete_owned(request, stock_id):
    stock = get_object_or_404(Owned, id=stock_id)

    if request.method == 'POST':
        stock.delete()

    return JsonResponse({'status': 'success', 'message': 'success'})


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

    return JsonResponse({'status': 'success', 'message': 'success'})

def delete_recommended(request, stock_id):
    stock = get_object_or_404(Recommended, id=stock_id)

    if request.method == 'POST':
        stock.delete()

    return JsonResponse({'status': 'success', 'message': 'success'})
