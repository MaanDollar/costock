from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Owned, Recommended
import requests


def list_owned(request):
    try:
        stocks = Owned.objects.all()
        return JsonResponse({
            'status': 'success',
            'data': {
                'stocks': [
                    {
                        'id': stock.id,
                        'code': stock.code,
                        'quantity': stock.quantity,
                        'price': stock.price
                    } for stock in stocks
                ]
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def add_owned(request):
    if request.user.is_anonymous:
        return JsonResponse({'status': 'error', 'message': 'Login required.'}, status=401)

    if request.method == 'POST':

        code = request.POST.get('code')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if Owned.objects.filter(code=code, customer_id=request.user.id).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Stock with code "{code}" already exists.'
            }, status=400)

        try:
            Owned.objects.create(
                code=code,
                quantity=int(quantity),
                price=float(price),
                customer_id=request.user.id
            )
            return JsonResponse({'status': 'success', 'message': 'Stock added successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def modify_owned(request, stock_id):
    if request.user.is_anonymous:
        return JsonResponse({'status': 'error', 'message': 'Login required.'}, status=401)

    stock = get_object_or_404(Owned, id=stock_id)
    if stock.customer_id != request.user.id:
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

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
    if request.user.is_anonymous:
        return JsonResponse({'status': 'error', 'message': 'Login required.'}, status=401)

    stock = get_object_or_404(Owned, id=stock_id)
    if stock.customer_id != request.user.id:
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    if request.method == 'POST':
        stock.delete()

    return JsonResponse({'status': 'success', 'message': 'success'})


def list_recommended(request):
    try:
        stocks = Recommended.objects.all()
        return JsonResponse({
            'status': 'success',
            'data': {
                'stocks': [
                    {
                        'id': stock.id,
                        'code': stock.code
                    } for stock in stocks
                ]
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def add_recommended(request):
    if request.user.is_anonymous:
        return JsonResponse({'status': 'error', 'message': 'Login required.'}, status=401)

    if request.method == 'POST':
        code = request.POST.get('code')

        if Recommended.objects.filter(code=code, customer_id=request.user.id).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Stock with code "{code}" already exists.'
            }, status=400)

        try:
            Recommended.objects.create(
                code=code,
                customer_id=request.user.id
            )
            return JsonResponse({'status': 'success', 'message': 'Stock added successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def delete_recommended(request, stock_id):
    if request.user.is_anonymous:
        return JsonResponse({'status': 'error', 'message': 'Login required.'}, status=401)

    stock = get_object_or_404(Recommended, id=stock_id)

    if stock.customer_id != request.user.id:
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    if request.method == 'POST':
        stock.delete()

    return JsonResponse({'status': 'success', 'message': 'success'})
