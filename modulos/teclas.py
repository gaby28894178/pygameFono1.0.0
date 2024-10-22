import pygame

def manejar_teclas(x, y, velocidad, ancho, alto, tamaño):
    # Obtener las teclas presionadas
    teclas = pygame.key.get_pressed()
    
    # Verificar si se ha hecho clic en la cruz para cerrar la ventana
  

    # Mover hacia la izquierda
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    # Mover hacia la derecha
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    # Mover hacia arriba
    if teclas[pygame.K_UP]:
        y -= velocidad
    # Mover hacia abajo
    if teclas[pygame.K_DOWN]:
        y += velocidad

    #marcar creditos
    if teclas[pygame.K_c]:
        print("Marcar creditos")
    # agregar a lista de reproduccion con tecla enter 
    if teclas[pygame.K_RETURN]:
        print("Agregar a lista de reproduccion")

    # salir de el programa con tecla q
    if teclas[pygame.K_q]:
        return x, y, False

    # Limitar el movimiento para no salir de la pantalla
    if x < 0:
        x = 0
    elif x + tamaño > ancho:
        x = ancho - tamaño
    if y < 0:
        y = 0
    elif y + tamaño > alto:
        y = alto - tamaño

    # Verificar si se presiona la tecla ESC para salir
    if teclas[pygame.K_ESCAPE]:
        return x, y, False  # Devuelve False para detener el bucle principal

    return x, y, True  # Continúa el juego
