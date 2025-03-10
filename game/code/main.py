import pygame, sys
from settings import *
from classes.Level import Level



class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption('Space Shooter')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.display_surface.fill('black')
            self.level.run()
            pygame.display.update() 
            self.clock.tick(FPS)  


if __name__ == "__main__":
    game = Game()
    game.run()