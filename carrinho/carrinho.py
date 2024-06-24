from loja.models import Produto, Perfil


class Carrinho():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        # Pega a chave da seção atual se ela existir
        carrinho = self.session.get('session_key')

        # Se o usuario for novo, vamos criar
        if 'session_key' not in request.session:
            carrinho = self.session['session_key'] = {}

        # Garantir que o carrinho esteja disponivel em todas as paginas
        self.carrinho = carrinho

    def db_add(self, produto, quantidade):
        produto_id = str(produto)
        produto_qtde = str(quantidade)

        if produto_id in self.carrinho:
            pass
        else:
            # self.carrinho[produto_id] = {'preco': str(produto.preco)}
            self.carrinho[produto_id] = int(produto_qtde)

        self.session.modified = True

        # Lidando com o usuario Logado
        if self.request.user.is_authenticated:

            current_user = Perfil.objects.filter(user__id=self.request.user.id)

            carrinho = str(self.carrinho)

            carrinho = carrinho.replace("\'", "\"")

            # salvando o carrinho no perfil

            current_user.update(old_cart=str(carrinho))

    def add(self, produto, quantidade):
        produto_id = str(produto.id)
        produto_qtde = str(quantidade)

        if produto_id in self.carrinho:
            pass
        else:
            # self.carrinho[produto_id] = {'preco': str(produto.preco)}
            self.carrinho[produto_id] = int(produto_qtde)

        self.session.modified = True

        # Lidando com o usuario Logado
        if self.request.user.is_authenticated:

            current_user = Perfil.objects.filter(user__id=self.request.user.id)

            carrinho = str(self.carrinho)

            carrinho = carrinho.replace("\'", "\"")

            # salvando o carrinho no perfil

            current_user.update(old_cart=str(carrinho))

    def __len__(self):
        return len(self.carrinho)

    def total_carrinho(self):
        # Pegando o Id do produto
        produto_id = self.carrinho.keys()
        # Pesquisando os ids na DB produto
        produtos = Produto.objects.filter(id__in=produto_id)
        quantidade = self.carrinho

        total = 0

        for key, value in quantidade.items():
            key = int(key)
            for produto in produtos:
                if produto.id == key:
                    total = total + (produto.preco * value)
        return total

    def get_prods(self):
        # Pegando os ids do carrinho
        produto_ids = self.carrinho.keys()

        # usando os ids para pesquisar os produtos no DB
        produtos = Produto.objects.filter(id__in=produto_ids)

        return produtos

    def get_quants(self):
        quantidades = self.carrinho
        return quantidades

    def update(self, produto, quantidade):
        produto_id = str(produto)
        produto_qtde = int(quantidade)

        # pegando o carrinho
        carrinho = self.carrinho

        # Atualizando o dicionario/carrinho
        carrinho[produto_id] = produto_qtde

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Perfil.objects.filter(user__id=self.request.user.id)

            carrinho = str(self.carrinho)

            carrinho = carrinho.replace("\'", "\"")

            # salvando o carrinho no perfil

            current_user.update(old_cart=str(carrinho))

        thing = self.carrinho
        return thing

    def delete(self, produto):
        produto_id = str(produto)
        # Deletrando do carrinho
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]

        self.session.modified = True

        if self.request.user.is_authenticated:

            current_user = Perfil.objects.filter(user__id=self.request.user.id)

            carrinho = str(self.carrinho)

            carrinho = carrinho.replace("\'", "\"")

            # salvando o carrinho no perfil

            current_user.update(old_cart=str(carrinho))
