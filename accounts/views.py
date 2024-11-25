from django.shortcuts import render, redirect
from django.conf import settings
from .models import User
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'accounts/login.html')

def kakao_callback(request):
    rest_api = getattr(settings, 'KAKAO_REST_API_KEY')
    redirect_uri = getattr(settings, 'KAKAO_REDIRECT_URI')
    code = request.GET.get("code")  # 인가 코드 가져오기
    if not code:
        print("No authorization code provided")
        return render(request, 'accounts/login_failed.html', {"error": "No authorization code provided"})

    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": rest_api,  # 카카오 앱의 REST API 키
        "redirect_uri": redirect_uri,  # Redirect URI (카카오 개발자 콘솔과 동일해야 함)
        "code": code,  # 인가 코드
    }

    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    try:
        response = requests.post(token_url, data=data, headers=headers)
        print("Token Request Response:", response.status_code, response.text)  # 디버깅

        # 3. 응답 상태 확인
        if response.status_code != 200:
            return render(request, 'accounts/login_failed.html', {
                "error": f"Failed to get access token: {response.json().get('error', 'Unknown error')}",
                "description": response.json().get('error_description', 'No description available')
            })

        # 4. 액세스 토큰 가져오기
        access_token = response.json().get("access_token")
        if not access_token:
            print("Access token not found in response")
            return render(request, 'accounts/login_failed.html', {"error": "Access token not found"})

        # 5. 사용자 정보 처리 함수 호출
        return handle_user_info(request, access_token)

    except requests.RequestException as e:
        print(f"RequestException occurred: {str(e)}")  # 디버깅
        return render(request, 'accounts/login_failed.html', {"error": "Failed to connect to Kakao API"})


def handle_user_info(request, access_token):
    """
    카카오 사용자 정보 처리 (프로필 사진 포함).
    """
    profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.get(profile_url, headers=headers)
        print("User Info Request Response:", response.status_code, response.text)  # 디버깅

        if response.status_code != 200:
            return render(request, 'accounts/login_failed.html', {
                "error": "Failed to get user info",
                "description": response.json().get('msg', 'No description available')
            })

        user_info = response.json()
        kakao_id = user_info.get("id")
        email = user_info.get("kakao_account", {}).get("email", "No email provided")
        nickname = user_info.get("kakao_account", {}).get("profile", {}).get("nickname", "No nickname")
        profile_image = user_info.get("kakao_account", {}).get("profile", {}).get("profile_image_url", "")
        thumbnail_image = user_info.get("kakao_account", {}).get("profile", {}).get("thumbnail_image_url", "")

        print(f"Kakao ID: {kakao_id}, Email: {email}, Nickname: {nickname}, Profile Image: {profile_image}, Thumbnail Image: {thumbnail_image}")  # 디버깅

        # 성공 페이지로 이동
        return render(request, 'accounts/login_success.html', {
            "profile": user_info,
            "nickname": nickname,
            "email": email,
            "profile_image": profile_image,
            "thumbnail_image": thumbnail_image,
        })

    except requests.RequestException as e:
        print(f"RequestException occurred while fetching user info: {str(e)}")
        return render(request, 'accounts/login_failed.html', {"error": "Failed to connect to Kakao API"})

def kakao_logout(request):
    """
    카카오 로그아웃 처리 함수
    """
    rest_api = getattr(settings, 'KAKAO_REST_API_KEY')
    logout_redirect_uri = getattr(settings, 'KAKAO_LOGOUT_REDIRECT_URI')  # 로그아웃 후 리다이렉트 URI

    # 1. 사용자 로그아웃 (서버 토큰 로그아웃)
    access_token = request.session.get('access_token')  # 세션에서 토큰 가져오기
    if access_token:
        headers = {"Authorization": f'Bearer {access_token}'}
        logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        print("User Logout Response:", logout_response.json())

    # 2. 카카오 계정 로그아웃 (카카오 로그인 창 로그아웃)
    kakao_account_logout_url = (
        f'https://kauth.kakao.com/oauth/logout?client_id={rest_api}&logout_redirect_uri={logout_redirect_uri}'
    )
    return redirect(kakao_account_logout_url)
