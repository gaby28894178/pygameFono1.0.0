import pygame
import sys
from pygame.locals import *

pygame.init()

# Agregamos el reloj para controlar los FPS
reloj = pygame.time.Clock() 

ventana = pygame.display.set_mode((1024, 810))
pygame.display.set_caption("Galería de Imágenes")

# Cargar el icono
try:
    icono = pygame.image.load("ovni.png")
    pygame.display.set_icon(icono)
except pygame.error as e :
    print (f'el error es {e}')

# Titulo de la app
fuente = pygame.font.Font(None, 42)  # Crear una fuente para el texto
titulo_APP = fuente.render("FonoRoka 1.0.0", True, (255, 255, 255))  # Renderizar el texto

while True:
    ventana.fill((30, 30, 30))
    ventana.blit(titulo_APP, (10, 10))  # Blitear la superficie de texto

    pygame.draw.line(ventana, (255, 0, 0), (45, 45), (920, 45), 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
