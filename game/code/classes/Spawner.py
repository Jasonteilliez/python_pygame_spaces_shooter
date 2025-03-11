import pygame
from random import randint, choice
from os import path
from json import load

from entities.Star import Star
from entities.Player import Player
from entities.Bullet import Bullet
from entities.Asteroid import Asteroid


class Spawner:
    def __init__(self):
        self.basedir = path.dirname(path.dirname(path.dirname(__file__)))
        self.display_surface = pygame.display.get_surface()

        self.path_to_sprite = path.join(self.basedir, "code", "sprites", "sprites.json")
        with open(self.path_to_sprite) as json_sprites:
            self.sprite_data = load(json_sprites)

        self.path_to_stats = path.join(self.basedir, "code", "entities", "stats.json") 
        with open(self.path_to_stats) as json_stats:
            self.stats_data = load(json_stats) 

        self.player_spritesheet_path = path.join(self.basedir, "graphics", "player", "player.png")
        self.star_spritesheet_path = path.join(self.basedir, "graphics", "environment", "star.png")
        self.bullet_spritesheet_path = path.join(self.basedir, "graphics", "bullet", "bullet.png")
        self.asteroid_spritesheet_path = path.join(self.basedir, "graphics", "enemy", "asteroid.png")

        self.player_spritesheet = pygame.image.load(self.player_spritesheet_path).convert_alpha()
        self.star_spritesheet = pygame.image.load(self.star_spritesheet_path).convert_alpha()
        self.bullet_spritesheet = pygame.image.load(self.bullet_spritesheet_path).convert_alpha()
        self.asteroid_spritesheet = pygame.image.load(self.asteroid_spritesheet_path).convert_alpha()


    def spawn_player(self, groups, scale, attack_event):
        name = "player"
        spritesheet = self.sprite_data[name]['spritesheet']
        sprites_list = self.sprite_data[name]['sprites']
        sprites = self.get_basic_sprite(spritesheet, sprites_list)

        pos={
            'x':self.display_surface.get_width()/2,
            'y':self.display_surface.get_height()/2
        }
        return Player(
            groups=groups,
            scale=scale,
            surf=choice(sprites),
            pos=pos,
            attack_event=attack_event
        )


    def spawn_small_star(self, groups,scale):
        name = "small_star"
        spritesheet = self.sprite_data[name]['spritesheet']
        sprites_list = self.sprite_data[name]['sprites']
        sprites = self.get_basic_sprite(spritesheet, sprites_list)

        pos={
            'x':randint(0,self.display_surface.get_width()),
            'y':randint(0,self.display_surface.get_height())
        }

        return Star(
            groups=groups,
            scale=scale,
            surf=choice(sprites),
            pos=pos,
        )


    def spawn_bullet(self, groups, scale, alliance, name, direction, speed, pos, dommage):
        name = name
        spritesheet = self.sprite_data[name]['spritesheet']
        sprites_list = self.sprite_data[name]['sprites']
        sprites = self.get_basic_sprite(spritesheet, sprites_list)

        return Bullet(
            groups=groups,
            scale=scale,
            surf=choice(sprites),
            pos=pos,
            direction=direction,
            speed=speed,
            dommage=dommage,
            alliance=alliance
        )


    def spawn_asteroid(self, groups, scale, alliance, name):
        name = name
        spritesheet = self.sprite_data[name]['spritesheet']
        sprites_list = self.sprite_data[name]['sprites']
        sprites = self.get_basic_sprite(spritesheet, sprites_list)

        pos = self.get_random_outside_spawn_position()
        direction = pygame.math.Vector2(randint(-10,10),randint(-10,10))
        direction = direction.normalize()
        speed = randint(50,300)
        rotation_speed = choice([randint(-300,-50),randint(50,300)])

        return Asteroid(
            groups = groups,
            scale = scale,
            surf = choice(sprites),
            pos = pos,
            direction = direction,
            speed = speed,
            rotation_speed = rotation_speed,
            alliance = alliance
        )


    def get_basic_sprite(self, spritesheet, sprites_list):
        spritesheet = self.get_spritesheet(spritesheet)
        sprites = []
        for s in sprites_list:
            sprite = spritesheet.subsurface(pygame.Rect(s['x'],s['y'],s['width'],s['height']))
            sprites.append(sprite)
        return sprites


    def get_spritesheet(self, spritesheet):
        match spritesheet:
            case 'star_spritesheet':
                return self.star_spritesheet
            case 'player_spritesheet':
                return self.player_spritesheet
            case 'bullet_spritesheet':
                return self.bullet_spritesheet
            case 'asteroid_spritesheet':
                return self.asteroid_spritesheet
            case _:
                print(f"Spritesheet {spritesheet} not found")
            

    def get_random_outside_spawn_position(self):
        pos = {
            'x': 0,
            'y': 0
        }
        side = choice(['left','right','top','bottom'])
        match side:
            case 'left':
                pos = {
                    'x': -50,
                    'y': randint(-50, self.display_surface.get_height()+50)          
                }
            case 'right':
                pos = {
                    'x': self.display_surface.get_width()+50,
                    'y': randint(-50, self.display_surface.get_height()+50)         
                }
            case 'top':
                pos = {
                    'x': randint(-50, self.display_surface.get_width()+50) ,
                    'y': -50        
                }
            case 'bottom':
                pos = {
                    'x': randint(-50, self.display_surface.get_width()+50) ,
                    'y': self.display_surface.get_height()+50          
                }
        return pos