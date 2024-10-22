import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho, alto = 500, 500
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Cuadro con triángulos dentro")

# Colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (55, 12, 125)

# Posición y tamaño del cuadrado
cuadro_x = 150
cuadro_y = 150
cuadro_ancho = 200
cuadro_alto = 200

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Limpiar la pantalla
    pantalla.fill(NEGRO)

    # Dibujar el cuadro (rectángulo)
    pygame.draw.rect(pantalla, ROJO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))

    # Dibujar triángulos en las esquinas (dentro del cuadro)
    # Esquina superior izquierda
    pygame.draw.polygon(pantalla, BLANCO, [(cuadro_x, cuadro_y), 
                                           (cuadro_x + 20, cuadro_y), 
                                           (cuadro_x, cuadro_y + 20)])

    # Esquina superior derecha
    pygame.draw.polygon(pantalla, BLANCO, [(cuadro_x + cuadro_ancho, cuadro_y), 
                                           (cuadro_x + cuadro_ancho - 20, cuadro_y), 
                                           (cuadro_x + cuadro_ancho, cuadro_y + 20)])

    # Esquina inferior izquierda
    pygame.draw.polygon(pantalla, BLANCO, [(cuadro_x, cuadro_y + cuadro_alto), 
                                           (cuadro_x + 20, cuadro_y + cuadro_alto), 
                                           (cuadro_x, cuadro_y + cuadro_alto - 20)])

    # Esquina inferior derecha
    pygame.draw.polygon(pantalla, BLANCO, [(cuadro_x + cuadro_ancho, cuadro_y + cuadro_alto), 
                                           (cuadro_x + cuadro_ancho - 20, cuadro_y + cuadro_alto), 
                                           (cuadro_x + cuadro_ancho, cuadro_y + cuadro_alto - 20)])

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
