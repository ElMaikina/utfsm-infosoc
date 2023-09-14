import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 960, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pensamiento Computacional')

# Define text parameters
font_path = 'space-mono.ttf'  # Replace with the path to your font file
font_size = 36
font = pygame.font.Font(font_path, font_size)
text_color_default = (255, 255, 255)  # Default text color (white)
text_color_hover = (255, 0, 0)  # Text color on hover (red)
text = 'Pensamiento Computacional'

# Main game loop
hovered = False  # Track if the mouse pointer is over the text
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            # Check if the mouse pointer is over the text
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            if text_rect.collidepoint(event.pos):
                hovered = True
            else:
                hovered = False

    # Clear the screen
    screen.fill((0, 0, 0))  # Black

    # Create a text surface with the appropriate color
    text_color = text_color_hover if hovered else text_color_default
    text_surface = font.render(text, True, text_color)

    # Get the bounding rectangle for the text surface
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))

    # Blit (draw) the text surface onto the screen
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

