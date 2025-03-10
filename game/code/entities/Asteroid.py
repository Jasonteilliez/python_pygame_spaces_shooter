import pygame
from random import randint


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, scale, surf, pos, direction, speed, rotation_speed, alliance):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()
        self.scale = scale
        self.surf = surf
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale)
        self.image = self.surf
        self.rect = self.image.get_frect(center = (pos['x'], pos['y']))
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
        if self.rect.left < -100:
            self.rect.x = -100
            self.direction.x = - self.direction.x
        elif self.rect.right > self.display_surface.get_width()+100:
            self.rect.x = self.display_surface.get_width() - self.rect.width + 100
            self.direction.x = - self.direction.x

        self.rect.centery += self.direction.y * self.speed * dt * self.scale
        if self.rect.top < -100:
            self.rect.y = -100
            self.direction.y = - self.direction.y
        elif self.rect.bottom > self.display_surface.get_height() + 100:
            self.rect.y = self.display_surface.get_height() - self.rect.height + 100
            self.direction.y = - self.direction.y


    def rotate(self, dt):
        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scale_surf, self.angle)
        self.rect = self.image.get_frect(center=self.rect.center) 


    def update(self, dt):
        self.move(dt)
        self.rotate(dt)