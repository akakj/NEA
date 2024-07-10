import pygame 

class HealthBar(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.Surface((20,5))
        self.rect = self.image.get_rect()
        self.image.fill('#544c4c')


    def display_healthbar(self,pos,max_health,current_health):
        ratio = current_health // max_health
        current_width = 20 * ratio
        current_health_rect = pygame.Rect(pos.x,pos.y,current_width,5)
        