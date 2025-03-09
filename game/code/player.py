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

        self.display_surface = pygame.display.get_surface()
        surf = pygame.image.load(path_to_image).convert_alpha()
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * self.scale)
        self.image = self.scale_surf
        self.rect = self.image.get_frect(center = (self.display_surface.get_width()/2,self.display_surface.get_height()/2))

        self.direction = pygame.math.Vector2()

        self.is_attacking = False
        self.attack_time = None

        self.stats = {
            'max_health': 5,
            'dommage': 1,
            'attack_speed': 0.5,
            'mov_speed': 200
        }

    
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

        self.rect.centerx += self.direction.x * self.stats['mov_speed'] * dt * self.scale
        if self.rect.left < 0:
            self.rect.x = 0
        elif self.rect.right > self.display_surface.get_width():
            self.rect.x = self.display_surface.get_width() - self.rect.width

        self.rect.centery += self.direction.y * self.stats['mov_speed'] * dt * self.scale
        if self.rect.top < 0:
            self.rect.y = 0
        elif self.rect.bottom > self.display_surface.get_height():
            self.rect.y = self.display_surface.get_height() - self.rect.height
        
    
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        angle = - degrees(atan2(dx,-dy))

        self.image = pygame.transform.rotate(self.scale_surf, angle)
        self.rect = self.image.get_frect(center=self.rect.center) 


    def attack(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        direction = pygame.math.Vector2()
        direction.x = dx
        direction.y = dy
        direction = direction.normalize()

        pos = pygame.math.Vector2()
        pos.x = self.rect.centerx + 15*direction.x*self.scale
        pos.y = self.rect.centery + 15*direction.y*self.scale

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
            if current_time - self.attack_time >= self.stats['attack_speed']:
                self.is_attacking = False

    def update(self, dt):
        self.input()
        self.cooldowns()
        self.move(dt)
        self.rotate()