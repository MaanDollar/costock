from django.shortcuts import render, redirect
from django.conf import settings
from .models import User
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.parse


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

    encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    print("Encoded Data:", encoded_data)
    print("Headers:", headers)

    try:
        response = requests.post(token_url, data=encoded_data, headers=headers)
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
    카카오 사용자 정보 처리.
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

        print(f"Kakao ID: {kakao_id}, Email: {email}, Nickname: {nickname}")  # 디버깅

        # 성공 페이지로 이동
        return render(request, 'accounts/login_success.html', {
            "profile": user_info,
            "nickname": nickname,
            "email": email,
        })

    except requests.RequestException as e:
        print(f"RequestException occurred while fetching user info: {str(e)}")
        return render(request, 'accounts/login_failed.html', {"error": "Failed to connect to Kakao API"})

