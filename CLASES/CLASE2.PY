# Importa las bibliotecas pygame y sys
import pygame,sys
# Importa todas las constantes de pygame.locals
from pygame.locals import *
# Inicializa todos los módulos de pygame
pygame.init()

# Crea una ventana de 800x600 píxeles
ventana = pygame.display.set_mode((800,600))
# Establece el título de la ventana
pygame.display.set_caption("Title Ventana")

# Bucle principal del juego
while True:
    
    # Itera sobre todos los eventos de pygame
    for event in pygame.event.get():
        # Si el evento es de tipo QUIT (cerrar ventana)
        if event.type==QUIT:
            # Cierra pygame
            pygame.quit()
            # Cierra el programa
            sys.exit()
    # Actualiza la pantalla
    pygame.display.update()
