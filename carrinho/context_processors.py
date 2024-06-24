from .carrinho import Carrinho

# Criando um processador de contexto para que o carrinho funcione em todas as paginas


def carrinho(request):
    # Retornando os dados padrões do carrinho
    return {'carrinho': Carrinho(request)}
