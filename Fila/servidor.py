from random import randint
from socket import socket, AF_INET, SOCK_DGRAM
import zmq

class CampoMinadoServer:

    PORT = "5560"
    ENCODE = "UTF-8"

    COORDENADAS_INVALIDAS = "Coodenadas Invalidas"
    GAME_OVER = "Game Over"

    def __init__(self):
        self.contexto = zmq.Context()
        self.socket = self.contexto.socket(zmq.REP)
        self.socket.connect("tcp://localhost:%s" % self.PORT)

    def server(self):
        while True:
            print("Servidor On-line... ")
            dados = self.socket.recv()
            text = dados.decode(self.ENCODE)
            print("Recebemos a pergunta: " + text)

            if text == "CRIAR NOVO JOGO":
                self.criar_novo_jogo(5, 5)
                text = "JOGO CRIADO"
            elif text == "CONTINUAR JOGO":
                pass 
            elif '.' in text:
                linha , coluna = self.__preparar_jogada(text)
                text = self.efetuar_jogada(linha, coluna)
            elif text == "JOGADAS RESTANTES":
                text = str(self.jogadas_restantes)
            elif text == "JOGO INCOMPLETO":
                if self.__jogo_incompleto():
                    text = "SIM"
                else:
                    text = "NAO"
            
            print("Resposta enviada para cliente: " + text)
            dados = text.encode(self.ENCODE)
            self.socket.send(dados)

    def criar_novo_jogo(self, linha, coluna):
        self.__linha = linha
        self.__coluna = coluna
        self.jogadas_restantes = self.__calcular_total_jogadas(linha, coluna)
        self.__coordenadas_bombas = self.__distribuir_bombas(linha,coluna)

    """ 1. Verifica se as coordenadas são válidas
            2. Validar se acertei uma mina: 
                caso sim:
                    Game Over 
                caso não: 
                    marcar a posição escolhida no tabuleiro com a quantidade de 
                    bombas existentes nos nós vizinhos 
    """
    def efetuar_jogada(self, linha, coluna):
        if not self.__validar_coordenadas(linha, coluna):
            return self.COORDENADAS_INVALIDAS
        if  (linha, coluna) in self.__coordenadas_bombas:
            return self.GAME_OVER
        
        self.jogadas_restantes -=1
        return str(self.__conta_bombas_vizinhos(linha, coluna))
    
    def __jogo_incompleto(self):
        return False

    def __preparar_jogada(self, text):
        jogada = text.split(".")
        return int(jogada[0]), int(jogada[1])

    def __distribuir_bombas(self, linha, coluna):
        """ Consulta o total de bombas permitidas e aleatoriamente definie as coordenadas de cada bomba"""
        coordenadas_bombas = [(randint(0, linha - 1), randint(0, coluna - 1)) for x in range(self.__total_bombas())]
        print(coordenadas_bombas)
        return coordenadas_bombas

    def __total_bombas(self):
        return int((self.__linha*self.__coluna)/3)
    
    def __calcular_total_jogadas(self,linha, coluna):
        return (linha*coluna) - self.__total_bombas()

    def __validar_coordenadas(self, linha, coluna):
        if linha in range(0, self.__linha) and coluna in range(0, self.__coluna):
            return True
        return False
    
    def __coordenada_e_bomba(self, coordenada):
        return coordenada in self.__coordenadas_bombas

    def __conta_bombas_vizinhos(self, linha, coluna):
        """ Soma -1,0 e 1 em linha e coluna e verifica se elas possuem uma bomba, caso sim, essa coordenada entra em uma lista """
        return len([(linha + x, coluna + y) for x in (-1,0,1) for y in (-1,0,1) if self.__coordenada_e_bomba((linha + x, coluna + y))])

if __name__ == "__main__":
    server = CampoMinadoServer()
    server.server()