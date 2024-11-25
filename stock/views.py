from django.shortcuts import render, redirect
from django.conf import settings
from .models import Owned, Recommended
import requests

def add_owned(request):
    return render(request, 'accounts/login.html')
def modify_owned(request):
    return render(request, 'accounts/login.html')
def delete_owned(request):
    return render(request, 'accounts/login.html')

def add_recommended(request):
    return render(request, 'accounts/login.html')
def delete_recommended(request):
    return render(request, 'accounts/login.html')
def modify_recommended(request):
    return render(request, 'accounts/login.html')
