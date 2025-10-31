class Loja:
    def __init__(self):
        # Define itens disponíveis por classe com flag "comprado"
        self.itens_por_classe = {
            "guerreira": [
                {"nome": "Espada do Templário", "preco": 60, "bonus": {"forca": 7}, "comprado": False},
                {"nome": "Escudo de Ferro", "preco": 50, "bonus": {"defesa": 5}, "comprado": False},
                {"nome": "Elmo de Aço", "preco": 40, "bonus": {"vida_max": 20}, "comprado": False}
            ],
            "mago": [
                {"nome": "Cajado de Carvalho", "preco": 50, "bonus": {"inteligencia": 5}, "comprado": False},
                {"nome": "Robe Arcano", "preco": 40, "bonus": {"mana_max": 20}, "comprado": False},
                {"nome": "Anel de Mana", "preco": 30, "bonus": {"mana_max": 10}, "comprado": False}
            ],
            "arqueiro": [
                {"nome": "Arco Longo", "preco": 50, "bonus": {"agilidade": 5}, "comprado": False},
                {"nome": "Aljava de Flechas", "preco": 40, "bonus": {"forca": 3}, "comprado": False},
                {"nome": "Capa de Caçador", "preco": 30, "bonus": {"agilidade": 3}, "comprado": False}
            ]
        }
        self.itens_universais = [
            {"nome": "Poção de Vida", "preco": 20, "efeito": "cura", "valor": 30},
            {"nome": "Poção de Mana", "preco": 20, "efeito": "mana", "valor": 30},
        ]

    def obter_itens_classe(self, jogador):
        """
        Retorna apenas os itens NÃO comprados da classe do jogador.
        """
        classe = jogador.classe.lower()
        itens = self.itens_por_classe.get(classe, [])
        return [item for item in itens if not item["comprado"]]

    def comprar_item(self, jogador, indice_item):
        """
        Processa a compra de um item com base no índice escolhido.
        Retorna (sucesso, resultado).
        """
        itens = self.obter_itens_classe(jogador)
        
        if indice_item < 1 or indice_item > len(itens):
            return False, "Item inválido!"
        
        item = itens[indice_item - 1]
        
        if jogador.ouro < item["preco"]:
            return False, "Ouro insuficiente!"
        
        # Deduz o custo
        jogador.ouro -= item["preco"]
        
        # Marca item como comprado
        classe_itens = self.itens_por_classe[jogador.classe.lower()]
        for original_item in classe_itens:
            if original_item["nome"] == item["nome"]:
                original_item["comprado"] = True
                break
        
        # Adiciona ao inventário
        jogador.inventario[item["nome"]] = jogador.inventario.get(item["nome"], 0) + 1
        
        # Aplica bônus
        for atributo, valor in item["bonus"].items():
            if hasattr(jogador, atributo):
                setattr(jogador, atributo, getattr(jogador, atributo) + valor)
        
        return True, item
