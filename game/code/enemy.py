import pygame
from os import path
from random import choice, randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, scale, enemy_type):
        super().__init__(groups)
        self.scale = scale
        self.enemy_type = enemy_type
        self.display_surface = pygame.display.get_surface()

        pos = self.init_position()
        self.direction = self.init_direction()
        self.rotation_speed = self.init_rotation()
        self.angle = 0
                        
        basedir = path.dirname(path.dirname(__file__))
        path_to_image = path.join(basedir, "graphics", "enemy", f"{self.enemy_type}.png")

        surf = pygame.image.load(path_to_image).convert_alpha()
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * self.scale)
        self.image = self.scale_surf
        self.rect = self.image.get_frect(center = (pos['x'],pos['y']))

        self.stats = {
            'max_health': 2,
            'dommage': 1,
            'mov_speed': randint(50,300)
        }


    def init_position(self):
        pos = {
            'x': 0,
            'y': 0
        }
        side = choice(['left','right','top','bottom'])
        if side == 'left':
            pos = {
                'x': -50,
                'y': randint(-50, self.display_surface.get_height()+50)          
            }
        if side == 'right':
            pos = {
                'x': self.display_surface.get_width()+50,
                'y': randint(-50, self.display_surface.get_height()+50)          
            }
        if side == 'top':
            pos = {
                'x': randint(-50, self.display_surface.get_width()+50) ,
                'y': -50          
            }
        if side == 'bottom':
            pos = {
                'x': randint(-50, self.display_surface.get_width()+50) ,
                'y': self.display_surface.get_height()+50          
            }
        return pos

    def init_direction(self):
        direction = pygame.math.Vector2(randint(-10,10), randint(-10,10))
        return direction.normalize()
    

    def init_rotation(self):
        return choice([randint(-300,-50),randint(50,300)])
    

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.stats['mov_speed'] * dt * self.scale
        if self.rect.left < -100:
            self.rect.x = -100
            self.direction.x = - self.direction.x
        elif self.rect.right > self.display_surface.get_width()+100:
            self.rect.x = self.display_surface.get_width() - self.rect.width + 100
            self.direction.x = - self.direction.x

        self.rect.centery += self.direction.y * self.stats['mov_speed'] * dt * self.scale
        if self.rect.top < -100:
            self.rect.y = -100
            self.direction.y = - self.direction.y
        elif self.rect.bottom > self.display_surface.get_height() + 100:
            self.rect.y = self.display_surface.get_height() - self.rect.height + 100
            self.direction.y = - self.direction.y


    def rotate(self, dt):
        self.angle += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scale_surf, self.angle)
        self.rect = self.image.get_frect(center=self.rect.center) 


    def update(self, dt):
        self.move(dt)
        self.rotate(dt)

    
