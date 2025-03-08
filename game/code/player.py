import pygame
from os import path
from math import degrees, atan2
from time import time

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scale, attack_event):
        super().__init__(groups)
        self.scale = scale
        self.attack_event = attack_event

        basedir = path.dirname(path.dirname(__file__))
        path_to_image = path.join(basedir, "graphics", "player", "player.png")

        display_surface = pygame.display.get_surface()
        surf = pygame.image.load(path_to_image).convert_alpha()
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * self.scale)
        self.image = self.scale_surf
        self.rect = self.image.get_rect(center = (display_surface.get_width()/2,display_surface.get_height()/2))
        self.pos =  pygame.math.Vector2(self.rect.center)

        self.direction = pygame.math.Vector2()
        self.speed = 300

        self.is_attacking = False
        self.attack_time = None
        self.attack_cooldowns = 0.2

    
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

        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack_time = time()
            self.attack()         


    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt * self.scale
        self.pos.y += self.direction.y * self.speed * dt * self.scale

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        angle = - degrees(atan2(dx,-dy))

        self.image = pygame.transform.rotate(self.scale_surf, angle)
        self.rect = self.image.get_rect(center=self.rect.center) 


    def attack(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        direction = pygame.math.Vector2()
        direction.x = dx
        direction.y = dy
        direction = direction.normalize()

        pos = pygame.math.Vector2()
        pos.x = self.pos.x + 20*direction.x*self.scale
        pos.y = self.pos.y + 20*direction.y*self.scale

        bullet={
            'pos': pos, 
            'direction': direction, 
            'entity': 'player_bullet', 
            'bullet_type': 'small_bullet'
        }
        self.attack_event(bullet)


    def cooldowns(self):
        current_time = time()

        if self.is_attacking:
            if current_time - self.attack_time >= self.attack_cooldowns:
                self.is_attacking = False

    def update(self, dt):
        self.input()
        self.cooldowns()
        self.move(dt)
        self.rotate()