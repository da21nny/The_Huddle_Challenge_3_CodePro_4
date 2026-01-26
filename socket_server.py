import socket
import threading

def broadcast(message, client_emisor, client_list):
    for client in client_list:
        if client != client_emisor:
            try:
                client.send(message.encode("utf-8"))

            except:
                client.close()
                if client in client_list:
                    client_list.remove(client)
    

def manage_client(client_socket, client_address, client_list):
    name = client_socket.recv(50).decode("utf-8")
    print(f"Cliente {name} conectado desde: {client_address}")
    client_list.append(client_socket)
    print(f"Total de clientes: {len(client_list)}")
    broadcast(f"+ {name} se unio al chat", client_socket, client_list)

    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break

            print(F"{name}: {message}")
            
            broadcast(f"{name}: {message}", client_socket, client_list)            

    except Exception:
        client_socket.close()
        if client_socket in client_list:
            client_list.remove(client_socket)
                
    finally:
        broadcast(f"-{name} se desconecto", client_socket, client_list)
        print(f"\n{name} se desconecto del server.\nTotal de Clientes: {len(client_list)}")
        client_socket.close()
        if client_socket in client_list:
            client_list.remove(client_socket)


def main():
    client_list = []
    server_host = "127.0.0.1"
    server_port = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((server_host, server_port))
        server.listen()
        server.settimeout(1.0)
        print(f"Server iniciado en {server_host}:{server_port}")

        while True:
            try:
                client_socket, client_address = server.accept()
                client_thread = threading.Thread(target=manage_client, args=(client_socket, client_address, client_list))
                client_thread.daemon = True
                client_thread.start()

            except socket.timeout:
                continue
            
    except KeyboardInterrupt:
        print("Server se esta apagando.")
    
    finally:
        server.close()
        print("Server apagado.")

main()              