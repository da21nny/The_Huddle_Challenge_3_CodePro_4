import socket
import threading

# Funcion para enviar un mensaje a todos los clientes conectados, excepto al emisor.
def broadcast(message, client_emisor, client_list): 
    for client in client_list: # Recorre la lista de clientes conectados.
        if client != client_emisor: # Si el cliente no es el emisor.
            try:
                client.send(message.encode("utf-8")) # Envía el mensaje al cliente.

            except: # Si hay un error al enviar el mensaje.
                client.close() # Cierra el socket del cliente.
                if client in client_list: # Si el cliente esta en la lista.
                    client_list.remove(client) # Lo elimina de la lista.
    
# Funcion para manejar la comunicacion con un cliente.
def manage_client(client_socket, client_address, client_list):
    name = client_socket.recv(50).decode("utf-8") # Recibe el nombre del cliente.
    print(f"Cliente {name} conectado desde: {client_address}") # Mensaje de conexion.
    client_list.append(client_socket) # Agrega el cliente a la lista de clientes.
    print(f"Total de clientes: {len(client_list)}") # Muestra el total de clientes conectados.
    broadcast(f"+ {name} se unio al chat", client_socket, client_list) # Notifica a los demas clientes.

    try:
        while True: # Bucle infinito para recibir mensajes del cliente.
            message = client_socket.recv(1024).decode("utf-8") # Recibe el mensaje del cliente.

            if not message: # Si el mensaje esta vacio.
                break # Sale del bucle.

            print(F"{name}: {message}") # Muestra el mensaje en el server.
            
            broadcast(f"{name}: {message}", client_socket, client_list) # Envía el mensaje a los demas clientes.        

    except Exception: # Si hay un error en la comunicacion.
        print(f"\nError de comunicacion con {name}.")
        client_socket.close() # Cierra el socket del cliente.
        if client_socket in client_list: # Si el cliente esta en la lista.
            client_list.remove(client_socket) # Lo elimina de la lista.
                
    finally: # Siempre se ejecuta al finalizar la comunicacion.
        broadcast(f"-{name} se desconecto", client_socket, client_list) # Notifica a los demas clientes.
        print(f"\n{name} se desconecto del server.\nTotal de Clientes: {len(client_list)}") # Mensaje de desconexion.
        client_socket.close() # Cierra el socket del cliente.
        if client_socket in client_list: # Si el cliente esta en la lista.
            client_list.remove(client_socket) # Lo elimina de la lista.

# Funcion principal del server donde se manejan las conexiones.
def main():
    client_list = [] # Lista para almacenar los clientes conectados.
    server_host = "127.0.0.1" # IP del server.
    server_port = 8000 # Puerto del server.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket del server.

    try:
        server.bind((server_host, server_port)) # Enlaza el socket a la direccion y puerto.
        server.listen() # Escucha conexiones entrantes.
        server.settimeout(1.0) # Establece un tiempo de espera para aceptar conexiones.
        print(f"Server iniciado en {server_host}:{server_port}") # Mensaje de inicio del server.

        while True: # Bucle infinito para aceptar conexiones de clientes.
            try:
                client_socket, client_address = server.accept() # Acepta una conexion entrante.
                # Crea un hilo para manejar la comunicacion con el cliente.
                client_thread = threading.Thread(target=manage_client, args=(client_socket, client_address, client_list))
                client_thread.daemon = True # Hace que el hilo sea daemon.
                client_thread.start() # Inicia el hilo.

            except socket.timeout: # Si no hay conexiones entrantes en el tiempo de espera.
                continue # Vuelve a intentar aceptar conexiones.
            
    except KeyboardInterrupt: # Si el usuario presiona Ctrl+C.
        print("Server se esta apagando.") # Mensaje de apagado del server.
    
    finally: # Siempre se ejecuta al finalizar el server.
        server.close() # Cierra el socket del server.
        print("Server apagado.") # Mensaje de server apagado.

if __name__ == "__main__":
    main() # Ejecuta el main principal.