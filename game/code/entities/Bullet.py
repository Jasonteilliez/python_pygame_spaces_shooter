import pygame
from entities.EntitiesBase import EntitiesBase

class Bullet(EntitiesBase):
    def __init__(self, groups, scale, surf, pos, alliance, order, data):
        super().__init__(groups, scale, surf, pos, alliance, order)

        self.direction = data['direction']
        self.speed = data['speed']
        self.dommage = data['dommage']


    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * self.scale
        self.rect.centery += self.direction.y * self.speed * dt * self.scale


    def bullet_kill(self):
        if self.rect.bottom <= -100 or self.rect.top >= self.display_surface.get_height() + 100 or \
        self.rect.left <= -100 or self.rect.right >= self.display_surface.get_width() + 100:
            self.kill()


    def update(self, dt):
        self.move(dt)
        self.bullet_kill()