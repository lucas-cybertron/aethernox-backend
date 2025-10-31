import numpy as np
from sklearn.linear_model import LinearRegression

# MODEL: Define o comportamento da IA de dificuldade
# Responsável apenas por aprender e prever a força recomendada dos inimigos
class IADificuldade:
    def __init__(self):
        # Modelo simples de regressão linear
        self.modelo = LinearRegression()
        
        # Dados de treino base iniciais (nível do jogador → força do inimigo)
        # Isso pode ser ajustado depois conforme o jogo coleta mais dados reais
        self.X_treino = np.array([[1], [2], [3], [4], [5]])
        self.y_treino = np.array([20, 30, 45, 60, 80])  # Força base dos inimigos
        
        # Treina o modelo inicial
        self.modelo.fit(self.X_treino, self.y_treino)

    def prever_forca_inimigo(self, nivel_jogador):
        """Prevê a força ideal do inimigo com base no nível atual do jogador"""
        forca = self.modelo.predict(np.array([[nivel_jogador]]))[0]
        return round(forca)

    def atualizar_dados_treino(self, nivel_jogador, resultado):
        """
        Atualiza o modelo com novos dados baseados no desempenho do jogador.
        Exemplo:
          resultado = +1 se foi muito fácil (aumentar dificuldade)
          resultado = -1 se foi muito difícil (reduzir dificuldade)
        """
        nova_forca = max(10, self.prever_forca_inimigo(nivel_jogador) + (resultado * 5))
        self.X_treino = np.append(self.X_treino, [[nivel_jogador]], axis=0)
        self.y_treino = np.append(self.y_treino, [nova_forca])
        self.modelo.fit(self.X_treino, self.y_treino)
