from pygame import font
font.init()

# Colors
white = (255, 255, 255)
black = (0, 0,  0)
red = (219, 32, 32)
green = (0, 255, 0)
blue = (51, 161, 224)
sky_blue = (68, 233, 255)
ocean_blue = (28, 149, 255)

# Display variables
display_width = 800
display_height = 640
title = "Platformer"
FPS = 60

# Player variables
player_acc = 1
player_grav = 0.5

# Font variables
"""
font_file = "fonts/8-Bit-Madness.ttf"
smallfont = font.Font(font_file, 35)
medfont = font.Font(font_file, 50)
largefont = font.Font(font_file, 75)
hugefont = font.Font(font_file, 150)
"""
