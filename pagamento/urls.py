from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sucesso_pagamento', views.sucesso_pagamento, name='sucesso_pagamento'),
    path('checkout', views.checkout, name='checkout'),
    path('info_pagamento', views.info_pagamento, name='info_pagamento'),
    path('processar_pedido', views.processar_pedido, name='processar_pedido'),
    path('lista_pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('orders/<int:pk>', views.orders, name='orders'),

]
