from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import User
import requests


def index(request):
    return JsonResponse({"message": "Hello, world!"})
