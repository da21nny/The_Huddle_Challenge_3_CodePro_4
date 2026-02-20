const net = require('net');

const clientes = []; // Lista para guardar todos los usuarios conectados

/* ======================================================
PSEUDOCÓDIGO: broadcast
PARA CADA cliente EN la lista de clientes:
    SI el cliente ES DIFERENTE al socket_emisor:
        ENVIAR el mensaje a ese cliente
FIN PARA
====================================================== */
function broadcast(mensaje, socket_emisor) {
    clientes.forEach((cliente) => {
        if (cliente !== socket_emisor) {
            cliente.write(mensaje);
        }
    });
}

/* ======================================================
PSEUDOCÓDIGO: manejo_de_clientes
AGREGAR el nuevo socket a la lista de clientes
MOSTRAR en consola la cantidad total de clientes

ESCUCHAR el evento 'data' (llegada de datos):
    CONVERTIR los datos recibidos a texto
    MOSTRAR el texto en la consola
    LLAMAR a la funcion broadcast enviando el texto y el socket
    
ESCUCHAR el evento 'close' (desconexión):
    BUSCAR la posicion del socket en la lista
    ELIMINAR el socket de esa posicion
    MOSTRAR en consola que un usuario salio
====================================================== */
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
PSEUDOCÓDIGO: crear_servidor
CREAR un servidor TCP pasandole la funcion de manejo_de_clientes
ENCENDER el servidor en el puerto y host indicados
MOSTRAR mensaje indicando que el servidor esta encendido
====================================================== */
function crear_servidor(puerto, host) {
    const servidor = net.createServer(manejo_de_clientes);

    servidor.listen(puerto, host, () => {
        console.log("Servidor iniciado y escuchando en el puerto " + puerto);
    });
}

/* ======================================================
PSEUDOCÓDIGO: main
DEFINIR variable puerto como 8000
DEFINIR variable host como '127.0.0.1'
LLAMAR a la funcion crear_servidor con el puerto y host
====================================================== */
function main() {
    const PUERTO = 8000;
    const HOST = '127.0.0.1';

    crear_servidor(PUERTO, HOST);
}

// Arrancamos el programa
main();