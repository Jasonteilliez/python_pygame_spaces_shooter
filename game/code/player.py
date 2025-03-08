import pygame
from os import path
from settings import *
from time import sleep
from math import degrees, atan2

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        basedir = path.dirname(path.dirname(__file__))
        path_to_image = path.join(basedir, "graphics", "player", "player.png")

        self.surf = pygame.image.load(path_to_image).convert_alpha()
        self.image = self.surf
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGTH/2))
        self.pos =  pygame.math.Vector2(self.rect.center)

        self.direction = pygame.math.Vector2()
        self.speed = 2

    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_o]:
            self.direction.y = -1
        elif keys[pygame.K_l]:
            self.direction.y = 1
        else:
            self.direction.y = 0     

        if keys[pygame.K_k]:
            self.direction.x = -1
        elif keys[pygame.K_m]:
            self.direction.x = 1
        else:
            self.direction.x = 0            


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed
        self.pos.y += self.direction.y * self.speed

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        angle = - degrees(atan2(dx,-dy))

        self.image = pygame.transform.rotate(self.surf, angle)
        self.rect = self.image.get_rect(center=self.rect.center) 
    

    def update(self):
        self.input()
        self.move()
        self.rotate()