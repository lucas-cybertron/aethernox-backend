from models.combate import Combate  # Model - lógica de combate
from views.combate_view import CombateView  # View - interface de combate

# CONTROLLER - Coordena combate entre Model e View
# Responsabilidade única: gerenciar fluxo de combate
# Interpreta ações do usuário, delega para Model, exibe via View
class CombateController:
    def __init__(self, jogador, inimigo):
        # Cria Model de combate e instância da View
        # Controller conecta Model e View sem misturar responsabilidades
        self.combate = Combate(jogador, inimigo)  # Model gerencia lógica
        self.view = CombateView()  # View gerencia apresentação

    def executar_combate(self):
        # Método principal que coordena todo o fluxo de combate
        # Demonstra claramente a separação MVC: Controller orquestra, Model processa, View exibe
        
        # View exibe início do combate
        self.view.mostrar_inicio_combate(self.combate.jogador, self.combate.inimigo)
        
        # Loop principal do combate
        while self.combate.jogador.esta_vivo() and self.combate.inimigo.esta_vivo():
            # View exibe status atual
            self.view.mostrar_status_combate(
                self.combate.jogador, 
                self.combate.inimigo, 
                self.combate.turno
            )
            
            # View coleta ação do jogador
            escolha = self.view.mostrar_menu_combate()
            
            # Controller processa ação (delega para Model)
            resultado_jogador = self._processar_acao_jogador(escolha)
            
            # Verifica fuga (interrompe combate)
            if resultado_jogador.get("fugiu"):
                return False
            
            # View exibe resultado da ação
            if resultado_jogador["mensagem"]:
                self.view.mostrar_resultado_acao(resultado_jogador["mensagem"])
            
            # Model verifica fim de combate após ação do jogador
            fim_combate = self.combate.verificar_fim_combate()
            if fim_combate["fim"]:
                self.view.mostrar_fim_combate(fim_combate)
                return fim_combate["vitoria"]
            
            # Turno do inimigo (se ainda estiver vivo)
            if self.combate.inimigo.esta_vivo():
                resultado_inimigo = self.combate.executar_turno_inimigo()
                if resultado_inimigo["mensagem"]:
                    self.view.mostrar_resultado_acao(resultado_inimigo["mensagem"])
            
            # Verifica fim de combate após turno do inimigo
            fim_combate = self.combate.verificar_fim_combate()
            if fim_combate["fim"]:
                self.view.mostrar_fim_combate(fim_combate)
                return fim_combate["vitoria"]
            
            # Model avança para próximo turno
            self.combate.proximo_turno()
        
        return True

    def _processar_acao_jogador(self, escolha):
        # Método privado que traduz escolha do usuário em ação do Model
        # Demonstra como Controller faz a ponte entre View (entrada) e Model (processamento)
        
        if escolha == 1:
            # Delega ataque para o Model
            return self.combate.executar_turno_jogador("atacar")
        elif escolha == 2:
            # Delega magia para o Model
            return self.combate.executar_turno_jogador("magia")
        elif escolha == 3:
            # View coleta item, Controller passa para Model
            item = self.view.mostrar_itens_disponiveis(self.combate.jogador)
            if item:
                return self.combate.executar_turno_jogador("item", item)
            return {"sucesso": False, "mensagem": ""}
        elif escolha == 4:
            # Delega tentativa de fuga para o Model
            return self.combate.executar_turno_jogador("fugir")
        else:
            # Controller trata entrada inválida
            return {"sucesso": False, "mensagem": "Opção inválida!"}