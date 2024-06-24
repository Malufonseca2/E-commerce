from django.contrib import admin
from .models import Categoria, Produto, Perfil
from django.contrib.auth.models import User
from django.utils.html import format_html

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Perfil)


# Misturando o perfil com o usuario
class PerfilInline(admin.StackedInline):
    model = Perfil

# estendendo o Model User


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['password', 'last_login', 'groups', 'user_permissions',
              'username', 'first_name', 'last_name', 'email', ]
    inlines = [PerfilInline]


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estoque', 'stock_status')

    def stock_status(self, obj):
        if obj.estoque <= 0.2 * 100:
            return format_html('<span style="color: red;">Estoque Baixo</span>')
        return format_html('<span style="color: green;">Em Estoque</span>')

    stock_status.short_description = 'Estatus do Estoque'


admin.site.register(Produto, ProdutoAdmin)


# cancelar registro no velho modelo
admin.site.unregister(User)

# Registrando no novo modelo
admin.site.register(User, UserAdmin)
