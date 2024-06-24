from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from loja.views import error_404_view


handler404 = error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loja.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('pagamento/', include('pagamento.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
