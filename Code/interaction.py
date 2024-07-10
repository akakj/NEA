import pygame

class Interaction(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, name):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.name = name