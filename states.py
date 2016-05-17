import pygame
import random

import sprites
import settings
import resources

# State template class
class States(object):
    # Initialize the states class
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

# Level template class
class Level(States):
    # Initialize the game state
    def __init__(self):
        States.__init__(self)

        # If quit on exit is true, the game will reset instead of going to the next level when exiting
        self.quit_on_exit = False

    # Function that creates a level from a list and returns the level list
    def create_level(self, level, solid=True, bg=False):
        level_x = 0

        # Make the bottom-left tile aligned with the bottom-left of the screen
        if len(level) <= 20:
            level_y = 0
        else:
            level_y = 0 - (32 * (len(level) - 20))

        for rows in level:
            for cols in rows:
                if cols == -1:
                    w = sprites.Wall(level_x, level_y, 32, 32, color=settings.green)
                    self.exits.add(w)
                if "d" in str(cols):
                    w = sprites.Door(level_x, level_y, int(cols[1:]))
                    self.walls.add(w)
                    self.doors.add(w)
                if cols == 1:
                    w = sprites.Wall(level_x, level_y, 32, 32)
                    self.walls.add(w)

                level_x += 32
            level_x = 0
            level_y += 32

        return level

    # Starting the Level state
    def init_level(self, level):
        # Sprite groups
        self.exits = pygame.sprite.Group()
        self.magic = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        # Create the level and set current_level to its level list (used for camera movement)
        self.current_level = self.create_level(level)

        # Level borders
        self.left_border = sprites.Wall(-1, 0, 1, settings.display_height)
        self.walls.add(self.left_border)

        self.right_border = sprites.Wall(len(self.current_level[0]) * 32, 0, 1, settings.display_height)
        self.walls.add(self.right_border)

        # We blit surfaces to the world surface, then blit the world surface to the game display
        self.world_surface = pygame.Surface((len(self.current_level[0]) * 32, settings.display_height))

        # Camera variables
        self.cam_x_offset = 0

        # Screen shake variables
        self.shake_amount = 10

    # Common events function
    def events(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        if event.type == pygame.KEYDOWN:
            # Player jumping
            if event.key == pygame.K_j or event.key == pygame.K_SPACE:
                if self.player.jumping:
                    self.player.test_for_jump()
                else:
                    self.player.jump()

            # Go to next level if player is standing within the exit
            if event.key == pygame.K_w and self.player.in_exit:
                if not self.quit_on_exit:
                    self.done = True
                else:
                    self.quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.magic.add(self.player.attack(self))

    # Common updates function
    def updates(self):
        self.magic.update()
        self.doors.update()

        for x in self.doors:
            print(x.id)

        # Horizontal Camera scrolling
        self.cam_x_offset = self.player.rect.x - settings.display_width / 2

        if self.cam_x_offset < 0:
            self.cam_x_offset = 0

        if self.cam_x_offset > (len(self.current_level[0]) - 25) * 32:
            self.cam_x_offset = (len(self.current_level[0]) - 25) * 32

        # Slowly stop screen shake
        if self.shake_amount > 0:
            self.shake_amount -= 0.5

        # If player is out of view, reset the game
        if self.player.rect.top > settings.display_height:
            self.startup()

    # Common draws function
    def draws(self, screen):
        self.world_surface.fill(settings.white)

        # Draw the player, walls and exits
        self.exits.draw(self.world_surface)
        self.magic.draw(self.world_surface)
        self.walls.draw(self.world_surface)
        self.doors.draw(self.world_surface)
        self.player.draw(self.world_surface)

        # Blit the world surface to the main display
        # If shake amount is more than 0, blit the world at a random location between
        # negative and positive shake amount, instead of 0, 0
        if self.shake_amount > 0:
            screen.blit(self.world_surface, (random.randint(int(-self.shake_amount), int(self.shake_amount))-self.cam_x_offset,
                                                        random.randint(int(-self.shake_amount), int(self.shake_amount))))
        else:
            screen.blit(self.world_surface, (0-self.cam_x_offset, 0))

    # Test if the player is within an exit's boundaries
    def test_for_exits(self, player):
        for exits in self.exits:
            if exits.rect.colliderect(player.rect):
                self.player.in_exit = True
                break
            else:
                self.player.in_exit = False

# Menu state
class Menu(States):
    # Initialize the menu state
    def __init__(self):
        States.__init__(self)
        self.next = "level_1"

    # Cleaning up the menu state
    def cleanup(self):
        pass

    # Starting the menu state
    def startup(self):
        pass

    # State event handling
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.done = True


    # Update the menu state
    def update(self, display):
        display.blit(resources.menu_background, (0, 0))

    # Menu state drawing
    def draw(self, screen):
        screen.fill((settings.red))

# Level 1 state
class Level_1(Level):
    # Initialize the game state
    def __init__(self):
        Level.__init__(self)
        self.next = "level_2"

    # Cleaning up the game state
    def cleanup(self):
        pass

    # Starting the game state
    def startup(self):
        # Level list
        self.level_list = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # Initializing the common level variables
        self.init_level(self.level_list)

        # Creating an instance of the player
        self.player = sprites.Lightning_Wizard(50, 450, self.walls)

    # State event handling
    def get_event(self, event):
        self.events(event)


    # Update the game state
    def update(self, display):
        self.player.update()

        self.updates()

        self.test_for_exits(self.player)

        self.draw(display)

    # game state drawing
    def draw(self, screen):
        self.draws(screen)

# Level 2 state
class Level_2(Level):
    # Initialize the game state
    def __init__(self):
        Level.__init__(self)
        self.next = "menu"

    # Cleaning up the game state
    def cleanup(self):
        pass

    # Starting the game state
    def startup(self):
        # Level list
        self.level_list = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # Initializing the common level variables
        self.init_level(self.level_list)

        # Creating an instance of the player
        self.player = sprites.Lightning_Wizard(50, 450, self.walls)

    # State event handling
    def get_event(self, event):
        self.events(event)


    # Update the game state
    def update(self, display):
        self.player.update()

        self.updates()

        self.test_for_exits(self.player)

        self.draw(display)

    # game state drawing
    def draw(self, screen):
        self.draws(screen)

# Level 3 state
class Level_3(Level):
    # Initialize the game state
    def __init__(self):
        Level.__init__(self)
        self.next = "menu"

    # Cleaning up the game state
    def cleanup(self):
        pass

    # Starting the game state
    def startup(self):
        # Level list
        self.level_list = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        ]

        # Initializing the common level variables
        self.init_level(self.level_list)

        # Creating an instance of the player
        self.player = sprites.Lightning_Wizard(50, 450, self.walls)

    # State event handling
    def get_event(self, event):
        self.events(event)


    # Update the game state
    def update(self, display):
        self.player.update()

        self.updates()

        self.test_for_exits(self.player)

        self.draw(display)

    # game state drawing
    def draw(self, screen):
        self.draws(screen)

# List of all levels (used for randomizing level order)
def setup_list():
    return [Level_1(), Level_2(), Level_3()]

level_list = setup_list()
