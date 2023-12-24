# Tarea 1: DCChexxploding 💥♟️

## Consideraciones generales :octocat:

* El programa comienza bien, permite elegir un nombre de usuario y abrir un tablero a partir de su nombre en ```archivos.txt```, ademas de manejar correctamente cualquier caso inválido en estos dos aspetos.
  
* El menú funciona de manera correcta. Maneja tanto los inputs válidos y su función asociada como los inválidos.


### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú: 18 pts (30%)
##### ✅ Consola: Permite el ingreso de un nombre de usuario y nombre de un tablero. Ambas son validadas de manera independiente.

##### ✅ Menú de Acciones: Implementa el saludo al usuario y las opciones ```mostrar```, ```limpiar```, ```solucionar``` y ```salir```.

##### ✅ Modularización: Ningún archivo supera las 400 líneas de codigo.

##### ✅ PEP8: Escrito acorde a las reglas PEP8.

#### Funcionalidades: 42 pts (70%)

##### ✅ Todos los metodos y properties implementados.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```system()```. Utilizado en ```main.py```.
2. ```sys```: ```exit()```, ```argv()```. Utilizado en ```main.py```.
3. ```copy```: ```deepcopy()```. Utilizado en ```tablero.py```, ```extras.py```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```tablero.py```: Contiene la clase ```Tablero```
2. ```pieza_explosiva.py```: Contiene la clase ```PiezaExplosiva```. Ademas, se creó el metodo ```verificar_alcance_efectivo(*args)```, utilizado en el modulo ```extras.py```. El método extra se encuentra comentado en profundidad.
3. ```funciones.py```:  Utilizado en ```tablero.py```, ```extras.py```. Contiene ```2``` funciones que corresponden a los métodos ```peones_invalidos(*args)``` y ```celdas_afectadas(*args)``` de ```Tablero``` en ```tablero.py``` El proposito de esto es poder utilizar estas dos funciones en el modulo ```extras.py```. El modulo está comentado en profundidad.
4. ```extras.py```: Utilizado en ```tablero.py```, ```main.py```. Contiene ```7``` funciones extras para el desarrollo mas eficiente de la tarea y a la función ```extras.solucionar(*args)```, función recursiva que llama el método ```solucionar(self)``` de ```Tablero``` en ```tablero.py```. El modulo está comentado en profundidad.

## Consideraciones adicionales :thinking:
Algunas cosas a considerar son las siguientes:

1. En cuanto a la interacción con el menú, tras seleccionar cualquier opción se llama a la funcion ```os.system("cls")``` para limpiar la consola, dando la impresion de un menú mas realista.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. https://www.geeksforgeeks.org/python-addition-of-tuples/:
   
   ```python
   res = tuple(map(sum, zip(test_tup1, test_tup2)))
   ```
   - Para suma de tuplas como si fueran vectores. 
   - Esta implementado en el archivo ```funciones.py``` en la linea numero ```28```.
   - Suma la posicion del peon en el tablero con 4 distintas coordenadas para encontrar peones vecinos.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).