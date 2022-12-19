import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import debug
from weapon import Weapon
from ui import UI

class Level:
  def __init__(self):

    # get the display surface
    self.display_surface = pygame.display.get_surface()
    
    #sprite group setup
    self.visible_sprites = YSortCameraGroup()
    self.obstacle_sprites = pygame.sprite.Group()
    
    # attack sprites
    self.current_attack = None

    # sprite setup
    self.create_map()

    # user interface
    self.ui = UI()
  def create_map(self):
    
    layouts = {
      'Boundary': import_csv_layout('CSV/TiledMap_Boundary.csv'),
      'grass': import_csv_layout('CSV/TiledMap_grass.csv'),
      
    }
    graphics = {
      
      'grass': import_folder('graphics/terrain/grass'),
      
    }
   
    for style,layout in layouts.items():
      for row_index,row in enumerate(layout):
        for col_index, col in enumerate(row):
          if col != '-1':
            x = col_index * TILESIZE
            y = row_index * TILESIZE
            if style == 'Boundary':
              
              Tile((x,y), [self.obstacle_sprites],'invisible')
            if style == 'grass':
              random_grass_image = choice(graphics['grass'])
              Tile((x,y), [self.visible_sprites,self.obstacle_sprites],'grass', random_grass_image,1)
            


    self.player = Player((1596 , 4250), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

  def create_attack(self):
    self.current_attack = Weapon(self.player,[self.visible_sprites])

  def destroy_attack(self):
    if self.current_attack:
      self.current_attack.kill()
    self.current_attack = None
    
  def run(self):
    #update and draw self
    
    self.visible_sprites.custom_draw(self.player)
    self.visible_sprites.update()
    self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load('graphics/TiledMap.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        #draws the sprites in order so the player is properly behind or infront of other sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: (sprite.image_depth, sprite.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
