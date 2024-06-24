from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria, Perfil
from django.contrib.auth import authenticate, login, logout
from carrinho.carrinho import Carrinho
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
import json

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from pagamento.models import ShippingAddress
from pagamento.forms import ShippingForm


def error_404_view(request, exception):
    return render(request, '404.html')


def home(request):
    low_stock_products = []
    if request.user.is_authenticated and request.user.is_superuser:

        # Verificar se há produtos antes de filtrar o estoque baixo
        if Produto.objects.exists():
            low_stock_products = [
                produto for produto in Produto.objects.all() if produto.estoque_baixo()]

            if low_stock_products:
                messages.warning(
                    request, 'Alguns produtos estão com estoque baixo.')

    return render(request, 'home.html', {'low_stock_products': low_stock_products})


def sobre(request):
    return render(request, 'sobre.html', {})


def contato(request):
    return render(request, 'contato.html', {})


def login_usuario(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Perfil.objects.get(user__id=request.user.id)
            # Obetendo o carrinho salve do BD
            saved_cart = current_user.old_cart
            # Convertendo a string BD em dicionario Python
            if saved_cart:
                # Convertendo o dicionario em JSON
                converted_cart = json.loads(saved_cart)
                # Adicionando e carrengo o dicionario do carrinho na sessão
                cart = Carrinho(request)
                # Percorrendo o carrinho e adicionando os itens do banco de dados
                for key, value in converted_cart.items():
                    cart.db_add(produto=key, quantidade=value)

            messages.success(request, ("Você foi logado com sucesso!"))
            return redirect('home')
        else:
            messages.success(
                request, ("nome de usuário ou senha incorretos, tente novamente..."))
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_usuario(request):
    logout(request)
    messages.success(request, ('Você foi desconectado com sucesso'))
    return redirect('home')


def cadastrar_usuario(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ("Nome de usuário criado - Preencha suas informações de usuário abaixo..."))
            return redirect('atualizar_info')
        else:
            messages.success(
                request, ("Opa! Ocorreu um problema ao registrar-se, tente novamente..."))
            return redirect('cadastrar')
    else:
        return render(request, 'cadastrar.html', {'form': form})


def produto(request, pk):
    produto = Produto.objects.get(id=pk)
    return render(request, 'produto.html', {'produto': produto})


def atualizar_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Perfil.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # Get original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User's Shipping Form
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()

            messages.success(request, "Suas informações foram atualizadas!!")
            return redirect('home')
        return render(request, "atualizar_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(
            request, "Você deve estar logado para acessar essa página!!")
        return redirect('home')


def atualizar_senha(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Sua senha foi atualizada...")
                login(request, current_user)
                return redirect('atualizar_usuario')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('atualizar_senha')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "atualizar_senha.html", {'form': form})
    else:
        messages.success(
            request, "Você deve estar logado para visualizar essa página...")
        return redirect('home')


def atualizar_usuario(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "atualizar_usuario.html", {'user_form': user_form})
    else:
        messages.success(
            request, "Você deve estar logado para acessar essa página!!")
        return redirect('home')


def categoria(request, foo):
    foo = foo.replace('-', ' ')

    try:
        categoria = get_object_or_404(Categoria, nome=foo)
        produtos = Produto.objects.filter(categoria=categoria)
        return render(request, 'categoria.html', {'produtos': produtos, 'categoria': categoria})
    except Categoria.DoesNotExist:
        messages.success(request, 'Essa Categoria não Existe!!!')
        return redirect('home')


def esqueceu_senha(request):
    if request.method == "POST":
        from django.contrib.auth import get_user_model
        User = get_user_model()

        email = request.POST.get('email')
        associated_user = User.objects.filter(email=email).first()
        if associated_user:
            uid = urlsafe_base64_encode(force_bytes(associated_user.pk))
            return redirect('redefinir_senha', uidb64=uid)
        else:
            messages.error(request, 'Email não encontrado.')
    return render(request, 'esqueceu_senha.html')


def redefinir_senha(request, uidb64=None):
    if uidb64 is not None:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            if request.method == "POST":
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(
                        request, 'Sua senha foi redefinida com sucesso.')
                    return redirect('login')
                else:
                    messages.error(request, 'As senhas não coincidem.')
            return render(request, 'redefinir_senha.html', {'uidb64': uidb64})
        else:
            messages.error(
                request, 'O link para redefinição de senha é inválido.')
            return redirect('esqueceu_senha')
    else:
        messages.error(request, 'O link para redefinição de senha é inválido.')
        return redirect('esqueceu_senha')


def buscar(request):
    if request.method == "POST":
        buscar = request.POST['busca']

        buscar = Produto.objects.filter(
            Q(nome__icontains=buscar) | Q(descricao__icontains=buscar))

        if not buscar:
            messages.success(
                request, 'Esse produto não existe.. Tente de novo')
            return render(request, 'buscar.html', {})
        else:
            return render(request, 'buscar.html', {'buscar': buscar})
    else:
        return render(request, 'buscar.html', {})
