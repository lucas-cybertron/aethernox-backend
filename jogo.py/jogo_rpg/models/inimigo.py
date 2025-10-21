import random

# MODEL - Representa os dados e comportamentos de um inimigo
# Responsabilidade única: Gerenciar apenas dados e ações do inimigo
# Mais simples que o jogador pois inimigos têm menos funcionalidades
class Inimigo:
    def __init__(self, nome, vida, forca, xp_inimigo, ouro_inimigo):
        # Inicializa atributos básicos do inimigo
        # Inimigos são mais simples: não têm inventário, magia ou progressão
        self.nome = nome
        self.vida = vida
        self.vida_max = vida  # Mantém referência da vida máxima para exibição
        self.forca = forca
        self.xp_inimigo = xp_inimigo  # XP que o jogador ganha ao derrotar
        self.ouro_inimigo = ouro_inimigo  # Ouro que o jogador ganha ao derrotar

    def atacar(self):
        # Responsabilidade única: calcular dano de ataque do inimigo
        # Mesmo sistema do jogador: força base + fator aleatório
        return self.forca + random.randint(1, 10)

    def receber_dano(self, dano):
        # Responsabilidade única: aplicar dano recebido
        # Inimigos não têm defesa, recebem dano total
        self.vida -= dano

    def esta_vivo(self):
        # Verifica se inimigo ainda está vivo
        # Método simples mas importante para lógica de combate
        return self.vida > 0