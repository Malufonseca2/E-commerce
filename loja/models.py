from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create a user Profile by default when user signs up


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Perfil(user=instance)
        user_profile.save()


# Automate the profile thing
post_save.connect(create_profile, sender=User)


# Categories of Products
class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Categorias'


# All of our Products
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, default=1)
    descricao = models.CharField(
        max_length=250, default='', blank=True, null=True)
    imagem = models.ImageField(upload_to='uploads/produtos/')
    a_venda = models.BooleanField(default=False)
    estoque = models.PositiveIntegerField(default=0)

    def estoque_baixo(self):
        return self.estoque <= 0.2 * 100

    def __str__(self):
        return self.nome
