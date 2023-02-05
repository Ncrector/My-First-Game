import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from debug import debug
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from upgrade import Upgrade
from magic import MagicPlayer
from dragon import Dragon
from slime import Slime

class Level:
  
  def __init__(self):
    

    # get the display surface
    self.display_surface = pygame.display.get_surface()
    self.game_paused = False
    
    #sprite group setup
    self.visible_sprites = YSortCameraGroup()
    self.obstacle_sprites = pygame.sprite.Group()
    
    # attack sprites
    self.current_attack = None
    self.attack_sprites = pygame.sprite.Group()
    self.attackable_sprites = pygame.sprite.Group()
    self.damage_sprites = pygame.sprite.Group()
    self.player_sprite = pygame.sprite.Group()
    self.enemy_sprite = pygame.sprite.Group()

    # sprite setup
    self.create_map()

    # user interface
    self.ui = UI()
    self.upgrade = Upgrade(self.player)

    # game over
    self.game_over_screen = GameOverScreen((960,540))
    self.game_over = False

    # particles
    self.animation_player = AnimationPlayer()
    self.magic_player = MagicPlayer(self.animation_player)

  def create_map(self):
    
    layouts = {
      'Boundary': import_csv_layout('CSV/TiledMap_Boundary.csv'),
      'grass': import_csv_layout('CSV/TiledMap_grass.csv'),
      'entities': import_csv_layout('CSV/TiledMap_entities.csv')
      
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

            if style == 'Boundary' and col == 0:       
              Tile((x,y), [self.obstacle_sprites],'invisible')
            if style == 'grass' and col == 0:
              random_grass_image = choice(graphics['grass'])
              Tile((x,y), [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass', random_grass_image)
            if style == 'entities':
              if col == 0:
                Enemy('spirit',(x,y), [self.visible_sprites,self.attackable_sprites, self.enemy_sprite], self.obstacle_sprites, self.damage_player,self.trigger_death_particles,self.add_xp)
              if col == 226:
                Enemy('squid',(x,y), [self.visible_sprites,self.attackable_sprites, self.enemy_sprite], self.obstacle_sprites, self.damage_player,self.trigger_death_particles,self.add_xp)
              if col == 212:
                Dragon('dragon',(x,y),[self.visible_sprites,self.attackable_sprites, self.enemy_sprite], self.obstacle_sprites, self.damage_player,self.trigger_death_particles,self.add_xp,self.create_fireball)
              if col == 272:
                Slime('slime',(x,y),[self.visible_sprites,self.attackable_sprites,self.enemy_sprite], self.obstacle_sprites, self.damage_player,self.trigger_death_particles, self.add_xp, self.create_slimeball)

    self.player = Player((3200 , 4500), [self.visible_sprites,self.player_sprite], self.obstacle_sprites, self.create_attack, self.destroy_attack,self.create_magic)

  def create_attack(self):
    self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
  
  def create_magic(self,style,strength,cost):
    if style == 'heal':
      self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

    if style == 'flame':
      self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
  
  def create_fireball(self,pos,direction):
    self.animation_player.create_fireball(pos, direction, [self.visible_sprites, self.damage_sprites])
  
  def create_slimeball(self,pos,direction):
    self.animation_player.create_slimeball(pos,direction, [self.visible_sprites, self.damage_sprites])
  
    
  def destroy_attack(self):
    if self.current_attack:
      self.current_attack.kill()
    self.current_attack = None
  
  def sprite_collision_logic(self):
    if self.enemy_sprite:
        self.enemy_list = self.enemy_sprite.copy()
        for colliding_sprite in self.enemy_list:
            if colliding_sprite.sprite_type == 'dragon':
                continue
            self.enemy_list.remove(colliding_sprite)
            collided_sprites = pygame.sprite.spritecollide(colliding_sprite, self.enemy_list, False)
            if collided_sprites:
                for target_sprite in collided_sprites:
                    target_sprite.detect_collision(target_sprite, colliding_sprite)
                    
  
  
     
  def player_attack_logic(self):
      if self.attack_sprites:
        for attack_sprite in self.attack_sprites:
          collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
          if collision_sprites:
            for target_sprite in collision_sprites:
              if target_sprite.sprite_type == 'grass':
                pos = target_sprite.rect.center
                offset = pygame.math.Vector2(0,35)
                for leaf in range(randint(3,6)):
                  self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                target_sprite.kill()
              else:
                target_sprite.get_damage(self.player,attack_sprite.sprite_type)

      # player taking damage from fireball damage sprite group
      if self.damage_sprites:
        for damage_sprite in self.damage_sprites:
          player_collision = pygame.sprite.spritecollide(damage_sprite, self.player_sprite, False)
          if player_collision:
            damage_sprite.kill()
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.player.health -= 10 # fireball does 10 damage shouldn't hardcode this...
            self.animation_player.create_particles('thunder',self.player.rect.center,[self.visible_sprites])
            self.fireball_sound = pygame.mixer.Sound('audio/Fire.wav')
            self.fireball_sound.set_volume(0.1)
            self.fireball_sound.play()

          obstacle_collision = pygame.sprite.spritecollide(damage_sprite, self.obstacle_sprites, False)
          if obstacle_collision:
            damage_sprite.kill()


                
              

  def damage_player(self,amount,attack_type):
    if self.player.vulnerable:
      self.player.health -= amount
      self.player.vulnerable = False
      self.player.hurt_time = pygame.time.get_ticks()
      self.animation_player.create_particles(attack_type, self.player.rect.center,[self.visible_sprites] )

  def trigger_death_particles(self,pos,particle_type):
    self.animation_player.create_particles(particle_type,pos, self.visible_sprites)

  def toggle_menu(self):
    self.game_paused = not self.game_paused

  def run(self):
    self.visible_sprites.custom_draw(self.player)
    self.ui.display(self.player)
    if self.game_paused:
        if self.player.health <= 0:
            self.game_over_screen.display()
            self.game_over = self.game_over_screen.display()
            
        else:
            self.upgrade.display()
    else:
        self.sprite_collision_logic()
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
  
  def add_xp(self,amount):
    self.player.exp += amount
  
  def get_players_health(self):
    return self.player.health

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
        for sprite in sorted(self.sprites(), key = lambda sprite: (sprite.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
      enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
      for enemy in enemy_sprites:
        enemy.enemy_update(player)