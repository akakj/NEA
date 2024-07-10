import pygame
from support import *
class Coin(pygame.sprite.Sprite):
    def __init__(self,position,groups,amount):
        super().__init__(groups)
        self.frames = import_folder('.\\Graphics\\Particle_Effects\\coin')
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)
        self.amount = amount



    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def check_collide(self,player_rect):
        if player_rect.colliderect(self.rect):
            return True
        else:
            return False

    def update(self):
        self.animate()