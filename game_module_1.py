import pygame
import os

# colors
DARKRED = pygame.color.THECOLORS['darkred']
DARKGREEN = pygame.color.THECOLORS['darkgreen']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']
YELLOW = pygame.color.THECOLORS['yellow1']
BLACK = pygame.color.THECOLORS['black']
GRAY = pygame.color.THECOLORS['gray40']

# path
BLOCK = pygame.image.load(os.path.join('png', 'black.png'))
WALL = pygame.image.load(os.path.join('png', 'rock.png'))
PATH = pygame.image.load(os.path.join('png', 'yellow.png'))

# player
PLAYER = pygame.image.load(os.path.join('png', 'player.png'))
PLAYER_R = pygame.image.load(os.path.join('png', 'player_1.png'))
PLAYER_DOWN = pygame.image.load(os.path.join('png', 'player_2.png'))
PLAYER_L = pygame.image.load(os.path.join('png', 'player_3.png'))
PLAYER_UP = pygame.image.load(os.path.join('png', 'player_4.png'))

# my player textures
MY_PLAYER = pygame.image.load(os.path.join('png', 'my_player.png'))
MY_PLAYER_R = pygame.image.load(os.path.join('png', 'my_player_1.png'))
MY_PLAYER_DOWN = pygame.image.load(os.path.join('png', 'my_player_2.png'))
MY_PLAYER_L = pygame.image.load(os.path.join('png', 'my_player_3.png'))
MY_PLAYER_UP = pygame.image.load(os.path.join('png', 'my_player_4.png'))

# main window
SCREEN_SIZE = WIDTH, HEIGHT = 1440, 900
MAZE = pygame.image.load(os.path.join('png', 'maze.png'))
