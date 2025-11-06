# ⚔️ Aethernox — RPG Terminal com IA Adaptativa

Bem-vindo ao **Aethernox**, um jogo de **RPG de terminal** desenvolvido em **Python** com arquitetura **MVC (Model-View-Controller)**.  
O projeto foi criado com foco em **organização de código, boas práticas de POO** e **inteligência artificial adaptativa**, que ajusta automaticamente a dificuldade conforme o desempenho do jogador.

---

## 🧠 Visão Geral

No Aethernox, o jogador cria um personagem (guerreira, mago ou arqueiro) e enfrenta inimigos em combates por turnos.  
A cada batalha, a **IA de dificuldade** aprende com o desempenho do jogador e ajusta automaticamente a força dos próximos inimigos.

O jogo conta com:
- 🎭 **Sistema de classes** com atributos e itens únicos  
- 🧙‍♂️ **IA adaptativa** baseada em *Machine Learning*  
- ⚔️ **Combate estratégico** por turnos  
- 🛒 **Loja interativa** com sistema de bônus  
- 📈 **Evolução de personagem** com XP e níveis  
- 🧩 **Separação MVC** completa: Models, Views e Controllers

---

## 🏗️ Estrutura do Projeto

```bash
Aethernox/
├── controllers/
│   ├── jogo_controller.py
│   ├── combate_controller.py
│   ├── inteligencia_controller.py
│
├── models/
│   ├── jogador.py
│   ├── inimigo.py
│   ├── loja.py
│   ├── combate.py
│   └── ia_dificuldade.py
│
├── views/
│   ├── menu_view.py
│   ├── jogador_view.py
│   ├── combate_view.py
│
├── main.py
└── README.md
📦 Padrão MVC:

Models → Lógica e dados do jogo

Views → Interface de texto e menus

Controllers → Coordenação do fluxo de jogo

⚙️ Instalação
🔧 Pré-requisitos
Python 3.10+

Biblioteca scikit-learn (para IA adaptativa)

📦 Instalar dependências
bash
Copiar código
pip install -r requirements.txt
Se o arquivo requirements.txt não estiver disponível:

bash
Copiar código
pip install scikit-learn numpy
▶️ Executando o Jogo
Execute o comando no terminal:

bash
Copiar código
python main.py
🎮 Funcionalidades Principais
👤 Criação de Personagem
Escolha entre Guerreira, Mago ou Arqueiro

Cada classe tem atributos e bônus únicos:

Guerreira: mais vida e força

Mago: mais mana e inteligência

Arqueiro: mais agilidade e precisão

⚔️ Sistema de Combate
Combate por turnos com quatro ações:

Atacar

Usar magia

Usar item

Fugir

O inimigo também realiza ataques automáticos.

O resultado é influenciado pelos atributos do personagem.

🧠 IA de Dificuldade Adaptativa
Implementada com Regressão Linear (scikit-learn).

A força dos inimigos aumenta ou diminui conforme:

Vitórias fáceis → aumenta a dificuldade

Derrotas → reduz a dificuldade

O modelo aprende em tempo real, criando uma curva de desafio equilibrada.

🛒 Sistema de Loja
Itens exclusivos por classe com bônus permanentes.

Exemplo:

Guerreira: Espada do Templário, Escudo de Ferro

Mago: Cajado de Carvalho, Robe Arcano

Arqueiro: Arco Longo, Capa de Caçador

Itens universais: Poção de Vida e Poção de Mana.

O jogador usa ouro para comprar e fortalecer seu personagem.

📈 Evolução e Progressão
Sistema completo de níveis, XP e atributos:

Suba de nível ao acumular XP.

Melhora automática de força, defesa e agilidade.

Restauração total de vida e mana ao evoluir.

🧩 Destaques Técnicos
Conceito	Descrição
🧱 MVC	Separação entre lógica, interface e controle
💡 POO e SRP	Cada classe/método tem uma função única
🤖 IA de Dificuldade	Regressão Linear adaptando força dos inimigos
🪄 Extensibilidade	Fácil adicionar novas classes, magias e inimigos
🧰 Modularização	Códigos curtos, reutilizáveis e bem comentados

💻 Exemplo de Uso
Criando um jogador e comprando um item:
python
Copiar código
from models.jogador import Jogador
from models.loja import Loja

# Cria um jogador da classe Mago
jogador = Jogador("mago")
loja = Loja()

# Exibe os itens disponíveis
itens = loja.obter_itens_classe(jogador)
print("Itens disponíveis:", [item["nome"] for item in itens])

# Compra o primeiro item da lista
sucesso, resultado = loja.comprar_item(jogador, 1)
if sucesso:
    print(f"✅ Você comprou: {resultado['nome']}")
else:
    print(f"❌ Falha na compra: {resultado}")
🧑‍💻 Tecnologias Utilizadas
🐍 Python 3.10+

📘 scikit-learn

🔢 NumPy

🧩 Paradigma MVC

⚙️ Programação Orientada a Objetos (POO)

🧾 Licença
Este projeto é livre para uso educacional e pessoal.
Sinta-se à vontade para estudar, modificar e expandir o código.

👨‍💻 Autor
Lucas Paiva
💼 Desenvolvedor Python e entusiasta de Inteligência Artificial
📧 Contato: (adicione seu e-mail ou GitHub aqui)