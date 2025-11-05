from models.inimigo import Inimigo
from models.loja import Loja
from models.jogador import Jogador
from views.loja_view import LojaView
from views.jogador_view import JogadorView
from controllers.combate_controller import CombateController
from views.cenario_view import CenarioView
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random


class CenarioController:
    def __init__(self, jogador: Jogador):
        self.jogador = jogador

        # Dados fictícios para aprendizado de máquina
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

        self.dados_ml = pd.DataFrame(
            dados_guerreira + dados_mago + dados_arqueiro + exemplos_extremos * 3
        )

        self.modelo = DecisionTreeClassifier()
        self._treinar_modelo()

    # ==================== MACHINE LEARNING ====================

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
        _, prob_vitoria = self.prever_resultado(inimigo)

        # Salva os valores iniciais para limitar o crescimento
        vida_base = inimigo.vida
        forca_base = inimigo.forca

        # Define limites para impedir absurdos
        max_vida = int(vida_base * 1.5)
        max_forca = int(forca_base * 1.6)
        min_vida = int(vida_base * 0.7)
        min_forca = int(forca_base * 0.7)

        tentativas = 0
        while abs(prob_vitoria - alvo_prob) > 0.03 and tentativas < 10:
            # Se a chance de vitória for ALTA (inimigo fraco) → FORTALECER inimigo
            if prob_vitoria > alvo_prob:
                inimigo.vida = min(max_vida, inimigo.vida + int(vida_base * 0.05))
                inimigo.forca = min(max_forca, inimigo.forca + int(forca_base * 0.05))
            # Se a chance de vitória for BAIXA (inimigo forte) → ENFRAQUECER inimigo
            else:
                inimigo.vida = max(min_vida, inimigo.vida - int(vida_base * 0.05))
                inimigo.forca = max(min_forca, inimigo.forca - int(forca_base * 0.05))

            _, prob_vitoria = self.prever_resultado(inimigo)
            tentativas += 1

        return inimigo

    # ==================== CENÁRIOS ====================

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
                print("⚰️ Jornada encerrada...")
                return

            if self.jogador.aethernox >= 1:
                print("🏆 Você completou o jogo!")
                return

    # ---------- CENÁRIO 1 ----------
    def floresta_morta(self):
        print("\n🌿 --- Floresta Morta --- 🌿")
        CenarioView.mostrar_vila_elder()
        JogadorView.mostrar_status(self.jogador)

        inimigo = Inimigo("Ladrão de Mória", 30, 8, 30, 20)
        inimigo = self.balancear_inimigo(inimigo, alvo_prob=0.6)

        classe_prevista, prob_vitoria = self.prever_resultado(inimigo)
        print(f"[ML] Probabilidade de vitória: {prob_vitoria*100:.1f}%")

        combate_controller = CombateController(self.jogador, inimigo)
        vitoria = combate_controller.executar_combate()
        self.registrar_resultado(inimigo, "vitoria" if vitoria else "derrota")

        return vitoria

    # ---------- CENÁRIO 2 ----------
    def floresta_assombrada(self):
        print("\n🌲 --- Floresta Assombrada --- 🌲")
        CenarioView.mostrar_floresta_assombrada()
        JogadorView.mostrar_status(self.jogador)

        # Agora todos têm status parecidos com o Ladrão de Mória
        inimigos = [
            Inimigo("Espectro Sombrio", 40, 10, 35, 20),
            Inimigo("Lobo Fantasma", 60, 10, 35, 20),
            Inimigo("Espantalho Amaldiçoado", 80, 10, 35, 20)
        ]

        for inimigo in inimigos:
            inimigo = self.balancear_inimigo(inimigo, alvo_prob=0.65)
            classe_prevista, prob_vitoria = self.prever_resultado(inimigo)
            print(f"[ML] Enfrentando {inimigo.nome} | Chance de vitória: {prob_vitoria*100:.1f}%")

            combate_controller = CombateController(self.jogador, inimigo)
            vitoria = combate_controller.executar_combate()

            if not vitoria:
                print(f"Você foi derrotado por {inimigo.nome}!")
                return False

        print("🌕 Você purificou a Floresta Assombrada!")
        return True

    # ---------- CENÁRIO FINAL ----------
    def caverna_misteriosa(self):
        print("\n💀 --- Caverna Misteriosa --- 💀")
        CenarioView.mostrar_caverna_misteriosa()
        JogadorView.mostrar_status(self.jogador)

        print("⚔️  O ar fica pesado... algo antigo desperta nas profundezas...")

        boss_final = Inimigo(
            "👑 Guardião Sombrio",
            vida=130,
            forca=25,
            xp_inimigo=300,
            ouro_inimigo=400
        )

        boss_final = self.balancear_inimigo(boss_final, alvo_prob=0.5)
        classe_prevista, prob_vitoria = self.prever_resultado(boss_final)
        print(f"[ML] Enfrentando o BOSS FINAL {boss_final.nome} | Probabilidade de vitória: {prob_vitoria*100:.1f}%")

        combate_controller = CombateController(self.jogador, boss_final)
        vitoria = combate_controller.executar_combate()
        self.jogador.vida = self.jogador.vida_max

        if not vitoria:
            print(f"O boss final {boss_final.nome} derrotou você...")
            return False

        print("🎉 Parabéns! Você derrotou o Guardião Sombrio e completou o jogo!")
        self.jogador.aethernox += 1
        return True

    # ---------- LOJA ----------
    def visitar_loja(self):
        loja = Loja()
        LojaView.mostrar_boas_vindas()

        while True:
            print(f"\nSeu ouro atual: {self.jogador.ouro}")
            itens_disponiveis = loja.obter_itens_classe(self.jogador) + loja.itens_universais
            LojaView.mostrar_itens(itens_disponiveis)

            escolha = LojaView.pedir_escolha()

            if escolha == 0:
                LojaView.mostrar_saida()
                break

            if escolha < 0 or escolha > len(itens_disponiveis):
                LojaView.mostrar_compra_falha("Escolha inválida!")
                continue

            sucesso, resultado = loja.comprar_item(self.jogador, escolha)

            if sucesso:
                bonus = resultado.get("bonus", {})
                LojaView.mostrar_compra_sucesso(resultado["nome"], bonus)
                print("\n--- STATUS ATUALIZADO ---")
                JogadorView.mostrar_status(self.jogador)
            else:
                LojaView.mostrar_compra_falha(resultado)

        return True
