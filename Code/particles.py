import pygame
from support import import_folder

class Animation:
    def __init__(self):
        self.frames = {
            #spells
            'fireball_forward': import_folder('.\\Graphics\\Spells\\fireball\\forward'),
            'fireball_back': import_folder('.\\Graphics\\Spells\\fireball\\back'),
            'fireball_left': import_folder('.\\Graphics\\Spells\\fireball\left'),
            'fireball_right': import_folder('.\\Graphics\\Spells\\fireball\\right'),
            'heal':import_folder('.\\Graphics\\Spells\\heal'),
            'shield' : import_folder('.\\Graphics\\Spells\\shield'),
            'icicle_forward' : import_folder('.\\Graphics\\Spells\\icicle\\forward'),
            'icicle_back' : import_folder('.\\Graphics\\Spells\\icicle\\back'),
            'icicle_left' : import_folder('.\\Graphics\\Spells\\icicle\\left'),
            'icicle_right' : import_folder('.\\Graphics\\Spells\\icicle\\right'),
            'quake': import_folder('.\\Graphics\\Spells\\quake'),
            #arrow
            'arrow_forward': import_folder('.\\Graphics\\Particle_Effects\\arrow\\forward'),
            'arrow_back': import_folder('.\\Graphics\\Particle_Effects\\arrow\\back'),
            'arrow_left': import_folder('.\\Graphics\\Particle_Effects\\arrow\\left'),
            'arrow_right': import_folder('.\\Graphics\\Particle_Effects\\arrow\\right'),
            #other
            'death': import_folder('.\\Graphics\\Particle_Effects\\death'),
            #enemy spells
            'dark_bolt' : import_folder('.\\Graphics\\Particle_Effects\\dark_bolt'),
            'fire_bomb' : import_folder('.\\Graphics\\Particle_Effects\\fire_bomb'),
            'lightning' : import_folder('.\\Graphics\\Particle_Effects\\lightning')
        }

    def create_particles(self,animation_type,pos,groups,sprite_type):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups,sprite_type)
        

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups,sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        if sprite_type == 'death':
            self.animation_speed = 0.29
        elif 'fireball' in self.sprite_type:
            self.animation_speed = 0.18
        elif 'arrow' in self.sprite_type:
            self.animation_speed = 0.09
        else:
            self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()