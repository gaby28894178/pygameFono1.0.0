import pygame
import os
import random
import time

# Inicializar Pygame
pygame.init()

# Configurar la ventana
ancho = 1024  # Aumentamos el ancho para el margen izquierdo
alto = 684  # Aumentamos la altura en 4 píxeles para el margen superior
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Visor de fotos y reproductor de música")

# Obtener la lista de archivos de imagen en la carpeta de música
ruta_carpeta = "C:\\musica"
# Colores para los recuadros
colores = [(215,0,0), (0,0,215), (0,215,0), (215,215,0), (118,0,118)]

# Función para obtener todas las imágenes en la carpeta y subcarpetas
imagenes = []
def obtener_imagenes(carpeta):
    global imagenes
    imagenes = []
    for raiz, dirs, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.lower().endswith(('.jpg', '.jpeg')):
                imagenes.append(os.path.join(raiz, archivo))
    if not imagenes:
        imagen_default = os.path.join(os.path.dirname(carpeta), "default.jpg")
        if os.path.exists(imagen_default):
            imagenes.append(imagen_default)
    return imagenes

# Función para obtener archivos de música en una carpeta
def obtener_canciones(carpeta):
    canciones = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('.mp3', '.wav', '.ogg',)):
            canciones.append(os.path.join(carpeta, archivo))
    return canciones

# Obtener la lista de archivos de imagen en la carpeta de música y subcarpetas
archivos = obtener_imagenes(ruta_carpeta)

# Verificar si se encontraron imágenes
if not archivos:
    print("No se encontraron imágenes en la carpeta especificada.")
    pygame.quit()
    exit()

# Índice de la imagen actual y posición del foco
indice_actual = 0
foco_x = 0
foco_y = 0

# Variables para el modo de lista de canciones
modo_canciones = False
canciones = []
indice_cancion = 0
lista_reproduccion = []

