import pygame
from random import randint
from entities.EntitiesBase import EntitiesBase

class Asteroid(EntitiesBase):
    def __init__(self, groups, scale, surf, pos, alliance, order, data):
        super().__init__(groups, scale, surf, pos, alliance, order)

        self.direction= data['direction']
        self.rotation_speed=data['rotation_speed']
        self.angle=0

        self.stats = {
            "max_health": data['stats']["max_health"],
            "impact_dommage": data['stats']['impact_dommage'],
            "mov_speed": data['speed']
        }
        self.current_health = self.stats['max_health']

        

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.stats["mov_speed"] * dt * self.scale
        if self.rect.right < -100:
            self.rect.x = self.display_surface.get_width() - self.rect.width + 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)
        elif self.rect.left > self.display_surface.get_width()+100:
            self.rect.x = - 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)

        self.rect.centery += self.direction.y * self.stats["mov_speed"] * dt * self.scale
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
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.move(dt)
        self.rotate(dt)