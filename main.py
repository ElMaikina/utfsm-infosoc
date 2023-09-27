import pygame
import random
import sys

# Colores
white = (255, 255, 255)
grey = (66, 66, 66)
header_color = (174, 129, 255)
option_colors = [(249, 38, 114), (166, 226, 46), (102, 217, 239), (253, 151, 31)]

# Función para dibujar un rectángulo con texto
def dibujar_encabezado_texto(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x - width//2, y - height//2, width, height))
    font = pygame.font.Font('space-mono.ttf', 62)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Función para dibujar un rectángulo con texto
def dibujar_parrafo_texto(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x - width//2, y - height//2, width, height))
    font = pygame.font.Font('space-mono.ttf', 30)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Función para dibujar un rectángulo con texto
def dibujar_estadistica_texto(x, y, text1, text2):
    separation = 16
    font1 = pygame.font.Font('space-mono.ttf', 25)
    font2 = pygame.font.Font('space-mono.ttf', 25)
    text_surface1 = font1.render(text1, True, grey)
    text_surface2 = font2.render(text2, True, white)
    text_rect1 = text_surface1.get_rect(topleft=(x, y - separation))
    text_rect2 = text_surface2.get_rect(topleft=(x, y + separation))
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

class Pregunta():
    def __init__(self, enunciado, opciones):
        self.enunciado = enunciado
        self.opciones = opciones

# Bucle principal del juego
running = True

arreglo_preguntas = []
arreglo_preguntas.append(Pregunta("¿Cómo se declara una variable X entera?", ["def X():", "X = 0", "int X = 0;", "declare X"]))
arreglo_preguntas.append(Pregunta("Indique como se define una función \"func\"", ["def func():", "func = []", "\"func\"", "func = True"]))
arreglo_preguntas.append(Pregunta("Señale la opción que muestre un String", ["string = \"string\"", "string = 6", "string = 'c'", "string = [0, 5, 1, -8]"]))

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pensamiento Computacional")

# Posicion, velocidad y aceleracion X del UI
x = 0
vx = 0
speed = screen_width // 20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lee las teclas oprimidas
    pressed_keys = pygame.key.get_pressed()

    # Acelera el UI
    if x % screen_width == 0:
        if pressed_keys[pygame.K_RIGHT] and x < (len(arreglo_preguntas) - 1) * screen_width:
            vx = speed

        elif pressed_keys[pygame.K_LEFT] and x > 0:
            vx = -speed

        if not pressed_keys[pygame.K_RIGHT] and not pressed_keys[pygame.K_LEFT]:
            vx = 0

    if x + vx < 0:
        x = 0
        vx = 0
    
    if x + vx > (len(arreglo_preguntas) - 1) * screen_width:
        x = (len(arreglo_preguntas) - 1) * screen_width
        vx = 0
        
    x += vx

    # Limpia la pantalla
    screen.fill((0, 0, 0))

    # Numero actual de la pregunta
    pregunta_i = 0

    # Dibuja rectángulos con texto
    for pregunta in arreglo_preguntas:
        dibujar_encabezado_texto(screen_width/2 - x + pregunta_i*screen_width, 300 - 60, 1600, 300, header_color, pregunta.enunciado)
        dibujar_parrafo_texto(screen_width/2 - 320 - x + pregunta_i*screen_width, 600 - 60, 600, 200, option_colors[0], pregunta.opciones[0])
        dibujar_parrafo_texto(screen_width/2 + 320 - x + pregunta_i*screen_width, 600 - 60, 600, 200, option_colors[1], pregunta.opciones[1])
        dibujar_parrafo_texto(screen_width/2 - 320 - x + pregunta_i*screen_width, 850 - 60, 600, 200, option_colors[2], pregunta.opciones[2])
        dibujar_parrafo_texto(screen_width/2 + 320 - x + pregunta_i*screen_width, 850 - 60, 600, 200, option_colors[3], pregunta.opciones[3])
        pregunta_i+= 1
    
    dibujar_estadistica_texto(160, 60, "# enunciado de la pregunta", "")
    dibujar_estadistica_texto(60, 1080 - 120, "# nombre del jugador", "player = \"ElMaikina\"")
    dibujar_estadistica_texto(800, 1080 - 120, "# tiempo restante", "time = 35:46")
    dibujar_estadistica_texto(1350 - 30, 1080 - 120, "# arreglo de preguntas totales", "questions = [0, 0, 0, 0, 0, 0, 0, 0]")
    
    # Actualiza la pantalla
    pygame.display.flip()

    # Limita la velocidad de fotogramas a 60 FPS
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
