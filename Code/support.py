from csv import reader
from os import walk
import pygame
from settings import *
import json
from item import Item


def import_csv_layout(path):

    terrain_map = []

    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []

    for folder,subfolders,image_files in walk(path):
        for image in image_files:
            full_path = path + '\\' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list

def play_sound(path):
	music = pygame.mixer.Sound(path)
	music.set_volume(effects_volume)
	music.play()
        

class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
    
class ItemDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if '__type__' in dct and dct['__type__'] == 'item':
            return Item(**dct)
        return dct
	

