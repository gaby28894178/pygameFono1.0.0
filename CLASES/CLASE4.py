# Importación de módulos necesarios
import pygame, sys
from pygame.locals import *
import os

# Obtener la ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Inicialización de Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))  # Creación de la ventana
pygame.display.set_caption("Ventana del Juego")

# Carga de la imagen del ovni
try:
    ruta_imagen = os.path.join(directorio_actual, "imagenes", "ovni.png")
    ovni = pygame.image.load(ruta_imagen)
    if ovni is None:
        print("Error: No se pudo cargar la imagen del ovni.")
        sys.exit()
except pygame.error as e:
    print(f"Error al cargar la imagen del ovni: {e}")
    sys.exit()

# Cambiar el tamaño de la imagen del ovni
ovni = pygame.transform.scale(ovni, (90, 90))  # Ajusta el tamaño a 90x90 píxeles
posicionX, posicionY = 10, 230
velocidad = 5
derecha = True
vidas = 3
credits = 0

rectangulo = pygame.Rect(0, 0, 90, 90)
rectangulo2 = pygame.Rect(posicionX, posicionY, 90, 10)

reloj = pygame.time.Clock()  # Agregamos el reloj para controlar los FPS

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    ventana.fill(pygame.Color(0, 0, 0))  # Limpia la pantalla con color negro
    
    # Actualización de la posición del rectángulo2
    if derecha:
        if posicionX < 710:
            posicionX += velocidad
        else:
            derecha = False
    else:
        if posicionX > 1:
            posicionX -= velocidad
        else:
            derecha = True
    
    rectangulo2.left = posicionX

    # Actualización de la posición del rectángulo controlado por el mouse
    rectangulo.left, rectangulo.top = pygame.mouse.get_pos()
    
    # Dibujo de los rectángulos
    pygame.draw.rect(ventana, (0, 255, 50), rectangulo)
    pygame.draw.rect(ventana, (255,255,255), rectangulo2, 1)
    
    # Detección de colisión
    if rectangulo.colliderect(rectangulo2):
        print("COLISION")
    
    pygame.display.update()
    reloj.tick(60)  # Limitamos el framerate a 60 FPS
