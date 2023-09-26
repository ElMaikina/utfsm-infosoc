import pygame
import sys

class BloqueConTexto(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, fpath, fsize, fncolor, fscolor, bncolor, bscolor, text):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fpath = fpath
        self.fsize = fsize
        self.fncolor = fncolor
        self.fscolor = fscolor
        self.bncolor = bncolor
        self.bscolor = bscolor
        self.text = text

        self.font = pygame.font.Font(fpath, fsize)
        self.text_surf = self.font.render(text, True, fncolor)

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(bncolor)
        self.rect = self.surf.get_rect(center = (self.x, self.y))

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 960, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pensamiento Computacional')

## Define text parameters
font_path = 'space-mono.ttf'  # Replace with the path to your font file
font_size = 36
font = pygame.font.Font(font_path, font_size)
text_color_default = (255, 255, 255)  # Default text color (white)
text_color_hover = (255, 0, 0)  # Text color on hover (red)
#text = 'Pensamiento Computacional'
text1 = "¿Cómo se declara una variable entera?"
text2 = "(Responde de forma honesta porfavor)"

hovered = False  # Track if the mouse pointer is over the text
running = True

# Main game loop
while running:

    pressed_keys = pygame.key.get_pressed()

	# See if the window has closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pressed_keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    # Clear the screen
    screen.fill((0, 0, 0))

    # Create a text surface with the appropriate color
    text_color = text_color_hover if hovered else text_color_default
    text_surface1 = font.render(text1, True, text_color)
    text_surface2 = font.render(text2, True, text_color)


    # Get the bounding rectangle for the text surface
    text_rect1 = text_surface1.get_rect(center=(width // 2, height // 2))
    text_rect2 = text_surface2.get_rect(center=(width // 2, height // 2 + 32))

    #for e in elementos:
    #    screen.blit(e.text_surf, e.rect)
    #
    # Blit (draw) the text surface onto the screen
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

