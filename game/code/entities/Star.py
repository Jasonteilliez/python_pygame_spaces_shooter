import pygame
from entities.EntitiesBase import EntitiesBase

class Star(EntitiesBase):
    def __init__(self, groups, scale, surf, pos):
        super().__init__(groups, scale, surf, pos)
