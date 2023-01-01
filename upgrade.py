import pygame
from settings import *

class Upgrade:

    def __init__(self,player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection__time = None
        self.can_move = True
    
    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_e] and self.selection_index - self.attribute_nr < -1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_q] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
    
    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + ((increment - self.width) // 2)
            top = self.display_surface.get_size()[1] * 0.1


            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)

    def tooltip(self):
        self.font = pygame.font.Font(UI_FONT, 14)
        text_surf = self.font.render("q and e to select, press spacebar to upgrade", False, TEXT_COLOR)
        display_width, display_height = self.display_surface.get_size()
        text_rect = text_surf.get_rect(midbottom=(display_width // 2, display_height - 10))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def display(self):
        self.tooltip()
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name,value, max_value,cost)
        
class Item:
    
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    
    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 10))

        # cost
        cost_surf = self.font.render('cost ' + f'{int(cost)}', False, color)
        cost_rect = title_surf.get_rect(bottomright = self.rect.midbottom - pygame.math.Vector2(-20, 10))
        # draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def display_bar(self,surface,value,max_value,selected):

        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,40)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,40)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number, 30,10)

        # DRAW ELEMENTS
        pygame.draw.line(surface,color,top,bottom, 6)
        pygame.draw.rect(surface,color,value_rect)
    
    def trigger (self,player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            print(upgrade_attribute)
            print(player.stats[upgrade_attribute])
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self,surface,selection_num,name,value,max_value,cost):
        if self.index == selection_num:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR, self.rect,4)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR, self.rect,4)

        self.display_names(surface,name,cost,self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)
