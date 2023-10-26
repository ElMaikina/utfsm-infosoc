import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Constantes
NUMERO_ALUMNOS = 9
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "18AX5ZbuK4wVRcN1gvTOL4fAGFjvK8QHlfUywbjXNbtQ" #id de la speadsheet, esta es la de prueba que hice xd



#el credentials.json aqui son del proyecto de prueba que hice, no se si vamos a hacer uno a parte xd
def autenticar():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("server/credentials.json",SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    return credentials

'''
Si se puede, identificar de antes un rut con una fila en un diccionario
'''
def insertar_valores(rut: str, correo: str, puntos_quiz: int, puntos_codigo: int, total: int, credenciales):
    try:
        service = build("sheets", "v4", credentials=credenciales)
        sheets = service.spreadsheets()

        #buscar la fila del alumno en la spreadsheet
        ruts = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Hoja1!A2:A{NUMERO_ALUMNOS+2}").execute()
        ruts = ruts.get("values",[])
        index = 2
        for line in ruts:
            if(line[0]==rut):
                break
            index+=1
        if index < NUMERO_ALUMNOS+2: #se encontro el rut
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Hoja1!B{index}:G{index}", valueInputOption="USER_ENTERED", body = {"values": [[correo, puntos_quiz, puntos_codigo, "comentarios equisde", total, "completado"]]}).execute()
        else:
            print(f"rut {rut} no encontrado")
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