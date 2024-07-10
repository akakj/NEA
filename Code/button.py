import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image,self.rect)
        screen.blit(self.text, self.text_rect)
        
    def checkForInput(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right)and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColour(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right)and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)

    def drawRectAround(self,screen,pos):
        if self.image is not None:
            if pos[0] in range(self.rect.left, self.rect.right)and pos[1] in range(self.rect.top, self.rect.bottom):
                pygame.draw.rect(screen,'white',self.rect,3)
        else:
            pass


