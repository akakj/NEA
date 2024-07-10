import pygame
from gui import GUI
from settings import *
from player import Player
from magic import MagicPlayer
from item import Item
from support import play_sound

class Inventory(GUI):
    def __init__(self, player):
        super().__init__()
        self.background = pygame.image.load(INVENTORY_BG)
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.capacity = 30
        self.items = []
        self.equipped_armour = Item(self.player.armour_name,'armour')
        self.equipped_weapon = Item('base_sword', 'weapon')
        self.main_font = pygame.font.Font(UI_FONT, 22)
        self.description_font = pygame.font.Font(UI_FONT, 15)

        self.armour = armour
        self.weapons = weapons
        self.weapon_key_list = list(weapons.keys())
        self.spells = magic_spells

        self.item_slots = [None] * self.capacity
        self.start_x = 150
        self.start_y = 150

        self.coins = player.coins

    def draw_armour_pieces(self):
        armour_surface = pygame.image.load(ARMOUR_SLOT)
        armour_surface = pygame.transform.scale(armour_surface, (280,350))
        armour_rect = armour_surface.get_rect(topleft = (900,80))
        self.display_surface.blit(armour_surface,armour_rect)

        rect_sizes = [
        (100, 84), # mid-top rectangle
        (100, 88), # center rectangle
        (100, 84) # mid-bottom rectangle
        ]

        x_offset = 1001
        y_offset = [160, 248, 336]

        for index, (slot, item) in enumerate(self.player.current_armour.items()):
            if item and item['graphic'] is not None:
                item_graphic = pygame.image.load(item['graphic'])
                item_graphic = pygame.transform.scale(item_graphic, (80,80))
                rect = pygame.Rect(x_offset,y_offset[index], rect_sizes[index][0], rect_sizes[index][1])
                self.display_surface.blit(item_graphic, rect)

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_x, mouse_y):
                    x = x_offset - item_graphic.get_width() - 20
                    y = y_offset[index] - index * 80
                    desc_rect = pygame.Rect(x, y, 245, 35)
                    desc_surface = pygame.Surface(desc_rect.size)
                    desc_surface.fill(DESC_BOX_COLOUR)
                    res_info = self.description_font.render(f"Resistance: {item['resistance']}", True, DESC_FONT_COLOUR)
                    desc_surface.blit(res_info, (10, 10))
                    self.display_surface.blit(desc_surface, desc_rect)
                    pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_2, desc_rect, 2)


        if isinstance(self.player, Player) and not isinstance(self.player, MagicPlayer):
            self.draw_current_weapons()

    def draw_current_weapons(self):
        current_weapons = []
        current_weapons.append(self.weapons[list(weapons.keys())[self.player.sword_index]])
        current_weapons.append(self.weapons[list(weapons.keys())[1]])
        
        rect_sizes = [
            (81, 88),  # mid-left rectangle
            (78, 88)  # mid-right rectangle
        ]

        x_offset = [923, 1100]
        y_offset = 260

        for i in range(len(rect_sizes)):
            if i < len(current_weapons) and current_weapons[i]['graphic'] is not None:
                image = pygame.image.load(current_weapons[i]['graphic'])
                image = pygame.transform.scale(image, (60,60))
                rect = pygame.Rect(x_offset[i],y_offset, rect_sizes[i][0], rect_sizes[i][1])
                self.display_surface.blit(image, rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                x = x_offset[i] - 275
                y = y_offset - image.get_height() - i * 80
                desc_rect = pygame.Rect(x, y, 275, 55)
                desc_surface = pygame.Surface(desc_rect.size)
                desc_surface.fill(DESC_BOX_COLOUR)
                damage_info = self.description_font.render(f"Attack damage: {current_weapons[i]['damage']}", True, DESC_FONT_COLOUR)
                radius_info = self.description_font.render(f"Attack radius: {current_weapons[i]['attack_radius']}", True, DESC_FONT_COLOUR)
                desc_surface.blit(damage_info, (10, 10))
                desc_surface.blit(radius_info,(10,30))
                self.display_surface.blit(desc_surface, desc_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_2, desc_rect, 2)

    def draw_coins(self):
        icon = pygame.image.load(COIN_ICON_1)
        icon = pygame.transform.scale(icon,(50,50))
        icon_rect = icon.get_rect(topright = (1270,5))
        self.display_surface.blit(icon,icon_rect)
        text_surface = self.description_font.render(str(self.player.coins), False, FONT_COLOUR)
        text_rect = text_surface.get_rect(topleft = (1180,20))
        self.display_surface.blit(text_surface,text_rect)

    def draw_player_stats(self):
        start_pos = 445
        stats = [
            (f"Level: {str(self.player.level)}", (0, 25)),
            (f"Exp: {round(self.player.exp)}/{round(self.player.exp_to_level_up)}", (0, 50)),
            (f"Health: {round(self.player.health)}/{round(self.player.stats['health'])}", (0, 75)),
            (f"Energy: {round(self.player.energy)}/{round(self.player.stats['energy'])}", (0, 100)),
            (f"Speed: {round(self.player.stats['speed'])}", (0, 125))
            ]
        for i, (stat_text, offset) in enumerate(stats):
            stat_surface = self.description_font.render(stat_text, False, FONT_COLOUR)
            stat_rect = stat_surface.get_rect(topleft=(905, start_pos + i * 25))
            self.display_surface.blit(stat_surface, stat_rect)

        if isinstance(self.player, Player) and not isinstance(self.player, MagicPlayer):
            player_attack = self.description_font.render( f"Attack: {round(self.player.stats['magic'])}", False, FONT_COLOUR)
            player_attack_rect = player_attack.get_rect(topleft = (905,570))
            full_damage = self.description_font.render(f"Full attack damage: {round(self.player.get_weapon_damage())}", False, FONT_COLOUR)
            full_damage_rect = full_damage.get_rect(topleft = (905, 595))
        else:
            player_attack = self.description_font.render( f"Magic Attack: {round(self.player.stats['magic'])}", False, FONT_COLOUR)
            player_attack_rect = player_attack.get_rect(topleft = (905,570))
            full_damage = self.description_font.render(f"Full attack damage: {round(self.player.full_magic_damage())}", False, FONT_COLOUR)
            full_damage_rect = full_damage.get_rect(topleft = (905, 595))
        
        self.display_surface.blit(player_attack,player_attack_rect)
        self.display_surface.blit(full_damage,full_damage_rect)

    def draw_spells(self):
        self.spell_rects = {}
        x = 125
        y = 585
        for spell_name, spell_info in self.spells.items():
            rect = pygame.Rect(x, y, 80, 80)
            self.spell_rects[spell_name] = rect
            pygame.draw.rect(self.display_surface, UI_BG_COLOUR,rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_2, rect,2)
            image = pygame.image.load(spell_info['graphic'])
            image_rect = image.get_rect(center = rect.center)
            self.display_surface.blit(image, image_rect)
            x += 105
    
    def draw_equipped_armour(self):
        text = self.main_font.render('Armour', False, FONT_COLOUR)
        text_rect = text.get_rect(topleft =(660,215))
        self.display_surface.blit(text,text_rect)

        inventory_image = pygame.transform.scale(self.inventory_slot_image,(80,80))
        inventory_item_rect = inventory_image.get_rect(x = 685, y = 260, width=self.slot_size, height=self.slot_size)
        self.display_surface.blit(inventory_image, inventory_item_rect)

        armour_graphic = pygame.image.load(self.equipped_armour.graphic)
        armour_graphic = pygame.transform.scale(armour_graphic,(70,70))
        armour_rect = armour_graphic.get_rect(x = 685, y = 260, center = inventory_item_rect.center + pygame.math.Vector2(5,6))
        self.display_surface.blit(armour_graphic, armour_rect)

    def equip_armour(self,index):
        armour_to_equip = self.items[index]
        self.items[index] = self.equipped_armour
        self.equipped_armour = armour_to_equip
        self.player.armour_name = self.equipped_armour.name
        self.player.update_armour(self.equipped_armour.name)
        play_sound(ARMOUR_EQUIP_AUDIO)

    def equip_weapon(self,index):
        if isinstance(self.player, Player) and not isinstance(self.player, MagicPlayer):
            previuos_weapon = self.equipped_weapon
            self.equipped_weapon = self.items[index]
            equipped_weapon_index = self.weapon_key_list.index(self.items[index].name)
            self.player.sword_index = equipped_weapon_index
            self.items[index] = previuos_weapon
            play_sound(SWORD_SOUND)

    def draw_spells_description(self):
        mouse_pos = pygame.mouse.get_pos()

        for spell_name, rect in self.spell_rects.items():
            if rect.collidepoint(mouse_pos):
                desc_rect = pygame.Rect(rect.right + 10, rect.top, 200, 80)

                spell = magic_spells[spell_name]
                name = spell['name']
                strength = spell['strength']
                cost = spell['cost']

                desc_surface = pygame.Surface(desc_rect.size)
                desc_surface.fill(DESC_BOX_COLOUR)
                name_text = self.description_font.render(f"{name}", True, DESC_FONT_COLOUR)
                strength_text = self.description_font.render(f"Strength: {strength}", True, DESC_FONT_COLOUR)
                cost_text = self.description_font.render(f"Cost: {cost}", True, DESC_FONT_COLOUR)
                desc_surface.blit(name_text, (10, 10))
                desc_surface.blit(strength_text, (10, 30))
                desc_surface.blit(cost_text, (10, 50))

                self.display_surface.blit(desc_surface, desc_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_2, desc_rect, 2)

    def display(self):
        self.display_surface.blit(self.background, (0,0))
        
        self.draw_slots_and_items()
        self.draw_equipped_armour()
        self.draw_armour_pieces()
        self.draw_coins()
        self.draw_player_stats()

        if not (isinstance(self.player, Player) and not isinstance(self.player, MagicPlayer)):
            self.draw_spells()
            self.draw_spells_description()

