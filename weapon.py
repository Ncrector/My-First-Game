import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.image_depth = 1
        direction = player.status.split('_')[0]
        

        # graphics
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if 'up' in direction or 'down' in direction:
            self.image = pygame.transform.scale(self.image, (12, 22))
            self.rect = pygame.Rect((0,0),(12,22))
        else:
            self.image = pygame.transform.scale(self.image, (22, 12))
            self.rect = pygame.Rect((0,0),(22,12))

        
        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 8))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 8))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0, 8))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0, 8))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)