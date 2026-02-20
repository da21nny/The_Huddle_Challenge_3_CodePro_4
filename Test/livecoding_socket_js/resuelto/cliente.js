const net = require('net');

/* ======================================================
PSEUDOCÓDIGO: enviar_mensaje
ESCUCHAR la entrada de teclado del sistema (process.stdin)
CUANDO el usuario escriba texto y presione Enter:
    ENVIAR ese texto directamente por el socket
====================================================== */
function enviar_mensaje(socket) {
    process.stdin.on('data', (texto_teclado) => {
        socket.write(texto_teclado);
    });
}

/* ======================================================
PSEUDOCÓDIGO: recibir_mensaje
ESCUCHAR el evento 'data' desde el servidor:
    CONVERTIR los datos a texto
    MOSTRAR en pantalla "Amigo: " mas el texto
    
ESCUCHAR el evento 'close' desde el servidor:
    MOSTRAR en pantalla "El servidor cerro la conexion"
    TERMINAR el programa
====================================================== */
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

/* ======================================================
PSEUDOCÓDIGO: crear_conexion
CREAR una conexion TCP usando el puerto y host indicados
RETORNAR el socket creado
====================================================== */
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