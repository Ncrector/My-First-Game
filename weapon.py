import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(center = player.rect.center)
        self.image_depth = 1
