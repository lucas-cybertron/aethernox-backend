from models.ia_dificuldade import IADificuldade

# CONTROLLER: Intermedia o uso da IA com o restante do jogo
class InteligenciaController:
    def __init__(self):
        self.ia = IADificuldade()

    def ajustar_dificuldade(self, nivel_jogador):
        """Retorna a força recomendada do inimigo com base no nível"""
        return self.ia.prever_forca_inimigo(nivel_jogador)

    def registrar_resultado(self, nivel_jogador, vitoria):
        """
        Atualiza a IA com o resultado da batalha:
          - Se vitória fácil → aumenta dificuldade
          - Se derrota → reduz dificuldade
        """
        resultado = +1 if vitoria else -1
        self.ia.atualizar_dados_treino(nivel_jogador, resultado)
