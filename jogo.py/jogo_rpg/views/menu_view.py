# VIEW - Responsável APENAS pela apresentação visual dos menus
# Princípio da responsabilidade única: só cuida da interface
# Não contém lógica de negócio, apenas exibe informações e coleta entrada do usuário
class MenuView:
    @staticmethod  # Método estático: não precisa de instância da classe
    def mostrar_menu_principal():
        # Responsabilidade única: exibir menu principal e coletar escolha
        # Apenas apresentação visual, sem lógica de validação
        print("\n *===============================================*")
        print(" *                  Aethernox                      *")
        print(" *               (1) - Novo Jogo                   *")
        print(" *               (2) - Sair do Jogo                *")
        print("\n *===============================================*")
        return input("Digite um número: ")  # Retorna entrada para o Controller processar

    @staticmethod
    def mostrar_criacao_personagem():
        # Exibe opções de classe
        print("\n *===============================================*")
        print(" *            Escolha seu personagem               *")
        print(" *               (1) - Guerreiro - Joana dark      *")
        print(" *               (2) - Mago - Merlin               *")
        print(" *               (3) - Arqueiro - Robin hood       *")
        print("\n *===============================================*")
        print(" ")
        
        # Loop de validação de entrada (parte da interface)
        while True:
            try:
                classe = int(input("Qual o número da sua escolha: "))
                classes = {1: "guerreira", 2: "mago", 3: "arqueiro"}
                if classe in classes:
                    return classes[classe]  # Retorna dados válidos
                else:
                    print("Escolha incorreta!!")
                    print("Tente novamente")
            except ValueError:
                print("Digite apenas números!")

    @staticmethod
    def mostrar_opcao_invalida():
        # Exibe mensagem de erro para opção inválida
        print("Opção digitada não é válida!")
        input("Pressione enter para tentar novamente...")

    @staticmethod
    def mostrar_jogo_finalizado():
        # Exibe mensagem de finalização do jogo
        print("JOGO FINALIZADO")
        input("Pressione enter para finalizar...")

    @staticmethod
    def aguardar_enter(mensagem="Pressione enter para continuar..."):
        # Método utilitário para pausar e aguardar interação do usuário
        # Reutilizável em várias partes da interface
        input(mensagem)