from models.inimigo import Inimigo  # Model
from views.cenario_view import CenarioView  # View
from views.jogador_view import JogadorView  # View
from controllers.combate_controller import CombateController  # Controller

# CONTROLLER - Gerencia progressão de cenários do jogo
# Responsabilidade única: coordenar sequência de eventos e combates
# Conecta narrativa (View) com mecânicas (Model) e outros Controllers
class CenarioController:
    def __init__(self, jogador):
        # Recebe referência do jogador para gerenciar progressão
        self.jogador = jogador

    def executar_cenarios(self):
        # Coordena execução sequencial dos cenários
        # Lista extensível: fácil adicionar novos cenários
        cenarios = [self.vila_elder]
        
        for cenario in cenarios:
            # View exibe status antes de cada cenário
            JogadorView.mostrar_status(self.jogador)
            
            # Executa cenário - se falhar, termina jogo
            if not cenario():
                CenarioView.mostrar_jornada_acabou()
                return
            
            # Verifica condição de vitória (Model define, Controller verifica)
            if self.jogador.reliquias == 3:
                CenarioView.mostrar_jogo_completo()
                JogadorView.mostrar_status(self.jogador)
                return

    def vila_elder(self):
        # Cenário específico: Vila Elder
        # Combina narrativa (View) com mecânicas (Model/Controller)
        
        # Views exibem narrativa
        CenarioView.mostrar_vila_elder()
        CenarioView.mostrar_primeiro_combate()
        
        # Model cria inimigo com atributos específicos
        ladrao = Inimigo("Ladrão de Mória", 30, 8, 30, 20)
        
        # Delega combate para Controller especializado
        combate_controller = CombateController(self.jogador, ladrao)
        
        # Se vencer o combate, ganha recompensa
        if combate_controller.executar_combate():
            # Model aplica bônus, Controller coordena, View exibe
            item_ganho = self.jogador.ganhar_item_classe()
            bonus_texto = self._obter_bonus_texto(self.jogador.classe)
            JogadorView.mostrar_item_ganho(item_ganho, bonus_texto)
            return True  # Cenário concluído com sucesso
        
        return False  # Falhou no combate

    def _obter_bonus_texto(self, classe):
        # Método utilitário para formatar texto de bônus
        # Separa lógica de apresentação da lógica de negócio
        bonus = {
            "guerreiro": "(+5 de força)",
            "mago": "(+5 de inteligência)",
            "elfo": "(+2 de agilidade e +3 de inteligência)",
            "arqueiro": "(+4 de agilidade)"
        }
        return bonus.get(classe.lower(), "")