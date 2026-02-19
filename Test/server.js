const net = require('net'); // Importa el módulo nativo de red de Node.js

const clientes = []; // Array para guardar a todos los usuarios conectados

/* ======================================================
PSEUDOCÓDIGO: enviarATodosMenosAlEmisor
======================================================
INICIO enviarATodosMenosAlEmisor (mensaje, socketEmisor)
    PARA CADA cliente EN la lista de clientes HACER
        SI el cliente NO ES IGUAL al socketEmisor ENTONCES
            Escribir (enviar) el mensaje al cliente
        FIN SI
    FIN PARA
FIN
======================================================
*/
function enviarATodosMenosAlEmisor(mensaje, socketEmisor) {
    // Recorre la lista de todos los sockets conectados
    clientes.forEach((cliente) => {
        // Verifica que no se le envíe el mensaje al mismo que lo escribió
        if (cliente !== socketEmisor) {
            cliente.write(mensaje); // Envía el texto a través de la red
        }
    });
}

/* ======================================================
PSEUDOCÓDIGO: manejarDesconexion
======================================================
INICIO manejarDesconexion (socketDesconectado)
    Buscar la posición del socketDesconectado en la lista de clientes
    SI la posición existe ENTONCES
        Eliminar el socket de la lista usando su posición
        Mostrar en consola "Un usuario se ha desconectado"
    FIN SI
FIN
======================================================
*/
function manejarDesconexion(socketDesconectado) {
    // Busca el índice exacto de este cliente en el array
    const indice = clientes.indexOf(socketDesconectado);
    
    // Si el índice es diferente a -1, significa que sí lo encontró
    if (indice !== -1) {
        clientes.splice(indice, 1); // Borra 1 elemento en esa posición
        console.log("Un usuario se ha desconectado. Total:", clientes.length);
    }
}

/* ======================================================
PSEUDOCÓDIGO: manejarNuevaConexion
======================================================
INICIO manejarNuevaConexion (socket)
    Mostrar "Nuevo usuario conectado"
    Agregar el nuevo socket a la lista de clientes
    
    CUANDO el socket reciba 'datos' HACER:
        Convertir los datos a texto
        Mostrar el texto en la consola del servidor
        Llamar a enviarATodosMenosAlEmisor(texto, socket)
        
    CUANDO el socket indique 'cierre' HACER:
        Llamar a manejarDesconexion(socket)
FIN
======================================================
*/
function manejarNuevaConexion(socket) {
    console.log("Un nuevo usuario se ha conectado.");
    
    clientes.push(socket); // Añade el nuevo usuario al array global

    // Evento que se dispara cada vez que este cliente envía un mensaje
    socket.on('data', (data) => {
        const mensajeTexto = data.toString().trim(); // Convierte los bytes a texto sin espacios extra
        console.log("Mensaje recibido en servidor: " + mensajeTexto);
        
        // Reparte el mensaje a los demás
        enviarATodosMenosAlEmisor(mensajeTexto, socket);
    });

    // Evento que se dispara cuando el cliente cierra su terminal o pierde internet
    socket.on('close', () => {
        manejarDesconexion(socket); // Llama a la función de limpieza
    });
    
    // Evento para evitar que el servidor se caiga si hay un error de red
    socket.on('error', () => {
        manejarDesconexion(socket);
    });
}

/* ======================================================
PSEUDOCÓDIGO: iniciarServidor
======================================================
INICIO iniciarServidor
    Crear el servidor TCP usando manejarNuevaConexion
    Poner el servidor a escuchar en el puerto 8000
    Mostrar "Servidor corriendo en puerto 8000"
FIN
======================================================
*/
function iniciarServidor() {
    // Crea la instancia del servidor y le asigna la función principal
    const servidor = net.createServer(manejarNuevaConexion);

    // Enciende el servidor en el puerto especificado
    servidor.listen(8000, () => {
        console.log("Servidor TCP corriendo en el puerto 8000");
    });
}

// Ejecución principal del script
iniciarServidor();