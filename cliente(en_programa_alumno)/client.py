import socket
import json

with open('config.json','r') as config_file:
    config = json.load(config_file)


HEADER = config["header"]     #tamaño del mensaje que incluye el tamano de lo que se quiere mandar xd  
PORT = config["server_port"]    #puerto: 5050 suele servir
SERVER = config["server_ip"] #ipv4
ADDR = (SERVER,PORT)
FORMAT = config["format"]
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)


def send_data(rut: str, correo: str, puntos_quiz: int, puntos_codigo: int, total: int):
    #de algun lado saco estos datos xd
    mensaje = {
        "rut": rut,
        "correo": correo,
        "puntos_quiz": puntos_quiz,
        "puntos_codigo": puntos_codigo,
        "total": total
    }

    mensaje_json = json.dumps(mensaje)
    send(mensaje_json)
    send(DISCONNECT_MESSAGE)



