import requests

def detectar_expresion_maliciosa(codigo):
    modulos_peligrosos = ["os", "subprocess", "sys", "shutil"]
    for modulo in modulos_peligrosos:
        if f"import {modulo}" in codigo or f"from {modulo}" in codigo:
            return f"Expresión maliciosa detectada: Importación de '{modulo}'", False

    return "No se detectaron expresiones maliciosas", True

def get(params:dict)->bool:
    '''
    params = {'dato':"""
    n=int(input())
    suma=0
    for j in range(1,n+1):
        suma+=j
    print(suma)
    """, 'tipo':"Sumatoria"}
    '''

    # Tipos de pregunta
    #   1) Sumatoria
    #   2) IfElse
    #   3) Triangulo

    api_url = 'http://SpicyMip.pythonanywhere.com/api' 
    resultado = detectar_expresion_maliciosa(params['dato'])

    if resultado[1]:
        response = requests.get(url=api_url, params=params)
        if response.status_code == 200:
            data = response.text
            print('Respuesta de la API:', data)
            return bool(data)
        else:
            print('Error en la solicitud. Código de respuesta:', response.status_code)
            return False
    else:
        return False
