import pygame, sys
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGTH))
        pygame.display.set_caption('Space Shooter')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('black')
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()