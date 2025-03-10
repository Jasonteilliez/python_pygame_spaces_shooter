import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, scale, surf, pos, alliance, direction, speed, dommage):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()
        self.scale = scale
        self.surf = surf
        self.scale_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale)
        self.image = self.surf
        self.rect = self.image.get_frect(center = (pos['x'], pos['y']))

        self.direction = direction
        self.speed = speed

        self.team = alliance
        self.dommage = dommage


    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * self.scale
        self.rect.centery += self.direction.y * self.speed * dt * self.scale


    def bullet_kill(self):
        if self.rect.bottom <= 0 or self.rect.top >= self.display_surface.get_height() or \
        self.rect.left <= 0 or self.rect.right >= self.display_surface.get_width():
            self.kill()


    def update(self, dt):
        self.move(dt)
        self.bullet_kill()