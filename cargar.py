import os
import random

# Clase que contiene la pregunta y sus respuestas
class Pregunta:
    def __init__(self, pregunta, opciones, respuesta):
        self.pregunta = pregunta
        self.opciones = opciones
        self.respuesta = respuesta
        self.elegida = -1

    def __str__(self):
        return f"Pregunta: {self.pregunta}\nOpciones: {', '.join(self.opciones)}\nRespuesta: {self.respuesta}\nElegida: {self.elegida}"

# Clase que sirve para responder la parte de desarrollo
class Desarrollo:
    def __init__(self, pregunta, tipo):
        self.pregunta = pregunta
        self.respuesta = ""
        self.intentos = 3
        self.puntaje = -1
        self.tipo = tipo

    def __str__(self):
        return f"Pregunta: {self.pregunta}\nRespuesta: {self.respuesta}\nTipo: {self.tipo}\nIntentos: {self.intentos}\nPuntaje: {self.puntaje}"

# Función para cargar preguntas de un archivo
def cargar_preguntas(archivo):
    preguntas = []
    with open(archivo, "r", encoding="utf-8") as file:
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

    return preguntas

# Función para cargar preguntas de un archivo
def cargar_desarrollo(archivo):
    with open(archivo, "r", encoding="utf-8") as file:
        lines = file.readlines()
        contexto = lines[0].strip()
        tipo = lines[1].strip()
        pregunta = Desarrollo(contexto, tipo)
        print(pregunta)
        return pregunta

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

    random.shuffle(todas_las_preguntas)
    todas_las_preguntas = todas_las_preguntas[0:20]
    return todas_las_preguntas

# Carga todas las preguntas de desarrollo
def cargar_todo_el_desarrollo():
    carpeta_preguntas = "desarrollo/"
    archivos = os.listdir(carpeta_preguntas)
    todas_las_preguntas = []

    for archivo in archivos:
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(carpeta_preguntas, archivo)
            preguntas = cargar_desarrollo(ruta_archivo)
            todas_las_preguntas.append(preguntas)

    random.shuffle(todas_las_preguntas)            
    return todas_las_preguntas
