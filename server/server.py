import socket
import threading
import json
import mandar_cosas.sending_weas as snd
from pathlib import Path

'''
TO DO:
*reajustar para incluir ipv4, puertos y tamaño del header en un archivo config, que sea igual para el cliente como el server: DONE

*preguntar si sera necesario hacerle algun tipo de ui al server

*probar la wea desde otro pc
'''


with open('config.json','r') as config_file:
    config = json.load(config_file)

HEADER = config["header"]     #tamaño del mensaje que incluye el tamano de lo que se quiere mandar xd  
PORT = config["server_port"]    #puerto: 5050 suele servir
SERVER = config["server_ip"] #ipv4
ADDR = (SERVER,PORT)
FORMAT = config["format"]
DISCONNECT_MESSAGE = "!DISCONNECT"
snd.NUMERO_ALUMNOS = config["numero_alumnos"]
snd.SPREADSHEET_ID = config["spreadsheet_id"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

credenciales = snd.autenticar()
def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    conn.send(send_length)
    conn.send(message)

lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    index_in_spreadsheet = -1
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

                if(datos_recibidos["tipo"]=="sending" and index_in_spreadsheet != -1):   #es datos a insertar
                    snd.insertar_valores(datos_recibidos["puntos_quiz"], datos_recibidos["puntos_codigo"], datos_recibidos["total"], index_in_spreadsheet,credenciales)
                    with lock:
                        with open("LOG.txt", 'a') as log_file:
                            log_file.write(f'rut: {datos_recibidos["rut"]}, puntos quiz: {datos_recibidos["puntos_quiz"]}, puntos codigo: {datos_recibidos["puntos_codigo"]}')
                    send("1", conn)
                elif(index_in_spreadsheet == -1 and datos_recibidos["tipo"]=="sending"):
                    print(f"[{addr}] Insercion invalida: no se ha validado posicion en spreadsheet")
                    send("-1", conn)
                elif(datos_recibidos["tipo"] == "verify"):
                    verification_output = snd.obtener_indice(datos_recibidos["rut"], datos_recibidos["email"], credenciales)
                    if(verification_output>0): #se encontro
                        index_in_spreadsheet = verification_output
                        print(f"[{addr}] Posicion en spreadsheet encontrada: {index_in_spreadsheet}")
                        send("1", conn)
                    elif(verification_output == -1):    #correo no encontrado
                        print(f"[{addr}] Error verificacion: correo ingresado no encontrado")
                        send("-1", conn)
                    elif(verification_output == -2):
                        print(f"[{addr}] Error de verificacion: correo y rut no coinciden")
                        send("-2", conn)

            print(f"[{addr}] {msg}")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    continuar = True
    while continuar:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]  {threading.activeCount()-1}")


print("[STARING]")
start()
