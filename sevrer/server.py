import socket
import threading
import json
from sending_weas import autenticar, insertar_valores

'''
TO DO:
*reajustar para incluir ipv4, puertos y tamaño del header en un archivo config, que sea igual para el cliente como el server: DONE

*preguntar si sera necesario hacerle algun tipo de ui al server

*probar la wea desde otro pc
'''

with open('server/config.json','r') as config_file:
    config = json.load(config_file)

HEADER = config["header"]     #tamaño del mensaje que incluye el tamano de lo que se quiere mandar xd  
PORT = config["server_port"]    #puerto: 5050 suele servir
SERVER = config["server_ip"] #ipv4
ADDR = (SERVER,PORT)
FORMAT = config["format"]
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

credenciales = autenticar()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)   #parametro: cuantos bytes vamos a aceptar
        if msg_length:  #ver que el mensaje sea valido
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                datos_recibidos = json.loads(msg)
                insertar_valores(datos_recibidos["rut"], datos_recibidos["correo"], datos_recibidos["puntos_quiz"], datos_recibidos["puntos_codigo"], datos_recibidos["total"], credenciales)
            print(f"[{addr}] {msg}")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]  {threading.activeCount()-1}")


print("[STARING]")
start()
