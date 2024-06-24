from django.shortcuts import render, get_object_or_404
from .carrinho import Carrinho
from loja.models import Produto
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.


def resumo_carrinho(request):
    carrinho = Carrinho(request)
    produtos_carrinho = carrinho.get_prods
    quantidades = carrinho.get_quants
    totals = carrinho.total_carrinho()
    return render(request, "resumo_carrinho.html", {"produtos_carrinho": produtos_carrinho, "quantidades": quantidades, "totals": totals})


def add_carrinho(request):
    # Pegando o carrinho
    carrinho = Carrinho(request)

    # testando o POST
    if request.POST.get('action') == 'post':
        # pegando o produto
        produto_id = int(request.POST.get('produto_id'))
        produto_qtde = int(request.POST.get('produto_qtde'))

        # pesquisando produto no DB
        produto = get_object_or_404(Produto, id=produto_id)

        if produto_qtde > produto.estoque:
            response = JsonResponse(
                {'error': 'Estoque insuficiente para o produto "{}".'.format(produto.nome)})
            messages.success(request, ('Estoque insuficiente...'))
            return response

        # Salvando na seção
        carrinho.add(produto=produto, quantidade=produto_qtde)

        # Pegando A quantidade no Carrinho
        quantidade_carrinho = carrinho.__len__()

        # Retornando
        # response = JsonResponse({'Produto nome': produto.nome})
        response = JsonResponse({'qted': quantidade_carrinho})
        messages.success(request, ('Produto Adicionado ao Carrinho...'))
        return response


def delete_carrinho(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        # pegando o produto
        produto_id = int(request.POST.get('produto_id'))
        # chamando função deletar
        carrinho.delete(produto=produto_id)
        response = JsonResponse({'produto': produto_id})
        messages.success(request, ('Produto deletado do Carrinho...'))
        return response


def update_carrinho(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        # pegando o produto
        produto_id = int(request.POST.get('produto_id'))
        produto_qtde = int(request.POST.get('produto_qtde'))

        carrinho.update(produto=produto_id, quantidade=produto_qtde)

        response = JsonResponse({'qtde': produto_qtde})
        messages.success(request, ('Seu carrinho foi atualizado...'))
        return response
