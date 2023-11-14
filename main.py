import pygame
from pygame.locals import *
from validar import *
from cargar import *

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
code_font = pygame.font.Font(None, 20)
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
cursor_visible = True
cursor_timer = 0

# Bucle principal
running = True
registered = False
trolling = False
pregunta_actual = 0
respuesta_sel = 0
respuesta_click = 99
todas_las_preguntas = cargar_todas_las_preguntas()
todo_el_desarrollo = cargar_todo_el_desarrollo()
letras = ["A", "B", "C", "D"]

respuesta_abierta = ""

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:            
            if event.key == K_SPACE:
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    respuesta_abierta += " "
    
            if event.key == K_TAB:
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    respuesta_abierta += "    "

            elif event.key == K_RETURN:
                if not registered:
                    print(f"Nombre: {name}\nCorreo: {email}\nRut: {rut}")
                    name = str(name)
                    email = str(email)
                    rut = str(rut)
                    # Registra exitosamente al usuario
                    if str(name) != "" and str(email) != "" and rut != "":
                        registered = True

                    # TODO: hacer un codigo que verifique con la base de
                    # datos las credenciales del login
                    else:
                        print("Registre un usuario valido!")
                        trolling = True
                        name = ""
                        email = ""
                        rut = ""
                
                if registered and pregunta_actual >= len(todas_las_preguntas):
                    respuesta_abierta += "\n"

            elif event.key == K_BACKSPACE:
                if not registered:
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
                    largo = len(respuesta_abierta)
                    largo -= 1
                    respuesta_abierta = respuesta_abierta[:largo]

            else:
                if not registered:
                    if input_rect_name.collidepoint(pygame.mouse.get_pos()):
                        name += event.unicode
                    elif input_rect_email.collidepoint(pygame.mouse.get_pos()):
                        email += event.unicode
                    elif input_rect_rut.collidepoint(pygame.mouse.get_pos()):
                        rut += event.unicode

                if registered and pregunta_actual >= len(todas_las_preguntas):
                    respuesta_abierta += event.unicode
        
        elif event.type == MOUSEBUTTONDOWN:
            if not registered:
                if event.button == 1 and input_rect_start.collidepoint(pygame.mouse.get_pos()):
                    print(f"Nombre: {name}\nCorreo: {email}\nRut: {rut}")
                    name = str(name)
                    email = str(email)
                    rut = str(rut)
                    # Registra exitosamente al usuario
                    if str(name) != "" and str(email) != "" and rut != "":
                        registered = True
                    else:
                        print("Registre un usuario valido!")
                        trolling = True
                        name = ""
                        email = ""
                        rut = ""
                
            if registered:
                if event.button == 1 and pygame.mouse.get_pos()[1] < (screen_height * 0.7) and pregunta_actual < len(todas_las_preguntas):
                    respuesta_click = respuesta_sel
                    # TODO: hacer un codigo que envie las preguntas al excel
                    print("Se eligio la respuesta " + str(respuesta_click))
                
                if event.button == 1 and input_rect_back.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual += 1
                    if pregunta_actual > len(todas_las_preguntas) + len(todo_el_desarrollo) - 1:
                        pregunta_actual = len(todas_las_preguntas) + len(todo_el_desarrollo) - 1

                    print("Pregunta actual " + str(pregunta_actual))
                    # TODO: hacer un codigo que envie las preguntas al excel
                    respuesta_abierta = ""
                
                if event.button == 1 and input_rect_next.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual -= 1
                    if pregunta_actual < 0:
                        pregunta_actual = 0
                    
                    print("Pregunta actual " + str(pregunta_actual))
                    # TODO: hacer un codigo que envie las preguntas al excel
                    respuesta_abierta = ""


                if event.button == 1 and input_rect_run.collidepoint(pygame.mouse.get_pos()):
                    print("Se envio la pregunta a la API")
                    # TODO: enviar respuesta a a la API

    # Alternar la visibilidad del cursor cada 500 ms
    cursor_timer += 1
    if cursor_timer >= 300:
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
    if registered:

        # Preguntas de alternativa
        if pregunta_actual < len(todas_las_preguntas):
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
                else:
                    if letras_index == respuesta_sel and letras_index != respuesta_click:
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
            lineas = respuesta_abierta.split("\n")
            offset = 0
            display_header(todo_el_desarrollo[desarrollo_actual].pregunta, int(screen_width*0.05), int(screen_height*0.1))
            
            for linea in lineas:
                display_code(f"{linea}", input_rect_answer.x + 5, input_rect_answer.y + 5 + offset*20)
                offset += 1

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


    pygame.display.flip()

# Salir de Pygame
pygame.quit()
