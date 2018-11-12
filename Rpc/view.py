from socket import socket, AF_INET, SOCK_DGRAM
import os
import rpyc
import sys

class CampoMinadoView:

    INSTANCIA = "instancia"
    VITORIA = "Você venceu"
    GAME_OVER = "Game Over"

    def __init__(self):
        self.config = {'allow_public_attrs': True}
        self.proxy = rpyc.connect('localhost', 18861, config=self.config)
        self.conn = self.proxy.root
        self.__tabuleiro = self.__inicializar_tabuleiro()

    def menu_inicial(self):
        print("---------------------------------------")
        print("------------ Campo Minado -------------")
        print("---------------------------------------")
        print("")
        print("Selecione uma opção")
        print("1. Criar novo jogo")
        if self.conn.jogo_incompleto():
            print("2. Continuar jogo anterior") 
        print("9. Sair do Jogo")

    def iniciar_novo_jogo(self):
        self.conn.criar_novo_jogo(5, 5)
        self.__imprimir_tabuleiro()
        return self.efetuar_nova_jogada()

    def continuar_jogo(self):
        pass

    def efetuar_nova_jogada(self):
        while self.conn.get_jogadas_restantes() > 0:
            linha = int(input("Defina uma linha: "))
            coluna = int(input("Defina uma coluna: "))
            resposta = self.conn.efetuar_jogada(linha, coluna)
            if resposta == self.GAME_OVER:
                print(self.GAME_OVER)
                return
            self.__tabuleiro[linha][coluna] = resposta
            os.system('cls' if os.name == 'nt' else 'clear')
            self.__imprimir_tabuleiro()
        
        return VITORIA

    def sair(self):
        sys.exit(0)

    def __imprimir_tabuleiro(self):
        for posicao in self.__tabuleiro:
            print(str(posicao))
        
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




