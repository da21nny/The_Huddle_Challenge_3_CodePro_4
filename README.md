# The_Huddle_Challenge_3_CodePro_4
"El mundo ha olvidado cómo hablar. Solo vos podés reescribir el protocolo. Bienvenido al Challenge 4."

## 📖 Descripción:
El proyecto es una aplicacion de chat grupal en tiempo real desarrollado en Python desde Cero utilizando el modulo Nativo Socket.
Implementa un Modelo Server-Cliente en donde se inicia el server y entra en modo espera, esperando la conexion de los clientes.
Una vez conectados, se identifican con un Nick para que puedan saber con quienes estan hablando.
El server hace de intermediario, recibe el mensaje de los clientes y luego comparte al resto excepto el que haya enviado.

## 🏗️ Arquitectura:
El proyecto presenta 2 script principales:
- Socket_server.py:
    Es el encargado de aceptar las conexiones, administrar los clientes y retransmitir los mensajes a los demas clientes (Broadcast).

- Socket_client.py:
    El encargado de crear hilos de clientes, enviar y recibir mensajes simultaneamente en la terminal.

## ⚙️ Detalles Tecnicos.
**Modelo:** Server-Client.
**Protocolo:** TCP/IP - IPv4.
**Codificacion:** UTF-.
**Lenguaje:** Python 3.14.
**Modulos:** Socket, Threading, Time, Sys (stdout).

## ✅ Funcionamiento.
### Server
- Crea un Socket TCP - IPv4  (socket.AF_INET, socket.SOCK_STREAM).
- Se asocia a una IP y Puerto (IP: 127.0.0.1 - Puerto: 8000)
- Escucha conexiones y lanza hilos de clientes.
- Reenvia cada mensaje recibido a los demas clientes excepto el que haya enviado (Broadcast).
- Maneja errores y desconexiones de clientes.

### Cliente
- Se conecta al server mediante el mismo IP y Puerto.
- Introduce un nick identificatorio para los demas clientes.
- Utiliza 2 hilos, uno para enviar el mensaje y el otro para recibir mensajes de los demas.
- Los mensajes son codificado y descodificado con el estandar UTF-8.
- Permite desconectarse con /salir o de forma forzada con CTRL + C.

### ▶️ Ejecucion:
1. Iniciar el Server:
python socket_server.py

2. Iniciar el Cliente:
python socket_client.py

3. Interactuar con los demas clientes
Cada cliente puede mandar y recibir mensajes. Si desea salir, debe escribir /salir o (CTRL + C) para salir de manera forzada.


### 🧠¿Quién sos después de este reto?
En una persona en donde usa herramientas con interfaces bonitos (Whatsapp) a entender el nivel primitivo de la mensajeria.

### 🩺¿Cómo sobrevivió tu aplicación?
Ha base de desiciones tecnicas de hilos independiente, sistema de reconexion que se niega a desconectar y manejo de errores que aparecen como arte de magia.

### 🛠 ¿Qué aprendiste cuando todo se rompió?
A como manejar los problemas que daba cada ejecucion, los mensajes apilados, textos vacios, fallos de reconexiones, desbordamiento de memoria por mala implementacion de hilos de clientes.