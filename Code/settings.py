# game setup
WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 32
MAIN_BACKGROUND = '.\\bg_2.png'
BACKGROUND_2 = '.\\bg.png'
MAP_SIZE = 10240

HITBOX_SIZE = {
    'player': -3.5,
    'object': -20,
    'floor_blocks': 0
}

#UI
INVENTORY_BG = '.\\bg_3.png'
BLACKSMITH_BG = '.\\Graphics\\UI\\blacksmith_bg.png'
ARMOUR_SLOT = '.\\Graphics\\UI\\armour.png'
SLOT_IMAGE = '.\\Graphics\\UI\\slot_1.png'
MENU_TEXT_COLOUR = '#d7fcd4'
CURSOR= '.\\Graphics\\UI\\cursor.png'
SWORD_ICON = '.\\Graphics\\UI\\icons\\sword_underline_scaled.png'
MAGIC_ICON = '.\\Graphics\\UI\\icons\\smoke_scaled.png'
BAR_HEIGHT = 12
BAR_WIDTH = 104
ITEM_BOX_SIZE = 80
UI_FONT = "PokemonGb-Raeo.ttf"
UI_FONT_SIZE = 18
STATS_IMAGE = '.\\Graphics\\UI\\health_exp_mana_lvl_1.png'
INVENTORY_ICON = '.\\Graphics\\UI\\inventory_icon.png'
COIN_ICON = '.\\Graphics\\UI\\coin_icon_1.png'
COIN_ICON_1 = '.\\Graphics\\UI\\coin_icon.png'
QUEST_BACKGROUND = '.\\Graphics\\UI\\quest_bg.png'

UI_BG_COLOUR = '#4e4a4e'
UI_BORDER_COLOUR = '#111111'
UI_BORDER_COLOUR_2 = '#2e2b2b'
TEXT_COLOUR = '#eeeeee'
EXP_COLOUR = '#597dce'
HEALTH_COLOUR = '#d04648'
ENERGY_COLOUR = '#812cee'
UI_BORDER_COLOUR_ACTIVE = '#a6680a'
DESC_BOX_COLOUR = '#413e41'
FONT_COLOUR = '#ffd1a4'
DESC_FONT_COLOUR = '#eec7a0'
QUEST_HEADLINE_COLOUR = '#351b11'
QUEST_FONT_COLOUR = '#4f2b1c'

UI_SLIDER_START_VALUE = 50
UI_SLIDER_LENGTH = 300
#audio
MENU_AUDIO = '.\\Audio\\booya_b.wav'
OPTIONS_AUDIO = '.\\Audio\\monoliths.wav'
GAMEPLAY_AUDIO = '.\\Audio\\To_Be_Tacribian.wav'
DEATH_AUDIO = '.\\Audio\\TragicDeath.wav'
MENU_SELECT_AUDIO = '.\\Audio\\MENU_Select.wav'
QUEST_COMPLETED = '.\\Audio\\win_music.wav'
COIN_PICKUP_AUDIO = '.\\Audio\\hjm-coin_clicker_1.wav'
OPEN_INVENTORY_AUDIO = '.\\Audio\\leather_inventory.wav'
ARMOUR_EQUIP_AUDIO = '.\\Audio\\cloth_inventory.wav'
SELL_AUDIO = '.\\Audio\\sell_buy_item.wav'
CHANGE_WEAPON = '.\\Audio\\MENU_Pick.wav'
SWORD_SOUND = '.\\Audio\\metal_clash.wav'
SWORD_ATTACK_SOUND = '.\\Audio\\Socapex _new_hits_3.wav'

effects_volume = 0.3

