from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import User
import requests

def index(request):
    return render(request, 'accounts/login.html')

def current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({'username': None})
    user = request.user

    try:
        kakao_account = user.socialaccount_set.filter(provider='kakao').first()
        extra_data = kakao_account.extra_data if kakao_account else {}
        profile_image = extra_data.get("kakao_account", {}).get("profile", {}).get("profile_image_url", "")
    except Exception as e:
        profile_image = ""

    # DB에 사용자 정보 저장 또는 업데이트
    try:
        user_record, created = User.objects.update_or_create(
            nickname=user.username,  # 사용자 이름을 닉네임으로 사용
            defaults={
                'profile_image': profile_image,  # 프로필 사진 업데이트
            }
        )
    except Exception as e:
        return JsonResponse({'error': f'Failed to save user info: {str(e)}'}, status=500)

    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'profile_image': profile_image,
    })

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
