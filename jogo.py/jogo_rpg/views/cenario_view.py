# VIEW - Apresentação visual dos cenários e narrativa do jogo
# Responsabilidade única: exibir textos narrativos e ambientar o jogador
# Separa conteúdo narrativo da lógica de jogo
class CenarioView:
    @staticmethod
    def mostrar_vila_elder():
        # Apresentação da narrativa inicial do jogo
        # Responsabilidade única: contar a história e ambientar o jogador
        # Não contém lógica de jogo, apenas conteúdo narrativo
        print("\n *================================================*")
        print(" *                 Floresta Morta                   *")
        print(" *                                                  *")
        print(" *   *")
        print(" *   *")
        print(" *          *")
        print(" *                                                  *")
        print(" *      *")
        print(" *      *")
        print(" *       *")
        print(" *                                      *")
        print(" *                                                  *")
        print(" *          *")
        print(" *         *")
        print(" *       *")
        print(" *                                                  *")
        print("\n *================================================*")

    @staticmethod
    def mostrar_primeiro_combate():
        # Apresentação dramática antes do primeiro combate
        # Cria tensão e expectativa para o jogador
        print("\n *===============================================*")
        print(" *                Primeiro combate                  *")
        print(" *                                                  *")
        print(" *                 LADRÃO DE MÓRIA                  *")
        print("\n *===============================================*")
        input("Pressione enter para continuar...")

    @staticmethod
    def mostrar_jornada_acabou():
        # Mensagem de fim de jogo por derrota ou fuga
        print("Sua jornada acaba aqui!!")
        input("Pressione enter para continuar...")

    @staticmethod
    def mostrar_jogo_completo():
        # Mensagem de conclusão bem-sucedida do jogo
        print("JOGO FINALIZADO")
        input("Pressione enter para finalizar...")