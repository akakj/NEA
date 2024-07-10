import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player
from magic import MagicPlayer
from support import *
from weapon import *
from ui import *
from enemy import Enemy
from particles import Animation
from coin import Coin
from inventory import *
from interaction import Interaction
from blacksmith import Blacksmith
from quest import Quest

class Level:
	def __init__(self):

		self.player_type = None

		self.display_surface = pygame.display.get_surface()
		self.inventory_display = False
		self.forge_display = False
		self.alchemy_display = False
		self.quest_display = False

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		#particles
		self.animation = Animation()

		# sprite setup
		self.create_map()

		self.ui = UI()
		
		self.coins = []


	def create_map(self):
		tmx_data = load_pygame('.\\Graphics\\map\\map.tmx')
		
		layouts = {
			'boundary': import_csv_layout('.\\Graphics\\map\\map_Floorblocks.csv'),
			'object': import_csv_layout('.\\Graphics\\map\\map_Objects.csv'),
			'entities' : import_csv_layout('.\\Graphics\\map\\map_Entities.csv')
			}
		graphics = {
			'objects': import_folder('.\\Graphics\\Obstacles')
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for column_index, column in enumerate(row):
					if column != '-1':
						x = column_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'floor_blocks')
						if style == 'object':
							surface = graphics['objects'][int(column)]
							Tile((x,y),[self.visible_sprites, self.obstacle_sprites],'object', surface)
						if style == 'entities':
							if column == '1':
								pass
							else:
								if column == '2' : name = 'mage'
								elif column == '3' :  name = 'skeleton_sword'
								elif column == '4' :  name = 'baldric'
								elif column == '7' : name = 'skeleton_magic'
								else: name = 'mage'
								Enemy(name, (x,y), [self.visible_sprites,self.attackable_sprites], 
								self.obstacle_sprites,self.damage_player,self.enemy_attack_particles,self.death_particles,self.coin_spawn,self.add_exp)

		
		for object in tmx_data.get_layer_by_name('Interact'):
			if object.name == 'Blacksmith':
				Interaction((object.x,object.y), (object.width,object.height), self.interaction_sprites, object.name)

	def set_player_type(self,player_type):
		self.player_type = player_type
		if self.player_type == "magic":
			self.player = MagicPlayer((2850,2400),[self.visible_sprites],self.obstacle_sprites,self.interaction_sprites,
			self.toggle_forge,self.toggle_alchemy,self.toggle_quest, self.create_magic_attack,self.destroy_attack,self.animation)
			
			self.ui.import_graphics(magic_spells)
		
		elif self.player_type == "sword":
			self.player = Player((2850,2400),[self.visible_sprites],self.obstacle_sprites,self.interaction_sprites,
			self.toggle_forge, self.toggle_alchemy, self.toggle_quest, self.create_attack,self.destroy_attack,self.animation)
			
			self.ui.import_graphics(weapons)

		self.inventory = Inventory(self.player)
		self.forge = Blacksmith(self.inventory)
		self.quest = Quest(self.player)


	def load_map(self):
		pass

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		self.quest.add_quest()
		
		if self.inventory_display and not self.forge_display and not self.alchemy_display and not self.quest_display:
			self.inventory.display()
		elif self.forge_display:
			self.visible_sprites.update()
			self.forge.display()
		elif self.alchemy_display:
			self.visible_sprites.update()
			self.alchemy.display()
		elif self.quest_display:
			self.quest.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack()
			self.coin_pickup()

	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.attack_sprites])
		if self.player.weapon_index == 1:
			self.player.bow_attack([self.visible_sprites,self.attackable_sprites])

	def create_magic_attack(self,style,strength,cost):
		if style == 'fireball':
			self.player.fireball(strength,cost,[self.visible_sprites,self.attack_sprites])
		elif style == 'heal':
			self.player.heal(strength,cost,self.visible_sprites)
		elif style == 'shield':
			self.player.shield(strength,cost,self.visible_sprites)
		elif style == 'icicle':
			self.player.icicle(strength,cost,[self.visible_sprites,self.attack_sprites])
		elif style == 'quake':
			self.player.quake(strength,cost,[self.visible_sprites,self.attack_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def player_attack(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'enemy':
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable and not self.player.shielded:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()

	def enemy_attack_particles(self,particle_type,position,sprite_type):
		self.animation.create_particles(particle_type,position,[self.visible_sprites,self.attackable_sprites],sprite_type)

	def death_particles(self,particle_type,position):
		self.animation.create_particles(particle_type,position,self.visible_sprites,'death')

	def toggle_inventory(self):
		play_sound(OPEN_INVENTORY_AUDIO)
		self.inventory_display = not self.inventory_display

	def toggle_forge(self):
		play_sound(SWORD_SOUND)
		self.forge_display = not self.forge_display

	def toggle_alchemy(self):
		self.alchemy_display = not self.alchemy_display

	def toggle_quest(self):
		self.quest_display = not self.quest_display

	def coin_spawn(self,position,amount):
		coin = Coin(position,self.visible_sprites,amount)
		self.coins.append(coin)

	def coin_pickup(self):
		if len(self.coins) == 0:
			pass
		else:
			for coin in self.coins:
				if coin.check_collide(self.player.rect):
					coin.kill()
					play_sound(COIN_PICKUP_AUDIO)
					self.coins.remove(coin)
					self.player.coins += coin.amount

	def add_exp(self,amount):
		self.player.exp += amount

	def add_item(self,item):
		self.inventory.add_item(item)


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load(".\\Graphics\\map\\map.png").convert()
		self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

	def custom_draw(self,player):
		#get offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
		
		#drawing the floor
		floor_offset_position = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_position)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_position = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_position)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for sprite in enemy_sprites:
			sprite.enemy_update(player)

