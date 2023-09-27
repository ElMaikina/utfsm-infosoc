import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectángulos con Texto")

# Colores
white = (255, 255, 255)
grey = (66, 66, 66)
header_color = (174, 129, 255)
option_colors = [(249, 38, 114), (166, 226, 46), (102, 217, 239), (253, 151, 31)]

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

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

# Bucle principal del juego
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica del juego aquí

    # Limpia la pantalla
    screen.fill((0, 0, 0))

    # Dibuja rectángulos con texto
    dibujar_encabezado_texto(screen_width/2, 300 - 60, 1600, 300, header_color, "¿Como se declara un entero en Python?")
    dibujar_parrafo_texto(screen_width/2 - 320, 600 - 60, 600, 200, option_colors[0], "variable = 0")
    dibujar_parrafo_texto(screen_width/2 + 320, 600 - 60, 600, 200, option_colors[1], "int variable = 0")
    dibujar_parrafo_texto(screen_width/2 - 320, 850 - 60, 600, 200, option_colors[2], "def variable():")
    dibujar_parrafo_texto(screen_width/2 + 320, 850 - 60, 600, 200, option_colors[3], "declare int")
    
    dibujar_estadistica_texto(30, 1080 - 120, "# nombre del jugador", "plyr = \"ElMaikina\"")
    dibujar_estadistica_texto(800, 1080 - 120, "# tiempo restante", "T = 35:46")
    dibujar_estadistica_texto(1400, 1080 - 120, "# arreglo de preguntas totales", "P = [0, 0, 0, 0, 0, 0, 0, 0]")
    
    
    # Actualiza la pantalla
    pygame.display.flip()

    # Limita la velocidad de fotogramas a 60 FPS
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
