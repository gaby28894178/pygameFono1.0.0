
# color rojo , verde , azul
# colores primario sistema RGB
#rojo 0,0,255
#verde 0,255,0
#azul 255,0,0

import pygame,sys
from pygame.locals import *

#tupla de color
color =(0,140,60,)
#con la clase Color de pygame
color2 =pygame.Color(220,140,6)

pygame.init()
# lienso
ventana = pygame.display.set_mode((800,600))
pygame.display.set_caption("Title Ventana")


while True:




    ventana.fill(color2)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()