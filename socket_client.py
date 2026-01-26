import socket
import threading
import time
import sys

user_wants_exit = False

# Funcion para recibir mensajes del server.
def receive_message(client_socket):
    global user_wants_exit
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                sys.stdout.write("\r\033[K")
                print(message)
                sys.stdout.write("Mensaje (exit para salir): ")
                sys.stdout.flush()
            else:
                if not user_wants_exit:
                    print("\n El server cerro Conexion.")
                client_socket.close()
                break

        except Exception:
            if not user_wants_exit:
                client_socket.close()
            break

# Funcion para enviar mensajes al server.
def send_message(client_socket):
    global user_wants_exit
    try:
        while True:
            message = input("Mensaje (exit para salir): ")

            if message.lower() == "exit":
                user_wants_exit = True
                print("\n Saliendo del server.")
                break
            
            client_socket.send(message.encode("utf-8"))
    
    except Exception:
        print("Error: Mensaje no enviado")
        
# Funcion principal donde se conecta al server y crear hilos de envio y recibo de mensajes.
def main():
    global user_wants_exit
    server_ip = "127.0.0.1"
    server_port = 8000
    
    while True:
        user_wants_exit = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)

        connected = False
        reconnect = 5
        for iterator in range(reconnect):
            try:
                print(f"Conectando: Intento {iterator + 1} de {reconnect}...")
                client_socket.connect((server_ip, server_port))
                connected = True
                break

            except Exception:
                print(f"Error: No se pudo conectar al server")
                time.sleep(2)

        if not connected:
            print("\n Error: Server no disponible. Reconectando...")
            time.sleep(3)
            continue
        
        client_socket.settimeout(None)
        print("\n Conectado al Server.")

        try:
            name = input("Introduce tu nick: ")
            if not name: name = "Anonimo"
            client_socket.send(name.encode("utf-8"))    

            thread_send = threading.Thread(target=send_message, args=(client_socket,))
            thread_send.daemon = True
            thread_send.start()

            thread_receive = threading.Thread(target=receive_message, args=(client_socket,))
            thread_receive.daemon = True
            thread_receive.start()

            thread_send.join()

            if user_wants_exit:
                client_socket.close()
                break
            else:
                print("Reconectando con el server...")
                client_socket.close()
                time.sleep(2)
                continue

        except KeyboardInterrupt:
            client_socket.close()
            print("Desconexion forzada...")
            break

        finally:
            client_socket.close()

if __name__ == "__main__":
    main() # Ejecuta el main principal.