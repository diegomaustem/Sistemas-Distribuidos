from socket import socket, AF_INET, SOCK_DGRAM
import os

class CampoMinadoView:

    INSTANCIA = "instancia"
    VITORIA = "Você venceu!"
    GAME_OVER = "Game Over"

    ENCODE = "UTF-8"
    MAX_BYTES = 28000
    PORT = 686
    HOST = "127.0.0.1"

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.dest = (self.HOST, self.PORT)
        self.__tabuleiro = self.__inicializar_tabuleiro()

    def menu_inicial(self):
        print("---------------------------------------")
        print("------------ Campo Minado -------------")
        print("---------------------------------------")
        print("")
        print("Selecione uma opção")
        print("1. Criar novo jogo")
        if self.__jogo_incompleto == True:
            print("2. Continuar jogo anterior") 
        print("9. Sair do Jogo")

    def iniciar_novo_jogo(self):
        text = "CRIAR NOVO JOGO"
        self.__requisicao(text) 
        self.__imprimir_tabuleiro()
        return self.efetuar_nova_jogada()

    def continuar_jogo(self, contexto):
        pass

    def efetuar_nova_jogada(self):
        text = "JOGADAS RESTANTES"
        jogadas_restantes = self.__requisicao(text)

        while jogadas_restantes > "0":
            linha = int(input("Defina uma linha: "))
            coluna = int(input("Defina uma coluna: "))
            text = str(linha) + "." + str(coluna)
            resposta = self.__requisicao(text)
            if resposta == self.GAME_OVER:
                print(self.GAME_OVER)
                return
            self.__tabuleiro[linha][coluna] = resposta
            os.system('cls' if os.name == 'nt' else 'clear')
            self.__imprimir_tabuleiro()
        
        return VITORIA

    def sair(self):
        sys.exit(0)

    def __jogo_incompleto(self):
        text = "JOGO INCOMPLETO"
        text = self.__requisicao(text)
        resposta = False
        if text == "SIM":
            resposta = True
        return resposta

    def __imprimir_tabuleiro(self):
        for posicao in self.__tabuleiro:
            print(str(posicao))

    def __requisicao(self, text):
        dados = text.encode(self.ENCODE)
        self.sock.sendto(dados, self.dest)
        dados, endereco = self.sock.recvfrom(self.MAX_BYTES)
        return dados.decode(self.ENCODE)
        
    def __inicializar_tabuleiro(self):
        return [[str('X') for x in range(5)] for j in range(5)]


if __name__ == "__main__":
    view = CampoMinadoView()
    switcher = {
        1: view.iniciar_novo_jogo,
        2: view.continuar_jogo,
        9: view.sair,
    }
    while True:
        view.menu_inicial()
        opcao = int(input("Opção escolhida: "))
        func = switcher.get(opcao)
        func()




