import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)

        self.sprite_type = 'weapon'
        #player direction
        direction = player.status.split('_')[0]

        #graphics
        full_path = f'.\\Graphics\\Weapons\\{player.weapon}\\{direction}.png'
        self.image = pygame.Surface((20,20))

        #placement
        if direction == 'forward':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-10))
        elif direction == 'back':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,10))
        elif direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft)

