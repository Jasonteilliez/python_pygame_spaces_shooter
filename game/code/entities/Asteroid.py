import pygame
from random import randint
from entities.EntitiesBase import EntitiesBase

class Asteroid(EntitiesBase):
    def __init__(self, groups, scale, surf, pos, direction, speed, rotation_speed, alliance):
        super().__init__(groups, scale, surf, pos)

        self.direction=direction
        self.speed=speed
        self.rotation_speed=rotation_speed
        self.alliance=alliance

        self.angle=0

        self.stats = {
            'max_health': 1,
            'impact_dommage': 1,
        }


    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * self.scale
        if self.rect.right < -100:
            self.rect.x = self.display_surface.get_width() - self.rect.width + 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)
        elif self.rect.left > self.display_surface.get_width()+100:
            self.rect.x = - 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)

        self.rect.centery += self.direction.y * self.speed * dt * self.scale
        if self.rect.bottom < -100:
            self.rect.y = self.display_surface.get_height() - self.rect.height + 100
            self.rect.x = randint(-50, self.display_surface.get_width()+50)
        elif self.rect.top > self.display_surface.get_height() + 100:
            self.rect.y = - 100
            self.rect.x = randint(-50, self.display_surface.get_width()+50)


    def rotate(self, dt):
        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scale_surf, self.angle)
        self.rect = self.image.get_frect(center=self.rect.center) 


    def update(self, dt):
        self.move(dt)
        self.rotate(dt)