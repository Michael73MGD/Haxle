import pygame
import pygame_gui
import math
import random
import numpy

#Initialization and global vars
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Haxle')
windowX = 1600
windowY = 900
startYOffset = .9
ticks=0
window_surface = pygame.display.set_mode((windowX, windowY))
camera_speed = 15
background_color = 'SeaGreen'
background = pygame.Surface((windowX, windowY))
background.fill(pygame.Color(background_color))
Trucks = pygame.sprite.Group()
#truck = pygame.image.load('truck.png')
#truck.convert_alpha()
#truckX = 100
#truckY = windowY*startYOffset - truck.get_size()[1]

manager = pygame_gui.UIManager((windowX, windowY))

points = [(0,windowY*startYOffset)]
lastY = windowY*startYOffset
bumpiness = .05
smoothness = 10
for i in range(1,windowX,smoothness):
    dy = random.uniform(-1*bumpiness,bumpiness)

    points.append((i,int(lastY+dy)))
    lastY = lastY+dy


class Truck(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.height = height
        self.width = width 
        self.x = 100
        self.y = windowY*startYOffset - self.height*2
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.suspension_height = 20
        
        self.rear_wheel = pygame.Surface([40, 40], pygame.SRCALPHA)
        pygame.draw.circle(self.rear_wheel, color, (20, 20), 20)
        
        self.front_wheel = pygame.Surface([40, 40], pygame.SRCALPHA)
        pygame.draw.circle(self.front_wheel, color, (20, 20), 20)

truck = Truck('Black', 150, 60)
Trucks.add(truck)

is_running = True
timing = 0
while is_running:
    
    for Truck in Trucks:
        background.blit(Truck.image, (Truck.x, Truck.y))
        background.blit(Truck.rear_wheel, (Truck.x, Truck.y+Truck.height+Truck.suspension_height))
        background.blit(Truck.front_wheel, (Truck.x+Truck.width-40, Truck.y+Truck.height+Truck.suspension_height))
    
    ticks+=1
    if bumpiness < 10: bumpiness+=(ticks/100000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    ms = clock.tick(60)
    window_surface.blit(background, (0, 0))
    
    background.fill(pygame.Color(background_color))
    pygame.draw.lines(background, (200,200,200), False, points, width=1)
    

    timing += camera_speed
    if timing >= 60:
        timing -=60
        for i in range(0,len(points)-1):
            points[i] = (points[i][0],points[i+1][1])
    newY = int(random.uniform(-1*bumpiness,bumpiness+1)+points[len(points)-1][1])
    if newY >= windowY-1: newY=windowY-1
    elif newY <= 0: newY=0
    points[len(points)-1]=(windowX,newY)

    
    pygame.display.update()