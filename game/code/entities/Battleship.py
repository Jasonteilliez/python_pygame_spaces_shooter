import pygame
from math import degrees, atan2
from time import time
from entities.EntitiesBase import EntitiesBase


class Battleship(EntitiesBase):
    def __init__(self, groups, scale, surf, pos, alliance, order, data):
        super().__init__(groups, scale, surf, pos, alliance, order)

        self.direction = pygame.math.Vector2()
        self.stats = data['stats']
        self.attack_event=data['attack_event']
        self.is_attacking = False
        self.attack_time = None
        self.bullet_sprites = data['bullet_sprites']

        self.stats = {
            "max_health": data['stats']['max_health'],
            "attack_dommage": data['stats']['attack_dommage'],
            "attack_speed": data['stats']['attack_speed'],
            "impact_dommage": data['stats']['impact_dommage'],
            "mov_speed": data['stats']['mov_speed']
        }
        self.current_health = self.stats['max_health']