const net = require('net'); // Importa el módulo nativo de red de Node.js

let clienteSocket = null; // Variable global para guardar nuestra conexión

/* ======================================================
PSEUDOCÓDIGO: leerTecladoYEnviar
======================================================
INICIO leerTecladoYEnviar
    CUANDO la consola (teclado) reciba 'datos' (Enter) HACER:
        SI el clienteSocket está conectado ENTONCES
            Enviar los datos por el socket al servidor
        FIN SI
FIN
======================================================
*/
function leerTecladoYEnviar() {
    // process.stdin escucha todo lo que el usuario escribe en la terminal
    process.stdin.on('data', (textoIngresado) => {
        // Verifica que la conexión exista antes de intentar enviar
        if (clienteSocket) {
            clienteSocket.write(textoIngresado); // Envía el texto al servidor
        }
    });
}

/* ======================================================
PSEUDOCÓDIGO: iniciarCliente
======================================================
INICIO iniciarCliente
    Conectar al servidor en el puerto 8000
    
    CUANDO la conexión sea exitosa HACER:
        Mostrar "Conectado. Puedes escribir:"
        Llamar a leerTecladoYEnviar()
        
    CUANDO lleguen 'datos' del servidor HACER:
        Convertir datos a texto y mostrarlos en consola
        
    CUANDO el servidor se desconecte HACER:
        Mostrar "Servidor cerrado"
        Apagar el programa
FIN
======================================================
*/
function iniciarCliente() {
    // Intenta establecer conexión con el servidor en el puerto 8000
    clienteSocket = net.createConnection({ port: 8000, host: '127.0.0.1' }, () => {
        console.log("Conectado al servidor. Ya puedes escribir:");
        
        // Activa la lectura del teclado solo cuando ya estamos conectados
        leerTecladoYEnviar(); 
    });

    // Evento que se dispara cuando alguien más manda un mensaje y el servidor nos lo pasa
    clienteSocket.on('data', (data) => {
        // Imprime el mensaje recibido de los demás usuarios
        console.log("\n[Chat]: " + data.toString().trim()); 
    });

    // Evento que se dispara si el creador del servidor lo apaga
    clienteSocket.on('end', () => {
        console.log("El servidor cerró la conexión.");
        process.exit(); // Fuerza el cierre de la terminal del cliente
    });
    
    // Evento para manejar errores si el servidor no está encendido
    clienteSocket.on('error', () => {
        console.log("Error: No se pudo conectar al servidor. Asegúrate de encenderlo primero.");
        process.exit();
    });
}

// Ejecución principal del script
iniciarCliente();