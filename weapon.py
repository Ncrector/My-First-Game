import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.image_depth = 1
        direction = player.status.split('_'[0])
        

        # graphics
        self.image = pygame.Surface((20,20))

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        else:
            self.rect = self.image.get_rect(center = player.rect.center)