import pygame, sys
from os import path
from time import time
from json import load

from settings import *
from classes.Spawner import Spawner

class Level:
    def __init__(self):
        self.basedir = path.dirname(path.dirname(path.dirname(__file__)))
        self.display_surface = pygame.display.get_surface()        
        self.display_width = self.display_surface.get_width()
        self.display_height = self.display_surface.get_height()
        self.scale = min(self.display_width/BASE_WIDTH, self.display_height/BASE_HEIGTH)

        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.ennemy_sprites = pygame.sprite.Group()
        self.player_bullet_sprites = pygame.sprite.Group()
        self.ennemy_bullet_sprites = pygame.sprite.Group()

        self.last_time = time()
        self.spawner = Spawner(
            sprite_groups={
                "visible_sprites": self.visible_sprites,
                "ennemy_sprites": self.ennemy_sprites,
                "player_bullet_sprites": self.player_bullet_sprites,
                "ennemy_bullet_sprites": self.ennemy_bullet_sprites
            },
            action={
            "attack_event": self.attack_event,
            "spawn_entity": self.spawn_entity
            }
        )

        levels_path = path.join(self.basedir, "code", "levels", "levels.json")
        with open(levels_path)as json_levels:
            self.levels = load(json_levels)
        self.level = 2

        self.init_level()
        self.player = self.init_player()


    def spawn_entity(self, groups, name, alliance="enemy", data={}, pos=None):
        player = self.spawner.spawn_entity(
            groups=groups,
            scale=self.scale, 
            name=name,
            alliance=alliance, 
            data=data,
            pos=pos
        )
        self.layer_order()
        return player


    def attack_event(self, bullet):
        self.spawner.spawn_entity(
            groups= [self.visible_sprites,bullet["groups"]],
            scale=self.scale, 
            name=bullet['name'], 
            alliance=bullet['alliance'],
            data={
                'direction':bullet['direction'], 
                'speed':bullet['speed'], 
                'pos':bullet['pos'], 
                'impact_dommage':bullet['impact_dommage']
            }
        )


    def layer_order(self):
        for sprite in self.visible_sprites:
            self.visible_sprites.change_layer(sprite, sprite.order)


    def init_level(self):
        for _ in range(20):
            self.spawn_entity(groups=self.visible_sprites, name="small_star", alliance='environment')


    def init_player(self):
        return self.spawn_entity(groups=self.visible_sprites, name="player", alliance='player')


    def spawn_wave(self):
        if (len(self.ennemy_sprites) == 0):
            level_data = self.levels[str(self.level)]
            for enemy_type, value in level_data.items():
                for _ in range(value[0]):
                    self.spawn_entity(groups=[self.visible_sprites,self.ennemy_sprites], name=enemy_type, alliance=value[0])
            self.level +=1

            if self.level > len(self.levels):
                self.level = 1


    def collision(self):
        # player - ennemy collision
        sprite = pygame.sprite.spritecollide(self.player, self.ennemy_sprites, False, pygame.sprite.collide_mask)
        for s in sprite:
            self.player.current_health -= s.stats["impact_dommage"] 
            s.current_health -= self.player.stats["impact_dommage"]

        # player - ennemy attack collision
        sprite = pygame.sprite.spritecollide(self.player, self.ennemy_bullet_sprites, False, pygame.sprite.collide_mask)
        for bullet in sprite:
            self.player.current_health -= bullet.stats["impact_dommage"] 
            bullet.kill()

        # enemy - player attack collision
        for bullet in self.player_bullet_sprites:
            sprite = pygame.sprite.spritecollide(bullet, self.ennemy_sprites, False, pygame.sprite.collide_mask)
            for s in sprite:
                s.current_health -= bullet.stats["impact_dommage"]
                bullet.kill()

        # kill
        if self.player.current_health <=0:
            self.player.kill()
        for enemy in self.ennemy_sprites:
            if enemy.current_health <=0:
                enemy.destroy()


    def run(self):
        dt = time() - self.last_time
        self.last_time = time()
        
        self.visible_sprites.update(dt)
        self.visible_sprites.draw(self.display_surface)
        self.collision()
        self.spawn_wave()