import pygame
from settings import *
from support import play_sound

class UI:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.exp_bar_rect = pygame.Rect(96,20,BAR_WIDTH,BAR_HEIGHT)
        self.health_bar_rect = pygame.Rect(96,40,BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(96,60,BAR_WIDTH,BAR_HEIGHT)
        
        self.weapon_graphics = []

            
    def import_graphics(self,type):
        for graphic in type.values():
            path = graphic['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def get_font(self, size):
        return pygame.font.Font(UI_FONT, size)

    def display_stats_image(self):
        image = pygame.image.load(STATS_IMAGE)
        image_rect = image.get_rect(topleft = (20,15))

        self.display_surface.blit(image,image_rect)

    def display_bar(self,current,max_amount,bg_rect,color):
        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,bg_rect)

        #stat to pixel
        ratio = current/ max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface,color,current_rect)

    def display_level(self,level):
        text_surface = self.font.render(str(level), False, TEXT_COLOUR)
        text_rect = text_surface.get_rect(center =(57,48))

        self.display_surface.blit(text_surface,text_rect)

    def display_coins(self,amount):
        icon = pygame.image.load(COIN_ICON)
        icon_rect = icon.get_rect(topright = (1250,25))
        text_surface = self.font.render(str(amount),False, TEXT_COLOUR)
        text_rect = text_surface.get_rect(topright = (1210,35))

        self.display_surface.blit(icon,icon_rect)
        self.display_surface.blit(text_surface,text_rect)

    def selection_box(self,left,top,box_size,switched):
        bg_rect = pygame.Rect(left,top,box_size,box_size)
        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,bg_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,bg_rect,2)
        if switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR_ACTIVE,bg_rect,2)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,bg_rect,2)
        return bg_rect

    def weapon_overlay(self,weapon_index,switched):
        bg_rect = self.selection_box(20,630,80,switched)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surface,weapon_rect)

    def display(self, player):
        self.display_stats_image()
        self.display_bar(player.exp, player.exp_to_level_up,self.exp_bar_rect, EXP_COLOUR)
        self.display_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOUR)
        self.display_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOUR)

        self.display_level(player.level)
        self.weapon_overlay(player.weapon_index,player.allowed_to_switch)
        self.display_coins(player.coins)
        