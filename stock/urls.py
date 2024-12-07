from django.urls import path, include

from . import views

urlpatterns = [
    path('owned/list/', views.list_owned, name='list_owned'),
    path('owned/add/', views.add_owned, name='add_owned'),
    path('owned/<int:stock_id>/modify/', views.modify_owned, name='modify_owned'),
    path('owned/<int:stock_id>/delete/', views.delete_owned, name='delete_owned'),
    path('recommended/list/', views.list_recommended, name='list_recommended'),
    path('recommended/add/', views.add_recommended, name='add_recommended'),
    path('recommended/<int:stock_id>/delete/', views.delete_recommended, name='delete_recommended'),
]
