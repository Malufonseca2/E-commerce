from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.resumo_carrinho, name='resumo_carrinho'),
    path('add/', views.add_carrinho, name='add_carrinho'),
    path('delete/', views.delete_carrinho, name='delete_carrinho'),
    path('update/', views.update_carrinho, name='update_carrinho'),
]
