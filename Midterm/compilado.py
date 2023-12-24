# pylint: disable=missing-docstring

# 1.1 OOP I
# %% 2


class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.edad = edad

    def elegir_carrera(self, carrera):
        self.carrera = carrera
        print(f"{self.nombre} estudiará {self.carrera}")


estudiante = Estudiante("Juan")

# %% 3


class Variable:
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, x):
        if x <= 0:
            self._valor = x
        else:
            self._valor = -x


variable_uno = Variable(5)
variable_uno.valor -= 3
print(variable_uno.valor)

variable_uno.valor = -1
print(variable_uno.valor)

variable_uno.valor += 3
print(variable_uno.valor)

# %% 4


class Auto:
    def __init__(self):
        self.marca = ""
        self.motor = ""
        self.color = ""

    def __repr__(self):
        return f"Mi marca es {self.marca}"


spark = Auto()
spark.marca = "chevrolet"
spark.patente = "GT HB 34"
print(spark.patente)


# 1.3 Built-in, Iterables y Funcional
# %% 9
def funcion_1(*args, primero=None, **kwargs):  # VALID
    pass

def funcion_2(*args, **kwargs, primero):  # INVALID
    pass

def funcion_3(*args, **kwargs, primero=None):  # INVALID
    pass

def funcion_4(*args, primero, **kwargs):  # VALID
    pass

def funcion_5(primero, *args, **kwargs):  # VALID
    pass


# %% 10
iterable = [1, 2, 3, 4, 5]
iter_a = iter(iterable)
iter_b = iter(iterable)
lista = []

for i in iter_a:
    lista.append(i)
    if i >= 3:
        break

for j in iter_b:
    lista.append(j)
    if j >= 2:
        break

for k in iter_a:
    lista.append(k)
    if k >= 4:
        break

print(lista)

# %% 11
nombres = ["DCCachorritos", "DIElefante", "DCCorales", "ICMagia"]
map_object = map(lambda s: s[0:3] == "DCC", nombres)
print(list(zip(map_object)))

# %% 12
def funcion(*args, **kwargs):
    print(args)
    print(kwargs)

funcion("test")

funcion(x="test")

funcion("test", x="test")

# %% 1.4 Interfaces Gráficas
import sys
import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QApplication


class Ventana(QWidget):
    def __init__(self, nombre, ancho, alto) -> None:
        super().__init__()

        self.setWindowTitle(nombre)

        self.setGeometry(0, 0, ancho, alto)

    def abrir_otra_ventana(self):
        self.hide() # Esconder la ventana actual
        otra_ventana = Ventana("Otra ventana", 300, 100) # Crear otra
        otra_ventana.show() # Mostrar nueva ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = Ventana("Ventana", 300, 300)
    ventana.show()

    ventana.abrir_otra_ventana()

    sys.exit(app.exec())


# 1.5 Threading
# %% 20
import threading
import time

lock_comida = threading.Lock()

def comer(nombre, comida, lock):
    print(f"{nombre} está esperando para comer...")
    time.sleep(1)
    lock.acquire()
    print(f"{nombre} está comiendo {comida}")
    time.sleep(3)
    print(f"{nombre} terminó de comer")
    lock.release()

pepito = threading.Thread(target=comer, args=("Pepito", "papas", lock_comida,))
juan = threading.Thread(target=comer, args=("Juan", "pizza", lock_comida,))
pepito.start()
juan.start()
pepito.join()
juan.join()
print("Ambos comieron")


# 1.7 Serialización y Excepciones
# %% 29

def favoritometro(series, nombre):
    if not isinstance(nombre, str):
        raise KeyError as "Nombre erróneo"
    else:
        print(f"Serie favorita: {series[nombre]}")

dict_series = {"Alice": "Breaking Bad", "Bob": "Dark"}
user = "uwu"
favoritometro(dict_series, user)

# %% 30

def calculadora(a, b):
    try:
        print(a + b)
    except TypeError:
        print("no")
    else:
        print("No hubo ninguna excepcion")
    finally:
        return a * b

k = calculadora(2, 4)
print(k)
# %%