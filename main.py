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
font = pygame.font.Font(None, 36)
header = pygame.font.Font(None, 60)

# Función para mostrar texto en la ventana
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Función para mostrar texto en la ventana
def display_header(text, x, y):
    text_surface = header.render(text, True, WHITE)
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

# Colores de las cajas de las respuestas
input_rect_answers = []
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  3*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  4*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  5*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))
input_rect_answers.append(pygame.Rect(  int(screen_width*0.2),  6*int(screen_height*0.1),  int(screen_width*0.6),   int(screen_height*0.05)))

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
letras = ["A", "B", "C", "D"]

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            # Primero toma los inputs para registrar el usuario
            if event.key == K_RETURN:
                if not registered:
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
            else:
                if not registered:
                    if input_rect_name.collidepoint(pygame.mouse.get_pos()):
                        name += event.unicode
                    elif input_rect_email.collidepoint(pygame.mouse.get_pos()):
                        email += event.unicode
                    elif input_rect_rut.collidepoint(pygame.mouse.get_pos()):
                        rut += event.unicode
        
        elif event.type == MOUSEBUTTONDOWN:
            if registered:
                if event.button == 1 and pygame.mouse.get_pos()[1] < (screen_height * 0.7):
                    respuesta_click = respuesta_sel
                    print("Se eligio la respuesta " + str(respuesta_click))
                
                if event.button == 1 and input_rect_back.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual += 1
                    if pregunta_actual > len(todas_las_preguntas) - 1:
                        pregunta_actual = len(todas_las_preguntas) - 1

                    print("Pregunta actual " + str(pregunta_actual))
                
                if event.button == 1 and input_rect_next.collidepoint(pygame.mouse.get_pos()):
                    pregunta_actual -= 1
                    if pregunta_actual < 0:
                        pregunta_actual = 0
                    
                    print("Pregunta actual " + str(pregunta_actual))

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
            display_header("Inserte usuario valido!", int(screen_width*0.2), int(screen_height*0.8))

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

    # Si ya se registro, mostrar las preguntas
    if registered:    
        display_header(todas_las_preguntas[pregunta_actual].pregunta, int(screen_width*0.05), int(screen_height*0.1))
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
