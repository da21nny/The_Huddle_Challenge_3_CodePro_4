const net = require('net');

const clientes = []; // Lista para guardar todos los usuarios conectados

// Función para enviar un mensaje a todos los clientes excepto al emisor
function broadcast(mensaje, socket_emisor) {
    clientes.forEach((cliente) => {
        if (cliente !== socket_emisor) {
            cliente.write(mensaje);
        }
    });
}

// Función para manejar la conexión de cada cliente
function manejo_de_clientes(socket) {
    // Guardamos al cliente
    clientes.push(socket);
    console.log("Un usuario se ha conectado. Total: " + clientes.length);

    // Recepción de mensajes
    socket.on('data', (datos) => {
        const mensaje = datos.toString();
        console.log("Recibido: " + mensaje);
        broadcast(mensaje, socket);
    });

    // Desconexión
    socket.on('close', () => {
        const posicion = clientes.indexOf(socket);
        if (posicion !== -1) {
            clientes.splice(posicion, 1);
        }
        console.log("Un usuario salió. Total: " + clientes.length);
    });

    socket.on('error', () => {}); 
}

// Función para crear el servidor
function crear_servidor(puerto, host) {
    const servidor = net.createServer(manejo_de_clientes);

    servidor.listen(puerto, host, () => {
        console.log("Servidor iniciado y escuchando en el puerto " + puerto);
    });
}

// Función principal del programa
function main() {
    const PUERTO = 8000;
    const HOST = '127.0.0.1';

    crear_servidor(PUERTO, HOST);
}

// Arrancamos el programa
main();