import pygame, sys
from settings import *
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGTH))
        pygame.display.set_caption('Space Shooter')

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player(self.visible_sprites)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('gray')
            self.visible_sprites.update()
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()