weapons = {
    'base_sword': {'cooldown': 100, 'damage' : 25,'attack_radius': 10, 'graphic': '.\\Graphics\\UI\\weapons\\basic_sword_scaled.png'},
    'bow': {'cooldown': 150, 'damage' : 8, 'attack_radius': 35, 'graphic': '.\\Graphics\\UI\\weapons\\bow.png'},
    'sword_upgrade_1': {'cooldown': 150, 'damage' : 25, 'attack_radius': 10, 'graphic': '.\\Graphics\\UI\\weapons\\sword_1.png'},
    'sword_upgrade_2': {'cooldown': 200, 'damage' : 45, 'attack_radius': 15, 'graphic': '.\\Graphics\\UI\\weapons\\sword_2.png'},
    'sword_upgrade_3': {'cooldown': 300, 'damage' : 55, 'attack_radius': 20, 'graphic': '.\\Graphics\\UI\\weapons\\sword_3.png'},
}

magic_spells = {
    'fireball': {'name': 'Fireball','strength': 10, 'cost': 5, 'audio': '.\\Audio\\fireball.wav', 'graphic': '.\\Graphics\\UI\\spells\\fireball.png'},
    'heal' : {'name': 'Healing','strength': 15, 'cost': 10, 'audio': '.\\Audio\\heal.wav', 'graphic': '.\\Graphics\\UI\\spells\\heal.png'},
    'shield': {'name': 'Shield','strength': 5, 'cost': 15, 'audio': '.\\Audio\\shield.wav', 'graphic': '.\\Graphics\\UI\\spells\\shield.png'},
    'icicle': {'name': 'Icicle','strength': 25, 'cost': 35, 'audio': '.\\Audio\\icicle.wav','graphic': '.\\Graphics\\UI\\spells\\icicle.png'},
    'quake': {'name': 'Earthquake','strength': 65, 'cost': 50, 'audio': '.\\Audio\\quake.wav','graphic': '.\\Graphics\\UI\\spells\\quake.png'}
}

armour = {

    'simple_clothes': 
    {
     'head': {'resistance': 0, 'graphic': None}, 
     'top': {'resistance': 2, 'graphic': '.\\Graphics\\Armour\\simple_clothes\\top.png'}, 
     'bottom': {'resistance': 2, 'graphic': '.\\Graphics\\Armour\\simple_clothes\\bottom.png'}
    },

    'leather_armour' : 
    {
     'head': {'resistance': 5, 'graphic': '.\\Graphics\\Armour\\leather_armour\\head.png'}, 
     'top': {'resistance': 15, 'graphic': '.\\Graphics\\Armour\\leather_armour\\top.png'}, 
     'bottom': {'resistance': 2, 'graphic': '.\\Graphics\\Armour\\leather_armour\\bottom.png'}
    },
    
    'robe' :
    {
     'head': {'resistance': 5, 'graphic': '.\\Graphics\\Armour\\robe\\head.png'}, 
     'top': {'resistance': 8, 'graphic': '.\\Graphics\\Armour\\robe\\top.png'}, 
     'bottom': {'resistance': 5, 'graphic': '.\\Graphics\\Armour\\robe\\bottom.png'}
    },

    'chain_armour': 
    {
     'head': {'resistance': 15, 'graphic': '.\\Graphics\\Armour\\chain_armour\\head.png'}, 
     'top': {'resistance': 45, 'graphic': '.\\Graphics\\Armour\\chain_armour\\top.png'}, 
     'bottom': {'resistance': 15, 'graphic': '.\\Graphics\\chain_armour\\bottom.png'}
    },

    'chain_armour_robe': 
    {
     'head': {'resistance': 10, 'graphic': '.\\Graphics\\Armour\\chain_armour_robe\\head.png'}, 
     'top': {'resistance': 50, 'graphic': '.\\Graphics\\Armour\\chain_armour_robe\\top.png'}, 
     'bottom': {'resistance': 10, 'graphic': '.\\Graphics\\Armour\\chain_armour_robe\\bottom.png'}
    },

    'plate_armour': 
    {
     'head': {'resistance': 55, 'graphic': '.\\Graphics\\Armour\\plate_armour\\head.png'},
     'top': {'resistance': 55, 'graphic': '.\\Graphics\\Armour\plate_armour\\top.png'}, 
     'bottom': {'resistance': 55, 'graphic': '.\\Graphics\\Armour\\plate_armour\\bottom.png'}
    }
}

