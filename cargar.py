import os
import random

# Clase que contiene la pregunta y sus respuestas
class Pregunta:
    def __init__(self, pregunta, opciones, respuesta):
        self.pregunta = pregunta
        self.opciones = opciones
        self.respuesta = respuesta

    def __str__(self):
        return f"Pregunta: {self.pregunta}\nOpciones: {', '.join(self.opciones)}\nRespuesta: {self.respuesta}"

# Función para cargar preguntas de un archivo
def cargar_preguntas(archivo):
    preguntas = []
    with open(archivo, "r") as file:
        lines = file.readlines()
        pregunta = lines[0].strip()  # La primera línea es la pregunta
        opciones = []
        opciones.append(lines[1].strip())
        opciones.append(lines[2].strip())
        opciones.append(lines[3].strip())
        opciones.append(lines[4].strip())
        
        respuesta = lines[5].strip()  # La última línea contiene la respuesta
        pregunta = Pregunta(pregunta, opciones, respuesta)
        print(pregunta)
        preguntas.append(pregunta)

    random.shuffle(preguntas)
    return preguntas

# Carga todas las preguntas
def cargar_todas_las_preguntas():
    carpeta_preguntas = "preguntas/"
    archivos = os.listdir(carpeta_preguntas)
    todas_las_preguntas = []

    for archivo in archivos:
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(carpeta_preguntas, archivo)
            preguntas = cargar_preguntas(ruta_archivo)
            todas_las_preguntas.extend(preguntas)

    return todas_las_preguntas

