const net = require('net');

function enviar_mensaje(socket) {
    process.stdin.on('data', (texto_teclado) => {
        socket.write(texto_teclado);
    });
}

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

function crear_conexion(puerto, host) {
    const socket = net.createConnection({ port: puerto, host: host });
    return socket;
}

/* ======================================================
PSEUDOCÓDIGO: main
DEFINIR variable puerto como 8000
DEFINIR variable host como '127.0.0.1'
ASIGNAR a una variable el resultado de crear_conexion

ESCUCHAR el evento 'connect' en el socket:
    MOSTRAR en pantalla "Conectado al servidor"
    LLAMAR a la funcion recibir_mensaje pasandole el socket
    LLAMAR a la funcion enviar_mensaje pasandole el socket
====================================================== */


// Arrancamos el programa
main();