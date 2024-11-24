from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('accounts/kakao/login/callback/', views.kakao_callback),
    path('accounts/', include('allauth.urls')),
]
