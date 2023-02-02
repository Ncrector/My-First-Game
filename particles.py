import pygame
from support import import_folder
from random import choice, randint
from settings import *

class AnimationPlayer:
    
    def __init__(self):
        self.frames = {
         # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            'fireball': import_folder ('graphics/particles/fireball'),
            'slimeball': import_folder('graphics/particles/slimeball'),
            

        # attacks 
        'claw': import_folder('graphics/particles/claw'),
        'slash': import_folder('graphics/particles/slash'),
        'sparkle': import_folder('graphics/particles/sparkle'),
        'leaf_attack': import_folder('graphics/particles/leaf_attack'),
        'thunder': import_folder('graphics/particles/thunder'),

        # monster deaths
        'squid': import_folder('graphics/particles/smoke_orange'),
        'raccoon': import_folder('graphics/particles/raccoon'),
        'spirit': import_folder('graphics/particles/nova'),
        'dragon': import_folder('graphics/particles/bamboo'),
        'slime': import_folder('graphics/particles/bamboo'),
        
        # leafs 
        'leaf': (
            import_folder('graphics/particles/leaf1'),
            import_folder('graphics/particles/leaf2'),
            import_folder('graphics/particles/leaf3'),
            import_folder('graphics/particles/leaf4'),
            import_folder('graphics/particles/leaf5'),
            import_folder('graphics/particles/leaf6'),
            self.reflect_images(import_folder('graphics/particles/leaf1')),
            self.reflect_images(import_folder('graphics/particles/leaf2')),
            self.reflect_images(import_folder('graphics/particles/leaf3')),
            self.reflect_images(import_folder('graphics/particles/leaf4')),
            self.reflect_images(import_folder('graphics/particles/leaf5')),
            self.reflect_images(import_folder('graphics/particles/leaf6'))
            )
        }

    def reflect_images(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        scaled_frames = []
        for frame in animation_frames:
            # Scale the image down by half
            scaled_frame = pygame.transform.scale(frame, (frame.get_width() // 2, frame.get_height() // 2))
            scaled_frames.append(scaled_frame)
        ParticleEffect(pos, scaled_frames,groups)
    
    def create_particles(self, animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        scaled_frames = []
        for frame in animation_frames:
            # Scale the image down by half
            scaled_frame = pygame.transform.scale(frame, (frame.get_width() // 2, frame.get_height() // 2))
            scaled_frames.append(scaled_frame)
        ParticleEffect(pos,scaled_frames,groups)
    
    def create_fireball(self, pos, direction, groups):
        animation_frames = self.frames['fireball']
        Fireball(pos, animation_frames, direction, groups)
    
    def create_slimeball(self,pos,direction,groups):
        animation_frames = self.frames['slimeball']
        Slimeball(pos,animation_frames,direction,groups)
    

class ParticleEffect(pygame.sprite.Sprite):
    
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.image_depth = 1
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update (self):
        self.animate()
    

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, direction, groups):
        
        super().__init__(groups)
        self.sprite_type = 'fire'
        self.frame_index = 0
        self.direction = direction
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        # creates the fireballs position depending direction facing
        if self.direction.x < 0:
            self.rect = self.image.get_rect(bottomleft = (pos[0] - 100, pos[1] + 100))
        else:
            self.rect = self.image.get_rect(bottomleft = (pos[0] + 110, pos[1] + 90))
        
        
        self.animation_speed = .15
        self.speed = 3  # Add a speed attribute
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update (self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.animate()

class Slimeball(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, direction, groups):
        
        super().__init__(groups)
        self.sprite_type = 'slime'
        self.frame_index = 0
        self.direction = direction
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        # creates the fireballs position depending direction facing
        self.speed = 3  # Add a speed attribute
        self.animation_speed = .15
        self.speed = 3  # Add a speed attribute
        if self.direction.x < 0:
            self.rect = self.image.get_rect(bottomleft = (pos[0] - 30, pos[1] + 25))
        else:
            self.rect = self.image.get_rect(bottomleft = (pos[0] + 25, pos[1] + 25))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    
    def update (self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.animate()