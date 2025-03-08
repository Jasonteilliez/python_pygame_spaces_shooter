import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        basedir = os.path.dirname(os.path.dirname(__file__))
        path_to_image = os.path.join(basedir, f"graphics{os.sep}player{os.sep}player.png")

        self.image = pygame.image.load(path_to_image).convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGTH/2))
        self.pos =  pygame.math.Vector2(self.rect.topleft)

    def update(self):
        pass