from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import User
import requests

def index(request):
    return render(request, 'accounts/login.html')

def kakao_logout(request):
    rest_api = getattr(settings, 'KAKAO_REST_API_KEY')
    logout_redirect_uri = getattr(settings, 'KAKAO_LOGOUT_REDIRECT_URI')

    access_token = request.session.get('access_token')
    if access_token:
        headers = {"Authorization": f'Bearer {access_token}'}
        logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        print("User Logout Response:", logout_response.json())

    kakao_account_logout_url = (
        f'https://kauth.kakao.com/oauth/logout?client_id={rest_api}&logout_redirect_uri={logout_redirect_uri}'
    )
    return redirect(kakao_account_logout_url)
