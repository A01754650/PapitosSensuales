from dagor import JugadorCaballosBailadores, \
    choice, JugadorCaballosBailadoresAleatorio, \
    JuegoCaballosBailadores


class JugadorCaballosBailadoresEquipo1(JugadorCaballosBailadores):
    '''Jugador de Caballos bailadores que tira con una estrategia.'''

    def evaluacion(self, posicion):
        if posicion[0] == 'B':
            fila, columna = posicion[5]
            filaRey, columnaRey = posicion[4]
        else:
            fila, columna = posicion[6]
            filaRey, columnaRey = posicion[3]

        distancia_al_rey = abs(fila - filaRey) + abs(columna - columnaRey)
        return -distancia_al_rey


    def minimax(self, posicion, maximizing: bool, max_depth: int) -> float:
        if max_depth == 0:
            return self.evaluacion(posicion)

        if maximizing:
            best_eval: float = float("-inf")
            for move in self.posiciones_siguientes(posicion):
                result: float = self.minimax(move, False, max_depth - 1)
                best_eval = max(result, best_eval)
            return best_eval
        else:
            worst_eval: float = float("inf")
            for move in self.posiciones_siguientes(posicion):
                result = self.minimax(move, True, max_depth - 1)
                worst_eval = min(result, worst_eval)
            return worst_eval


    def find_best_move(self, posicion, max_depth: int = 1):
        best_eval: float = float("-inf")
        best_move = None

        for move in self.posiciones_siguientes(posicion):
            result: float = self.minimax(move, False, max_depth)
            if result > best_eval:
                best_eval = result
                best_move = move

        return best_move


    def heuristica(self, posicion):
        '''Devuelve True si posicion resulta en un tiro ganador para este
        Jugador. De otra forma regresa False.'''
        return self.triunfo(posicion) == self.simbolo


    def matar_rey(self, posicion):
        if posicion[0] == 'N':
            new_position = (posicion[0], posicion[1], posicion[2], posicion[6], posicion[4], posicion[5], posicion[3])
        elif posicion[0] == 'B':
            new_position = (posicion[0], posicion[1], posicion[2], posicion[3], posicion[5], posicion[4], posicion[6])

        return new_position


    def tira(self, posicion):
        '''Busca el mejor tiro posible, sino selecciona cualquier
        tiro válido al azar.'''
        invertirPos = self.matar_rey(posicion)
        posibles_matar = self.posiciones_siguientes(invertirPos)
        posibles = self.posiciones_siguientes(posicion)
        best = self.find_best_move(posicion)
        if self.heuristica(best):
            return best
        else:
            for p in posibles:
                for pm in posibles_matar:
                    if posicion[0] == 'B':
                        if p[5] == pm[5]:
                            return p
                    elif posicion[0] == 'N':
                        if p[6] == pm[6]:
                            return p

            if self.heuristica(p):
                return p
            return choice(posibles)


if __name__ == '__main__':
    juego = JuegoCaballosBailadores(
        JugadorCaballosBailadoresEquipo1('Smart Boy'),
        JugadorCaballosBailadoresAleatorio('Random Boy'),
        5, 8)
    juego.inicia(veces=100, delta_max=2)


#  La posición que maneja un juego de Caballos bailadores es
#     una tupla de la siguiente forma:

#         (T, #R, #C, rB, rN, cB, cN)

#     En donde:

#         T:  turno actual (símbolo del jugador asignado por la clase
#             de JuegoCaballosBailadores: B y N [blanco y negro])
#         #R: Número de renglones (fijo durante todo el juego)
#         #C: Número de columnas (fijo durante todo el juego)
#         rB: Tupla (r, c) con la coordenada del rey blanco (fija
#             durante todo el juego)
#         rN: Tupla (r, c) con la coordenada del rey negro (fija
#             durante todo el juego)
#         cB: Tupla (r, c) con la coordenada del caballo blanco
#         cN: Tupla (r, c) con la coordenada del caballo negro

#     Por ejemplo:

#         ('B', 5, 6, (4, 0), (4, 1), (0, 5), (0, 1))
