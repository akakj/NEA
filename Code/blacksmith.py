import pygame
from gui import GUI
from inventory import Inventory
from item import Item
from settings import *
from support import play_sound

class Blacksmith(GUI):
    def __init__(self, inventory):
        super().__init__()
        self.background = pygame.image.load(BLACKSMITH_BG)
        self.display_surface = pygame.display.get_surface()
        self.capacity = 36
        self.items = []
        self.item_slots = [None] * self.capacity
        self.player_inventory = inventory
        self.start_x = 780
        self.start_y = 120

        for item_type, items in item_attributes.items():
            for name, attributes in items.items():
                item = Item(name, item_type)
                if not (name == 'simple_clothes' or name == 'base_sword'):
                    if item not in self.player_inventory.items:
                        self.items.append(item)
        
    def remove_item(self, item_index):
        self.items[item_index].cost = round(self.items[item_index].cost * 0.85)
        self.items[item_index] = None
        self.item_slots[item_index] = None

    def draw_player_inventory(self):
        self.player_inventory.draw_slots_and_items(True, True, self)
        self.player_inventory.draw_coins()

    def sell_item(self, item_index):
       item = self.items[item_index]
       if self.player_inventory.player.coins >= item.cost:
            self.player_inventory.add_item(item)
            self.player_inventory.player.coins -= item.cost
            self.remove_item(item_index)
            self.last_click = 0
            play_sound(SELL_AUDIO)
       return None

    def display(self):
        self.display_surface.blit(self.background, (0,0))
        self.draw_slots_and_items(False)
        self.draw_player_inventory()
