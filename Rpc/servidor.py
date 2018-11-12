from random import randint
import rpyc
from rpyc.utils.server import ThreadedServer
import sys

class CampoMinadoServer(rpyc.Service):

    COORDENADAS_INVALIDAS = "Coodenadas Invalidas"
    GAME_OVER = "Game Over"

    def exposed_criar_novo_jogo(self, linha, coluna):
        self.__linha = linha
        self.__coluna = coluna
        self.jogadas_restantes = self.__calcular_total_jogadas(linha, coluna)
        self.__coordenadas_bombas = self.__distribuir_bombas(linha,coluna)

    def exposed_efetuar_jogada(self, linha, coluna):

        if not self.__validar_coordenadas(linha, coluna):
            return self.COORDENADAS_INVALIDAS
        if  (linha, coluna) in self.__coordenadas_bombas:
            return self.GAME_OVER

        self.jogadas_restantes -=1
        return str(self.__conta_bombas_vizinhos(linha, coluna))

    def exposed_get_jogadas_restantes(self):
        return self.jogadas_restantes
    
    def exposed_jogo_incompleto(self):
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
        """ Verifica se a coodenada informada possui uma bomba """
        return coordenada in self.__coordenadas_bombas

    def __conta_bombas_vizinhos(self, linha, coluna):
        """ Soma -1,0 e 1 em linha e coluna e verifica se elas possuem uma bomba, caso sim, essa coordenada entra em uma lista """
        return len([(linha + x, coluna + y) for x in (-1,0,1) for y in (-1,0,1) if self.__coordenada_e_bomba((linha + x, coluna + y))])

if __name__ == "__main__":
    try:
        print("servidor ativo")
        thread = ThreadedServer(CampoMinadoServer, port=18861)
        thread.start() 
    except:
        for val in sys.exc_info():
            print(val)