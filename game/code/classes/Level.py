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

        self.visible_sprites = pygame.sprite.LayeredUpdates()

        self.last_time = time()
        self.spawner = Spawner(self.visible_sprites)

        self.level = 0

        for _ in range(20):
            self.spawn_entity(name="small_star", alliance='environment')

        self.player = self.spawn_entity(name="player", alliance='player', data={
            'attack_event':self.attack_event
        })

        for _ in range(10):
            self.spawn_entity(name='small_asteroid', alliance="neutral")
        for _ in range(5):
            self.spawn_entity(name="medium_asteroid", alliance="neutral")
        for _ in range(2):
            self.spawn_entity(name="large_asteroid", alliance="neutral")


    def spawn_entity(self, name, alliance, data={}, pos=None):
        self.spawner.spawn_entity(
            groups=self.visible_sprites,
            scale=self.scale, 
            name=name,
            alliance=alliance, 
            data=data,
            pos=pos
        )
        self.layer_order()


    def attack_event(self, bullet):
        self.spawner.spawn_entity(
            groups=self.visible_sprites,
            scale=self.scale, 
            name=bullet['name'], 
            alliance=bullet['alliance'],
            data={
                'direction':bullet['direction'], 
                'speed':bullet['speed'], 
                'pos':bullet['pos'], 
                'dommage':bullet['dommage']
            }
        )


    def layer_order(self):
        for sprite in self.visible_sprites:
            self.visible_sprites.change_layer(sprite, sprite.order)


    def run(self):
        dt = time() - self.last_time
        self.last_time = time()
        
        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)