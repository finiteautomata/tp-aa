import random


class CuatroEnLinea:
    def __init__(self, player1, player2,cant_filas,cant_columnas):

        self.player1, self.player2 = player1, player2
        self.player1_turn = random.choice([True, False])
        self.tablero = Tablero(can_filas,cant_columnas)


    def play_game(self):
        #self.player1.start_game(1)
        #self.player2.start_game(2)

        terminamos = False

        while not terminamos:
            if self.player1_turn:
                player, simbolo = self.player1, 1
            else:
                player, simbolo = self.player2, 2

            self.mostrar_tablero()

            player.move(self)-1

            if self.hay_ganador():
                print("ganó el jugador " + str(symbol))
                self.mostrar_tablero()
                terminamos = True


            if self.hay_empate():
                print("tablero lleno")
                terminamos = True

            self.player1_turn = not self.player1_turn


            #if self.player_wins():
            #   player.reward(1, self.board)
            #  other_player.reward(-1, self.board)
            # break
            #if self.board_full(): # tie game
            #    player.reward(0.5, self.board)
            #    other_player.reward(0.5, self.board)
            #    break
            #other_player.reward(0, self.board)

    def hay_ganador():
        return self.tablero.hay_ganador()

    def mostrar_tablero(self):
        self.tablero.mostrar_tablero()

    def acciones_posibles(self):
        return self.tablero.acciones_posibles()

    def poner_ficha(columna,simbolo):
        self.tablero.poner_ficha(columna,simbolo)


    def hay_empate(self):
        return self.tablero.tablero_lleno()

    def dame_copia_del_tablero():
        return self.tablero.copy()


#########################################################################################################



class Tablero

    def __init__(self, cant_filas,cant_columnas):

        self.cant_filas = cant_filas
        self.cant_columnas = cant_columnas
        self.tablero = [[0 for j in range(0,cant_columnas)] for i in range(0,cant_filas)]


    def copy():

        nuevo_tablero = Tablero(self.cant_filas,self.cant_columnas)
        nuevo_estado = nuevo_tablero.tablero

        for i in range(0..self.cant_filas):
            for j in range(0..self.cant_columnas):
                nuevo_estado[i][j] = tablero[i][j]

        return nuevo_tablero


    def mostrar_tablero(self):
        for i in reversed(range(0,self.cant_filas)):
            print self.tablero[i]
            print "\n"


    def gana_jugador(simbolo):

        gana = false
        for i in range(0..self.cant_filas):
            for j in range(0..self.cant_columnas):
                if tablero[i][j] == simbolo:
                    if hay_cuatro_en_linea = self.cuatro_en_linea(i,j,i-3,j) or self.cuatro_en_linea(i,j,i-3,j+3) or self.cuatro_en_linea(i,j,i,j+3) or self.cuatro_en_linea(i,j,i+3,j+3) or self.cuatro_en_linea(i,j,i+3,j) or self.cuatro_en_linea(i,j,i+3,j-3) or self.four_in_line(i,j,i,j-3) or self.four_in_line(i,j,i-3,j-3):
                        return true


        return gana



    def build_range(self,i1,i2):

        rango = []
        if ( i1 < i2 ):
            rango = [i1,i1+1,i1+2,i1+3]
        elif ( i1 == i2 ):
            rango = [i1,i1,i1,i1]
        else:
            rango = [i1,i1-1,i1-2,i1-3]

        return rango


    def fila_disponible_en(self,j):
        for i in range(0,self.cant_filas):
            if self.tablero[i][j] == 0:
                return i
        return -1


    def poner_ficha(self,j,symbol):
        tablero = self.tablero
        columna = j
        for i in range(0,self.cant_filas):
            if tablero[i][columna] == 0:
                tablero[i][columna] = symbol
                break


    def cuatro_en_linea(self, i1,j1,i2,j2):

        if i2 < 0 or i2 >= self.cant_filas or j2 < 0 or j2 >= self.cant_columnas:
            return False

        fila = self.build_range(i1,i2)
        columna = self.build_range(j1,j2)

        return (tablero[fila[0]][columna[0]] == tablero[fila[1]][columna[1]] == tablero[fila[2]][columna[2]] == tablero[fila[3]][columna[3]]) and tablero[fila[0]][columna[0]] != 0



    def acciones_posibles(self):
        accionesPosibles = []
        for j in range(0,self.cant_columnas):
            for i in range(0,self.cant_filas):
                if unTablero[i][j] == 0:
                    accionesPosibles.append(j)

        return accionesPosibles

    def cuatro_en_linea(self, i1,j1,i2,j2):
        return self.tablero.cuatro_en_linea(i1,j1,i2,j2)


    def proximo_estado_para(accion):
        nuevo_tablero = Tablero(self.cant_filas,self.cant_columnas)
        nuevo_estado = nuevo_tablero.tablero

        for i in range(0..self.cant_filas):
            for j in range(0..self.cant_columnas):
                nuevo_estado[i][j] = tablero[i][j]

        nuevo_tablero.poner_ficha(accion)

        return nuevo_tablero



