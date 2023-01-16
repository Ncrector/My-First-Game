import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups,):  
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.image_depth = 1
        direction = player.status.split('_')[0]
        
    
        # graphics
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        image_width, image_height = self.image.get_size()

        scale_factor = 0.5
        scaled_width = int(image_width * scale_factor)
        scaled_height = int(image_height * scale_factor)

        if 'up' in direction or 'down' in direction:
            self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.rect = pygame.Rect((0,0),(scaled_width,scaled_height))
        else:
            self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.rect = pygame.Rect((0,0),(scaled_width,scaled_height))
       

        
        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 5))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 3))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(5, 8))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-7, -10))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)          