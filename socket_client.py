import socket
import threading
import time
import sys

# Funcion para recibir mensajes del server.
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                sys.stdout.write("\r\033[K")
                print(message)
                sys.stdout.write("Ingrese mensaje: ")
                sys.stdout.flush()
            else:
                print("\n Cerrando Conexion")
                client_socket.close()
                break

        except Exception as e:
            print(f"\nError de conexion: {e}")
            client_socket.close()
            break

# Funcion para enviar mensajes al server.
def send_message(client_socket):
    try:
        while True:
            message = input("Ingrese mensaje: ")

            if message.lower() == "salir":
                print("\n Saliendo del server")
                break
            
            client_socket.send(message.encode("utf-8"))
    
    except Exception:
        print("Error: Mensaje no enviado")

# Funcion principal donde se conecta al server y crear hilos de envio y recibo de mensajes.
def main():
    server_ip = "127.0.0.1"
    server_port = 8000
    
    while True:
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

            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)

        if not connected:
            print("\n Error: Server no disponible. Intentando en 3 segundos...")
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

            break

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()
            print("\n Desconectado!")

main() # Ejecuta el main principal.