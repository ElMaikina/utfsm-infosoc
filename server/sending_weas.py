import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
import json


script_path = Path(__file__, '..').resolve()
with open(script_path.joinpath('config.json'),'r') as config_file:
    config = json.load(config_file)
#Constantes
NUMERO_ALUMNOS = config["numero_alumnos"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = config["spreadsheet_id"] #id de la speadsheet, esta es la de prueba que hice xd

script_path = Path(__file__, '..').resolve()

#el credentials.json aqui son del proyecto de prueba que hice, no se si vamos a hacer uno a parte xd
def autenticar():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(script_path.joinpath('credentials.json'),SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    return credentials

def obtener_indice(rut: str, email: str, credenciales):
    try:
        service = build("sheets", "v4", credentials=credenciales)
        sheets = service.spreadsheets()

        #buscar la fila del alumno en la spreadsheet
        ruts_emails = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Hoja1!A2:B{NUMERO_ALUMNOS+2}").execute()
        ruts_emails = ruts_emails.get("values",[])
        index = 2
        for line in ruts_emails:
            if(line[1]==email): #encontre el correo
                if(line[0] == rut): #el correo matchea con el rut
                    return index
                else:
                    return -2 #encontre el correo, pero el rut no calza
            
            index+=1
        return -1 #no encontre el correo
    except HttpError as error:
        print(error)


'''
Si se puede, identificar de antes un rut con una fila en un diccionario
'''
def insertar_valores(puntos_quiz: int, puntos_codigo: int, total: int, index: int, credenciales):
    try:
        service = build("sheets", "v4", credentials=credenciales)
        sheets = service.spreadsheets()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Hoja1!C{index}:G{index}", valueInputOption="USER_ENTERED", body = {"values": [[puntos_quiz, puntos_codigo, "comentarios equisde", total, "completado"]]}).execute()
    except HttpError as error:
        print(error)  




# def main():
#     # credenciales = autenticar()
#     # correo = "curanto"
#     # quiz = 6
#     # codigo = 8
#     # total = 14
#     # try:
#     #     service = build("sheets", "v4", credentials=credenciales)
#     #     sheets = service.spreadsheets()
#     #     sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Hoja1!A2:F2", valueInputOption="USER_ENTERED", body = {"values": [["amogus?", correo, quiz, codigo, "le fue como la tula", total]]}).execute()
#     # except HttpError as error:
#     #     print(error)
#     insertar_valores("11111-1", "avemapyo@mayo.cl", 6, 8, 14)
#     insertar_valores("22222-2", "curanto.mayonesa@mayo.cl", 10, 10, 20)
#     insertar_valores("1115611-1", "peo@mayo.cl", 6, 8, 14)




# if __name__ == "__main__":
#     main()