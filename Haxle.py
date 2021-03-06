import pygame
from pygame.constants import K_LEFT, K_RIGHT
import pygame_gui
import math
import random
import numpy
def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)

class Truck(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        # Basic shape params
        self.height = height
        self.width = width 
        self.x = 100
        self.y = 400  #windowY*startYOffset - self.height*2
        self.angle = 0

        # Vertical velocity for jumps.
        self.lastY = 400
        self.deltaY = 0

        # Image params
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image = pygame.image.load('truckPro.png')

        # [Sus]pension params
        self.rear_suspension_height = 20
        self.front_suspension_height = 20
        self.suspension_constant = suspension_constant #random guess, no idea what units are
        self.wheel_radius = 32
        self.rear_wheel_spring_force = 0
        self.front_wheel_spring_force = 0

        # Rear wheel params
        self.rear_wheel = pygame.Surface([self.wheel_radius*2, self.wheel_radius*2], pygame.SRCALPHA)
        self.rear_wheel = pygame.image.load('WHEEL.png')
        self.rear_wheel_y = self.y+self.height+self.rear_suspension_height+self.wheel_radius
        self.rear_wheel_x = self.x+10

        self.rear_wheel_x_V = 0 
        self.rear_wheel_x_F = 0
        self.rear_wheel_y_V = 0
        self.rear_wheel_y_F = 0
        self.rear_wheel_touching_ground = False
        
        # Front wheel params
        self.front_wheel = pygame.Surface([self.wheel_radius*2, self.wheel_radius*2], pygame.SRCALPHA)
        self.front_wheel = pygame.image.load('WHEEL.png')
        self.front_wheel_y = self.y+self.height+self.front_suspension_height+self.wheel_radius
        self.front_wheel_x = self.x+self.width- self.wheel_radius*2

        self.front_wheel_x_V = 0
        self.front_wheel_x_F = 0
        self.front_wheel_y_V = 0
        self.front_wheel_y_F = 0
        self.front_wheel_touching_ground = False

        # Draw wheels
        #pygame.draw.circle(self.rear_wheel, color, (self.wheel_radius, self.wheel_radius), self.wheel_radius)
        #pygame.draw.circle(self.front_wheel, color, (self.wheel_radius, self.wheel_radius), self.wheel_radius)

        # Force vectors
        self.x_F = 0 #x force component (acceleration)
        self.y_F = 0
        self.x_V = 0 #x velecity component (speed)
        self.y_V = 0
        
        
    def check_collision(self):
        # use this method for lines intersecting a rectangle http://www.pygame.org/docs/ref/rect.html#pygame.Rect.clipline
        self.rear_wheel_touching_ground = False
        self.front_wheel_touching_ground = False
        for point in points:
            if math.hypot(point[0]-self.rear_wheel_x, point[1]-self.rear_wheel_y) < self.wheel_radius*2:
                #print('rear wheel collision')
                self.rear_wheel_touching_ground = True
                self.rear_wheel_spring_force = -1*self.rear_wheel_y_V
                
                #F=kx   x=F/k
                if self.rear_suspension_height > 0:
                    self.rear_suspension_height += self.rear_wheel_spring_force/self.suspension_constant
                #print(self.rear_suspension_height)
                self.rear_wheel_y_V = 0
                self.rear_wheel_y_F = 0
                self.rear_wheel_y = point[1]-self.wheel_radius*2

            if math.hypot(point[0]-self.front_wheel_x, point[1]-self.front_wheel_y) < self.wheel_radius*2:
                #print('front wheel collision')
                self.front_wheel_touching_ground = True
                self.front_wheel_spring_force = -1*self.front_wheel_y_V
                if self.front_suspension_height > 0:
                    self.front_suspension_height += self.front_wheel_spring_force/self.suspension_constant
                self.front_wheel_y_V = 0
                self.front_wheel_y_F = 0
                self.front_wheel_y = point[1]-self.wheel_radius*2

            if self.rect.collidepoint(point):
                print('Crash')
                return False

    def update(self, keys):  #eventually, pass the gas/brake, angular velocity etc
        self.check_collision()
        if not self.rear_wheel_touching_ground and not self.front_wheel_touching_ground:
            if keys[K_RIGHT]:
                self.angle +=10
            elif keys[K_LEFT]:
                self.angle -= 10
        self.y_F += Gravity
        if not self.rear_wheel_touching_ground:
            self.rear_wheel_y_F += Gravity
            #print(self.rear_wheel_y_F)
        if not self.front_wheel_touching_ground:
            self.front_wheel_y_F += Gravity
        

        if self.y_V < terminal_velocity:
            self.y_V += self.y_F
        if self.rear_wheel_y_V < terminal_velocity:
            self.rear_wheel_y_V += self.rear_wheel_y_F
            #print(self.rear_wheel_y_F)
        if self.front_wheel_y_V < terminal_velocity: 
            self.front_wheel_y_V += self.front_wheel_y_F
        #self.y += self.y_V
        if self.rear_suspension_height < 20:
            self.rear_suspension_height += 1.5
        if self.front_suspension_height < 20:
            self.front_suspension_height += 1.5
        
        

        #print(self.rear_suspension_height)
        #should NOT be self.width but whatevs
        self.angle = math.degrees(math.atan2((self.rear_wheel_y+self.rear_suspension_height)-(self.front_wheel_y + self.front_suspension_height), self.width))
        print(self.rear_suspension_height,self.front_suspension_height)
        print(self.angle)

        self.rear_wheel_y += self.rear_wheel_y_V + self.y_V
        self.front_wheel_y += self.front_wheel_y_V + self.y_V

        self.lastY = self.y
        self.y = ((self.rear_wheel_y - self.rear_suspension_height) + (self.front_wheel_y - self.front_suspension_height))/2- self.height
        self.deltaY = self.y - self.lastY

        # warning we have no idea what x is for
        self.y_V = self.deltaY * .9
        self.x_V += self.x_F
        self.x += self.x_V
        blitRotate2(background, self.image, (self.x, self.y), self.angle)
        #self.image, self.rect = rot_center(self.image, self.angle, self.x, self.y)
        #self.image = pygame.transform.rotate(pygame.image.load('truckButBetter.png'), self.angle)
    

#Initialization and global vars
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Haxle')
windowX = 1600
windowY = 900
startYOffset = .95
ticks=0
window_surface = pygame.display.set_mode((windowX, windowY))
camera_speed = 50
background_color = 'SeaGreen'
background = pygame.Surface((windowX, windowY))
background.fill(pygame.Color(background_color))
Trucks = pygame.sprite.Group()
#truck = pygame.image.load('truck.png')
#truck.convert_alpha()
#truckX = 100
#truckY = windowY*startYOffset - truck.get_size()[1]

manager = pygame_gui.UIManager((windowX, windowY))
Gravity = .0005 #random guess
suspension_constant = Gravity * 100
terminal_velocity = 10
points = [(0,windowY*startYOffset)]
lastY = windowY*startYOffset
bumpiness = 0.5
smoothness = 100
for i in range(1,windowX,smoothness):
    dy = random.uniform(-1*bumpiness,bumpiness)

    points.append((i,int(lastY+dy)))
    lastY = lastY+dy

truck = Truck('Black', 192, 60)
Trucks.add(truck)

is_running = True
timing = 0
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        if camera_speed < max_camera_speed:
            camera_speed+=0.5
    elif keys[K_LEFT]:
        if(camera_speed > 0):
            camera_speed -= 0.5
    #print(camera_speed)
    
    for Truck in Trucks:
        Truck.update(keys)
        #background.blit(Truck.image, (Truck.x, Truck.y))
        background.blit(Truck.rear_wheel, (Truck.rear_wheel_x, Truck.rear_wheel_y))
        background.blit(Truck.front_wheel, (Truck.front_wheel_x, Truck.front_wheel_y))
    
    ticks+=1
    if bumpiness < 30: bumpiness+=(ticks/100000)
    
    ms = clock.tick(120)
    window_surface.blit(background, (0, 0))
    
    background.fill(pygame.Color(background_color))
    pygame.draw.lines(background, (200,200,200), False, points, width=1)
    

    timing += camera_speed
    if timing >= max_camera_speed:
        timing -= max_camera_speed
        for i in range(0,len(points)-1):
            points[i] = (points[i][0],points[i+1][1])
    newY = int(random.uniform(-1*bumpiness,bumpiness+1)+points[len(points)-1][1])
    if newY >= windowY-1: newY=windowY-1
    elif newY <= 100: newY=100
    points[len(points)-1]=(windowX,newY)

    
    pygame.display.update()