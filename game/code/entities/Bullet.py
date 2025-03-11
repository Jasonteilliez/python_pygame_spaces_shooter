import pygame
from entities.EntitiesBase import EntitiesBase

class Bullet(EntitiesBase):
    def __init__(self, groups, scale, surf, pos, alliance, direction, speed, dommage):
        super().__init__(groups, scale, surf, pos)

        self.direction = direction
        self.speed = speed

        self.alliance = alliance
        self.dommage = dommage


    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * self.scale
        self.rect.centery += self.direction.y * self.speed * dt * self.scale


    def bullet_kill(self):
        if self.rect.bottom <= 0 or self.rect.top >= self.display_surface.get_height() or \
        self.rect.left <= 0 or self.rect.right >= self.display_surface.get_width():
            self.kill()


    def update(self, dt):
        self.move(dt)
        self.bullet_kill()