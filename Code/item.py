from settings import *

class Item:
    def __init__(self,name,type):
        self.name = name
        self.type = type
        self.stockable = type != 'weapon' and type != 'armour'
        self.cost = 0
        self.description = ""

        self.set_attributes()


    def set_attributes(self):
        item_attributes_access = item_attributes.get(self.type, {}).get(self.name, {})
        self.description = item_attributes_access.get('description', '')
        self.cost = item_attributes_access.get('cost', None)
        self.graphic = item_attributes_access.get('graphic', None)

