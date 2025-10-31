from models.inimigo import Inimigo  # Model
from models.loja import Loja
from models.jogador import Jogador  # Model
from views.loja_view import LojaView
from views.jogador_view import JogadorView
from controllers.combate_controller import CombateController  # Controller
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random
from views.cenario_view import CenarioView

class CenarioController:
    def __init__(self, jogador: Jogador):
        self.jogador = jogador

        # Dataset inicial fictício para ML
        dados_guerreira = [
            {"forca_j": 15, "vida_j": 120, "agilidade_j": 6, "vida_i": 30, "forca_i": 8, "resultado": "vitoria"},
            {"forca_j": 12, "vida_j": 110, "agilidade_j": 6, "vida_i": 40, "forca_i": 10, "resultado": "vitoria"},
            {"forca_j": 8, "vida_j": 90, "agilidade_j": 5, "vida_i": 60, "forca_i": 12, "resultado": "derrota"},
        ]
        dados_mago = [
            {"forca_j": 6, "vida_j": 80, "agilidade_j": 8, "vida_i": 50, "forca_i": 12, "resultado": "derrota"},
            {"forca_j": 10, "vida_j": 90, "agilidade_j": 7, "vida_i": 40, "forca_i": 10, "resultado": "vitoria"},
        ]
        dados_arqueiro = [
            {"forca_j": 10, "vida_j": 100, "agilidade_j": 15, "vida_i": 50, "forca_i": 12, "resultado": "vitoria"},
            {"forca_j": 7, "vida_j": 85, "agilidade_j": 12, "vida_i": 70, "forca_i": 15, "resultado": "derrota"},
        ]
        exemplos_extremos = [
            {"forca_j": 1, "vida_j": 10, "agilidade_j": 6, "vida_i": 50, "forca_i": 12, "resultado": "derrota"},
            {"forca_j": 20, "vida_j": 150, "agilidade_j": 10, "vida_i": 20, "forca_i": 5, "resultado": "vitoria"},
        ]

        # Combina tudo em um único DataFrame
        self.dados_ml = pd.DataFrame(dados_guerreira + dados_mago + dados_arqueiro + exemplos_extremos*3)
         
        self.modelo = DecisionTreeClassifier()
        self._treinar_modelo()

    # ---------------- ML ----------------
    def _treinar_modelo(self):
        X = self.dados_ml[["forca_j", "vida_j", "agilidade_j", "vida_i", "forca_i"]]
        y = self.dados_ml["resultado"]
        self.modelo.fit(X, y)

    def prever_resultado(self, inimigo: Inimigo):
        novo_cenario = pd.DataFrame([{
            "forca_j": self.jogador.forca,
            "vida_j": self.jogador.vida,
            "agilidade_j": self.jogador.agilidade,
            "vida_i": inimigo.vida,
            "forca_i": inimigo.forca
        }])
        prob = self.modelo.predict_proba(novo_cenario)[0]
        prob_vitoria = prob[list(self.modelo.classes_).index("vitoria")]
    
        classe_prevista = self.modelo.predict(novo_cenario)[0]
        return classe_prevista, prob_vitoria
            
    def registrar_resultado(self, inimigo: Inimigo, resultado: str):
        novo_dado = {
            "forca_j": self.jogador.forca,
            "vida_j": self.jogador.vida,
            "agilidade_j": self.jogador.agilidade,
            "vida_i": inimigo.vida,
            "forca_i": inimigo.forca,
            "resultado": resultado
        }
        self.dados_ml = pd.concat([self.dados_ml, pd.DataFrame([novo_dado])], ignore_index=True)
        self._treinar_modelo()
        
    def balancear_inimigo(self, inimigo: Inimigo, alvo_prob=0.6):
        """
        Ajusta inimigo para que a chance de vitória do jogador fique próxima de 'alvo_prob'
        sem criar inimigos absurdamente fortes.
        """
        _, prob_vitoria = self.prever_resultado(inimigo)

        max_vida = int(self.jogador.vida * 1.2)
        max_forca = int(self.jogador.forca * 1.2)
        min_vida = int(self.jogador.vida * 0.3)
        min_forca = 1

        tentativas = 0
        while abs(prob_vitoria - alvo_prob) > 0.03 and tentativas < 15:
            dif = prob_vitoria - alvo_prob

            # Ajuste proporcional baseado na diferença
            inimigo.forca = max(min_forca, min(int(inimigo.forca * (1 + dif)), max_forca))
            inimigo.vida  = max(min_vida, min(int(inimigo.vida * (1 + dif)), max_vida))

            _, prob_vitoria = self.prever_resultado(inimigo)
            tentativas += 1

        return inimigo


    # ---------------- Cenários ----------------
    def executar_cenarios(self):
        cenarios = [
            self.floresta_morta,
            self.visitar_loja,
            self.floresta_assombrada,
            self.visitar_loja,
            self.caverna_misteriosa,
            self.visitar_loja
        ]

        for cenario in cenarios:
            if not cenario():
                print("Jornada acabou!")
                return

            if self.jogador.reliquias >= 3:
                print("Parabéns! Você completou o jogo!")
                return

    def floresta_morta(self):
        print("\n--- Floresta Morta ---")
        CenarioView.mostrar_vila_elder()
        JogadorView.mostrar_status(self.jogador)
        ladrao = Inimigo("Ladrão de Mória", 30, 8, 30, 20)
        ladrao = self.balancear_inimigo(ladrao, alvo_prob=0.6)  # 60% de chance de vitória do jogador
        classe_prevista, prob_vitoria = self.prever_resultado(ladrao)
        print(f"[ML] Probabilidade de vitória do jogador após balanceamento: {prob_vitoria*100:.1f}%")


        
        # Prever resultado antes do combate
        previsao = self.prever_resultado(ladrao)
        print(f"[ML] Previsão do combate: {previsao}")
        print(f"[IA] Previsão de combate: {previsao}")

        # Executar combate
        combate_controller = CombateController(self.jogador, ladrao)
        vitoria = combate_controller.executar_combate()
        self.jogador.vida = self.jogador.vida_max
        # Registrar resultado no ML
        self.registrar_resultado(ladrao, "vitoria" if vitoria else "derrota")

        if vitoria:
            item_ganho = self.jogador.ganhar_item_classe()
            print(f"Você ganhou: {item_ganho}")
            return True

        return False

    def visitar_loja(self):
        loja = Loja()
        LojaView.mostrar_boas_vindas()

        while True:
            # Mostra ouro atual do jogador
            print(f"\nSeu ouro atual: {self.jogador.ouro}")
            
            # Obtém itens da classe do jogador + itens universais
            itens_disponiveis = loja.obter_itens_classe(self.jogador) + loja.itens_universais
            LojaView.mostrar_itens(itens_disponiveis)

            # Pede escolha do jogador (já retorna int)
            escolha = LojaView.pedir_escolha()

            # Validação do input
            if escolha < 0 or escolha > len(itens_disponiveis):
                LojaView.mostrar_compra_falha("Escolha inválida!")
                continue

            if escolha == 0:
                LojaView.mostrar_saida()
                break

            # Compra de item
            sucesso, resultado = loja.comprar_item(self.jogador, escolha)

            if sucesso:
                # Usa get para evitar KeyError em bonus
                bonus = resultado.get("bonus", {})
                LojaView.mostrar_compra_sucesso(resultado["nome"], bonus)
                print("\n--- STATUS ATUALIZADO ---")
                JogadorView.mostrar_status(self.jogador)
            else:
                LojaView.mostrar_compra_falha(resultado)

        return True
    def floresta_assombrada(self):
        print("\n--- Floresta Assombrada ---")
        CenarioView.mostrar_floresta_assombrada()
        JogadorView.mostrar_status(self.jogador)

        # Inimigos normais
        inimigos = [
            Inimigo(
                "Espectro Sombrio",
                vida=random.randint(20, 50),
                forca=random.randint(5, 12),
                xp_inimigo=15,
                ouro_inimigo=random.randint(5, 15)
            ),
            Inimigo(
                "Lobo Fantasma",
                vida=random.randint(20, 50),
                forca=random.randint(5, 12),
                xp_inimigo=15,
                ouro_inimigo=random.randint(5, 15)
            ),
        ]

        # Batalha com inimigos normais
        for inimigo in inimigos:
            inimigo = self.balancear_inimigo(inimigo, alvo_prob=0.65)
            classe_prevista, prob_vitoria = self.prever_resultado(inimigo)
            print(f"[ML] Enfrentando {inimigo.nome} | Probabilidade de vitória: {prob_vitoria*100:.1f}%")
            
            combate_controller = CombateController(self.jogador, inimigo)
            vitoria = combate_controller.executar_combate()
            self.jogador.vida = self.jogador.vida_max
            self.registrar_resultado(inimigo, "vitoria" if vitoria else "derrota")

            if not vitoria:
                print(f"Você foi derrotado por {inimigo.nome}!")
                return False

        # --- Boss da Floresta ---
        boss = Inimigo(
            "Guardião Sombrio",
            vida=120,   # Vida maior
            forca=20,   # Força maior
            xp_inimigo=150,  # XP muito maior
            ouro_inimigo=200 # Ouro muito maior
        )
        boss = self.balancear_inimigo(boss, alvo_prob=0.55)  # Leve desafio extra
        classe_prevista, prob_vitoria = self.prever_resultado(boss)
        print(f"[ML] Enfrentando o BOSS {boss.nome} | Probabilidade de vitória: {prob_vitoria*100:.1f}%")
        
        combate_controller = CombateController(self.jogador, boss)
        vitoria = combate_controller.executar_combate()
        self.jogador.vida = self.jogador.vida_max
        self.registrar_resultado(boss, "vitoria" if vitoria else "derrota")

        if not vitoria:
            print(f"O boss {boss.nome} derrotou você!")
            return False

        print("Parabéns! Você derrotou todos os inimigos e o boss da Floresta Assombrada!")
        return True


    def visitar_loja(self):
        loja = Loja()
        LojaView.mostrar_boas_vindas()

        while True:
            # Mostra ouro atual do jogador
            print(f"\nSeu ouro atual: {self.jogador.ouro}")
            
            # Obtém itens da classe do jogador + itens universais
            itens_disponiveis = loja.obter_itens_classe(self.jogador) + loja.itens_universais
            LojaView.mostrar_itens(itens_disponiveis)

            # Pede escolha do jogador (já retorna int)
            escolha = LojaView.pedir_escolha()

            # Validação do input
            if escolha < 0 or escolha > len(itens_disponiveis):
                LojaView.mostrar_compra_falha("Escolha inválida!")
                continue

            if escolha == 0:
                LojaView.mostrar_saida()
                break

            # Compra de item
            sucesso, resultado = loja.comprar_item(self.jogador, escolha)

            if sucesso:
                # Usa get para evitar KeyError em bonus
                bonus = resultado.get("bonus", {})
                LojaView.mostrar_compra_sucesso(resultado["nome"], bonus)
                print("\n--- STATUS ATUALIZADO ---")
                JogadorView.mostrar_status(self.jogador)
            else:
                LojaView.mostrar_compra_falha(resultado)

        return True

    def caverna_misteriosa(self):
        print("\n--- Caverna Misteriosa ---")
        CenarioView.mostrar_caverna_misteriosa()
        JogadorView.mostrar_status(self.jogador)

        # Criação dos inimigos
        inimigos = [
            Inimigo(
                "Goblin Selvagem",
                vida=random.randint(20, 50),
                forca=random.randint(5, 12),
                xp_inimigo=25,
                ouro_inimigo=random.randint(5, 15)
            ),
            Inimigo(
                "Troll Ancião",
                vida=random.randint(20, 50),
                forca=random.randint(5, 12),
                xp_inimigo=25,
                ouro_inimigo=random.randint(5, 15)
            ),
        ]

        # Batalha com cada inimigo
        for inimigo in inimigos:
            inimigo = self.balancear_inimigo(inimigo, alvo_prob=0.55)  # Ajusta dificuldade
            classe_prevista, prob_vitoria = self.prever_resultado(inimigo)
            print(f"[ML] Enfrentando {inimigo.nome} | Probabilidade de vitória: {prob_vitoria*100:.1f}%")
            
            combate_controller = CombateController(self.jogador, inimigo)
            vitoria = combate_controller.executar_combate()

            # Recupera vida do jogador para o próximo inimigo
            self.jogador.vida = self.jogador.vida_max

            self.registrar_resultado(inimigo, "vitoria" if vitoria else "derrota")

            # Se perder para algum inimigo, termina a caverna
            if not vitoria:
                print(f"Você foi derrotado por {inimigo.nome}!")
                return False

        # Se vencer todos os inimigos
        print("Você derrotou todos os inimigos da Caverna Misteriosa!")
        return True

    def visitar_loja(self):
        loja = Loja()
        LojaView.mostrar_boas_vindas()

        while True:
            # Mostra ouro atual do jogador
            print(f"\nSeu ouro atual: {self.jogador.ouro}")
            
            # Obtém itens da classe do jogador + itens universais
            itens_disponiveis = loja.obter_itens_classe(self.jogador) + loja.itens_universais
            LojaView.mostrar_itens(itens_disponiveis)

            # Pede escolha do jogador (já retorna int)
            escolha = LojaView.pedir_escolha()

            # Validação do input
            if escolha < 0 or escolha > len(itens_disponiveis):
                LojaView.mostrar_compra_falha("Escolha inválida!")
                continue

            if escolha == 0:
                LojaView.mostrar_saida()
                break

            # Compra de item
            sucesso, resultado = loja.comprar_item(self.jogador, escolha)

            if sucesso:
                # Usa get para evitar KeyError em bonus
                bonus = resultado.get("bonus", {})
                LojaView.mostrar_compra_sucesso(resultado["nome"], bonus)
                print("\n--- STATUS ATUALIZADO ---")
                JogadorView.mostrar_status(self.jogador)
            else:
                LojaView.mostrar_compra_falha(resultado)

        return True