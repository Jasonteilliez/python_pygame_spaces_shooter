import pygame
from random import randint, choice
from os import path
from json import load

from entities.Star import Star
from entities.Player import Player
from entities.Bullet import Bullet
from entities.Asteroid import Asteroid
from entities.Battleship import Battleship


class Spawner:
    def __init__(self, sprite_groups, action):
        self.basedir = path.dirname(path.dirname(path.dirname(__file__)))
        self.display_surface = pygame.display.get_surface()
        self.sprite_groups = sprite_groups
        self.action = action
        self.player = None

        self.entities_type = self.init_entities_type()
        self.spritesheet = self.init_spritesheet()
        self.sprite_data = self.init_sprite_data()
        self.stats_data = self.init_stats_data()

        self.order = {'environment': 0, 'enemy': 1, 'bullet': 2, 'player': 3}


    def init_spritesheet(self):
        path_to_spritesheet = path.join(self.basedir, "code", "sprites", "spritesheet.json")
        with open(path_to_spritesheet)as json_spritesheet:
            spritesheet_data = load(json_spritesheet)

        spritesheet = {}
        for key, value in spritesheet_data.items():
            spritesheet_path = path.join(self.basedir, "graphics", value['folder'], value['file'])
            spritesheet[key] = pygame.image.load(spritesheet_path).convert_alpha()
        
        return spritesheet


    def init_entities_type(self):
        return {
            "player": Player,
            "star": Star,
            "asteroid": Asteroid,
            "bullet": Bullet,
            "battleship": Battleship
        }


    def init_sprite_data(self):
        path_to_sprite = path.join(self.basedir, "code", "sprites", "sprites.json") 
        with open(path_to_sprite) as json_sprite:
            sprite_data = load(json_sprite) 
        return sprite_data
    

    def init_stats_data(self):
        path_to_stats = path.join(self.basedir, "code", "entities", "entities_info.json") 
        with open(path_to_stats) as json_stats:
            stats_data = load(json_stats) 
        return stats_data


    def spawn_entity(self, groups, scale, name, alliance, data = {}, pos = None):
        # Base #
        name = name
        spritesheet = self.sprite_data[name]['spritesheet']
        sprites_list = self.sprite_data[name]['sprites']
        sprites = self.get_basic_sprite(spritesheet, sprites_list)
        surf = choice(sprites)
        order = self.order[self.stats_data[name]['order']]
        entity_type = self.stats_data[name]['entity_type']
        entity = self.entities_type[entity_type]

        # Init #
        pos, data = self.options(entity_type, name, data, pos)

        # Return #
        if entity_type == "player":
            self.player = entity(
            groups=groups,
            scale=scale,
            surf=surf,
            order=order,
            alliance=alliance,
            pos=pos,
            data=data
        )
            return self.player
        return entity(
            groups=groups,
            scale=scale,
            surf=surf,
            order=order,
            alliance=alliance,
            pos=pos,
            data=data
        )


    def options(self, entity_type, name, data, pos):
        match entity_type:
            case "player":
                stats = self.stats_data[name]
                if not pos:
                    pos={
                        'x':self.display_surface.get_width()/2,
                        'y':self.display_surface.get_height()/2
                    }
                data['stats'] = stats['base_stats']
                data['bullet_sprites'] = self.sprite_groups['player_bullet_sprites']
                data['attack_event'] = self.action["attack_event"]
            case "star":
                if not pos:
                    pos={
                        'x':randint(0,self.display_surface.get_width()),
                        'y':randint(0,self.display_surface.get_height())
                    }
            case "bullet":
                if not pos:
                    pos = data['pos']
            case "asteroid":
                stats = self.stats_data[name]
                if not pos:
                    pos = self.get_random_outside_spawn_position()
                direction = pygame.math.Vector2(randint(-10,10),randint(-10,10))
                if direction.magnitude() != 0:
                    direction = direction.normalize()
                speed = randint(stats['mov_speed_min'],stats['mov_speed_max'])
                rotation_speed = choice([
                    randint(-stats['rotation_speed_max'],-stats['rotation_speed_min']),
                    randint(stats['rotation_speed_min'],stats['rotation_speed_max'])
                    ])
                data['direction'] = direction
                data['speed'] = speed
                data['rotation_speed'] = rotation_speed
                data['stats'] = stats['base_stats']
                data['spawn_entity'] = self.action['spawn_entity']
                data['division'] = stats['division']
                data['division_groups'] = [self.sprite_groups['visible_sprites'], self.sprite_groups["ennemy_sprites"]]
            case "battleship":
                stats = self.stats_data[name]
                if not pos:
                    pos = self.get_random_outside_spawn_position()
                data['stats'] = stats['base_stats']
                data['bullet_sprites'] = self.sprite_groups['ennemy_bullet_sprites']
                data['attack_event'] = self.action['attack_event']
                data['player'] = self.player
        return (pos, data)


    def get_basic_sprite(self, spritesheet, sprites_list):
        spritesheet = self.spritesheet[spritesheet]
        sprites = []
        for s in sprites_list:
            sprite = spritesheet.subsurface(pygame.Rect(s['x'],s['y'],s['width'],s['height']))
            sprites.append(sprite)
        return sprites
            

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