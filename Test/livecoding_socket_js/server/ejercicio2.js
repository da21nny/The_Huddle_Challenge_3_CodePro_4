const net = require('net');

const clientes = []; // Lista para guardar todos los usuarios conectados

// Funcion broadcast para enviar un mensaje a todos los clientes excepto al emisor
function broadcast(mensaje, socket_emisor) {
    clientes.forEach((cliente) => {
        if (cliente !== socket_emisor) {
            cliente.write(mensaje);
        }
    });
}

// Funcion para manejar la conexión de cada cliente
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

/* ======================================================
PSEUDOCÓDIGO: crear_servidor(puerto, host)
    CREAR un servidor TCP pasandole la funcion de manejo_de_clientes
    ENCENDER el servidor en el puerto y host indicados
    MOSTRAR mensaje indicando que el servidor esta encendido
====================================================== */


// Función principal para arrancar el servidor
function main() {
    const PUERTO = 8000;
    const HOST = '127.0.0.1';

    crear_servidor(PUERTO, HOST);
}

// Arrancamos el programa
main();