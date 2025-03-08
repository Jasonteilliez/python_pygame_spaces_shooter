import pygame, sys
from time import time
from settings import *
from player import Player

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

        self.player = Player(self.visible_sprites, self.scale)
        self.last_time = time()

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
                
            self.display_surface.fill('gray')
            self.visible_sprites.update(dt = dt)
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()