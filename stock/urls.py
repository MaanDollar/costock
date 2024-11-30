from django.urls import path, include

from . import views

urlpatterns = [
    path('owned/<int:stock_id>/add/', views.add_owned, name='edit_stock'),

    path('owned/modify_owned(request, stock_id)

    path(delete_owned(request)

    path(add_recommended(request)

    path(delete_recommended(request)

    path(modify_recommended(request, stock_id)
]
