import socket
import json
import sys
import os
from pathlib import Path

#script_path = Path(__file__, '..').resolve()
script_path = os.path.dirname(sys.executable)
with open('config.json','r') as config_file:
    config = json.load(config_file)

HEADER = config["header"]     #tamaño del mensaje que incluye el tamano de lo que se quiere mandar xd  
PORT = config["server_port"]    #puerto: 5050 suele servir
SERVER = config["server_ip"] #ipv4
ADDR = (SERVER,PORT)
FORMAT = config["format"]
DISCONNECT_MESSAGE = "!DISCONNECT"

#variables especificas del cliente
INDEX_IN_SPREADSHEET = -1 #numero de la linea que contiene info del usuario actual (rut matches con alguno en el excel)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''
connect_to_server establece la coneccion con el servidor especificado en config.json,
es necesario conectar al servidor para llamar al resto de funciones o estas fallan
'''
def connect_to_server():
    client.connect(ADDR)



'''
send codifica y envia el mensaje al servidor conectado
msg: es el mensaje a enviar
'''
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)


'''
verify_email_rut envia el rut y correo para revisar si estan en el archivo spreadsheet, estableciendo en el lado del servidor la posicion de este en el spreadsheet,
es necesario llamar a esta funcion antes de enviar datos
params:
    email: es el email a verificar dentro del spreadsheet
    rut: es el rut a verificar sea el adecuado en el email
return:
    1 si se encontro exitosamente el correo y el rut es el que corresponde
    -1 si el correo ingresado no se encontro en el spreadsheet
    -2 si el correo se encontro, pero el rut no es el que corresponde al correo

'''
def verify_email_rut(email: str, rut: str):
    mensaje = {

        "email": email,
        "rut": rut,
        "tipo": "verify"
    }

    mensaje_json = json.dumps(mensaje)
    send(mensaje_json)
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return(int(msg))

'''
send_data envia la indformacion al servidor para que este la suba al spreadsheet
params:
    rut, correo, puntos_quiz, puntos_codigo, total: son los datos a enviar para que se suban a la spreadsheet
return:
    1 si se enviaron los datos correctamente
    -1 si se trataron de enviar datos sin antes verificar el email y rut
'''
def send_data(rut: str, correo: str, puntos_quiz: int, puntos_codigo: int, total: int):
    #de algun lado saco estos datos xd
    mensaje = {
        "tipo": "sending",
        "rut": rut,
        "correo": correo,
        "puntos_quiz": puntos_quiz,
        "puntos_codigo": puntos_codigo,
        "total": total
    }

    mensaje_json = json.dumps(mensaje)
    send(mensaje_json)
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return(int(msg))

'''
disconect_from_server envia el mensaje de desconeccion al servidor, si no se llama antes de terminar el proceso del cliente, el servidor mantendra activa esa hebra hasta
que termine el proceso (lo cual es malo xd)
'''
def disconnect_from_server():
    send(DISCONNECT_MESSAGE)

