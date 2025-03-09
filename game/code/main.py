import pygame, sys
from time import time
from settings import *
from player import Player
from star import Star
from bullet import Bullet
from enemy import Enemy
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        display_width = self.display_surface.get_width()
        display_height = self.display_surface.get_height()

        self.scale = min(display_width/GAME_WIDTH, display_height/GAME_HEIGTH)

        pygame.display.set_caption('Space Shooter')

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        for _ in range(20):
            Star(self.visible_sprites, self.scale)
        self.spawn_enemy_event()

        self.player = Player(self.visible_sprites, self.scale, self.attack_event)

        self.last_time = time()


    def attack_event(self, bullet):
        Bullet(
            groups=self.visible_sprites, 
            scale=self.scale, 
            pos=bullet['pos'], 
            direction=bullet['direction'], 
            entity=bullet['entity'], 
            bullet_type=bullet['bullet_type']
        )

    
    def spawn_enemy_event(self):
        Enemy(
            groups=self.visible_sprites, 
            scale=self.scale, 
            enemy_type="small_asteroid"
        )


    def run(self):

        while True:
            dt = time() - self.last_time
            self.last_time = time()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
            self.display_surface.fill('black')
            self.visible_sprites.update(dt = dt)
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()