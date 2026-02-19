import socket
import threading
import time
import sys

user_wants_exit = False # Variable global para controlar la salida del cliente.

# Funcion para recibir mensajes del server.
def receive_message(client_socket):
    global user_wants_exit # Variable global para controlar la salida del cliente.
    while True: # Bucle infinito para recibir mensajes.
        try:
            message = client_socket.recv(1024).decode("utf-8") # Recibe el mensaje del server.
            if message: # Si el mensaje no esta vacio.
                sys.stdout.write("\r\033[K") # Limpia la linea actual en la consola.
                print(message) # Imprime el mensaje recibido.
                sys.stdout.write("Mensaje (/salir): ") # Vuelve a imprimir el prompt.
                sys.stdout.flush() # Fuerza la impresion inmediata en la consola.
            else:
                if not user_wants_exit: # Si el usuario no quiere salir.
                    print("\n El server cerro Conexion.") # Mensaje de desconexion.
                client_socket.close() # Cierra el socket del cliente.
                break

        except Exception: # Si hay un error al recibir el mensaje.
            if not user_wants_exit: # Si el usuario no quiere salir.
                print("\n Error: Conexion perdida con el server.") # Mensaje de error.  
                client_socket.close() # Cierra el socket del cliente.
            break

# Funcion para enviar mensajes al server.
def send_message(client_socket):
    global user_wants_exit # Variable global para controlar la salida del cliente.
    while True: # Bucle infinito para enviar mensajes.
        try:
            message = input("Mensaje (/salir): ") # Solicita el mensaje al usuario.

            if message.lower() == "/salir": # Si el usuario quiere salir.
                user_wants_exit = True # Actualiza la variable global.
                print("\n Saliendo del server.\nDesconectado.") # Mensaje de salida.
                client_socket.close() # Cierra el socket del cliente.
                break
            
            client_socket.send(message.encode("utf-8")) # Envía el mensaje al server.
    
        except Exception: # Si hay un error al enviar el mensaje.
            print("Error: Mensaje no enviado") # Mensaje de error.
            client_socket.close() # Cierra el socket del cliente.
            break
        
# Funcion principal donde se conecta al server y crear hilos de envio y recibo de mensajes.
def main():
    global user_wants_exit # Variable global para controlar la salida del cliente.
    server_ip = "127.0.0.1" # IP del server.
    server_port = 8000 # Puerto del server.
    
    while True: # Bucle infinito para reconectar al server.
        user_wants_exit = False # Reinicia la variable global para controlar la salida del cliente.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket del cliente.
        client_socket.settimeout(5) # Establece un tiempo de espera para la conexion.

        connected = False # Variable para controlar la conexion.
        reconnect = 5 # Numero de intentos de reconexion. 
        for iterator in range(reconnect): # Bucle para intentar reconectar al server.
            try:
                print(f"Conectando: Intento {iterator + 1} de {reconnect}...") # Mensaje de intento de conexion.
                client_socket.connect((server_ip, server_port)) # Intenta conectar al server.
                connected = True # Si se conecta, actualiza la variable de conexion.
                break

            except Exception: # Si hay un error al conectar. 
                print(f"Error: No se pudo conectar al server") # Mensaje de error.
                time.sleep(2) # Espera 2 segundos antes de intentar reconectar.

        if not connected: # Si no se pudo conectar al server.
            print("\n Error: Server no disponible. Reconectando...") # Mensaje de error.
            time.sleep(3) # Espera 3 segundos antes de intentar reconectar.
            continue # Vuelve a intentar conectar al server.
        
        client_socket.settimeout(None) # Elimina el tiempo de espera para la conexion.
        print("\n Conectado al Server.") # Mensaje de conexion exitosa.

        try:
            name = input("Introduce tu nick: ") # Solicita el nombre del usuario.
            if not name: name = "Anonimo" # Si no se introduce un nombre, usa "Anonimo".
            client_socket.send(name.encode("utf-8")) # Envía el nombre al server.

            thread_send = threading.Thread(target=send_message, args=(client_socket,)) # Crea el hilo para enviar mensajes.
            thread_send.daemon = True # Establece el hilo como daemon.
            thread_send.start() # Inicia el hilo para enviar mensajes.

            thread_receive = threading.Thread(target=receive_message, args=(client_socket,)) # Crea el hilo para recibir mensajes.
            thread_receive.daemon = True # Establece el hilo como daemon.
            thread_receive.start() # Inicia el hilo para recibir mensajes.

            thread_send.join() # Espera a que el hilo de envio termine.
            thread_receive.join() # Espera a que el hilo de recepcion termine.

            if user_wants_exit: # Si el usuario quiere salir.
                client_socket.close() # Cierra el socket del cliente.
                break
            else: # Si la conexion se perdio inesperadamente.
                print("Reconectando con el server...") # Mensaje de reconexion.
                client_socket.close() # Cierra el socket del cliente.
                time.sleep(2) # Espera 2 segundos antes de intentar reconectar.
                continue # Vuelve a intentar conectar al server.

        except KeyboardInterrupt: # Si el usuario presiona Ctrl+C.
            user_wants_exit = True # Actualiza la variable global.  
            client_socket.close() # Cierra el socket del cliente.
            print("Desconexion forzada...") # Mensaje de desconexion.
            break

        finally: # Siempre se ejecuta al finalizar el bloque try.
            client_socket.close() # Cierra el socket del cliente.

if __name__ == "__main__":
    main() # Ejecuta el main principal.