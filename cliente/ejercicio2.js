const net = require('net');

// Función para enviar mensajes al servidor
function enviar_mensaje(socket) {
    process.stdin.on('data', (texto_teclado) => {
        socket.write(texto_teclado);
    });
}

/* ======================================================
PSEUDOCÓDIGO: recibir_mensaje(socket)
ESCUCHAR el evento 'data' desde el servidor:
    CONVERTIR los datos a texto
    MOSTRAR en pantalla "Amigo: " mas el texto
    
ESCUCHAR el evento 'close' desde el servidor:
    MOSTRAR en pantalla "El servidor cerro la conexion"
    TERMINAR el programa

ESCUCHAR el evento 'error' desde el servidor:
    MOSTRAR en pantalla "Error de conexión con el servidor"
    TERMINAR el programa
====================================================== */


// Funcion para crear la conexion con el servidor
function crear_conexion(puerto, host) {
    const socket = net.createConnection({ port: puerto, host: host });
    return socket;
}

// Funcion main para arrancar el programa
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