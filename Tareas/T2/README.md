# Tarea 2: DCConejoChico 🐇💨

## Consideraciones generales :octocat:

#### General

* La mayor parte del código esta escrita en ```inglés```.

* Ambas ventanas tienen ```musica```. Con el volumen del computador en ```20``` se escucha decente (subjetivo).

* Se creo la carpeta ```assets_extra``` que contiene assets adicionales a los entregados.

#### Ventana Inicio

* La ventana de inicio recibe el nombre de usuario y realiza la validación del formato de este. Los nombres de usuario ```test1```, ```test2``` y ```test3``` son casos especiales que, a pesar de no pasar la validación, permiten jugar los niveles ```1```, ```2``` y ```3``` respectivamente. Pasar un nivel con estos usuarios no guardará el progreso ni incrementará el puntaje.

* Los datos de cada usuario se guardan en el archivo ```server.json``` dentro del parametro ```users``` con el formato ```[username]: {"level": [nivel_actual], "score": [puntaje_acumulado]}```.

* Si el nombre de usuario no existe al comenzar la partida, este se agrega automaticamente a ```server.json```, con ```"level": 1``` y ```"score": 0.0```.

* Usuarios con un ```"score"``` igual a ```0.0``` no son mostrados en el ```hall of fame```.

#### Ventana Juego
  
* Al comenzar el nivel, el ```DCConejoChico``` realiza una corta animación de entrada. Una vez finalizada esta se permiten los inputs de movimiento y comienza a correr el tiempo. Lo mismo ocurre en la salida, deteniendo el reloj al momento de comenzar la animación.
  
* Al perder una vida, el ```DCConejoChico``` realiza una corta animación de ```respawn```. Esta es solo de caracter visual y afecta unicamente la acción de ```pausar```, bloqueandola temporalmente.
  
* El movimiento de todos los ```sprites``` es por celda individual, ligado a un ```QTimer``` dependiente del ```sprite```. En el ```backend```, el movimiento del ```sprite``` de una celda a otra es instantaneo, mientras que en el ```frontend``` tiene una duración. Para detectar colisiones se utilizan únicamente las posiciones registradas en el ```backend```.
  
* Al ```pausar```, los ```sprites``` finalizaran su animación de movimiento a la siguiente celda antes de detenerse.

* Durante la animación de movimiento del ```DCConejoChico```, este no registra ningun ```input``` de movimiento. Se espera a que finalice la ultima animación antes de habilitarlo nuevamente. Otros ```input``` como ```pausar``` y ```objetos``` se mantienen habilitados.

* Al finalizar un nivel se habilita el botón ```[next level]```, que se encuentra en la ```esquina inferior izquierda```. Este botón debe ser presionado para avanzar al siguiente laberinto. Presionarlo tras completar el ```nivel 3``` finaliza el juego.

* El uso erroneo de la ```bomba manzana``` y ```bomba de congelacion``` se transmite a travez de un efecto de sonido.

* La cantidad de vidas se representa según el numero de corazones en la esquina superior derecha.

* El modo ```INF``` se representa con un corazon dorado.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio: Desplega el logo, permite el ingreso de nombre de usuario y muestra el "hall of fame".
##### ✅ Ventana Juego: Crea todos los sprites, muestra el tiempo, inventario, puntaje y vidas restantes.
##### ✅ ConejoChico: Se mueve respecto al input WASD con animacion fluida, se queda quieto solo al colisionar con una pared.
##### ✅ Lobos: Se mueven acuerdo su tipo, cambian de direccion al colisionar con una pared, cambian de velocidad segun el nivel. Le quitan una vida a ConejoChico al colisionar.
##### ✅ Cañón de Zanahorias: Dispara zanahorias cada 2 segundos. Estas se mueven en una direccion hasta colisionar con una pared. Le quitan una vida a ConejoChico al colisionar.
##### ✅ Bomba Manzana: Elimina los lobos que entren en contacto con esta durante la duracion de su efecto.
##### ✅ Bomba Congeladora: Relantiza a los lobos que entren en contacto con esta durante la duracion de su efecto.
##### ✅ Fin del nivel: Una vez ConejoChico llega a la salida, se habilita el boton para avanzar al siguiente nivel.
##### ✅ Fin del Juego: El juego finaliza al compltar el nivel 3 y presionar "next level" o bien cuando ConejoChico se queda sin vidas
##### ✅ Recoger (G): Funciona correctamente.
##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F): Ambos codigos funcionan correctamente.
##### ✅ Networking: Servidor implementado. Este maneja los usuarios, el ultimo nivel que completaron y el puntaje acumulado de estos, ademas de los usuarios baneados. Cliente implementado. Recibe la informacion del servidor para seleccionar que nivel le corresponde a cada usuario.
##### ✅ Decodificación: Se decodifica y desencripta la inforamcion en una unica funcion.
##### ✅ Desencriptación: Se decodifica y desencripta la inforamcion en una unica funcion.
##### ✅ Archivos: Se utilizan los archivos entregados.
##### 🟠 Funciones: Se utilizan principalmete las funciones de ```funciones_servidor.py```.


## Ejecución :computer:
Los módulos principals de la tarea a ejecutar son:
1.  ```main.py``` de la carpeta ```entrega_final/server```
2.  ```main.py``` de la carpeta ```entrega_final/client```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```json```
2. ```sys```
3. ```os```
4. ```threading```
5. ```socket```
6. ```dataclasses```: ```dataclass```, ```field```
7. ```itertools```: ```count```, ```cycle```
8. ```PyQt6```

## Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

### General

1. ```funciones_cliente.py```: Funciones de la entrega intermedia.
2. ```funciones_servidor.py```: Funciones de la entrega intermedia.

### Cliente

1. ```DCConejoChico.py```: Contiene a ```DCConejoChico``` - conecta señales.

#### Backend

1. ```game.py```: Contiene a ```GameEngine``` - logica principal del juego.
2. ```sprites.py```: Contiene las clases de todos los sprites y sus logicas.
3. ```battle_items.py```: Contiene las clases de todos los consumibles y sus logicas.
4. ```client.py```: Contiene la clase ```Client``` - maneja la comunicacion con ```Server```

#### Frontend

1. ```board.py```: Contiene a ```Board``` - crea una ```GridLayout``` con el laberinto.
2. ```game_widgets.py```: Contiene diferentes ```widgets``` para armar la ventana de juego completa.
3. ```game_window.py```: Contiene a ```FullWindow``` - ventana principal del juego.
4. ```sprite_widgets.py```: Contiene diferentes ```widgets``` para cada sprite.
5. ```item_widgets.py```: Contiene diferentes ```widgets``` para cada consumible.
6. ```start_window.py```: Contiene a ```LoginWindow``` - ventana de inicio.
7. ```stylesheets.py```: Contiene diferentes ```stylesheets``` para ```QObjects```.

### Servidor

1. ```logger.py```: Contiene a ```Logger``` - clase para imprimir server logs.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los archivos ```main.py``` de tanto ```client``` como ```server``` se correran desde sus respectivos directorios.
2. Eliminar lobos con el comando ```K+I+L``` no otorga puntaje.

## Referencias externas :book:

La musica fue obtenida de:
1. \<https://store.steampowered.com/app/2420510/HoloCure__Save_the_Fans/>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).