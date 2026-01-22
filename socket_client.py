import socket

def main():
    server_ip = "127.0.0.1"
    server_port = 8000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, server_port))

    except KeyboardInterrupt:
        print("saliendo")

    finally:
        client.close()
        print("desconectado")

main()
