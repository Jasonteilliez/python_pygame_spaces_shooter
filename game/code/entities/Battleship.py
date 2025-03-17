import pygame
from math import degrees, atan2, dist
from time import time
from random import randint
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
        self.player = data['player']

        self.stats = {
            "max_health": data['stats']['max_health'],
            "attack_dommage": data['stats']['attack_dommage'],
            "attack_speed": data['stats']['attack_speed'],
            "impact_dommage": data['stats']['impact_dommage'],
            "mov_speed": data['stats']['mov_speed']
        }
        self.current_health = self.stats['max_health']

        self.state = "patrol"

        self.is_patroling = False
        self.patrol_time = 10
        self.patroling_time = None

        self.engaging_direction = randint(0,1)


    def distance_with_player(self):
        
        distance = dist(self.rect.center, self.player.rect.center)/self.scale
        if distance < 200: self.state = "step_back"
        elif distance < 300: self.state = "circle"
        elif distance < 400: self.state = "follow"
        else : self.state = "patrol"


    def patrol(self):
        if self.is_patroling:
            current_time = time()
            if current_time - self.patroling_time >= self.patrol_time:
                self.is_patroling = False
                self.direction = pygame.math.Vector2(0,0)

        else:
            self.is_patroling = True
            self.patroling_time = time()

            self.direction = pygame.math.Vector2(randint(-10,10),randint(-10,10))
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()


    def follow(self):
        self.is_patroling = False

        self.direction.x = self.player.rect.centerx - self.rect.centerx
        self.direction.y = self.player.rect.centery - self.rect.centery
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


    def circle(self):

        if self.engaging_direction:
            self.direction.x = -(self.player.rect.centery - self.rect.centery)
            self.direction.y = self.player.rect.centerx - self.rect.centerx
        else:
            self.direction.x = self.player.rect.centery - self.rect.centery
            self.direction.y = -(self.player.rect.centerx - self.rect.centerx)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


    def step_back(self):
        self.direction.x = -(self.player.rect.centerx - self.rect.centerx)
        self.direction.y = -(self.player.rect.centery - self.rect.centery)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


    def move(self,dt):
        self.rect.centerx += self.direction.x * self.stats["mov_speed"] * dt * self.scale
        if self.rect.right < -100:
            self.rect.x = self.display_surface.get_width() - self.rect.width + 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)
        elif self.rect.left > self.display_surface.get_width()+100:
            self.rect.x = - 100
            self.rect.y = randint(-50, self.display_surface.get_height()+50)

        self.rect.centery += self.direction.y * self.stats["mov_speed"] * dt * self.scale
        if self.rect.bottom < -100:
            self.rect.y = self.display_surface.get_height() - self.rect.height + 100
            self.rect.x = randint(-50, self.display_surface.get_width()+50)
        elif self.rect.top > self.display_surface.get_height() + 100:
            self.rect.y = - 100
            self.rect.x = randint(-50, self.display_surface.get_width()+50)


    def rotate(self):
        dx = self.direction.x
        dy = self.direction.y
        if self.state != "patrol":
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery

        angle= - degrees(atan2(dx,-dy))
        self.image = pygame.transform.rotate(self.scale_surf, angle)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image) 


    def attack(self):
        direction = pygame.math.Vector2()
        direction.x = self.player.rect.centerx - self.rect.centerx
        direction.y = self.player.rect.centery - self.rect.centery
        if direction.magnitude() != 0:
            direction = direction.normalize()

        pos = {
         'x': self.rect.centerx + 15*direction.x*self.scale,
         'y': self.rect.centery + 15*direction.y*self.scale
        }

        bullet={
            'groups': self.bullet_sprites,
            'pos': pos, 
            'direction': direction, 
            'alliance': 'ennemy_bullet', 
            'name': 'small_blue_bullet',
            'speed': 300,
            'impact_dommage':self.stats['attack_dommage']
        }
        self.attack_event(bullet)


    def cooldowns(self):
        current_time = time()

        if self.is_attacking:
            if current_time - self.attack_time >= self.stats['attack_speed']:
                self.is_attacking = False

    
    def action(self):
        if self.state == "patrol" : 
            self.patrol()
        if self.state == "follow":
            self.follow()
        if self.state == "circle":
            self.circle()
        if self.state == "step_back":
            self.step_back()
        
        if self.state != "patrol" and self.is_attacking == False:
            self.is_attacking = True
            self.attack_time = time()
            self.attack() 



    def update(self, dt):
        self.distance_with_player()
        self.action()
        self.cooldowns()
        self.move(dt)
        self.rotate()

