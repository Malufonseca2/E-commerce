from django.shortcuts import render, redirect, get_object_or_404
from carrinho.carrinho import Carrinho
from pagamento.forms import ShippingForm, PaymentForm
from pagamento.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from loja.models import Produto, Perfil
import datetime

# Create your views here.


def orders(request, pk):
    if request.user.is_authenticated:
        # Obtendo os pedidos e  os itens do pedido
        order = get_object_or_404(Order, id=pk, user=request.user)
        items = OrderItem.objects.filter(order=order)

        if request.method == 'POST' and not order.refund_requested and order.status == 'F':
            order.refund_requested = True
            order.save()

            messages.success(
                request, f'Reembolso solicitado para o pedido {order.id}. As instruções foram enviadas para o seu e-mail.')
            return redirect('orders', pk=pk)

        return render(request, 'pagamento/orders.html', {"order": order, "items": items})
    else:
        messages.success(request, "Acesso negado!")
        return redirect('home')


def lista_pedidos(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'pagamento/lista_pedidos.html', {'orders': orders})
    else:
        messages.success(request, "Acesso negado!")
        return redirect('home')


def processar_pedido(request):

    if request.POST:
        # Pegando o carrinho
        carrinho = Carrinho(request)
        produtos_carrinho = carrinho.get_prods
        quantidades = carrinho.get_quants
        totals = carrinho.total_carrinho()

        # obtendo informações de faturamento na última página
        payment_form = PaymentForm(request.POST or None)
        # Obtendo dados da sessão de envio
        my_shipping = request.session.get('my_shipping')

        # Reunindo informações do pedido
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Criando o endereço de entrega a partir das informações da sessão
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # Logado
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Adicionando items do pedido
            # Obtendo o ID do pedido
            order_id = create_order.pk

            # pegando info do produto
            for produto in produtos_carrinho():

                produto_id = produto.id
                preco = produto.preco

                for key, value in quantidades().items():
                    if int(key) == produto.id:
                        if produto.estoque < value:
                            messages.error(
                                request, f"Estoque insuficiente para o produto {produto.nome}.")

                            return redirect('resumo_carrinho')

                        create_order_item = OrderItem(
                            order_id=order_id, product_id=produto_id, user=user, quantity=value, price=preco)
                        create_order_item.save()

                        # Diminuindo o estoque de produtos  e salvando
                        produto.estoque -= value
                        produto.save()

            # Deletando o carrihno da sessão
            for key in list(request.session.keys()):
                if key == 'session_key':

                    del request.session[key]

            # Excluindo o carrinho do Banco de dados
            current_user = Perfil.objects.filter(user__id=request.user.id)

            current_user.update(old_cart="")

            messages.success(request, "Pedido realizado com sucesso!")
            return redirect('home')

        else:
            messages.success(request, "Acesso Negado!")
            return redirect('home')

    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')


def checkout(request):
    # Pegando o carrinho
    carrinho = Carrinho(request)
    produtos_carrinho = carrinho.get_prods
    quantidades = carrinho.get_quants
    totals = carrinho.total_carrinho()

    if request.user.is_authenticated:
        # Finalizando a compra como usuário logado
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
        return render(request, "pagamento/checkout.html", {"produtos_carrinho": produtos_carrinho, "quantidades": quantidades, "totals": totals, "shipping_form": shipping_form})

    else:
        messages.success(
            request, "Precisa está logado para finalizar a compra!")
        return redirect('login')


def info_pagamento(request):
    if request.POST:
        carrinho = Carrinho(request)
        produtos_carrinho = carrinho.get_prods
        quantidades = carrinho.get_quants
        totals = carrinho.total_carrinho()

        # Criando uma sessão com informações de envio
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Verificando se o usuário está logado
        if request.user.is_authenticated:
            # Obtendo o formulario de pagamento
            billing_form = PaymentForm()
            return render(request, "pagamento/info_pagamento.html", {"produtos_carrinho": produtos_carrinho, "quantidades": quantidades, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})

    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')


def sucesso_pagamento(request):
    return render(request, 'pagamento/sucesso_pagamento.html')
