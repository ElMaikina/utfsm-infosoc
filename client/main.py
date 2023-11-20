import pygame
import sys
from pygame.locals import *
from validar import *
from cargar import *
from client import *
from conexion_api import *

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height), HWSURFACE | DOUBLEBUF)
pygame.display.set_caption("Pensamiento Computacional")

# Colores
WHITE = (255, 255, 255)
BGCOL = (33, 33, 33)
SELCOL = (66, 66, 66)
CLKCOL = (150, 150, 150)

# Fuentes
code_font = pygame.font.Font(None, 25)
font = pygame.font.Font(None, 36)
header = pygame.font.Font(None, 40)

# Función para mostrar texto en la ventana
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Función para mostrar texto en la ventana
def display_header(text, x, y):
    text_surface = header.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Función para mostrar texto en la ventana
def display_code(text, x, y):
    text_surface = code_font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Colores para cuadros
input_color = BGCOL
selection_color = SELCOL
clicked_color = CLKCOL

# Campos de entrada de texto
input_rect_name = pygame.Rect(  int(screen_width*0.4),  3*int(screen_height*0.1),  int(screen_width*0.4),   int(screen_height*0.05))
input_rect_email = pygame.Rect( int(screen_width*0.4),  4*int(screen_height*0.1),  int(screen_width*0.4),   int(screen_height*0.05))
input_rect_rut = pygame.Rect(   int(screen_width*0.4),  5*int(screen_height*0.1),  int(screen_width*0.4),   int(screen_height*0.05))

# Para recorrer las preguntas
input_rect_next = pygame.Rect(   int(screen_width*0.25),  int(screen_height*0.75),  int(screen_width*0.2),   int(screen_height*0.15))
input_rect_back = pygame.Rect(   int(screen_width*0.55),  int(screen_height*0.75),  int(screen_width*0.2),   int(screen_height*0.15))
input_rect_start = pygame.Rect(  int(screen_width*0.3),  int(screen_height*0.75),  int(screen_width*0.4),   int(screen_height*0.15))
input_rect_run = pygame.Rect(   int(screen_width*0.65),  int(screen_height*0.2),  int(screen_width*0.175),   int(screen_height*0.175))

# Colores de las cajas de las respuestas
input_rect_answers = []
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  3*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  4*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  5*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  6*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))

# Box de texto para insertar codigo
input_rect_question = pygame.Rect(  int(screen_width*0.2),  2*int(screen_height*0.1),  int(screen_width*0.4),   int(screen_height*0.5))
input_rect_answer = pygame.Rect(  int(screen_width*0.2),  2*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.4))

name = ""
email = ""
rut = ""
puntaje = 0
puntos_desarrollo = 0
cursor_visible = True
cursor_timer = 0

# Bucle principal
clock = pygame.time.Clock()
fps = 60
running = True
registered = False
trolling = False
pregunta_actual = 0
respuesta_sel = 0
respuesta_click = 99
key_repeat_pause = 5
key_repeat_counter = key_repeat_pause
todas_las_preguntas = cargar_todas_las_preguntas()
todo_el_desarrollo = cargar_todo_el_desarrollo()
letras = ["A", "B", "C", "D"]

# Duracion de la prueba en frames
# Actualmente dura hora y media
#tiempo = fps * 60 * 60 * 1.5

#todo_el_desarrollo[desarrollo_actual].respuesta = ""

connect_to_server()

