from django.urls import path, include

from . import views

urlpatterns = [
    path('price/', views.price, name='price'),
    path('<int:stock_id>/add/', views.add_ai, name='add_ai'),
    path('modify/', views.modify_ai, name='modify_ai'),
    path('delete/', views.delete_ai, name='delete_ai'),
]