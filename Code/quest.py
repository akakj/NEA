import pygame
from settings import *
from support import play_sound

class Quest:
    def __init__(self,player):
        self.player = player
        self.background = pygame.image.load(QUEST_BACKGROUND)
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, 15)
        self.quests = quests
        self.current_quest = None
        self.completed = []


    def add_quest(self):
        for quest_key, quest_value in quests.items():
            if self.current_quest == None and not self.quests[quest_key]['objective']['completed']:
                self.current_quest = quest_key
            elif self.quests[quest_key]['objective']['completed'] and quest_key not in self.completed:
                self.completed.append(quest_key)
                self.current_quest = None

    def set_completed(self):
        if self.current_quest == 'first_steps':
            if self.player.coins >= 5:
                self.quests[self.current_quest]['objective']['completed'] = True
                play_sound(QUEST_COMPLETED)
        elif self.current_quest == 'protection':
            if self.player.armour_name == 'leather_armour':
                self.quests[self.current_quest]['objective']['completed'] = True
                play_sound(QUEST_COMPLETED)

    def get_rewards(self):
        for reward_key, reward_value in quests['first_steps']['reward'].items():
            if reward_key == 'exp':
                self.player.exp += reward_value
            elif reward_key == 'coins':
                self.player.coins += reward_value
    
    def draw_avaliable_quests(self):
        headline = self.font.render('Current quest', True, QUEST_HEADLINE_COLOUR)
        headline_rect = headline.get_rect(topleft=(340, 250))
        self.display_surface.blit(headline, headline_rect)

        name = self.font.render(self.quests[self.current_quest]['name'], True, QUEST_FONT_COLOUR)
        name_rect = name.get_rect(topleft = (340,295))
        self.display_surface.blit(name, name_rect)

        lines = ["Objective:", self.quests[self.current_quest]['objective']['text'], self.quests[self.current_quest]['description'],
        "Reward:", f"{self.quests[self.current_quest]['reward']['exp']} exp, {self.quests[self.current_quest]['reward']['coins']} coins"]
        line_height = 40
        y = name_rect.bottom + 20

        for line in lines:
            text_surface = self.font.render(line, True, QUEST_FONT_COLOUR)
            text_rect = text_surface.get_rect(topleft=(340, y))
            self.display_surface.blit(text_surface, text_rect)
            y += line_height
        

    def draw_complete_quests(self):
        x_offset = 735
        y_offset = 250
        headline = self.font.render('Completed quests', True, QUEST_HEADLINE_COLOUR)
        headline_rect = headline.get_rect(topleft=(x_offset, y_offset))
        self.display_surface.blit(headline, headline_rect)

        for quest in self.completed:
            y_offset += 30
            name = self.font.render(self.quests[quest]['name'], True, QUEST_FONT_COLOUR)
            name_rect = name.get_rect(topleft = (x_offset,y_offset))
            self.display_surface.blit(name,name_rect)
    

    def display(self):
        self.display_surface.blit(self.background, (250,85))
        self.draw_avaliable_quests()
        self.draw_complete_quests()
        self.set_completed()