while running:
    manteniendo_teclas = pygame.key.get_pressed()
    if key_repeat_counter < key_repeat_pause:
        key_repeat_counter += 1
    if manteniendo_teclas[K_BACKSPACE] and key_repeat_counter > key_repeat_pause - 1:
        if not registered:
            key_repeat_counter = 0
            if input_rect_name.collidepoint(pygame.mouse.get_pos()):
                if len(name) > 0:
                    name = name[:-1]
            elif input_rect_email.collidepoint(pygame.mouse.get_pos()):
                if len(email) > 0:
                    email = email[:-1]
            elif input_rect_rut.collidepoint(pygame.mouse.get_pos()):
                if len(rut) > 0:
                    rut = rut[:-1]

        if registered and pregunta_actual >= len(todas_las_preguntas):
            key_repeat_counter = 0
            largo = len(todo_el_desarrollo[desarrollo_actual].respuesta)
            largo -= 1
            todo_el_desarrollo[desarrollo_actual].respuesta = todo_el_desarrollo[desarrollo_actual].respuesta[:largo]

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:            
            if event.key == K_SPACE:
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    todo_el_desarrollo[desarrollo_actual].respuesta += " "
    
            if event.key == K_TAB:
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    todo_el_desarrollo[desarrollo_actual].respuesta += "    "

            elif event.key == K_RETURN:
                if not registered:
                    print(f"Nombre: {name}\nCorreo: {email}\nRut: {rut}")
                    name = str(name)
                    email = str(email)
                    rut = str(rut)
                    # Registra exitosamente al usuario
                    if verify_email_rut(email, rut) == 1:
                        registered = True
                    
                    if verify_email_rut(email, rut) != 1:
                        registered = False
                        print("Registre un usuario valido!")
                        trolling = True
                        name = ""
                        email = ""
                        rut = ""
                
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    todo_el_desarrollo[desarrollo_actual].respuesta += "\n"

            elif event.key != K_BACKSPACE:
                if not registered:
                    if input_rect_name.collidepoint(pygame.mouse.get_pos()):
                        name += event.unicode
                    elif input_rect_email.collidepoint(pygame.mouse.get_pos()):
                        email += event.unicode
                    elif input_rect_rut.collidepoint(pygame.mouse.get_pos()):
                        rut += event.unicode

                if registered and pregunta_actual >= len(todas_las_preguntas):
                    todo_el_desarrollo[desarrollo_actual].respuesta += event.unicode
        
        elif event.type == MOUSEBUTTONDOWN:
            if not registered:
                if event.button == 1 and input_rect_start.collidepoint(pygame.mouse.get_pos()):
                    print(f"Nombre: {name}\nCorreo: {email}\nRut: {rut}")
                    name = str(name)
                    email = str(email)
                    rut = str(rut)
                    # Registra exitosamente al usuario
                    if verify_email_rut(email, rut) == 1:
                        registered = True
                    
                    if verify_email_rut(email, rut) != 1:
                        registered = False
                        print("Registre un usuario valido!")
                        trolling = True
                        name = ""
                        email = ""
                        rut = ""
                
            if registered:
                if event.button == 1 and pygame.mouse.get_pos()[1] < (screen_height * 0.7) and pregunta_actual < len(todas_las_preguntas):
                    respuesta_click = respuesta_sel
                    todas_las_preguntas[pregunta_actual].elegida = respuesta_click + 1
                    print(todas_las_preguntas[pregunta_actual])
    
                if event.button == 1 and input_rect_back.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual += 1
                    if pregunta_actual > len(todas_las_preguntas) + len(todo_el_desarrollo) - 1:
                        pregunta_actual = len(todas_las_preguntas) + len(todo_el_desarrollo) - 1
                
                if event.button == 1 and input_rect_next.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual -= 1                        
                    if pregunta_actual < 0:
                        pregunta_actual = 0

                if pregunta_actual >= len(todas_las_preguntas):
                    if event.button == 1 and input_rect_run.collidepoint(pygame.mouse.get_pos()):
                        if todo_el_desarrollo[desarrollo_actual].intentos > 0:
                            print("Se envio la pregunta a la API")
                            diccionario_respuesta = {'dato':todo_el_desarrollo[desarrollo_actual].respuesta,'tipo':str(todo_el_desarrollo[desarrollo_actual].tipo)}
                            estado_respuesta = get(diccionario_respuesta)

                            if estado_respuesta:
                                print("Respuesta valida")
                                todo_el_desarrollo[desarrollo_actual].puntaje = 4
                            if not estado_respuesta:
                                print("Respuesta invalida")
                                todo_el_desarrollo[desarrollo_actual].puntaje = 0

                            todo_el_desarrollo[desarrollo_actual].intentos -= 1

                        if todo_el_desarrollo[desarrollo_actual].intentos < 1:
                            print("Se acabaron los intentos")

                    # TODO: enviar respuesta a a la API

    # Alternar la visibilidad del cursor cada 500 ms
    cursor_timer += 1
    if cursor_timer >= 30:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    screen.fill((0, 0, 0))

    # Si no se ha registrado, mostrar el formulario
    if not registered:    
        pygame.draw.rect(screen, input_color, input_rect_name)
        display_header("Registrese como Alumno", int(screen_width*0.1), int(screen_height*0.1))

        if trolling:
            pygame.draw.rect(screen, input_color, input_rect_name)
            display_header("Inserte usuario valido!", int(screen_width*0.2), int(screen_height*0.6))

        pygame.draw.rect(screen, input_color, input_rect_name)
        display_text("Nombre:", int(screen_width*0.2), 3*int(screen_height*0.1))
        display_text(f"{name}", input_rect_name.x + 5, input_rect_name.y + 5)

        pygame.draw.rect(screen, input_color, input_rect_email)
        display_text("Correo:", int(screen_width*0.2), 4*int(screen_height*0.1))
        display_text(f"{email}", input_rect_email.x + 5, input_rect_email.y + 5)

        pygame.draw.rect(screen, input_color, input_rect_rut)
        display_text("Rut:", int(screen_width*0.2), 5*int(screen_height*0.1))
        display_text(f"{rut}", input_rect_rut.x + 5, input_rect_rut.y + 5)

        if cursor_visible:
            if input_rect_name.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.line(screen, WHITE, (input_rect_name.x + 5 + font.size(name)[0], input_rect_name.y + 0),
                                 (input_rect_name.x + 5 + font.size(name)[0], input_rect_name.y + 5 + font.get_height()))
            elif input_rect_email.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.line(screen, WHITE, (input_rect_email.x + 5 + font.size(email)[0], input_rect_email.y + 0),
                                 (input_rect_email.x + 5 + font.size(email)[0], input_rect_email.y + 5 + font.get_height()))
            elif input_rect_rut.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.line(screen, WHITE, (input_rect_rut.x + 5 + font.size(rut)[0], input_rect_rut.y + 0),
                                 (input_rect_rut.x + 5 + font.size(rut)[0], input_rect_rut.y + 5 + font.get_height()))
        
        # Para ir hacia adelante
        if input_rect_start.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, selection_color, input_rect_start)
        elif not input_rect_start.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, input_color, input_rect_start)
            
        display_header("Empezar", int(screen_width*0.38), int(screen_height*0.8))


    # Si ya se registro, mostrar las preguntas
    if registered:# and tiempo > 0:
        #tiempo -=1
        # Preguntas de alternativa
        if pregunta_actual < len(todas_las_preguntas):
            respuesta_click = todas_las_preguntas[pregunta_actual].elegida - 1
            display_header(todas_las_preguntas[pregunta_actual].pregunta[:52], int(screen_width*0.05), int(screen_height*0.1))
            display_header(todas_las_preguntas[pregunta_actual].pregunta[52:90], int(screen_width*0.05), int(screen_height*0.15))
            display_header(todas_las_preguntas[pregunta_actual].pregunta[90:], int(screen_width*0.05), int(screen_height*0.2))
            vertical_offset = 3*int(screen_height*0.1)
            letras_index = 0

            # Muestra todas las preguntas y les da un color si estan seleccionadas
            for pregunta_index in range(len(input_rect_answers)):
                if input_rect_answers[pregunta_index].collidepoint(pygame.mouse.get_pos()):
                    respuesta_sel = pregunta_index

            for opcion in todas_las_preguntas[pregunta_actual].opciones:
                if letras_index == respuesta_click:
                    pygame.draw.rect(screen, clicked_color, input_rect_answers[respuesta_click])

                elif letras_index == respuesta_sel:
                    pygame.draw.rect(screen, selection_color, input_rect_answers[letras_index])

                else:
                    pygame.draw.rect(screen, input_color, input_rect_answers[letras_index])

                display_text(str(letras[letras_index]) + ") "+ str(opcion), int(screen_width*0.2), vertical_offset)
                vertical_offset += 1*int(screen_height*0.1)
                letras_index += 1


        # Preguntas de desarrollo
        if pregunta_actual >= len(todas_las_preguntas):

            if input_rect_run.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, selection_color, input_rect_run)  
            elif not input_rect_run.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, input_color, input_rect_run)

            display_header("Run", int(screen_width*0.7), int(screen_height*0.252))

            desarrollo_actual = pregunta_actual - len(todas_las_preguntas)
            pygame.draw.rect(screen, input_color, input_rect_question)
            lineas = todo_el_desarrollo[desarrollo_actual].respuesta.split("\n")
            linea_actual = ""
            offset = 0

            #display_header(todo_el_desarrollo[desarrollo_actual].pregunta, int(screen_width*0.05), int(screen_height*0.1))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[:90], int(screen_width*0.025), int(screen_height*0.06))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[90:180], int(screen_width*0.025), int(screen_height*0.09))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[180:270], int(screen_width*0.025), int(screen_height*0.12))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[270:360], int(screen_width*0.025), int(screen_height*0.15))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[360:450], int(screen_width*0.025), int(screen_height*0.18))
            display_code(todo_el_desarrollo[desarrollo_actual].pregunta[450:], int(screen_width*0.025), int(screen_height*0.21))

            for linea in lineas:
                display_code(f"{linea}", input_rect_answer.x + 5, input_rect_answer.y + 5 + offset*code_font.size(linea_actual)[1])        
                linea_actual = linea
                offset += 1

            if cursor_visible:
                pygame.draw.line(screen, WHITE, (input_rect_answer.x + 5 + code_font.size(linea_actual)[0], input_rect_answer.y + 5 + (offset-1)*code_font.size(linea_actual)[1]),
                                (input_rect_answer.x + 5 + code_font.size(linea_actual)[0], input_rect_answer.y + 5 + offset*code_font.size(linea_actual)[1]))
            
            if (todo_el_desarrollo[desarrollo_actual].puntaje == 0):
                display_text("Pregunta incorrecta!", int(screen_width*0.65), int(screen_height*0.4))
                display_text("Intentos: " + str(todo_el_desarrollo[desarrollo_actual].intentos), int(screen_width*0.65), int(screen_height*0.45))

            if (todo_el_desarrollo[desarrollo_actual].puntaje > 0):
                display_text("Pregunta correcta!", int(screen_width*0.65), int(screen_height*0.4))
                display_text("Intentos: " + str(todo_el_desarrollo[desarrollo_actual].intentos), int(screen_width*0.65), int(screen_height*0.45))

        # La seccion de navegacion

        # Para ir hacia atras
        if input_rect_next.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, selection_color, input_rect_next)  
        elif not input_rect_next.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, input_color, input_rect_next)

        display_header("Back", int(screen_width*0.285), int(screen_height*0.8))

        # Para ir hacia adelante
        if input_rect_back.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, selection_color, input_rect_back)
        elif not input_rect_back.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, input_color, input_rect_back)

        display_header("Next", int(screen_width*0.585), int(screen_height*0.8))

    #if registered and tiempo <= 1:
    #    running = False

    #pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
    #print("Tiempo restante: " + str(tiempo))

