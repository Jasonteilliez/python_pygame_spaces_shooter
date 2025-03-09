import pygame
from os import path
from random import randint


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, scale):
        super().__init__(groups)
    
        basedir = path.dirname(path.dirname(__file__))
        path_to_image = path.join(basedir, "graphics", "environment", "star.png")

        display_surface = pygame.display.get_surface()
        surf = pygame.image.load(path_to_image).convert_alpha()
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale)
        self.image = self.scale_surf
        pos = {
            'x': randint(0,display_surface.get_width()),
            'y': randint(0,display_surface.get_height())
        }
        self.rect = self.image.get_rect(center = (pos['x'],pos['y']))

    def update(self, dt):
        pass
