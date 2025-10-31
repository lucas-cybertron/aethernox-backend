# VIEW - Interface visual da loja
# Responsabilidade única: exibir itens disponíveis e preços
class LojaView:
    @staticmethod
    def mostrar_boas_vindas():
        print("\n=== Bem-vindo à Loja! ===")
        print("Aqui você pode comprar equipamentos e poções para melhorar seu personagem.\n")
    
    @staticmethod
    def mostrar_itens(itens_disponiveis):
        if not itens_disponiveis:
            print("\n--- Nenhum item disponível ---")
            return

        print("\n=== Itens disponíveis na Loja ===")
        for i, item in enumerate(itens_disponiveis, start=1):
            nome = item.get("nome", "Item desconhecido")
            preco = item.get("preco", 0)
            # Usa get para evitar KeyError quando não houver 'bonus'
            bonus_texto = ", ".join([f"{k}: {v}" for k, v in item.get("bonus", {}).items()])
            if bonus_texto:
                print(f"{i}º - {nome} | Preço: {preco} ouro | Bônus: {bonus_texto}")
            else:
                # Para itens como poções que não têm bônus
                print(f"{i}º - {nome} | Preço: {preco} ouro")
                
                
    @staticmethod
    def mostrar_compra_sucesso(nome_item, bonus):
        bonus_texto = ", ".join([f"{k}: {v}" for k, v in bonus.items()]) if bonus else ""
        if bonus_texto:
            print(f"Compra realizada! Você adquiriu {nome_item} | Bônus: {bonus_texto}")
        else:
            print(f"Compra realizada! Você adquiriu {nome_item}")

    @staticmethod
    def mostrar_compra_falha(mensagem):
        print(f"Falha na compra: {mensagem}")

    @staticmethod
    def mostrar_saida():
        print("Saindo da loja...")
    
                
    @staticmethod
    def pedir_escolha():
        try:
            escolha = int(input("Escolha o número do item ou 0 para sair: "))
            return escolha
        except ValueError:
            print("Digite apenas números válidos!")
            return -1
