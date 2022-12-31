from csv import reader
from os import walk
import pygame, sys
from settings import *
import pygame.freetype


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append([int(x) for x in row])
        return terrain_map

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

class GameOverScreen:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.text_surface = self.font.render("You have lost", True, (TEXT_COLOR))
        screen_width, screen_height = self.screen_size
        center_x = screen_width // 2
        center_y = screen_height // 2
        self.text_rect = self.text_surface.get_rect(center=(center_x, center_y))
        self.game_over = False

        self.Start_Over_Bar()

    def Start_Over_Bar(self):
        self.font = pygame.font.Font(UI_FONT, 10)
        self.button_rect = pygame.Rect(self.text_rect.centerx - 100, self.text_rect.centery + 50, 200, 45)
        self.button_text_surface = self.font.render("Start Over? (Y) (N)", True, (0,0,0))
        self.button_text_rect = self.button_text_surface.get_rect(center=self.button_rect.center)
        self.button_bg_color = (200, 200, 200)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.text_surface, self.text_rect)
        pygame.draw.rect(surface, self.button_bg_color, self.button_rect)
        surface.blit(self.button_text_surface,self.button_text_rect)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            self.game_over = True
        elif keys[pygame.K_n]:
            pygame.quit()
            sys.exit()


    def display(self):
        screen = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw(screen)
            self.check_input()
            pygame.display.flip()
            pygame.time.delay(100) 
            clock.tick(60)
            return self.game_over
        pygame.quit()
        