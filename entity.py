import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        
        if self.direction.x > 0:
            self.hitbox.x += 1 * speed
        elif self.direction.x < 0:
            self.hitbox.x += -1 * speed
        self.collision('horizontal')

        
        if self.direction.y > 0:
            self.hitbox.y += 1 * speed
        elif self.direction.y < 0:
            self.hitbox.y += -1 * speed   
        self.collision('vertical')

        self.rect.center = self.hitbox.center
        

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: 
            return 255
        else: 
            return 0