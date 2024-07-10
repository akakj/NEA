import pygame
from gui import GUI
from inventory import Inventory
from item import Item
from settings import *

class Alchemist(GUI):
    def __init__(self,inventory):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.capacity = 25
        self.items = []
        self.item_slots = [None] * self.capacity

        for item_type, items in item_attributes.items():
            for name, attributes in items.items():
                item = Item(name, item_type)
                if item_type == 'potion':
                    self.items.append(item)
       
        self.player_inventory = inventory

        self.slot_size = 100
        self.inventory_slot_image = pygame.image.load(SLOT_IMAGE)
        self.inventory_slot_image = pygame.transform.scale(self.inventory_slot_image, (self.slot_size, self.slot_size))
        self.slot_spacing = 5
        self.main_font = pygame.font.Font(UI_FONT,25)
        self.description_font = pygame.font.Font(UI_FONT, 15) 

    def draw_selling_items(self):
        items_surface = self.main_font.render('Shop', True, DESC_FONT_COLOUR)
        items_rect = items_surface.get_rect(topleft = (950,60))
        self.display_surface.blit(items_surface,items_rect)

        x = 800
        y = 120
        for i in range (len(self.items)):
            if self.items[i] is not None:
                item_graphic = pygame.image.load(self.items[i].graphic)
                item_graphic = pygame.transform.scale(item_graphic, (self.slot_size, self.slot_size))
                self.item_slots[i] = item_graphic
                slot_rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
                self.display_surface.blit(item_graphic, (x, y))

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if slot_rect.collidepoint(mouse_x, mouse_y):
                    name_text = self.description_font.render(self.items[i].name, True, 'white')
                    description_text = self.description_font.render(self.items[i].description, True, 'white')
                    name_rect = name_text.get_rect(center=(self.display_surface.get_width() // 2, y + self.slot_size + 10))
                    description_rect = description_text.get_rect(center=(self.display_surface.get_width() // 2, y + self.slot_size + 30))
                    pygame.draw.rect(self.display_surface, 'black', (name_rect.x - 5, name_rect.y - 5, name_rect.width + 10, name_rect.height + description_rect.height + 20))
                    self.display_surface.blit(name_text, name_rect)
                    self.display_surface.blit(description_text, description_rect)
                
                x += self.slot_size + self.slot_spacing
                
                if x > 1210:
                    x = 800
                    y += self.slot_size + self.slot_spacing

    def draw_player_inventory(self):
        pass

    def buy_item(self):
        pass

    def sell_item(self):
        pass

    def display(self):
        self.display_surface.fill('green')
        self.draw_selling_items()