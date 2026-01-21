import socket
import threading

list_client= []

def main():
    server_host = "127.0.0.1"
    server_port = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((server_host, server_port))
        server.listen()
        print(f"Server iniciado en {server_host}:{server_port}")

        while True:
            client_socket, address = server.accept()
            print(f"Conexion entrante desde {address[0]}:{address[1]}")
            pass

    except KeyboardInterrupt:
        print("Server se esta apagando.")
    
    finally:
        server.close()
        print("Server apagado.")

main()