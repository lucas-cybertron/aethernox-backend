# Importações organizadas por camada MVC
from models.jogador import Jogador  # Model
from views.menu_view import MenuView  # View
from views.jogador_view import JogadorView  # View
from controllers.cenario_controller import CenarioController  # Controller

# CONTROLLER - Coordena interação entre Models e Views
# Responsabilidade única: gerenciar fluxo principal do jogo
# Não contém lógica de negócio (Model) nem apresentação (View)
class JogoController:
    def __init__(self):
        # Inicializa controller sem jogador (será criado quando necessário)
        self.jogador = None

    def executar(self):
        # Loop principal do jogo - coordena todo o fluxo
        # Responsabilidade: interpretar escolhas do usuário e delegar ações
        while True:
            # View coleta entrada, Controller processa
            escolha = MenuView.mostrar_menu_principal()
            
            if escolha == "1":
                self.iniciar_novo_jogo()  # Delega criação de jogo
            elif escolha == "2":
                MenuView.mostrar_jogo_finalizado()  # View exibe, Controller controla fluxo
                break
            else:
                MenuView.mostrar_opcao_invalida()  # View trata erro de entrada

    def iniciar_novo_jogo(self):
        # Coordena criação de novo jogo
        # Separa responsabilidades: View coleta dados, Model cria objeto, Controller coordena
        
        # View coleta informações do usuário
        classe = MenuView.mostrar_criacao_personagem()
        
        # Model cria o jogador com os dados fornecidos
        self.jogador = Jogador(classe)
        
        # Views exibem informações
        JogadorView.mostrar_personagem_criado(self.jogador)
        JogadorView.mostrar_status(self.jogador)
        MenuView.aguardar_enter("Pressione enter para começar...")
        
        # Delega controle dos cenários para controller específico
        cenario_controller = CenarioController(self.jogador)
        cenario_controller.executar_cenarios()