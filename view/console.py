import sys
from typing import Optional

from blackjack.model.blackjack import Blackjack  

class UIConsola:

    def __init__(self):
        self.blackjack: Blackjack = Blackjack()
        self.opciones = {
            "1": self.iniciar_nuevo_juego,
            "2": self.salir
        }

    @staticmethod
    def mostrar_menu():
        titulo = "BLACKJACK"
        print(f"\n{titulo:_^30}")
        print("1. Iniciar nuevo juego")
        print("2. Salir")
        print(f"{'_':_^30}")

    def registrar_usuario(self):
        print("\nHola, bienvenid@ al juego de blackjack")
        nombre: str = input("¿Cuál es tu nombre?: ")
        self.blackjack.registrar_usuario(nombre)

    def ejecutar_app(self):
        self.registrar_usuario()
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print(f"{opcion} no es una opción válida")

    def iniciar_nuevo_juego(self):
        apuesta: int = self.pedir_apuesta()
        self.blackjack.iniciar_juego(apuesta)
        self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)

        if not self.blackjack.jugador.mano.es_blackjack():
            self.hacer_jugada_del_jugador()
        else:
            print("FELICITACIONES, LOGRASTE BLACKJACK. HAS GANADO EL JUEGO")

    def hacer_jugada_del_jugador(self):
        while not self.blackjack.jugador_perdio():
            respuesta = input("¿Quiere otra carta? s(si), n(no): ")
            if respuesta == "s":
                self.blackjack.repartir_carta_a_jugador()
                self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)
            elif respuesta == "n":
                break

        if self.blackjack.jugador_perdio():
            print("\nHAS PERDIDO EL JUEGO")
        else:
            self.ejecutar_turno_de_la_casa()

    def ejecutar_turno_de_la_casa(self):
        while not self.blackjack.casa_perdio():
            if self.blackjack.casa_debe_pedir_carta():
                self.blackjack.repartir_carta_a_casa()
            else:
                break

        self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano, mostrar_casa=True)
        if self.blackjack.casa_perdio():
            print("¡La casa se ha pasado de 21! ¡Has ganado el juego!")
        else:
            self.calcular_ganador()

    def calcular_ganador(self):
        if self.blackjack.jugador.mano.calcular_valor() > self.blackjack.cupier.mano.calcular_valor():
            print("¡Felicidades, has ganado!")
        elif self.blackjack.jugador.mano.calcular_valor() < self.blackjack.cupier.mano.calcular_valor():
            print("La casa gana. Has perdido.")
        else:
            print("Es un empate. Recibes tu apuesta de vuelta.")

    def pedir_apuesta(self):
        apuesta: int = int(input("¿Cuál es tu apuesta?: "))
        while not self.blackjack.jugador.puede_apostar(apuesta) or apuesta <= 0:
            print(f"ADVERTENCIA: No tienes suficientes fichas para apostar {apuesta} o tu apuesta es de 0")
            print("Ingresa una nueva apuesta.")
            apuesta = int(input("¿Cuál es tu apuesta?: "))
        return apuesta

    @staticmethod
    def mostrar_manos(mano_casa, mano_jugador, mostrar_casa=False):
        print("\nMANO DE LA CASA:")
        print(str(mano_casa) if mostrar_casa else "Carta oculta")
        if mostrar_casa:
            print(f"VALOR: {str(mano_casa.calcular_valor())}")

        print("\nTU MANO:")
        print(str(mano_jugador))
        print(f"VALOR: {str(mano_jugador.calcular_valor())}")

    @staticmethod
    def salir():
        print("\nGRACIAS POR JUGAR BLACKJACK. VUELVE PRONTO")
        sys.exit(0)

