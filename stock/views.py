from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Owned, Recommended
import requests

def add_owned(request):
    if request.method == 'POST':

        code = request.POST.get('code')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if Owned.objects.filter(code=code).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Stock with code "{code}" already exists.'
            }, status=400)

        try:
            Owned.objects.create(
                code=code,
                quantity=int(quantity),
                price=float(price)
            )
            return JsonResponse({'status': 'success', 'message': 'Stock added successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def modify_owned(request, stock_id):

    stock = get_object_or_404(Owned, id=stock_id)

    if request.method == 'POST':

        code = request.POST.get('code')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        stock.code = code
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
        code = request.POST.get('code')

        if Recommended.objects.filter(code=code).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Stock with code "{code}" already exists.'
            }, status=400)

        try:
            Recommended.objects.create(
                code=code,
            )
            return JsonResponse({'status': 'success', 'message': 'Stock added successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def delete_recommended(request, stock_id):
    stock = get_object_or_404(Recommended, id=stock_id)

    if request.method == 'POST':
        stock.delete()

    return JsonResponse({'status': 'success', 'message': 'success'})
