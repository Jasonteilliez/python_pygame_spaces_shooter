import pygame
from time import time
from classes.Spawner import Spawner
from settings import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()        
        self.display_width = self.display_surface.get_width()
        self.display_height = self.display_surface.get_height()
        self.scale = min(self.display_width/BASE_WIDTH, self.display_height/BASE_HEIGTH)

        self.visible_sprites = pygame.sprite.Group()

        self.last_time = time()
        self.spawner = Spawner()

        self.spawn_small_star()
        self.player = self.spawner.spawn_player(self.visible_sprites,self.scale, self.attack_event)
        for _ in range(10):
            self.spawn_asteroid()

    def spawn_small_star(self):
        for _ in range(20):
            self.spawner.spawn_small_star(self.visible_sprites,self.scale)


    def attack_event(self, bullet):
        self.spawner.spawn_bullet(
            groups=self.visible_sprites,
            scale=self.scale, 
            alliance=bullet['alliance'], 
            name=bullet['name'], 
            direction=bullet['direction'], 
            speed=bullet['speed'], 
            pos=bullet['pos'], 
            dommage=bullet['dommage']
        )

    
    def spawn_asteroid(self):
        self.spawner.spawn_asteroid(
            groups=self.visible_sprites,
            scale=self.scale,
            alliance='neutral',
            name='small_asteroid'
        )


    def run(self):
        dt = time() - self.last_time
        self.last_time = time()
        
        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)