# Salir de Pygame


# Asigna los puntajes finales
puntaje = 0
puntos_desarrollo = 0
for i in range(len(todas_las_preguntas) - 1):
    pregunta_subida = todas_las_preguntas[i]
    print(str(i) + ") Correcta: " + str(pregunta_subida.respuesta) + ", Elegida: " + str(pregunta_subida.elegida))
    if int(pregunta_subida.respuesta) == int(pregunta_subida.elegida):
        puntaje += 1

for i in range(len(todo_el_desarrollo) - 1):
    desarrollo_actual = todo_el_desarrollo[i]
    print(str(i) + ") Enunciado: " + desarrollo_actual.pregunta + "\nRespuesta: " + desarrollo_actual.respuesta)
    diccionario_respuesta = {'dato':desarrollo_actual.respuesta,'tipo':str(desarrollo_actual.tipo)}
    estado_respuesta = get(diccionario_respuesta)
    print("Se envio la pregunta a la API")

    if estado_respuesta:
        print("Respuesta valida")
        puntos_desarrollo += 4
    if not estado_respuesta:
        print("Respuesta invalida")

print("Puntaje de alternativas: " + str(puntaje))
print("Puntaje de desarrollo: " + str(puntos_desarrollo))
    
output = send_data(rut, email, puntaje, puntos_desarrollo, puntaje+puntos_desarrollo)

if output == 1:
    print("Se mandaron las preguntas al server!")
if output != 1:
    print("No se mando la respuesta al server!")

disconnect_from_server()
pygame.quit()

