import pygame
from settings import *
from entity import Entity
from support import *
import random

class Enemy(Entity):
    
    def __init__(self,name,position,groups,obstacle_sprites,damage_player,attack_particles,death_particles,coin_spawn,add_exp):
        
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics setup
        self.import_graphics(name)
        self.status = 'forward_idle'
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.start_position = position
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.name = name
        enemy_info = enemies[self.name]
        self.health = enemy_info['health']
        self.max_health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.coins = enemy_info['coins']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']
        self.attack_sound = enemy_info['attack_sound']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = enemy_info['cooldown']
        self.damage_player = damage_player
        self.attack_particles = attack_particles
        self.death_particles = death_particles
        self.coin_spawn = coin_spawn
        self.add_exp = add_exp

        self.vulnerable = True
        self.hit_time = None
        self.invulnerable_duration = 400

        self.moving = False
        self.last_position = position
        
        #magic enemy
        self.spells = ['dark_bolt','fire_bomb','lightning']
        
        self.graph = self.create_graph()
        self.movement_speed = 1.5
        self.movement_radius = 100
        self.target_position = pygame.math.Vector2(random.randint(-50, 50), random.randint(-50, 50)) + self.hitbox.center

    def create_graph(self):
        graph = {}
        for sprite in self.obstacle_sprites:
            if sprite.sprite_type == 'object':
                node = (sprite.rect.center[0], sprite.rect.center[1])
                graph[node] = []
                for neighbor in self.get_neighbors(sprite):
                    if neighbor.sprite_type == 'object':
                        neighbor_node = (neighbor.rect.center[0], neighbor.rect.center[1])
                        distance = ((node[0] - neighbor_node[0])**2 + (node[1] - neighbor_node[1])**2)**0.5
                        graph[node].append((neighbor_node, distance))
        return graph

    def get_neighbors(self, sprite):
        neighbours = []
        for obstacle in self.obstacle_sprites:
            if sprite != obstacle:
                if sprite.rect.colliderect(obstacle.rect):
                    neighbours.append(obstacle)
        return neighbours

    def idle(self):
        distance_to_target = self.target_position - self.hitbox.center
        if distance_to_target.magnitude() < 5:
            x = random.uniform(-self.movement_radius, self.movement_radius)
            y = random.uniform(-self.movement_radius, self.movement_radius)
            self.target_position = self.hitbox.center + pygame.math.Vector2(x, y)
        
        self.direction = (self.target_position - self.hitbox.center).normalize()
        self.move(self.movement_speed)

    def import_graphics(self,name):
        self.animations = {'forward_idle': [], 'left_idle': [], 'right_idle': [],'back_idle': [],
        'forward_walking': [], 'left_walking': [], 'right_walking': [], 'back_walking': [],
        'forward_attack' : [], 'left_attack': [], 'right_attack': [], 'back_attack': [] }
        main_path = f'.\\Graphics\\Enemies\\{name}\\'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_direction_distance_player(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        
        return(distance,direction)
    
    def get_status(self,player):
        distance = self.get_direction_distance_player(player)[0]
        direction = self.get_direction_distance_player(player)[1]

        if distance <= self.attack_radius and self.can_attack:
            if not 'attack' in self.status:
                self.frame_index = 0
            if round(direction.y) == -1:
                self.status = 'back_attack'
            elif round(direction.y) == 1:
                self.status = 'forward_attack'
            elif round(direction.x) == -1:
                self.status = 'left_attack'
            elif round(direction.x) == 1:
                self.status = 'right_attack'

        elif distance <= self.attack_radius and not self.can_attack:
            if round(direction.y) == -1:
                self.status = 'back_idle'
            elif round(direction.y) == 1:
                self.status = 'forward_idle'
            elif round(direction.x) == -1:
                self.status = 'left_idle'
            elif round(direction.x) == 1:
                self.status = 'right_idle'

        elif distance <= self.notice_radius:
            if round(direction.y) == -1:
                self.status = 'back_walking'
            elif round(direction.y) == 1:
                self.status = 'forward_walking'
            elif round(direction.x) == -1:
                self.status = 'left_walking'
            elif round(direction.x) == 1:
                self.status = 'right_walking'

        elif distance <= 1300 and distance > self.notice_radius:
            self.idle()

        else:
            if 'walking' in self.status:
                self.status  = self.status.replace('_walking', '_idle')
            elif 'attack' in self.status:
                self.status = self.status.replace('_attack','_idle')


    def action(self,player):
        if 'attack' in self.status and self.health > 0:
            self.attack_time = pygame.time.get_ticks()
            if self.attack_type == 'magic':
                self.magic_attack(player)
            else:
                self.damage_player(self.attack_damage,self.attack_type)
            play_sound(self.attack_sound)
        elif 'walking' in self.status and self.health > 0:
            self.direction = self.get_direction_distance_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def magic_attack(self,player):
        if not self.check_movement() and self.can_attack:
            spell = self.spells[random.randint(0,2)]

            if spell == 'dark_bolt':
                self.attack_particles(spell, player.rect.center + pygame.math.Vector2(0,-20), 'magic')
            elif spell == 'fire_bomb':
                self.attack_particles(spell, player.rect.center, 'magic')
            else:
                self.attack_particles(spell, player.rect.center + pygame.math.Vector2(0,-50), 'magic')

            self.can_attack = False

            self.damage_player(self.attack_damage,self.attack_type)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'death' in self.status:
                self.kill()
            elif 'attack' in self.status:
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
   
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time -self.hit_time >= self.invulnerable_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.direction = self.get_direction_distance_player(player)[1]
            if attack_type == 'weapon' or attack_type == 'bow':
                self.health -= player.get_weapon_damage()
            elif attack_type == 'magic':
                self.health -= player.full_magic_damage()
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def check_death(self,player):
        if self.health <= 0:
            self.kill()
            self.add_exp(self.exp)
            self.death_particles('death',self.rect.center)
            self.coin_spawn(self.rect.center,self.coins)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def check_movement(self):
        if self.rect.topleft == self.last_position:
            self.last_position = self.rect.topleft
            return False
        else:
            self.last_position = self.rect.topleft
            return True

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.check_death(player)
        self.get_status(player)
        self.action(player)

      