# Función para mostrar múltiples imágenes en una cuadrícula
def mostrar_imagenes(indice, foco_x, foco_y):
    # Esta función muestra una cuadrícula de imágenes en la ventana principal
    # Incluye la lógica para cargar, escalar y mostrar las imágenes
    # También dibuja el foco en la imagen seleccionada
    ventana.fill((0, 4, 0))  # Fondo negro
    imagenes_por_fila = 4  # Fijamos 4 imágenes por fila
    ancho_imagen = (ancho - 240) // imagenes_por_fila  # Restamos 200 para el margen izquierdo
    alto_imagen = int(ancho_imagen * 0.8)  # Altura menor para dejar espacio a los botones
    imagenes_por_columna = (alto - 54) // alto_imagen  # Dejamos espacio para los botones abajo y el margen superior
    total_imagenes = imagenes_por_fila * imagenes_por_columna

    for i in range(total_imagenes):
        indice_imagen = (indice + i) % len(archivos)
        x = 200 + (i % imagenes_por_fila) * ancho_imagen  # Añadimos 200 para el margen izquierdo
        y = 14 + (i // imagenes_por_fila) * alto_imagen  # Añadimos 4 para el margen superior
        
        try:
            ruta_imagen = archivos[indice_imagen]
            imagen = pygame.image.load(ruta_imagen)
            imagen = pygame.transform.scale(imagen, (ancho_imagen - 10, alto_imagen - 29))
            
            nombre_carpeta = os.path.basename(os.path.dirname(ruta_imagen))
            fuente = pygame.font.Font(None, 16)
            texto = fuente.render(nombre_carpeta, True, (255, 255, 255))
            ancho_texto = texto.get_width()
            ventana.blit(texto, (x + (ancho_imagen - ancho_texto) // 2, y + 5))
            
            ventana.blit(imagen, (x + 5, y + 29))
            
            if i == foco_y * imagenes_por_fila + foco_x:
                pygame.draw.rect(ventana, (0, 33, 0), (x-2, y-2, ancho_imagen+4, alto_imagen+2), 2)  # Borde negro más grueso
                pygame.draw.rect(ventana, (255, 255, 255), (x, y, ancho_imagen, alto_imagen), 2, 2)  # Borde blanco
                pygame.draw.rect(ventana, (240, 230, 240), (x+2, y+2, ancho_imagen-4, alto_imagen-4),  3)
                # Dibujar triángulo invertido en el centro
                centro_x = x + ancho_imagen // 2
                centro_y = y + alto_imagen // 4
                altura_triangulo = alto_imagen //4
                # Triángulo original (apuntando hacia abajo)
                pygame.draw.polygon(ventana, (0, 0, 230), [
                    (centro_x, centro_y + altura_triangulo // 4),
                    (centro_x - altura_triangulo // 2, centro_y - altura_triangulo // 2),
                    (centro_x + altura_triangulo // 2, centro_y - altura_triangulo // 2)
                ])
                
                # Triángulo invertido (apuntando hacia arriba)
                pygame.draw.polygon(ventana, (0, 0, 230), [
                    (centro_x, centro_y + altura_triangulo),
                    (centro_x - altura_triangulo // 4, centro_y + altura_triangulo * 1.5),
                    (centro_x + altura_triangulo // 6, centro_y + altura_triangulo * 1.5)
                ])
            else:
                color_recuadro = random.choice(colores)
                pygame.draw.rect(ventana, color_recuadro, (x, y, ancho_imagen, alto_imagen), 4, 4)
            
        except pygame.error:
            print(f"No se pudo cargar la imagen: {ruta_imagen}")

    # Mostrar lista de canciones en el margen izquierdo
    mostrar_lista_canciones_margen()

    pygame.display.flip()

# Función para mostrar la lista de canciones en el margen izquierdo
def mostrar_lista_canciones_margen():
    # Esta función muestra la lista de canciones en el margen izquierdo de la ventana
    # Incluye canciones anteriores, la canción actual y las canciones siguientes
    fuente = pygame.font.Font(None, 20)
    y = 14  # Aumentamos en 4 píxeles para el margen superior
    
    # Título para canciones anteriores
    pygame.draw.rect(ventana, (100, 100, 100), (5, y, 190, 25))
    texto_titulo = fuente.render("Canciones anteriores", True, (255, 255, 255))
    ventana.blit(texto_titulo, (10, y))
    y += 30
    
    for i, cancion in enumerate(lista_reproduccion[:indice_cancion]):
        color = (200, 200, 200)
        pygame.draw.rect(ventana, (50, 50, 50), (5, y-2, 190, 24))
        texto = fuente.render(os.path.basename(cancion)[:25], True, color)
        ventana.blit(texto, (10, y))
        y += 25
    
    # Título para canción actual
    y += 5
    pygame.draw.rect(ventana, (100, 100, 100), (5, y, 190, 25))
    texto_titulo = fuente.render("Canción actual", True, (255, 255, 255))
    ventana.blit(texto_titulo, (10, y))
    y += 30
    
    if indice_cancion < len(lista_reproduccion):
        color = (255, 255, 255)
        pygame.draw.rect(ventana, (0, 0, 0), (5, y-2, 190, 24))
        pygame.draw.rect(ventana, (255, 255, 255), (5, y-2, 190, 24), 2)
        texto = fuente.render(os.path.basename(lista_reproduccion[indice_cancion])[:25], True, color)
        ventana.blit(texto, (10, y))
        # Dibujar triángulo decorativo
        pygame.draw.polygon(ventana, (255, 255, 255), [(100, y+24), (95, y+19), (105, y+19)])
        y += 25
    
    # Título para canciones siguientes
    y += 5
    pygame.draw.rect(ventana, (100, 100, 100), (5, y, 190, 25))
    texto_titulo = fuente.render("Canciones siguientes", True, (255, 255, 255))
    ventana.blit(texto_titulo, (10, y))
    y += 30
    
    for i, cancion in enumerate(lista_reproduccion[indice_cancion+1:]):
        color = (0, 255, 0) if i == 0 else (255, 255, 255)
        pygame.draw.rect(ventana, (0, 50, 0) if i == 0 else (50, 50, 50), (5, y-2, 190, 24))
        texto = fuente.render(os.path.basename(cancion)[:25], True, color)
        ventana.blit(texto, (10, y))
        y += 25
    
    # Llamar a la nueva función para agregar más texto
    y = agregar_texto_adicional(y)

# Nueva función para agregar más texto
def agregar_texto_adicional(y):
    fuente = pygame.font.Font(None, 20)
    
    # Título para el texto adicional
    y += 10
    pygame.draw.rect(ventana, (100, 100, 100), (5, y, 190, 25))
    texto_titulo = fuente.render("Información adicional", True, (255, 255, 255))
    ventana.blit(texto_titulo, (10, y))
    y += 30
  
  

    # Agregar más texto aquí
    textos_adicionales = [
        "codigo desarrollador:", " 2024-03-01",
        "PROGAMADOR:", "Gabriel Gabrielli",
       
        "gabrielgabrielli@gmail.com",
        "11-2167-4227", "**********",
        "TECLAS DE USO ",
        "FLECHA ",
        "m","s","Enter",
        
        "**********"

        # Agrega más líneas según sea necesario
    ]
    
    for texto in textos_adicionales:
        pygame.draw.rect(ventana, (50, 50, 50), (5, y-2, 190, 24))
        texto_renderizado = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(texto_renderizado, (10, y))
        y += 25
    
    return y

# Función para mostrar la lista de canciones y la imagen de la carpeta
def mostrar_lista_canciones(carpeta, indice_cancion):
    # Esta función muestra la lista de canciones de una carpeta específica
    # También muestra la imagen de la carpeta o una imagen por defecto
    ventana.fill((0, 0, 0))  # Fondo negro
    
    # Mostrar imagen de la carpeta o imagen por defecto si no hay imagen
    try:
        imagen_carpeta = obtener_imagenes(carpeta)[0]
        imagen = pygame.image.load(imagen_carpeta)
    except (IndexError, pygame.error):
        imagen_default = os.path.join(os.path.dirname(ruta_carpeta), "default.jpg")
        try:
            imagen = pygame.image.load(imagen_default)
        except pygame.error:
            fuente_carpeta = pygame.font.Font(None, 36)
            texto_carpeta = fuente_carpeta.render(os.path.basename(carpeta), True, (255, 255, 255))
            ventana.blit(texto_carpeta, (210, 14))  # Aumentamos en 4 píxeles para el margen superior
        else:
            imagen = pygame.transform.scale(imagen, (200, 200))
            ventana.blit(imagen, (210, 14))  # Aumentamos en 4 píxeles para el margen superior
    else:
        imagen = pygame.transform.scale(imagen, (200, 200))
        ventana.blit(imagen, (210, 14))  # Aumentamos en 4 píxeles para el margen superior
    
    # Mostrar título del disco
    nombre_disco = os.path.basename(carpeta)
    fuente_titulo = pygame.font.Font(None, 24)
    texto_titulo = fuente_titulo.render(nombre_disco, True, (255, 255, 255))
    ancho_texto = texto_titulo.get_width()
    ventana.blit(texto_titulo, ((ancho - ancho_texto) // 2, 14))  # Aumentamos en 4 píxeles para el margen superior
    
    # Mostrar lista de canciones
    fuente = pygame.font.Font(None, 24)
    y = 54  # Aumentamos en 4 píxeles para el margen superior
    ancho_lista = 500
    alto_lista = alto - 104  # Restamos 4 píxeles más para mantener la proporción
    color_borde = random.choice(colores)
    pygame.draw.rect(ventana, color_borde, (445, 49, ancho_lista + 10, alto_lista + 10), 2)  # Aumentamos en 4 píxeles para el margen superior
    for i, cancion in enumerate(canciones):
        color = (255, 255, 255)
        if i == indice_cancion:
            pygame.draw.rect(ventana, (0, 0, 0), (450, y-2, ancho_lista, 24))
            pygame.draw.rect(ventana, (255, 255, 255), (450, y-2, ancho_lista, 24), 2)
            pygame.draw.polygon(ventana, (255, 255, 255), [(700, y+24), (695, y+19), (705, y+19)])
        texto = fuente.render(os.path.basename(cancion), True, color)
        ventana.blit(texto, (450, y))
        y += 30
    
    # Mostrar lista de canciones en el margen izquierdo
    mostrar_lista_canciones_margen()
    
    pygame.display.flip()

# Inicializar el mixer de Pygame
pygame.mixer.init()

# Función para reproducir la siguiente canción
def reproducir_siguiente_cancion():
    # Esta función reproduce la siguiente canción en la lista de reproducción
    global indice_cancion
    if lista_reproduccion:
        indice_cancion = (indice_cancion + 1) % len(lista_reproduccion)
        try:
            pygame.mixer.music.load(lista_reproduccion[indice_cancion])
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error al reproducir la canción: {e}")

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if not modo_canciones:
                imagenes_por_fila = 4
                imagenes_por_columna = (alto - 54) // ((ancho - 200) // imagenes_por_fila)  # Restamos 4 píxeles más para mantener la proporción
                total_imagenes = len(archivos)
                indice_actual_en_pantalla = foco_y * imagenes_por_fila + foco_x
                
                if evento.key == pygame.K_RIGHT:
                    if foco_x < imagenes_por_fila - 1 and indice_actual_en_pantalla < total_imagenes - 1:
                        foco_x += 1
                    elif indice_actual < total_imagenes - imagenes_por_fila:
                        indice_actual += 1
                elif evento.key == pygame.K_LEFT:
                    if foco_x > 0:
                        foco_x -= 1
                    elif indice_actual > 0:
                        indice_actual -= 1
                        foco_x = imagenes_por_fila - 1
                elif evento.key == pygame.K_DOWN:
                    if foco_y < imagenes_por_columna - 1 and indice_actual_en_pantalla + imagenes_por_fila < total_imagenes:
                        foco_y += 1
                    elif indice_actual + imagenes_por_fila < total_imagenes:
                        indice_actual += imagenes_por_fila
                elif evento.key == pygame.K_UP:
                    if foco_y > 0:
                        foco_y -= 1
                    elif indice_actual >= imagenes_por_fila:
                        indice_actual -= imagenes_por_fila
                        foco_y = imagenes_por_columna - 1
                elif evento.key == pygame.K_RETURN:
                    carpeta_seleccionada = os.path.dirname(archivos[indice_actual_en_pantalla])
                    canciones = obtener_canciones(carpeta_seleccionada)
                    if canciones:
                        modo_canciones = True
                        indice_cancion = 0
            else:
                if canciones:  # Verificar si la lista de canciones no está vacía
                    if evento.key == pygame.K_DOWN:
                        indice_cancion = (indice_cancion + 1) % len(canciones)
                    elif evento.key == pygame.K_UP:
                        indice_cancion = (indice_cancion - 1) % len(canciones)
                    elif evento.key == pygame.K_m:
                        modo_canciones = False
                    elif evento.key == pygame.K_RETURN:
                        if canciones[indice_cancion] not in lista_reproduccion:
                            lista_reproduccion.append(canciones[indice_cancion])
                        if not pygame.mixer.music.get_busy():
                            try:
                                pygame.mixer.music.load(canciones[indice_cancion])
                                pygame.mixer.music.play()
                            except pygame.error as e:
                                print(f"Error al reproducir la canción: {e}")
                    elif evento.key == pygame.K_s:
                        # Si no estamos en la última canción de la lista
                        if indice_cancion < len(canciones) - 1:
                            # Avanzamos al siguiente índice de canción
                            indice_cancion += 1
                            # Si la canción no está en la lista de reproducción, la añadimos
                            if canciones[indice_cancion] not in lista_reproduccion:
                                lista_reproduccion.append(canciones[indice_cancion])
                            # Cargamos la nueva canción
                            pygame.mixer.music.load(canciones[indice_cancion])
                            # Reproducimos la nueva canción
                            pygame.mixer.music.play()
                        # Si estamos en la última canción de la lista:
                        else:
                            # Detenemos la reproducción de música
                            pygame.mixer.music.stop()
                        # Llamamos a la función para reproducir la siguiente canción
                        # (Esta función probablemente maneja la lógica de reproducción continua)
                        reproducir_siguiente_cancion()

                    elif evento.key == pygame.K_SPACE:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        
    if modo_canciones:
        mostrar_lista_canciones(carpeta_seleccionada, indice_cancion)
    else:
        mostrar_imagenes(indice_actual, foco_x, foco_y)
    
    # Verificar si la canción actual ha terminado
    if not pygame.mixer.music.get_busy() and lista_reproduccion:
        reproducir_siguiente_cancion()
    
    # Pequeña pausa para reducir el uso de CPU
    pygame.time.delay(100)

pygame.quit()