enemies = {
    'skeleton_sword' : {'health' : 100, 'exp': 15, 'coins': 1, 'damage': 5, 'attack_type' : 'slash', 'attack_sound': '.\\Audio\\Socapex_ new_hits_1.wav','speed' : 2, 'resistance' : 4, 'attack_radius': 50, 'notice_radius': 360, 'cooldown': 500},
    'skeleton_magic' : {'health' : 125, 'exp': 25, 'coins': 5, 'damage': 27, 'attack_type' : 'magic', 'attack_sound': '.\\Audio\\Magic_Smite.wav','speed' : 4, 'resistance' : 3, 'attack_radius': 100, 'notice_radius': 360, 'cooldown': 1800},
    'mage': {'health' : 150, 'exp': 35, 'coins': 10, 'damage': 32, 'attack_type' : 'magic', 'attack_sound': '.\\Audio\\Magic_Smite.wav','speed' : 4, 'resistance' : 4, 'attack_radius': 130, 'notice_radius': 360, 'cooldown': 1500},
    'baldric' : {'health' : 200, 'exp': 75, 'coins': 15,'damage': 40, 'attack_type' : 'slash', 'attack_sound': '.\\Audio\\Socapex_ new_hits_2.wav','speed' : 4, 'resistance' : 4, 'attack_radius': 60, 'notice_radius': 360, 'cooldown': 500}
}


quests= {
    'first_steps': {'name': 'First Steps', 'objective': {'text': 'Collect 5 coins', 'completed': False}, 'description' : 'Money is money', 'reward': {'exp': 20, 'coins': 0}},
    'protection': {'name': 'Protection', 'objective': {'text': 'Buy leather armour', 'completed': False}, 'description' : 'Increase resistance', 'reward': {'exp': 35, 'coins': 5}}

}

item_attributes = {
    'weapon': {
        'base_sword': {'description': 'A basic sword', 'cost': 5, 'graphic': '.\\Graphics\\UI\\weapons\\basic_sword.png'},
        'sword_upgrade_1': {'description': 'Upgraded sword', 'cost': 15, 'graphic': '.\\Graphics\\UI\\weapons\\sword_1.png'},
        'sword_upgrade_2': {'description': 'Even more upgraded sword', 'cost': 20, 'graphic': '.\\Graphics\\UI\\weapons\\sword_2.png'},
        'sword_upgrade_3': {'description': 'Ultimate sword upgrade', 'cost': 35, 'graphic': '.\\Graphics\\UI\\weapons\\sword_3.png'},
    },
    
    'armour': {
        'simple_clothes': {'description': 'Basic armour', 'cost': 2, 'graphic': '.\\Graphics\\Armour\\simple_clothes\\full_armour.png'},
        'leather_armour': {'description': 'Light and flexible armour', 'cost': 20, 'graphic': '.\\Graphics\\Armour\\leather_armour\\full_armour.png'},
        'robe': {'description': 'A simple robe for mages', 'cost': 15, 'graphic': '.\\Graphics\\Armour\\robe\\full_armour.png'},
        'chain_armour': {'description': 'Heavy chain armour', 'cost': 45, 'graphic': '.\\Graphics\\Armour\\chain_armour\\full_armour.png'},
        'chain_armour_robe': {'description': 'Upgraded robe for mages', 'cost': 45, 'graphic': '.\\Graphics\\Armour\\chain_armour_robe\\full_armour.png'},
        'plate_armour': {'description': 'Thick and heavy armour', 'cost': 70, 'graphic': '.\\Graphics\\Armour\\plate_armour\\full_armour.png'},
    }
}
