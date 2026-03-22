# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('menu-items/<int:pk>/', views.MenuItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]