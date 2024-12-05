from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('kakao/login/callback/', views.kakao_callback),
    path('logout/', views.kakao_logout, name='logout'),
]
