import pygame
import pygame_gui
import math
import random
import numpy

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Haxle')
windowX = 1600
windowY = 900

window_surface = pygame.display.set_mode((windowX, windowY))

window_surface.fill(pygame.Color('black'))

manager = pygame_gui.UIManager((windowX, windowY))


is_running = True

while is_running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    pygame.display.update()