# VIEW - Responsável APENAS pela exibição de informações do jogador
# Separação clara: Model tem os dados, View os exibe, Controller coordena
class JogadorView:
    @staticmethod
    def mostrar_status(jogador):
        # Responsabilidade única: formatar e exibir status do jogador
        # Recebe objeto jogador mas NÃO modifica seus dados
        # Apenas lê e apresenta as informações de forma organizada
        print("\n *=================================*")
        print(f" *  STATUS DO {jogador.nome}       ")
        print(f" *                                 ")
        print(f" *  Classe: {jogador.classe}        ")
        print(f" *  Nível: {jogador.nivel}         ")
        print(f" *  Vida: {jogador.vida}          ")
        print(f" *  Mana: {jogador.mana}          ")
        print(f" *  XP: {jogador.xp}            ")
        print(f" *  Ouro: {jogador.ouro}          ")
        print(f" *  Agilidade: {jogador.agilidade}     ")
        print(f" *  Inteligência: {jogador.inteligencia}  ")
        print(f" *                                 ")
        print("  *=================================*")

    @staticmethod
    def mostrar_subida_nivel(jogador):
        # Exibe mensagem de parabéns por subir de nível
        # View apenas apresenta, não calcula nem modifica nível
        print(f"PARABÉNS {jogador.nome} por subir de nível {jogador.nivel}")
        print("Todos seus atributos foram melhorados")
        print(" ")
        input("Pressione enter para continuar...")

    @staticmethod
    def mostrar_personagem_criado(jogador):
        # Mensagem de boas-vindas após criação do personagem
        print(f"\n{jogador.nome}, sua aventura está pronta para iniciar!!!")

    @staticmethod
    def mostrar_item_ganho(item, bonus_texto):
        # Exibe item ganho com seus bônus
        # Recebe informações já processadas pelo Controller
        print(f"Você ganhou {item} {bonus_texto}!")
        input("Pressione enter para continuar...")