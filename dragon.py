import pygame
from settings import *
from entity import Entity
from support import *
from pygame.math import Vector2
from random import randint
from particles import *


class Dragon(Entity):
    def __init__(self,monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, create_fireball):
        super().__init__(groups)
        self.sprite_type = 'enemy' 
          
        # graphics
        monster_name = 'dragon'
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image_depth = 1
        self.image = self.animations[self.status][self.frame_index]
        # resize image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites
    
        # stats
        self.monster_name = 'dragon'
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # fireball stats
        self.create_fireball = create_fireball
        self.sounds = {
        'flame':pygame.mixer.Sound('audio/Fire.wav')
        }
        self.sounds['flame'].set_volume(0.1)
        self.fireball_speed = .5
        self.fire_ball_coowldown = 3000
        self.fireball_damage = 30

        # player interaction
        self.can_attack = True
        self.fireball_can_attack = True
        self.attack_time = None
        self.attack_cooldown = 5000
    
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

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
        self.animations = {'idle':[],'move_left':[],'move_right':[],'attack':[],'fireball':[],}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
            self.speed = 1.5
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def actions(self,player):
        distance, direction = self.get_player_distance_direction(player)
        
        if self.status == 'attack':
            self.attack_type = 'claw'
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'fireball':
            animation_type = 'fireball'
            self.attack_type = 'flame'
            self.attack_time = pygame.time.get_ticks()
            pos = self.rect.x,self.rect.y

            self.create_fireball(pos, animation_type)
            self.sounds['flame'].play()
            self.damage_player(self.attack_damage,self.attack_type)

        elif self.status == 'move_left' or self.status == 'move_right':
            if distance > self.attack_radius:
                self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            self.direction = pygame.math.Vector2()
            self.can_attack = False
        
        elif distance <= self.notice_radius and self.status != 'attack' and self.fireball_can_attack:
            if self.status != 'fireball':
                self.frame_index = 0
            self.status = 'fireball'
            self.direction =pygame.math.Vector2()
            self.fireball_can_attack = False

        elif distance <= self.notice_radius and self.status != 'attack' and self.status != 'fireball':
            if direction.x > 0:
                self.status = 'move_right'
            elif direction.x < 0:
                self.status = 'move_left'

        elif distance > self.attack_radius:
            self.status = 'idle'

        else:
            self.status = 'idle'
        
        if self.status == 'fireball':
            print(self.status)
    
    def animate(self):

        if self.status == 'fireball':
            self.animation_speed = 0.01
        else:
            self.animation_speed = 0.05

        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            if self.status == 'fireball':
                self.fireball_can_attack = False
            self.frame_index = 0

        frame = animation[int(self.frame_index)]
        width, height = frame.get_size()
        frame = pygame.transform.scale(frame, (width * 2, height * 2))
        self.image = frame
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_damage(self, player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
    
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
        
        if not self.fireball_can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.fireball_can_attack = True

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
            self.speed += self.resistance

   


    """ def shoot_fireball(self, player,groups):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]
        # Create a fireball sprite and add it to the sprite group
        self.attack_time = pygame.time.get_ticks()
        for i in range(1,6):
            if self.direction.x: #horizontal
                offset_x = (self.direction.x * i) * TILESIZE
                x = self.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                y = self.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('fireball',(x,y),groups)
            else: # vertical
                offset_y = (self.direction.y * i) * TILESIZE
                x = self.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = self.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles('fireball',(x,y),groups) """
    
             
        
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)

""" class Fireball(Entity):

    def __init__(self, pos, speed, damage, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40, 40))  # Replace this with the fireball graphic
        self.image.fill((255, 0, 0))  # Replace this with the fireball color
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.damage = damage
        self.hitbox = self.rect.inflate(0, -20)
        self.velocity = Vector2()
    
    def update(self):
        self.rect.move_ip(self.velocity)
        # Check if the fireball has gone off the screen
        if self.attack_time > 500:
            self.kill() """