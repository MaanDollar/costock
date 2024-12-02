from django.urls import path, include

from . import views

urlpatterns = [
    path('owned/<int:stock_id>/add/', views.add_owned, name='add_owned'),
    path('owned/modify/', views.modify_owned, name='modify_owned'),
    path('owned/delete/', views.delete_owned, name='delete_owned'),
    path('recommended/<int:stock_id>/add/', views.add_recommended, name='add_recommended'),
    path('recommended/modify/', views.modify_recommended, name='modify_recommended'),
    path('recommended/delete/', views.delete_recommended, name='delete_recommended'),
]
