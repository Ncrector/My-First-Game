import pygame
from settings import *
from entity import Entity
from support import *

class Slime(Entity):

    def __init__(self,monster_name,pos,groups, obstacle_sprites):

        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy' 
        # graphics
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image_depth = 1
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
        self.fireball_can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1000
    
        """ self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp """

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
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        self.animation_speed = 0.05

        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        frame = animation[int(self.frame_index)]
        width, height = frame.get_size()
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
            self.speed = 1.5
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            self.direction = pygame.math.Vector2()
            self.can_attack = False

        elif distance <= self.notice_radius and self.status != 'attack':
                self.status = 'move'

        elif distance > self.attack_radius:
            self.status = 'idle'

        else:
            self.status = 'idle'
    
    def actions(self,player):
        distance, direction = self.get_player_distance_direction(player)
        
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            if distance > self.attack_radius:
                self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
    
    def update(self):
        self.move(self.speed)
        self.animate()
        