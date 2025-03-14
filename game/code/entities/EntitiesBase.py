import pygame


class EntitiesBase(pygame.sprite.Sprite):
    def __init__(self, groups, scale, surf, pos, alliance, order):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()
        self.scale = scale
        self.surf = surf
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale)
        self.image = self.scale_surf
        self.rect = self.image.get_frect(center = (pos['x'], pos['y']))

        self.mask = pygame.mask.from_surface(self.image)

        self.alliance = alliance
        self.order = order

    
        def update(self, dt):
            pass