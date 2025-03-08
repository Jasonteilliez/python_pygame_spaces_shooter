import pygame
from os import path
from settings import *
from math import degrees, atan2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, scale, pos, direction, entity='bullet_player', bullet_type="small_bullet"):
        super().__init__(groups)
        
        self.scale = scale
        self.bullet_type = bullet_type
        self.pos = pos
        self.direction = direction
        self.entity = entity
        self.speed = 300
        self.dommage = 10
        self.display_surface = pygame.display.get_surface()

        basedir = path.dirname(path.dirname(__file__))
        path_to_image = path.join(basedir, "graphics", "bullet", f"{self.bullet_type}.png")
        
        surf = pygame.image.load(path_to_image).convert_alpha()
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * self.scale)
        self.image = self.scale_surf
        self.pos =  pos
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))


    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt * self.scale
        self.pos.y += self.direction.y * self.speed * dt * self.scale

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)


    def bullet_kill(self):
        if self.rect.bottom <= 0 or self.rect.top >= self.display_surface.get_height() or \
        self.rect.left <= 0 or self.rect.right >= self.display_surface.get_width():
            self.kill()


    def update(self, dt):
        self.move(dt)
        self.bullet_kill()
