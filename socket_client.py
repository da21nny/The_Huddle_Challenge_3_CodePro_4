import socket
import threading

# Funcion para recibir mensajes del server.
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print("\n" + message)
            else:
                print("\n Cerrando Conexion")
                client_socket.close()
                break

        except:
            print("\n Error: Se perdio conexion con el servidor")
            client_socket.close()
            break

# Funcion para enviar mensajes al server.
def send_message(client_socket):
    while True:
        message = input("Ingrese mensaje: ")

        if message.lower() == "salir":
            print("saliendo del server")
            break
        
    client_socket.send(message.encode("utf-8"))

# Funcion principal donde se conecta al server y crear hilos de envio y recibo de mensajes.
def main():
    server_ip = "127.0.0.1"
    server_port = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((server_ip, server_port))
    print("Conectado al server")

    try:
        name = input("Introduce tu nick: ")
        client_socket.send(name.encode("utf-8"))

        thread_send = threading.Thread(target=send_message, args=(client_socket,))
        thread_send.daemon = True
        thread_send.start()

        thread_receive = threading.Thread(target=receive_message, args=(client_socket,))
        thread_receive.daemon = True
        thread_receive.start()

            
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("desconectado")

main() # Ejecuta el main principal.