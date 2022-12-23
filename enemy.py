import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init_(self,monster_name,pos,groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'



        #graphics
        self.import_graphics(monster_name)
        self.status - 'idle'
        self.image_depth = 1
        self.image = self.animation[self.status][self.frame_index]
        #resize image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.infalte(0, -20)

    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
