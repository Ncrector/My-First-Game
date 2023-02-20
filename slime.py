import pygame
from settings import *
from entity import Entity
from support import *
import math
import random
import time

class Slime(Entity):

    def __init__(self,monster_name,pos,groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, create_slimeball):

        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy' 
        # graphics
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # resize image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites
    
        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.velocity = (self.speed*self.direction.x, self.speed*self.direction.y)
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        
        self.attack_time = None
        self.attack_cooldown = 6000
        self.create_slimeball = create_slimeball
        self.has_casted = False
        self.index = 0
    
        
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 500

        # sounds
        self.death_sound = pygame.mixer.Sound("audio/death.wav")
        self.hit_sound = pygame.mixer.Sound("audio/hit.wav")
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.1)
        self.hit_sound.set_volume(0.1)
        self.attack_sound.set_volume(0.1)

    def import_graphics(self,name): 
        self.animations = {'idle':[],'move':[],'attack_left':[],'attack_right':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        self.animation_speed = 0.05
        if self.status == 'attack_left' or self.status == 'attack_right':
            self.animation_speed = 0.15

        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack_left' or self.status == 'attack_right':
                self.can_attack = False
            
            self.frame_index = 0

        frame = animation[int(self.frame_index)]
        self.image = frame
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]
        
        self.speed = monster_data[self.monster_name]['speed']
       

        if distance <= self.attack_radius and self.can_attack and direction.x < 0:
            if self.status != 'attack_left':
                self.frame_index = 0
            self.status = 'attack_left'
            self.direction = pygame.math.Vector2()
        
        elif distance <= self.attack_radius and self.can_attack and direction.x > 0:
            if self.status != 'attack_right':
                self.frame_index = 0
            self.status = 'attack_right'
            self.direction = pygame.math.Vector2()

        elif distance <= self.notice_radius and self.status != 'attack_right' and self.status != 'attack_left' and distance >= self.attack_radius:
                self.status = 'move'

        elif distance > self.attack_radius:
            self.status = 'idle'

        else:
            self.status = 'idle'
    
    def detect_collision(self, sprite1, sprite2, overlap=0.5):
        if sprite1.hitbox.colliderect(sprite2.hitbox):
            # Get the collision offset
            offset_x = sprite1.hitbox.x - sprite2.hitbox.x
            offset_y = sprite1.hitbox.y - sprite2.hitbox.y
            # Get the absolute values of the offsets
            abs_offset_x = abs(offset_x)
            abs_offset_y = abs(offset_y)
            # Check which axis has the largest offset
            if abs_offset_x > abs_offset_y:
                # Move the sprite on the x-axis
                if offset_x * overlap > 0:
                    sprite1.hitbox.right += 1
                else:
                    sprite1.hitbox.left -= 1
            else:
                # Move the sprite on the y-axis
                if offset_y * overlap > 0:
                    sprite1.hitbox.bottom -= 1
                else:
                    sprite1.hitbox.top += 1

    def get_damage(self, player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    
    

    def actions(self,player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]
        
        
        if (self.status == 'attack_left' or self.status == 'attack_right') and self.can_attack:
            
            if not self.has_casted:
                self.attack_time = pygame.time.get_ticks()
                self.cast_slimeball(direction)
                self.has_casted = True
                    
                
                
        if self.status != 'attack_left' and self.status != 'attack_right':
            self.has_casted = False

        if self.status == 'move':
            if distance > self.attack_radius:
                self.direction = direction

        else:
            self.direction = pygame.math.Vector2()

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)


    def cast_slimeball(self,direction):
        self.create_slimeball((self.rect.x,self.rect.y),direction)
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
            self.speed += self.resistance
    
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_death()
        self.cooldown()

    def enemy_update(self,player):
        
        self.get_status(player)
        self.actions(player)
        