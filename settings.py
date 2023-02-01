import pygame
# game setup
WIDTH = 960
HEIGHT = 540
FPS = 60
TILESIZE = 32

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 50
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


# weapons
weapon_data = {
    'sword': {'cooldown': 250, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 500, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'}}

# magic
magic_data = {
    'flame': {'strength': 15,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}


# enemy
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 1.5, 'resistance': 5, 'attack_radius': 40, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 5, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':150,'damage':6,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 20, 'notice_radius': 350},
    'slime': {'health': 70,'exp':150,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 1, 'resistance': 5, 'attack_radius': 200, 'notice_radius': 400},
    'dragon': {'health': 500,'exp':1000,'damage':6,'attack_type': 'claw', 'attack_sound':'audio/attack/slash.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 180, 'notice_radius': 400},}