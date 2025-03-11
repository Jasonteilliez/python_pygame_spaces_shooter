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

        for _ in range(20):
            self.spawn_entity(name="small_star", data={})
        self.spawn_entity(name="player", data={
            'alliance':'player',
            'attack_event':self.attack_event
        })


        for _ in range(10):
            self.spawn_entity(name='small_asteroid', data={
                'alliance':'neutral'
            })
        for _ in range(5):
            self.spawn_entity(name="medium_asteroid", data={
                'alliance':'neutral'
            })
        for _ in range(2):
            self.spawn_entity(name="large_asteroid", data={
                'alliance':'neutral'
            })   


    def spawn_entity(self, name, data, pos=None):
            self.spawner.spawn_entity(
                groups=self.visible_sprites,
                scale=self.scale, 
                name=name, 
                data=data,
                pos=pos
            )


    def attack_event(self, bullet):
        self.spawner.spawn_entity(
            groups=self.visible_sprites,
            scale=self.scale, 
            name=bullet['name'], 
            data={
                'alliance':bullet['alliance'], 
                'direction':bullet['direction'], 
                'speed':bullet['speed'], 
                'pos':bullet['pos'], 
                'dommage':bullet['dommage']
            }
        )


    def run(self):
        dt = time() - self.last_time
        self.last_time = time()
        
        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)