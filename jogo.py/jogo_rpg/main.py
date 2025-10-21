# Ponto de entrada da aplicação
# Responsabilidade única: inicializar o jogo
from controllers.jogo_controller import JogoController

def main():
    # Cria controller principal e inicia execução
    # Toda a lógica fica nos Controllers, Models e Views
    jogo = JogoController()
    jogo.executar()

# Padrão Python: executa main() apenas se arquivo for executado diretamente
if __name__ == "__main__":
    main()