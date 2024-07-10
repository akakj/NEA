import pygame
from player import Player
from support import *
from settings import *

class MagicPlayer(Player):
    def __init__(self,position,groups,obstacle_sprites,interaction,toggle_forge, toggle_inventory,toggle_quest,create_magic_attack,destroy_attack,animation):
        Player.__init__(self,position,groups,obstacle_sprites,interaction,toggle_forge, toggle_inventory,toggle_quest,create_magic_attack,destroy_attack,animation)
        
        self.animation_spells = animation
        self.create_magic_attack = create_magic_attack
        self.weapon_list = magic_spells
        self.weapon = list(magic_spells.keys())[self.weapon_index]

        self.shielded = False

    def import_player_assets(self):
        character_path = f'.\\Graphics\\Main_Character\\{self.armour_name}\\'
        self.animations = {
        'forward_walking': [], 'back_walking': [], 'left_walking': [], 'right_walking': [], 
		'right_idle': [], 'left_idle': [], 'forward_idle': [], 'back_idle': [], 
        'right_magic_attack': [],'left_magic_attack': [], 'back_magic_attack': [], 'forward_magic_attack': []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'back_walking'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'forward_walking'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right_walking'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left_walking'
            else:
                self.direction.x = 0

            #speed up
            if keys[pygame.K_LSHIFT]:
                if 'walking' in self.status:
                    self.speed = self.stats['speed'] + 2
            else:
                self.speed = self.stats['speed']

            #attack input
            if keys[pygame.K_e]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_spells.keys())[self.weapon_index]
                strength = list(magic_spells.values())[self.weapon_index]['strength']
                cost = list(magic_spells.values())[self.weapon_index]['cost']
                self.create_magic_attack(style,strength,cost)

            if keys[pygame.K_n]:
                self.get_health(5)

            #switch spells
            if keys[pygame.K_z] and self.allowed_to_switch:
                self.allowed_to_switch = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index >= len(list(magic_spells.keys())) - 1 :
                    self.weapon_index = 0
                else:
                    self.weapon_index += 1
                play_sound(CHANGE_WEAPON)
                self.weapon = list(magic_spells.keys())[self.weapon_index]

            #forge
            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Blacksmith':
                        if current_time - self.last_interaction_time > 300:
                            self.toggle_forge()
                            self.last_interaction_time = current_time

    def get_status(self):
		#idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'walking' in self.status:
                self.status = self.status.replace('_walking', '_idle')
            elif not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        #magic attack
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_magic_attack')
                elif 'walking' in self.status:
                    self.status = self.status.replace('_walking', '_magic_attack')
                else:
                    self.status = self.status + '_magic_attack'

        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_magic_attack', '_walking')

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + magic_spells[self.weapon]['strength']:
                self.attacking = False
                self.destroy_attack()

        if not self.allowed_to_switch:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.allowed_to_switch = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerable_duration:
                self.vulnerable = True

        if self.shielded:
            if not self.attacking:
                self.shielded = False


    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def full_magic_damage(self):
        return self.stats['attack'] + magic_spells[self.weapon]['strength']

    def fireball(self,strength,cost,groups):
        self.shielded = False
        if self.energy >= cost:
            self.energy -= cost
            if 'forward' in self.status:
                self.animation_spells.create_particles('fireball_forward',self.rect.center + pygame.math.Vector2(0,32),groups,'magic')
            elif 'back' in self.status:
                self.animation_spells.create_particles('fireball_back',self.rect.center + pygame.math.Vector2(0,-32),groups,'magic')
            elif 'left' in self.status:
                self.animation_spells.create_particles('fireball_left',self.rect.center + pygame.math.Vector2(-32,2),groups,'magic')
            elif 'right' in self.status:
                self.animation_spells.create_particles('fireball_right',self.rect.center + pygame.math.Vector2(32,2),groups,'magic')

            play_sound(self.weapon_list['fireball']['audio'])

    def heal(self,strength,cost,groups):
        self.shielded = False
        if self.energy >= cost:
            self.health += strength
            self.energy -= cost
            if self.health >= self.stats['health']:
                self.health = self.stats['health']
            self.animation_spells.create_particles('heal',self.rect.center + pygame.math.Vector2(0,-5),groups,'magic')
            
            play_sound(self.weapon_list['heal']['audio'])

    def shield(self,strength,cost,groups):
        if self.energy >= cost:
            self.energy -= cost
            self.shielded = True
            self.animation_spells.create_particles('shield',self.rect.center + pygame.math.Vector2(0,-5),groups,'magic')
            play_sound(self.weapon_list['shield']['audio'])
        else:
            self.shielded = False
    
    def icicle(self,strength,cost,groups):
        self.shielded = False
        if self.energy >= cost:
            self.energy -= cost
            if 'forward' in self.status:
                self.animation_spells.create_particles('icicle_forward',self.rect.center + pygame.math.Vector2(0,38),groups,'magic')
            elif 'back' in self.status:
                self.animation_spells.create_particles('icicle_back',self.rect.center + pygame.math.Vector2(0,-38),groups,'magic')
            elif 'left' in self.status:
                self.animation_spells.create_particles('icicle_left',self.rect.center + pygame.math.Vector2(-38,2),groups,'magic')
            elif 'right' in self.status:
                self.animation_spells.create_particles('icicle_right',self.rect.center + pygame.math.Vector2(38,2),groups,'magic')
            
            play_sound(self.weapon_list['icicle']['audio'])

    def quake(self,strength,cost,groups):
        self.shielded = False
        if self.energy >= cost:
            self.energy -= cost
            if 'forward' in self.status:
                self.animation_spells.create_particles('quake',self.rect.center + pygame.math.Vector2(0,80),groups,'magic')
            elif 'back' in self.status:
                self.animation_spells.create_particles('quake',self.rect.center + pygame.math.Vector2(0,-72),groups,'magic')
            elif 'left' in self.status:
                self.animation_spells.create_particles('quake',self.rect.center + pygame.math.Vector2(-95,0),groups,'magic')
            elif 'right' in self.status:
                self.animation_spells.create_particles('quake',self.rect.center + pygame.math.Vector2(95,0),groups,'magic')

            play_sound(self.weapon_list['quake']['audio'])

    def get_damage(self, amount):
        if not self.shielded:
            if self.health > 0:
                self.health -= amount
            if self.health <= 0:
                self.health = 0

    def update(self):
        self.check_death()
        self.check_for_level_up(self.exp)
        self.health_recovery()
        self.energy_recovery()
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)

