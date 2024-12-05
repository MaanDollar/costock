from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('current_user/', views.current_user, name='current_user'),
    path('kakao/logout/', views.kakao_logout, name='logout'),
]
