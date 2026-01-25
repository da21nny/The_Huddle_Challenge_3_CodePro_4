import socket
import threading

def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message:
                print("\n" + message)
            else:
                break

        except:
            break


def main():
    server_ip = "127.0.0.1"
    server_port = 8000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client.connect((server_ip, server_port))
    print("Conectado al server")

    try:
        name = input("Introduce tu nick: ")
        client.send(name.encode("utf-8"))

        client_thread = threading.Thread(target=receive_message, args=(client,))
        client_thread.daemon = True
        client_thread.start()

        while True:
            message = input("Ingrese mensaje: ")

            if message.lower() == "salir":
                print("saliendo del server")
                break
        
            client.send(message.encode("utf-8"))
            
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()
        print("desconectado")

main()
