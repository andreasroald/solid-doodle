import pygame

# Initialize pygame so that sounds can load
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# -- IMAGES --
menu_background = pygame.image.load("sprites/backgrounds/menu_bg.png")
brick_background = pygame.image.load("sprites/backgrounds/brick_bg.png")
