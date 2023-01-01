import pygame, sys
from level import Level
from settings import *
from debug import *

class Game:
    def __init__(self):
      
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Adventure Game")
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.game_over_sound_played = False
   
    def run(self):
      
      main_sound = pygame.mixer.Sound('audio/Epic1x.wav')
      main_sound.set_volume(0.2)
      main_sound.play(loops = -1)

      while True:
        for event in pygame.event.get():

          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
              self.level.toggle_menu()

          # game over sequence
          if self.level.get_players_health() <= 0:
              self.level.game_paused = True
              main_sound.stop()
              
              if not self.game_over_sound_played:  # Only play the game over sound if it hasn't been played already
                  game_over_sound = pygame.mixer.Sound('audio/NoHope.wav')
                  game_over_sound.set_volume(.5)
                  game_over_sound.play(loops=0)
                  self.game_over_sound_played = True  # Set the flag to True after playing the sound
            
        self.screen.fill('black')
        self.level.run()
        pygame.display.update()
        self.clock.tick(FPS)

        if self.level.game_over == True:
            game_over_sound.stop()
            game = Game()
            game.run()                

if __name__ == '__main__':
  game = Game()
  game.run()