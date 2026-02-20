const net = require('net');

// Función para enviar mensajes al servidor
function enviar_mensaje(socket) {
    process.stdin.on('data', (texto_teclado) => {
        socket.write(texto_teclado);
    });
}

// Función para recibir mensajes del servidor
function recibir_mensaje(socket) {
    socket.on('data', (datos) => {
        console.log("Amigo: " + datos.toString());
    });

    socket.on('close', () => {
        console.log("El servidor cerró la conexión.");
        process.exit();
    });

    socket.on('error', () => {
        console.log("Error de conexión con el servidor.");
        process.exit();
    });
}

// Función para crear la conexión al servidor
function crear_conexion(puerto, host) {
    const socket = net.createConnection({ port: puerto, host: host });
    return socket;
}

// Función principal del programa
function main() {
    const PUERTO = 8000;
    const HOST = '127.0.0.1';

    const mi_socket = crear_conexion(PUERTO, HOST);

    mi_socket.on('connect', () => {
        console.log("¡Conectado al servidor! Ya puedes escribir:");

        recibir_mensaje(mi_socket);
        enviar_mensaje(mi_socket);
    });
}

// Arrancamos el programa
main();