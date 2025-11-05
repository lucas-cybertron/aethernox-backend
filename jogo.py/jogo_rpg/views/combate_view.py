# VIEW - Interface visual para o sistema de combate
# Responsabilidade única: apresentar informações de combate e coletar ações do jogador
# Não processa lógica de combate, apenas exibe e coleta dados
class CombateView:
    @staticmethod
    def mostrar_inicio_combate(jogador, inimigo):
        # Exibe cabeçalho do combate
        # Apresentação visual simples mas importante para imersão
        print("\n Combate Iniciado!!!")
        print(f"{jogador.nome} vs {inimigo.nome}")

    @staticmethod
    def mostrar_status_combate(jogador, inimigo, turno):
        # Exibe status atual do combate a cada turno
        # Informações essenciais: vida dos participantes, mana do jogador
        print(f"\n ---turno {turno}---")
        print(" ")
        print(f"{inimigo.nome} : vida = {inimigo.vida} / {inimigo.vida_max}")
        print(" ")
        print(f"{jogador.classe} : {jogador.nome} : vida = {jogador.vida} / {jogador.vida_max}")
        print(" ")
        print(f"{jogador.classe} : {jogador.nome} : mana = {jogador.mana} / {jogador.mana_max}")
        print(" ")

    @staticmethod
    def mostrar_menu_combate():
        # Exibe opções de ação do jogador no combate
        # Inclui validação básica de entrada (parte da apresentação)
        print("===========================")
        print("*  1 - Atacar             *")
        print("*  2 - Magia (15 de mana) *")
        print("*  3 - Usar Item          *")
        print("*  4 - Fugir              *")
        print("===========================")
        
        try:
            return int(input("Escolha: "))
        except ValueError:
            return 0  # Retorna valor inválido para o Controller tratar

    @staticmethod
    def mostrar_itens_disponiveis(jogador):
        # Exibe itens do inventário e permite seleção
        # Lê dados do jogador mas não os modifica (isso fica para o Model)
        print("\n ---Itens disponíveis---")
        itens_disponiveis = []
        contador = 1
        
        # Lista apenas itens com quantidade > 0
        for item, qtd in jogador.inventario.items():
            if qtd > 0:
                print(f"{contador}º {item} - ({qtd})")
                itens_disponiveis.append(item)
                contador += 1
        
        if not itens_disponiveis:
            print("\n---Nenhum item disponível no inventário---")
            return None
        
        # Coleta e valida escolha do usuário
        try:
            escolha_item = int(input("Escolha o número do item: ")) - 1
            if 0 <= escolha_item < len(itens_disponiveis):
                return itens_disponiveis[escolha_item]  # Retorna item válido
            else:
                print("\n ---Item escolhido é inválido---")
                return None
        except ValueError:
            print("\n Digite apenas números")
            return None

    @staticmethod
    def mostrar_resultado_acao(mensagem):
        # Exibe resultado de uma ação (ataque, magia, item, etc.)
        # Recebe mensagem já formatada do Model/Controller
        print(mensagem)
    
    @staticmethod
    def mostrar_texto(mensagem):
        # Exibe uma mensagem genérica ao jogador durante o combate
        # Usado pelo Controller para feedbacks sem lógica extra
        print("\n✨ " + mensagem + " ✨\n")

        

    @staticmethod
    def mostrar_fim_combate(resultado):
        # Exibe mensagem de fim de combate (vitória ou derrota)
        # Recebe resultado processado pelo Model de combate
        print(resultado["mensagem"])