# ----------------------------------------------------------
# Project: Knight’s Dance
#
# Date: 29-Nov-2023
# Authors:
#           A01753505 Alan Alcántara Ávila
#           A01754650 Andrés Iván Rodríguez Méndez
# ----------------------------------------------------------

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
            new_position = (posicion[0], posicion[1], posicion[2],
                            posicion[6], posicion[4], posicion[5], posicion[3])
        elif posicion[0] == 'B':
            new_position = (posicion[0], posicion[1], posicion[2],
                            posicion[3], posicion[5], posicion[4], posicion[6])

        return new_position
    
    def checar_casillas(self, posicion, posibles_matar, posible_enemigo, posibles):
        lst = []
        lst_rey = []
        movimientos = []
        mejor_movimiento = self.find_best_move(posicion)
        
        if posicion[0] == 'B':
            for pe in posible_enemigo:
                lst.append(pe[5])
                
            for pm in posibles_matar:
                lst_rey.append(pm[5])
                
            # print(f'lst: {lst}')
            # print(f'lst_rey: {lst_rey}')
                
            for p in posibles:
                if p[5] in lst_rey and p[5] not in lst:
                    return p
                
                if p[5] not in lst:
                    movimientos.append(p)
                
                if self.heuristica(p) and p[5] not in lst:
                    return p
                
            if mejor_movimiento[5] not in lst:
                # print(f'mejor movimiento: {mejor_movimiento}')
                return mejor_movimiento
            
                
        elif posicion[0] == 'N':
            for pe in posible_enemigo:
                lst.append(pe[6])
                
            for pm in posibles_matar:
                lst_rey.append(pm[6])
                
            # print(f'lst: {lst}')
            # print(f'lst_rey: {lst_rey}')
                
            for p in posibles:
                if p[6] in lst_rey and p[6] not in lst:
                    return p
                
                if p[6] not in lst:
                    movimientos.append(p)
                
                if self.heuristica(p) and p[5] not in lst:
                    return p
                
            if mejor_movimiento[6] not in lst:
                return mejor_movimiento 
            
        if movimientos == []:
            return mejor_movimiento
                
        random_choice = choice(movimientos)
        # print(f'random choice: {random_choice}')
        
        return random_choice
    
            
        
        
        # for p in posibles:
        #         print(f'p: {p}')
        #         for pe in posible_enemigo:
        #             for pm in posibles_matar:
        #                 if posicion[0] == 'B':
        #                     if p[5] == pm[5] and p[5] not in pe:
        #                         return p
        #                 elif posicion[0] == 'N':
        #                     if p[6] == pm[6] and p[6] not in pe:
        #                         return p

    def tira(self, posicion):
        '''Busca el mejor tiro posible, sino selecciona cualquier
        tiro válido al azar.'''
        invertirPos = self.matar_rey(posicion)
        enemigoPos = (posicion[0], posicion[1], posicion[2],
                      posicion[3], posicion[4], posicion[6], posicion[5])
        posibles_matar = self.posiciones_siguientes(invertirPos)
        posible_enemigo = self.posiciones_siguientes(enemigoPos)
        posibles = self.posiciones_siguientes(posicion)
        best = self.find_best_move(posicion)
        
        # print(f'posibles matar: {posibles_matar}')
        # print(f'posibles enemigo: {posible_enemigo}')

        if self.heuristica(best):
            return best
        else:
            checar_casillas = self.checar_casillas(posicion, posibles_matar, posible_enemigo, posibles)
            if checar_casillas != None:
                print(f'checar casillas: {checar_casillas}')
                return checar_casillas



if __name__ == '__main__':
    juego = JuegoCaballosBailadores(
        JugadorCaballosBailadoresEquipo1('Smart Boy'),
        JugadorCaballosBailadoresAleatorio('Random Boy'),
        6, 6)
    juego.inicia(veces=1000, delta_max=2)


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
