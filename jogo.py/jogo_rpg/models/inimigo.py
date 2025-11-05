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

    def atacar(self, jogador):
        """O inimigo tenta atacar o jogador, mas pode errar com base na agilidade do jogador."""
        base_erro = 0.1  # chance base de 10%
        bonus_esquiva = jogador.agilidade * 0.01  # +1% de esquiva por ponto de agilidade
        chance_erro = min(0.4, base_erro + bonus_esquiva)  # máximo de 40% de erro

        # Verifica se o ataque erra
        if random.random() < chance_erro:
            print(f"💨 {jogador.nome} esquivou do ataque de {self.nome}!")
            return {"dano": 0, "mensagem": f"{self.nome} errou o ataque!"}

        # --- Cálculo de dano ---
        dano_bruto = random.randint(int(self.forca * 0.8), int(self.forca * 1.5))

        # A defesa reduz cerca de 10% do seu valor (para não anular totalmente o ataque)
        reducao_defesa = int(jogador.defesa * 0.1)
        dano_final = max(1, dano_bruto - reducao_defesa)

        mensagem = f"⚔️ {self.nome} atacou causando {dano_final} de dano!"
        return {"dano": dano_final, "mensagem": mensagem}
    
    def receber_dano(self, dano):
        # Responsabilidade única: aplicar dano recebido
        # Inimigos não têm defesa, recebem dano total
        self.vida -= dano

    def esta_vivo(self):
        # Verifica se inimigo ainda está vivo
        # Método simples mas importante para lógica de combate
        return self.vida > 0