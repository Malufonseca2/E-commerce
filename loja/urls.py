from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar'),
    path('atualizar_senha/', views.atualizar_senha, name='atualizar_senha'),
    path('atualizar_usuario/', views.atualizar_usuario, name='atualizar_usuario'),
    path('atualizar_info/', views.atualizar_info, name='atualizar_info'),
    path('produto/<int:pk>', views.produto, name='produto'),
    path('categoria/<str:foo>', views.categoria, name='categoria'),
    path('esqueceu-senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('redefinir-senha/<uidb64>/',
         views.redefinir_senha, name='redefinir_senha'),
    path('buscar/', views.buscar, name='buscar')

]
