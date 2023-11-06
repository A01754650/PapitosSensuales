from dagor import JugadorCaballosBailadores, \
    choice, JugadorCaballosBailadoresAleatorio, \
    JuegoCaballosBailadores


class JugadorCaballosBailadoresEquipo1(JugadorCaballosBailadores):
    '''Jugador de Caballos bailadores que tira con una estrategia.'''

    def heuristica(self, posicion):
        '''Devuelve True si posicion resulta en un tiro ganador para este
        Jugador. De otra forma regresa False.'''
        # return self.triunfo(posicion) == self.simbolo
        # INTENTAR SIEMPRE ESTAR EN EL CENTRO
        def redondear (numero):
            if numero % 2 == 0:
                return round(numero) + 1
            else:
                return round(numero)

        if posicion[0] == 'B':
            return posicion[5][0] in [redondear(posicion[1]/2)] and posicion[5][1] in [redondear(posicion[2]/2)]
        elif posicion[0] == 'N':
            return posicion[6][0] in [redondear(posicion[1]/2)] and posicion[6][1] in [redondear(posicion[2]/2)]
        else:
            return self.triunfo(posicion) == self.simbolo

    def tira(self, posicion):
        '''Busca el mejor tiro posible, sino selecciona cualquier
        tiro válido al azar.'''
        posibles = self.posiciones_siguientes(posicion)
        for p in posibles:
            if self.heuristica(p):
                return p
        return choice(posibles)
        # return posibles[0]


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
#         cN: Tupla (r, c) con la coordenada del caballo blanco

#     Por ejemplo:

#         ('B', 5, 6, (4, 0), (4, 1), (0, 5), (0, 1))
