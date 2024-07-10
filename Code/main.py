from pygame import *
import pygame_gui
import pygame, sys
from settings import *
from level import Level
from button import *
import json
from support import *

import unittest

class Game:
	def __init__(self):

		#general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('NEA')
		self.clock = pygame.time.Clock()

		self.level = Level()

		self.gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

		self.music_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((400, 190), (450, 40)),start_value=50,value_range=(0, 100), manager = self.gui_manager)
		self.sound_effects = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((400, 350), (450, 40)),start_value=50,value_range=(0, 100), manager = self.gui_manager)

		self.music = None
		self.music_volume = 0.5
		

	def get_font(self, size):
		return pygame.font.Font(UI_FONT, size)
	
	def play_music(self,path):
		if self.music is not None:
			self.music.stop()
		self.music = pygame.mixer.Sound(path)
		self.music.set_volume(self.music_volume)
		self.music.play()
	
	def main_menu(self):
		background = pygame.image.load(MAIN_BACKGROUND)
		self.play_music(MENU_AUDIO)

		while True:
			self.screen.blit(background, (0,0))
			menu_mouse_pos = pygame.mouse.get_pos()

			menu_Text = self.get_font(45).render("NEO'S ENCHANTING ADVENTURES", True, "#b68f40")
			menu_Rect = menu_Text.get_rect(center =(640, 100))

			LOAD_BUTTON = Button(image = None, pos =(640, 225), 
		    text_input = "PLAY", font = self.get_font(52), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")
			NEW_GAME_BUTTON = Button(image = None, pos =(640, 350), 
		    text_input = "NEW GAME", font = self.get_font(52), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")
			OPTIONS_BUTTON = Button(image = None, pos =(640, 475), 
		    text_input = "OPTIONS", font = self.get_font(52), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")
			QUIT_BUTTON = Button(image = None, pos =(640, 600), 
		    text_input = "QUIT", font = self.get_font(52), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")

			self.screen.blit(menu_Text, menu_Rect)

			for button in [LOAD_BUTTON, NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
				button.changeColour(menu_mouse_pos)
				button.update(self.screen)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if LOAD_BUTTON.checkForInput(menu_mouse_pos):
						self.play_music(MENU_SELECT_AUDIO)
						self.load()
					if NEW_GAME_BUTTON.checkForInput(menu_mouse_pos):
						self.play_music(MENU_SELECT_AUDIO)
						self.choose_character()
					if OPTIONS_BUTTON.checkForInput(menu_mouse_pos):
						self.play_music(OPTIONS_AUDIO)
						self.options()
					if QUIT_BUTTON.checkForInput(menu_mouse_pos):
						pygame.quit()
						sys.exit()

			pygame.display.update()

		
	def run(self):
		self.play_music(GAMEPLAY_AUDIO)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						self.pause()
					if event.key == pygame.K_i:
						self.level.toggle_inventory()
					elif event.key == pygame.K_q:
						self.level.toggle_quest()

			self.screen.fill('pink')
			if self.level.player_type == None:
				self.choose_character()
			if self.level.player.check_death():
				self.death_screen()
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	def choose_character(self):
		background = pygame.image.load(MAIN_BACKGROUND)
		sword_icon = pygame.image.load(SWORD_ICON)
		magic_icon = pygame.image.load(MAGIC_ICON)

		while True:
			mouse_pos = pygame.mouse.get_pos()
			self.screen.blit(background, (0,0))

			choose_text = self.get_font(35).render('YOU MUST CHOOSE A CHARACTER FIRST', True, 'white')
			choose_text_rect = choose_text.get_rect(center = (640,175))
			self.screen.blit(choose_text, choose_text_rect)

			SWORD_BUTTON = Button(image = sword_icon, pos =(400, 375), 
		    text_input = "", font = self.get_font(50), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			MAGIC_BUTTON = Button(image = magic_icon, pos =(850, 375), 
		    text_input = "", font = self.get_font(50), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')

			for button in [SWORD_BUTTON, MAGIC_BUTTON]:
				button.drawRectAround(self.screen,mouse_pos)
				button.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if SWORD_BUTTON.checkForInput(mouse_pos):
						self.play_music(MENU_SELECT_AUDIO)
						self.level.set_player_type("sword")
						self.run()
					if MAGIC_BUTTON.checkForInput(mouse_pos):
						self.play_music(MENU_SELECT_AUDIO)
						self.level.set_player_type("magic")
						self.run()
			
			pygame.display.update()

	def save(self):
		self.play_music(MENU_SELECT_AUDIO)
		game_data = {
            'player': {
			    'type': self.level.player_type,
                'inventory': self.level.inventory.items,
		        'level': self.level.player.level,
		        'health': self.level.player.health,
				'energy': self.level.player.energy,
                'coins': self.level.player.coins,
                'exp': self.level.player.exp,
                'armour_name': self.level.player.armour_name,
			    'sword_index': self.level.player.sword_index,
            },
            'quest': {
                'current_quest': self.level.quest.current_quest,
                'completed': self.level.quest.completed,
            }
        }
		
		with open('save_file.json', 'w') as file:
			json.dump(game_data, file, cls=ItemEncoder)

	def load(self):
		with open('save_file.json', 'r') as file:
			game_data = json.load(file, cls=ItemDecoder)

		if 'type' in game_data['player']:
			self.level.player_type = game_data['player']['type']
			self.level.inventory.items = game_data['player']['inventory']
			self.level.player.level = game_data['player']['level']
			self.level.player.health = game_data['player']['health']
			self.level.player.energy = game_data['player']['energy']
			self.level.player.coins = game_data['player']['coins']
			self.level.player.exp = game_data['player']['exp']
			self.level.player.armour_name = game_data['player']['armour_name']
			self.level.player.sword_index = game_data['player']['sword_index']

			self.level.quest.current_quest = game_data['quest']['current_quest']
			self.level.quest.completed = game_data['quest']['completed']
		else:
			self.choose_character()


		self.run()


	def options(self):
		background = pygame.image.load(BACKGROUND_2)
		self.play_music(OPTIONS_AUDIO)
		clock = pygame.time.Clock()
	
		while True:
			time_delta = clock.tick(60) / 1000.0
			self.screen.blit(background, (0,0))
			options_mouse_pos = pygame.mouse.get_pos()

			music_text = self.get_font(45).render("Music Volume", True, MENU_TEXT_COLOUR)
			music_rect = music_text.get_rect(center=(640,140))
			self.screen.blit(music_text, music_rect)

			effects_text = self.get_font(45).render("Sound Effects Volume", True, MENU_TEXT_COLOUR)
			effects_rect = effects_text.get_rect(center=(640,290))
			self.screen.blit(effects_text, effects_rect)

			OPTIONS_BACK = Button(image = None, pos =(640,460), text_input = "BACK", font = self.get_font(50), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			OPTIONS_BACK.changeColour(options_mouse_pos)
			OPTIONS_BACK.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if OPTIONS_BACK.checkForInput(options_mouse_pos):
						return None
					
				self.gui_manager.process_events(event)

			self.gui_manager.update(time_delta)
			self.gui_manager.draw_ui(self.screen)
			self.music_volume = self.music_slider.get_current_value() / 100
			effects_volume = self.sound_effects.get_current_value() / 100
			pygame.display.update()


	def pause(self):
		background = pygame.image.load(BACKGROUND_2)
		self.play_music(OPTIONS_AUDIO)
	
		while True:
			self.screen.blit(background, (0,0))
			load_mouse_pos = pygame.mouse.get_pos()


			RESUME_BUTTON = Button(image = None, pos =(640, 120), 
		    text_input = "RESUME", font = self.get_font(35), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			SAVE_BUTTON = Button(image = None, pos =(640, 245), 
		    text_input = "SAVE", font = self.get_font(35), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			HELP_BUTTON = Button(image = None, pos =(640, 370), 
		    text_input = "HELP", font = self.get_font(35), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			OPTIONS_BUTTON = Button(image = None, pos =(640, 495), 
		    text_input = "OPTIONS", font = self.get_font(35), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			QUIT_BUTTON = Button(image = None, pos =(640, 620), 
		    text_input = "EXIT TO MAIN MENU", font = self.get_font(35), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')

			for button in [RESUME_BUTTON, SAVE_BUTTON,HELP_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
				button.changeColour(load_mouse_pos)
				button.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if RESUME_BUTTON.checkForInput(load_mouse_pos):
						self.play_music(GAMEPLAY_AUDIO)
						self.run()
					if SAVE_BUTTON.checkForInput(load_mouse_pos):
						self.save()
					if HELP_BUTTON.checkForInput(load_mouse_pos):
						self.help()
					if OPTIONS_BUTTON.checkForInput(load_mouse_pos):
						self.options()
					if QUIT_BUTTON.checkForInput(load_mouse_pos):
						self.play_music(MENU_AUDIO)
						self.main_menu()
				if event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						return None

			pygame.display.update()

	def help(self):
		background = pygame.image.load(BACKGROUND_2)
		while True:
			self.screen.blit(background, (0,0))
			mouse_pos = pygame.mouse.get_pos()

			key_bindings = ["ATTACK: E","SWITCH WEAPON: Z","INVENTORY: I", "QUESTS: Q", "BLACKMISMITH INTERACTION: ENTER"]
			y = 120

			for key in key_bindings:
				text = self.get_font(30).render(key, True, MENU_TEXT_COLOUR)
				rect = text.get_rect(center=(640, y))
				self.screen.blit(text, rect)
				y += 100
			
			BACK = Button(image = None, pos =(640,620), text_input = "BACK", font = self.get_font(50), base_colour = MENU_TEXT_COLOUR, hovering_colour = 'white')
			BACK.changeColour(mouse_pos)
			BACK.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if BACK.checkForInput(mouse_pos):
						return None

			pygame.display.update()

	def death_screen(self):
		self.play_music(DEATH_AUDIO)

		while True:
			self.screen.fill('black')
			mouse_pos = pygame.mouse.get_pos()

			dead_text = self.get_font(60).render("YOU DIED", True, "red")
			dead_rect = dead_text.get_rect(center=(640,220))
			self.screen.blit(dead_text,dead_rect)

			LOAD = Button(image = None, pos =(640,340), text_input = "LOAD RECENT SAVE FILE", font = self.get_font(30), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")
			BACK = Button(image = None, pos =(640,460), text_input = "QUIT TO MAIN MENU", font = self.get_font(30), base_colour = MENU_TEXT_COLOUR, hovering_colour = "white")

			for button in [LOAD, BACK]:
				button.changeColour(mouse_pos)
				button.update(self.screen)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if LOAD.checkForInput(mouse_pos):
						self.load()
					if BACK.checkForInput(mouse_pos):
						self.main_menu()
			
			pygame.display.update()
	
		

if __name__ == '__main__':
	game = Game()
	game.main_menu()