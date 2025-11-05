import random

# MODEL - Gerencia a lógica de combate entre jogador e inimigo
# Responsabilidade única: Coordenar turnos e regras de batalha
# Separa a lógica de combate da interface (View) e controle (Controller)
class Combate:
    def __init__(self, jogador, inimigo):
        # Inicializa combate com referências aos participantes
        # Não cria cópias, trabalha com os objetos originais
        self.jogador = jogador
        self.inimigo = inimigo
        self.turno = 1  # Contador de turnos para exibição

    def executar_turno_jogador(self, acao, item=None):
        # Responsabilidade única: processar ações do jogador no combate
        # Retorna dicionário com resultado para o Controller decidir o que fazer
        resultado = {"sucesso": True, "mensagem": "", "dano": 0}
        
        if acao == "atacar":
            # Executa ataque físico
            dano = self.jogador.atacar()
            self.inimigo.receber_dano(dano)
            resultado["dano"] = dano
            resultado["mensagem"] = f"Ataque de {dano} dano no inimigo"
            
        elif acao == "magia":
            # Executa ataque mágico (pode falhar por falta de mana)
            dano = self.jogador.usar_magia()
            if dano > 0:
                self.inimigo.receber_dano(dano)
                resultado["dano"] = dano
                resultado["mensagem"] = f"Ataque de {dano} dano mágico no inimigo"
            else:
                resultado["sucesso"] = False
                resultado["mensagem"] = "Mana insuficiente!"
                
        elif acao == "item" and item:
            # Usa item do inventário (delega para o método do jogador)
            resultado["mensagem"] = self.jogador.usar_item(item)
            
        elif acao == "fugir":
            # Tentativa de fuga com chance de falha
            if random.randint(1, 6) >= 5:
                resultado["mensagem"] = "Você conseguiu fugir do combate!"
                resultado["fugiu"] = True  # Flag especial para indicar fuga
            else:
                resultado["sucesso"] = False
                resultado["mensagem"] = "Você falhou ao fugir do combate!"
                
        return resultado

    def executar_turno_inimigo(self):
        # Se o inimigo estiver morto, não faz nada
        if not self.inimigo.esta_vivo():
            return {"dano": 0, "mensagem": ""}

        # Inimigo tenta atacar o jogador
        ataque = self.inimigo.atacar(self.jogador)
        dano_inimigo = ataque["dano"]
        mensagem = ataque["mensagem"]

        # Aplica o dano ao jogador
        dano_recebido = max(1, int(dano_inimigo * 0.9 - self.jogador.defesa * 0.2))

        # Se o ataque acertou, substitui o texto por algo mais direto
        if dano_inimigo > 0:
            mensagem = f"{self.inimigo.nome} causou {dano_recebido} de dano!"
            self.jogador.vida -= dano_recebido

        # Garante que a vida não fique negativa
        if self.jogador.vida < 0:
            self.jogador.vida = 0

        # Atualiza mensagem para feedback
        if dano_inimigo > 0:
            mensagem = f"{self.inimigo.nome} causou {dano_recebido} de dano!"
        else:
            mensagem = f"{self.inimigo.nome} errou o ataque!"

        return {
            "dano": dano_recebido,
            "mensagem": mensagem
        }
        
    def verificar_fim_combate(self):
        # Responsabilidade única: verificar condições de fim de combate
        # Retorna informações para o Controller decidir o que fazer
        
        if not self.inimigo.esta_vivo():
            # Jogador venceu: ganha recompensas
            self.jogador.ganhar_xp(self.inimigo.xp_inimigo)
            self.jogador.ouro += self.inimigo.ouro_inimigo
            return {
                "fim": True,
                "vitoria": True,
                "mensagem": f"Você derrotou {self.inimigo.nome}! Ganhou {self.inimigo.xp_inimigo} XP e {self.inimigo.ouro_inimigo} moedas de ouro!"
            }
            
        if not self.jogador.esta_vivo():
            # Jogador perdeu: game over
            return {
                "fim": True,
                "vitoria": False,
                "mensagem": "GAME OVER!!! Você foi derrotado..."
            }
            
        # Combate continua
        return {"fim": False}

    def proximo_turno(self):
        # Avança contador de turnos
        # Método simples mas importante para organização
        self.turno += 1