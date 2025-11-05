import random

# MODEL - Representa os dados e regras de negócio do jogador
# Responsabilidade única: Gerenciar apenas os dados e comportamentos do jogador
class Jogador:
    def __init__(self, classe):
        # Inicializa os atributos básicos do jogador
        # Cada atributo tem uma responsabilidade específica no jogo

        self.classe = classe.lower()
        self.nivel = 1
        self.xp = 0
        self.xp_proximo_nivel = 100
        self.ouro = 100
        self.aethernox = 0
        
        # Delega a definição de atributos para um método específico
        # Princípio da responsabilidade única: cada método faz uma coisa
        self._definir_atributos_classe(classe)
        
        # Define vida e mana atuais baseadas nos valores máximos
        self.vida = self.vida_max
        self.mana = self.mana_max
        self.inventario = {"poção de vida": 4, "poção de mana": 4}

    def _definir_atributos_classe(self, classe):
        # Método privado (prefixo _) - responsável APENAS por definir atributos por classe
        # Usa dicionário para evitar múltiplos if/elif - mais limpo e extensível
        atributos = {
            "guerreira": {"nome": "JOANA D'ARC", "vida_max": 120, "mana_max": 30, "forca": 15, "defesa": 12, "agilidade": 6, "inteligencia": 4},
            "mago": {"nome": "MERLIN","vida_max": 80, "mana_max": 100, "forca": 6, "defesa": 5, "agilidade": 8, "inteligencia": 15},
            "arqueiro": {"nome":"ROBIN HOOD","vida_max": 100, "mana_max": 50, "forca": 10, "defesa": 8, "agilidade": 15, "inteligencia": 7}
        }
        
        # Busca os atributos da classe, usa arqueiro como padrão se não encontrar
        stats = atributos.get(classe.lower(), atributos["arqueiro"])
        
        # setattr define dinamicamente os atributos do objeto
        # Evita repetir self.vida_max = stats["vida_max"] para cada atributo
        for attr, valor in stats.items():
            setattr(self, attr, valor)

    def atacar(self):
        # Método com responsabilidade única: calcular dano de ataque físico
        # Combina força do jogador com fator aleatório
        return self.forca + random.randint(1, 10)

    def usar_magia(self):
        # Responsabilidade única: gerenciar uso de magia
        # Verifica se tem mana suficiente antes de executar
        if self.mana < 15:
            return 0
        
        # Consome mana e calcula resultado da magia
        self.mana -= 15
        ataque = random.randint(1, 20)
        
        # Magia pode falhar e causar dano ao próprio jogador (risco vs recompensa)
        if ataque < 5:
            self.vida -= 10
            return ataque
        
        # Sucesso: dano baseado na inteligência + fator aleatório
        return self.inteligencia + ataque

    def usar_item(self, item):
        # Responsabilidade única: gerenciar uso de itens do inventário
        # Valida se o item existe e está disponível
        if item not in self.inventario or self.inventario[item] <= 0:
            return "Item não disponível"
        
        # Consome o item do inventário
        self.inventario[item] -= 1
        
        # Aplica efeito específico de cada item
        if item == "poção de vida":
            # min() garante que não cure além do máximo
            cura = min(30, self.vida_max - self.vida)
            self.vida += cura
            return f"Você recuperou {cura} pontos de vida"
        elif item == "poção de mana":
            mana_recuperada = min(30, self.mana_max - self.mana)
            self.mana += mana_recuperada
            return f"Você recuperou {mana_recuperada} pontos de mana"

    def ganhar_xp(self, xp):
        # Responsabilidade única: gerenciar ganho de experiência
        self.xp += xp
        # Verifica automaticamente se deve subir de nível
        if self.xp >= self.xp_proximo_nivel:
            self.subir_nivel()

    def subir_nivel(self):
        # Responsabilidade única: gerenciar progressão de nível
        # Aumenta nível e ajusta XP necessário para próximo nível
        self.nivel += 1
        self.xp = 10  # XP excedente após subir de nível
        self.xp_proximo_nivel += 50  # Aumenta requisito para próximo nível
        
        # Melhora todos os atributos do jogador
        self.vida_max += 20
        self.mana_max += 10
        self.forca += 2
        self.defesa += 2
        self.agilidade += 5
        self.inteligencia += 2
        
        # Restaura vida e mana completamente ao subir de nível
        self.vida = self.vida_max
        self.mana = self.mana_max

    def receber_dano(self, dano):
        # Responsabilidade única: calcular e aplicar dano recebido
        # Defesa reduz dano, mas sempre recebe pelo menos 1 de dano
        dano_recebido = max(1, dano - self.defesa // 2)
        self.vida -= dano_recebido
        return dano_recebido

    def esta_vivo(self):
        # Método simples para verificar se jogador ainda está vivo
        # Encapsula a lógica de verificação em um método claro
        return self.vida > 0

    def ganhar_item_classe(self):
        # Responsabilidade única: aplicar bônus específico da classe
        # Cada classe ganha um item diferente com bônus únicos
        bonus = {
            "guerreira": {"forca": 5, "item": "espada de aço"},
            "mago": {"inteligencia": 5, "item": "cajado de carvalho élfico"},
            "arqueiro": {"agilidade": 4, "item": "arco de caça de longo alcance"}
        }
        
        classe_bonus = bonus.get(self.classe.lower())
        if classe_bonus:
            # Aplica todos os bônus de atributos (exceto o nome do item)
            for attr, valor in classe_bonus.items():
                if attr != "item" and hasattr(self, attr):
                    # getattr pega o valor atual, soma o bônus, setattr define o novo valor
                    setattr(self, attr, getattr(self, attr) + valor)
            return classe_bonus["item"]
        return None