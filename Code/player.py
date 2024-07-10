import pygame 
from settings import *
from support import *
from entity import Entity

class Player(Entity):
	def __init__(self,position,groups,obstacle_sprites,interaction,toggle_forge,toggle_alchemy,toggle_quest,create_attack,destroy_attack,animation):
		super().__init__(groups)
		
		self.armour_name = 'simple_clothes'
		self.image = pygame.image.load(f'.\\Graphics\\Main_Character\\{self.armour_name}\\forward_idle\\forward_idle.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = position)
		self.hitbox = self.rect.inflate(-5, HITBOX_SIZE['player'])

		#graphics setup
		self.import_player_assets()
		self.status = 'forward'

		#movement
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.can_attack = True

		self.obstacle_sprites = obstacle_sprites
		self.interaction = interaction

		#weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.animation_arrow = animation
		self.weapon_list = weapons
		self.weapon_index = 0
		self.sword_index  = 0
		self.weapon = list(weapons.keys())[self.weapon_index]
		self.allowed_to_switch = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		#forge and alchemy
		self.toggle_forge = toggle_forge
		self.toggle_alchemy = toggle_alchemy
		self.toggle_quest = toggle_quest

		#stats
		self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 5, 'speed': 5, 'level': 1}
		self.max_stats = {'health': 200, 'energy': 100, 'attack': 20, 'magic': 15, 'speed': 8}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.exp_to_level_up = 100
		self.exp = 0
		self.speed = self.stats['speed']
		self.level = self.stats['level']
		self.coins = 100
		self.armour = armour
		self.current_armour = self.armour[self.armour_name]
		self.health_before_armour = self.stats['health']
		for piece in self.current_armour:
			self.stats['health'] += self.armour[self.armour_name][piece]['resistance']

		self.vulnerable = True
		self.hurt_time = None
		self.invulnerable_duration = 600
		
		self.shielded = False
		self.last_interaction_time = 0

	def import_player_assets(self):
		character_path = f'.\\Graphics\\Main_Character\\{self.armour_name}\\'
		self.animations = {'forward_walking': [], 'back_walking': [], 'left_walking': [], 'right_walking': [], 
		'right_idle': [], 'left_idle': [], 'forward_idle': [], 'back_idle': [], 
		'right_sword_attack': [], 'left_sword_attack': [], 'back_sword_attack': [], 'forward_sword_attack': [], 
		'back_bow_attack' : [], 'forward_bow_attack': [], 'right_bow_attack':[], 'left_bow_attack':[]
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
				self.create_attack()
				play_sound(SWORD_ATTACK_SOUND)

			if keys[pygame.K_n]:
				self.get_health(5)
			
			#switching weapons
			if keys[pygame.K_z] and self.allowed_to_switch:
				self.allowed_to_switch = False
				self.weapon_switch_time = pygame.time.get_ticks()
				if self.weapon_index != 1:
					self.weapon_index = 1
					self.animation_speed = 0.10
				else:
					self.weapon_index = self.sword_index
					self.animation_speed = 0.15
				play_sound(CHANGE_WEAPON)
				self.weapon = list(weapons.keys())[self.weapon_index]

			#interaction
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
		# sword attack status
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if self.weapon_index == 0:
				if not 'attack' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_sword_attack')
					elif 'walking' in self.status:
						self.status = self.status.replace('_walking', '_sword_attack')
					else:
						self.status = self.status + '_sword_attack'
			if self.weapon_index == 1:
				if not 'attack' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_bow_attack')
					elif 'walking' in self.status:
						self.status = self.status.replace('_walking', '_bow_attack')
					else:
						self.status = self.status + '_bow_attack'
		else:
			if 'attack' in self.status and self.weapon_index == 0:
				self.status = self.status.replace('_sword_attack', '_walking')
			elif 'attack' in self.status and self.weapon_index == 1:
				self.status = self.status.replace('_bow_attack', '_walking')


	def cooldown(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapons[self.weapon]['damage']:
				self.attacking = False
				self.destroy_attack()
		
		if not self.allowed_to_switch:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.allowed_to_switch = True

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerable_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		#flicker
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def bow_attack(self,groups):
		if 'forward' in self.status:
			self.animation_arrow.create_particles('arrow_forward',self.rect.center + pygame.math.Vector2(0,64),groups,'weapon')
		elif 'back' in self.status:
			self.animation_arrow.create_particles('arrow_back',self.rect.center + pygame.math.Vector2(0,-64),groups,'weapon')
		elif 'left' in self.status:
			self.animation_arrow.create_particles('arrow_left',self.rect.center + pygame.math.Vector2(-64,0),groups,'weapon')
		elif 'right' in self.status:
			self.animation_arrow.create_particles('arrow_right',self.rect.center + pygame.math.Vector2(64,0),groups,'weapon')
		
	def get_health(self,amount):
		if self.health < self.stats['health']:
			self.health += amount
		if self.health >= self.stats['health']:
			self.health = self.stats['health']

	def health_recovery(self):
		if self.health < self.stats['health']:
			self.health += 0.01
		else:
			self.health = self.stats['health']

	def check_death(self):
		if self.health <= 0:
			return True
		else:
			return False

	def check_level(self):
		return self.level 
	
	def check_for_level_up(self,exp):
		if exp >= self.exp_to_level_up:
			self.level +=1
			self.exp = exp - self.exp_to_level_up
			self.exp_to_level_up *= 1.05
			self.stats['health'] *= 1.02
			self.health_before_armour *= 1.02
			self.stats['energy'] *= 1.01
			self.stats['attack'] *= 1.005
			self.stats['speed'] += 1
			self.stats['magic'] *= 1.005

			if self.stats['health'] >= self.max_stats['health']:
				self.stats['health'] = self.max_stats['health']
			if self.stats['energy'] >= self.max_stats['energy']:
				self.stats['energy'] = self.max_stats['energy']
			if self.stats['attack'] >= self.max_stats['attack']:
				self.stats['attack'] = self.max_stats['attack']
			if self.stats['speed'] >= self.max_stats['speed']:
				self.stats['speed'] = self.max_stats['speed']
			if self.stats['magic'] >= self.max_stats['magic']:
				self.stats['magic'] = self.max_stats['magic']

	def get_weapon_damage(self):
		if self.can_attack:
			full_damage = self.stats['attack'] + weapons[self.weapon]['damage']
		else:
			full_damage = 0
		return full_damage
	
	def update_armour(self,name):
		self.current_armour = self.armour[name]
		for piece in self.current_armour:
			self.stats['health'] += self.armour[self.armour_name][piece]['resistance']
		self.import_player_assets()

	def update(self):
		self.check_death()
		self.check_for_level_up(self.exp)
		self.health_recovery()
		self.input()
		self.cooldown()
		self.get_status()
		self.animate()
		self.move(self.speed)