#########################################################################################################


class Player():
    def __init__(self):
        self.breed = "human"

    def move(self, juego):
        return int(raw_input("Qué columna elegís? "))


class RandomPLayer(object):
    def __init__(self):
        self.breed = "random"

    def move(self,juego):
        return random.randint(1,7)


#########################################################################################################



class QPlayer():
    def __init__(self,alpha,gamma,simbolo,profundidad):
        self.breed = "qplayer"
        self.gamma = gamma
        self.alpha = alpha
        self.tabla_q = {}
        self.simbolo = simbolo
        self.profundidad = profundidad

    def move(self,juego):
        estado = self.juego.dame_copia_del_tablero()
        accion = self.mejor_accion_para(estado, self.profundidad)
        juego.poner_ficha(accion)


    def mejor_accion_para(self,estado,profundidad)
        acciones_posibles = estado.acciones_posibles()
        mejor_valor = -100
        mejor_accion = 0
        valor_candidato = 0
        for j in acciones_posibles:
            valor_candidato = self.q(estado,j,profundidad)
            if mejor_valor < valor_candidato:
                mejor_valor = valor_candidato
                mejor_accion = j

        viejo_valor = self.tabla_q[(estado,mejor_accion)]
        self.tabla_q[(estado,mejor_accion)] = viejo_valor + alpha ( self.recompensa() + gamma * mejor_valor - viejo_valor )

        return mejor_accion

    def q(self,estado,accion,profundidad):

        peor_valor = -100

        proximo_estado = estado.proximo_estado_para(accion)

        if proximo_estado.gana_jugador(simbolo):
            peor_valor = 100
        elif proximo_estado.gana_jugador(self.simbolo_del_rival()):
            peor_valor = -100
        elif proximo_estado.hay_empate():
            peor_valor = 0
        elif profundidad == 0:

            acciones_posibles_del_rival = proximo_estado.acciones_posibles()

            for j in acciones_posibles_del_rival:

                proximo_estado_a_explorar = proximo_estado.proximo_estado_para(j)
                nuevas_acciones_posibles_mias = proximo_estado_a_explorar.acciones_posibles()

                for k in nuevas_acciones_posibles_mias:
                    valor_en_tabla_q = self.obtener_valor_en_tabla_q(proximo_estado_a_explorar,k)
                    if peor_valor > valor_en_tabla_q
                        peor_valor = valor_en_tabla_q
        else:
            acciones_posibles_del_rival = proximo_estado.acciones_posibles()

            for j in acciones_posibles_del_rival:

                proximo_estado_a_explorar = proximo_estado.proximo_estado_para(j)
                nuevas_acciones_posibles_mias = proximo_estado_a_explorar.acciones_posibles()

                for k in nuevas_acciones_posibles_mias:
                    valor_en_tabla_q = self.q(proximo_estado_a_explorar,k,profundidad-1)
                    if peor_valor > valor_en_tabla_q
                        peor_valor = valor_en_tabla_q


        return peor_valor



    def recompensa(self):
        return 1

    def recompensa_por_defecto(self):
        return 1


    def obtener_valor_en_tabla_q(estado,accion):
        if (estado,accion) in tabla_q:
            return tabla_q.get((estado,k))
        else:
            return 1

    def simbolo_del_rival():
        if self.simbolo == 1:
            return 2
        else:
            return 1


#########################################################################################################

p1 = QPlayer(1,1,True,2)
p2 = RandomPlayer(2)

repetir 50 veces:
    t = CuatroEnLinea(p1, p2,6,7)
    t.play_game()