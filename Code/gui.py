import pygame
from button import Button
from settings import *
class GUI:
    def __init__(self):
        self.items = []
        self.item_size = 55
        self.slot_size = 70
        self.inventory_slot_image = pygame.image.load(SLOT_IMAGE)
        self.inventory_slot_image = pygame.transform.scale(self.inventory_slot_image, (self.slot_size, self.slot_size))
        self.start_x = 150
        self.start_y = 150
        self.slot_spacing = 5
        self.main_font = pygame.font.Font(UI_FONT,25)
        self.description_font = pygame.font.Font(UI_FONT, 15)
        self.last_click = 0
        self.last_remove = 0

    def draw_slots_and_items(self, is_inventory = True, is_in_shop = False, shop = None):
        if is_inventory:
            desc_box_offset = 50
            items_surface = self.main_font.render('Items', True, FONT_COLOUR)
            items_rect = items_surface.get_rect(topleft=(325, 105))
            self.display_surface.blit(items_surface, items_rect)
        elif not is_inventory:
            desc_box_offset = 200
            items_surface = self.main_font.render('Shop', True, FONT_COLOUR)
            items_rect = items_surface.get_rect(topleft=(965, 65))
            self.display_surface.blit(items_surface, items_rect)

        for i in range(self.capacity):
            x_offset = self.slot_spacing + ((self.slot_spacing + self.slot_size) * (i % 6)) + self.start_x
            y_offset = self.slot_spacing + ((self.slot_spacing + self.slot_size) * (i // 6)) + self.start_y

            slot_rect = self.inventory_slot_image.get_rect(center=(x_offset + self.slot_size // 2, y_offset + self.slot_size // 2))
            self.display_surface.blit(self.inventory_slot_image, slot_rect)

            if i < len(self.items) and self.items[i] is not None:
                item_graphic = pygame.image.load(self.items[i].graphic)
                item_graphic = pygame.transform.scale(item_graphic, (self.item_size, self.item_size))
                self.item_slots[i] = item_graphic
                item_rect = item_graphic.get_rect(center = slot_rect.center)
                self.display_surface.blit(item_graphic, item_rect)

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if item_rect.collidepoint(mouse_x, mouse_y):
                    desc_rect = pygame.Rect(x_offset-desc_box_offset, y_offset-100, 400, 80)
                    desc_surface = pygame.Surface(desc_rect.size)
                    desc_surface.fill(DESC_BOX_COLOUR)
                    name = self.description_font.render(self.items[i].name.title(), True, DESC_FONT_COLOUR)
                    cost = self.description_font.render(f"Cost: {self.items[i].cost}", True, DESC_FONT_COLOUR)
                    description = self.description_font.render(self.items[i].description, True, DESC_FONT_COLOUR)
                    desc_surface.blit(name, (10, 10))
                    desc_surface.blit(cost,(10,30))
                    desc_surface.blit(description,(10,50))
                    self.display_surface.blit(desc_surface, desc_rect)
                    pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_2, desc_rect, 2)


                    if pygame.mouse.get_pressed()[0]:
                        if pygame.time.get_ticks() - self.last_click < 500:
                            if is_in_shop:
                                shop.add_item(self.items[i])
                                self.coins += self.items[i].cost
                                self.remove_item(i)
                            elif not is_inventory:
                                self.sell_item(i)
                            elif is_inventory and not is_in_shop:
                                if self.items[i].type == 'armour':
                                    self.equip_armour(i)
                                elif self.items[i].type == 'weapon':
                                    self.equip_weapon(i)
                        self.last_click = pygame.time.get_ticks()
            elif i < len(self.items) and self.items[i] is None:
                if pygame.time.get_ticks() - self.last_remove > 500:
                    self.items = [item for item in self.items if item is not None]
                    self.last_remove = pygame.time.get_ticks()


    def add_item(self,item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        else:
            return False

    def remove_item(self,index):
        self.items[index] = None
        self.item_slots[index] = None

