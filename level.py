import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
  def __init__(self):

    # get the display surface
    self.display_surface = pygame.display.get_surface()
    
    #sprite group setup
    self.visible_sprites = YSortCameraGroup()
    self.obstacle_sprites = pygame.sprite.Group()

    # sprite setup
    self.create_map()

  def create_map(self):
<<<<<<< HEAD
    for row_index,row in enumerate(WORLD_MAP):
      for col_index, col in enumerate(row):
        x = col_index * TILESIZE
        y = row_index * TILESIZE
        if col == 'x':
          Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        if col == 'p':
          self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
=======
    # for row_index,row in enumerate(WORLD_MAP):
    #   for col_index, col in enumerate(row):
    #     x = col_index * TILESIZE
    #     y = row_index * TILESIZE
    #     if col == 'x':
    #       Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
    #     if col == 'p':
          self.player = Player((2600, 6500), [self.visible_sprites], self.obstacle_sprites)
>>>>>>> c5c4d4f5acfab0d842974928206f047dc76f9071

  def run(self):
    #update and draw self
    
    self.visible_sprites.custom_draw(self.player)
    self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

<<<<<<< HEAD
=======
        #creating the floor
        self.floor_surf = pygame.image.load('BackGround.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

>>>>>>> c5c4d4f5acfab0d842974928206f047dc76f9071
    def custom_draw(self,player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
<<<<<<< HEAD
        for sprite in self.sprites():
=======
        #drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        #draws the sprites in order so the player is properly behind or infront of other sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
>>>>>>> c5c4d4f5acfab0d842974928206f047dc76f9071
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
