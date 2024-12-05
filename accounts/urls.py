from django.urls import path, include

from . import views

urlpatterns = [
    path('kakao/login/callback/', views.kakao_callback),
    path('logout/', views.kakao_logout, name='logout'),
]
