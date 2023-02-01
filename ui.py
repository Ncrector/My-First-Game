import pygame
from settings import *

class UI:
    
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,3)

        font = pygame.font.Font(None, 18)
        text = font.render(f"{int(current)}/{int(max_amount)}", True, (255,255,255))
        text_rect = text.get_rect()
        text_rect.center = bg_rect.center
        self.display_surface.blit(text, text_rect)

    def show_exp(self,exp):
        text_surf = self.font.render('xp ' + str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 10
        y = self.display_surface.get_size()[1] - 10
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)
    
    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched): 
        bg_rect = self.selection_box(10,400,has_switched)

        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        weapon_surf = pygame.transform.scale(weapon_surf, (weapon_surf.get_width() // 2, weapon_surf.get_height() // 2))
        weapon_rect.move_ip(5, 15)
        self.display_surface.blit(weapon_surf, weapon_rect)

        # Add this line to display the letter "Q" below the rectangle
        text_surf = self.font.render("Q", False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(bg_rect.centerx - 5, bg_rect.bottom + 15))
        self.display_surface.blit(text_surf, text_rect)

    def upgrade_menu(self):
        text_surf = self.font.render("Upgrades: M", False, TEXT_COLOR)
        display_width, display_height = self.display_surface.get_size()
        text_rect = text_surf.get_rect(bottomleft=(10, display_height - 10))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.selection_index += 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            
    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(50,420,has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        magic_surf = pygame.transform.scale(magic_surf, (magic_surf.get_width() // 2, magic_surf.get_height() // 2))
        magic_rect.move_ip(15, 15)
        self.display_surface.blit(magic_surf, magic_rect)

        # Add this line to display the letter "Q" below the rectangle
        text_surf = self.font.render("E", False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(bg_rect.centerx, bg_rect.bottom + 15))
        self.display_surface.blit(text_surf, text_rect)

    def player_stats(self, player):
        rect_height = self.display_surface.get_size()[1] / 2
        rect_width = 15 # Position the rectangle on the very left side of the screen
        rect = pygame.Rect(rect_width, rect_height - 72, 100, 150) # Adjust the position and size of the rectangle
        # Draw the rectangle with a gray fill at 50% opacity
        gray = (128, 128, 128)
        rect_fill = pygame.Surface((rect.width, rect.height))
        rect_fill.fill(gray)
        rect_fill.set_alpha(128) 
        self.display_surface.blit(rect_fill, (rect.x, rect.y))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect,3)

        # Get the player's stats
        attack = int(player.stats['attack'])
        magic = int(player.stats['magic'])
        speed = int(player.stats['speed'])
        health = int(player.stats['health'])
        energy = int(player.stats['energy'])

        # Render the stats text
        self.font = pygame.font.Font(None, 23)
        attack_text = self.font.render("Attack: " + str(attack), False, TEXT_COLOR)
        magic_text = self.font.render("Magic: " + str(magic), False, TEXT_COLOR)
        speed_text = self.font.render("Speed: " + str(speed), False, TEXT_COLOR)
        health_text = self.font.render("health: " + str(health), False, TEXT_COLOR)
        energy_text = self.font.render("mana: " + str(energy), False, TEXT_COLOR)

        # Blit the text to the screen inside the rectangle
        self.display_surface.blit(attack_text, (rect_width + 10, rect_height - 67.5 + 10))
        self.display_surface.blit(magic_text, (rect_width + 10, rect_height - 67.5 + 35))
        self.display_surface.blit(speed_text, (rect_width + 10, rect_height - 67.5 + 60))
        self.display_surface.blit(health_text, (rect_width + 10, rect_height - 67.5 + 85))
        self.display_surface.blit(energy_text, (rect_width + 10, rect_height - 67.5 + 110))


    def display(self, player):
        self.show_bar(player.health, player.stats['health'],self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'],self.energy_bar_rect, ENERGY_COLOR)

        self.player_stats(player)
        self.show_exp(player.exp)
        self.upgrade_menu()
        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
        self.magic_overlay(player.magic_index,not player.can_switch_magic)   