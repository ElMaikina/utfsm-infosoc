import tkinter as tk
import random
class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Opción Múltiple")
        self.root.geometry("1280x720")
        self.puntaje=0
        # Preguntas y respuestas
        self.preguntas = [
            {
                'pregunta': '¿Cuál es la función principal de la declaración "if" en Python?',
                'respuestas': ['Definir una función', 'Ejecutar una función', 'Tomar decisiones condicionales', 'Generar bucles'],
                'respuesta_correcta': 'Tomar decisiones condicionales'
            },
            {
                'pregunta': '¿Qué tipo de estructura de datos se utiliza para almacenar una secuencia de elementos en Python?',
                'respuestas': ['Lista', 'Enteros', 'Strings', 'Booleano'],
                'respuesta_correcta': 'Lista'
            },
            {
                'pregunta': '¿Cuál es el operador utilizado para la concatenación de Strings en Python?',
                'respuestas': ['+', '-', '*', '/',],
                'respuesta_correcta': '+'
            },
            {
                'pregunta': '¿Cuál es el tipo de dato utilizado para representar números enteros en Python?',
                'respuestas': ['int', 'float', 'str', 'bool'],
                'respuesta_correcta': 'int'
            },
            {
                'pregunta': '¿Qué tipo de bucle se utiliza para iterar sobre una secuencia en Python?',
                'respuestas': ['Bucle for', 'Bucle while', 'Bucle do-while', 'Bucle switch'],
                'respuesta_correcta': 'Bucle for'
            },
            {
                'pregunta': '¿Qué función se utiliza para obtener la longitud de una lista en Python?',
                'respuestas': ['longitud()', 'len()', 'length()', 'count()'],
                'respuesta_correcta': 'len()'
            },
            {
                'pregunta': '¿Cuál es el resultado de 2 + 3 * 4 en Python?',
                'respuestas': ['9', '14', '20', '5'],
                'respuesta_correcta': '14'
            },
            {
                'pregunta': '¿Qué tipo de datos se utiliza para representar un valor verdadero o falso en Python?',
                'respuestas': ['Entero', 'Cadena', 'Booleano', 'Flotante'],
                'respuesta_correcta': 'Booleano'
            },
            {
                'pregunta': '¿Cuál es el operador de igualdad en Python?',
                'respuestas': ['=', '==', '===', '!='],
                'respuesta_correcta': '=='
            },
            {
                'pregunta': '¿Qué función se utiliza para imprimir en la consola en Python?',
                'respuestas': ['print()', 'log()', 'display()', 'write()'],
                'respuesta_correcta': 'print()'
            }

        ]

        random.shuffle(self.preguntas)
        self.pregunta_actual = 0
        self.respuesta_seleccionada = tk.StringVar()

        self.label_pregunta = tk.Label(root, text="", font=("Times New Roman", 25), anchor="w")
        self.label_pregunta.pack(fill="x", padx=15, pady=20)  # Rellenar y agregar espacios

        # Configurar las opciones de respuesta alineadas a la izquierda con espacio
        self.opciones_respuesta = []
        for i in range(4):
            opcion = tk.Radiobutton(root, text="", variable=self.respuesta_seleccionada, value="", indicatoron=0, font=("Times New Roman", 20), anchor="w")
            opcion.pack(fill="both", padx=30, pady=6)  # Rellenar y agregar espacios
            self.opciones_respuesta.append(opcion)

        # Configurar el botón "Siguiente Pregunta" abajo a la derecha
        self.boton_siguiente = tk.Button(root, text="Siguiente Pregunta", command=self.siguiente_pregunta, font=("Times New Roman", 20))
        self.boton_siguiente.pack(side="bottom", padx=30, pady=30, anchor="se")  # Posicionar abajo a la derecha

        # Mostrar la primera pregunta
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas):
            pregunta = self.preguntas[self.pregunta_actual]
            self.label_pregunta.config(text=str(self.pregunta_actual+1)+") "+pregunta['pregunta'])
            respuestas = pregunta['respuestas']
            random.shuffle(respuestas)
            for i in range(4):
                self.opciones_respuesta[i].config(text=respuestas[i], value=respuestas[i])
            self.respuesta_seleccionada.set("")  # Reiniciar selección
        else:
            self.limpiar_interfaz()
            if self.puntaje!=1:
                self.label_pregunta.config(text=f"Test Terminado\n     Obtuviste {self.puntaje} puntos")
            else:
                self.label_pregunta.config(text=f"Test Terminado\n     Obtuviste {self.puntaje} punto")

    def siguiente_pregunta(self):
        if self.pregunta_actual < len(self.preguntas):
            pregunta = self.preguntas[self.pregunta_actual]
            respuesta_elegida = self.respuesta_seleccionada.get()
            respuesta_correcta = pregunta['respuesta_correcta']
            if respuesta_elegida == respuesta_correcta:
                self.puntaje+=1
            self.pregunta_actual += 1
            self.mostrar_pregunta()

    def limpiar_interfaz(self):
        self.label_pregunta.config(text="")
        for opcion in self.opciones_respuesta:
            opcion.destroy()
        self.boton_siguiente.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()