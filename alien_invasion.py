import sys
import pygame

from settings import Settings
from ship import Ship

# Create the Alien Invasion class
# Overall class to manage game assets and behavior
class AlienInvasion:
    # Initializes background settings
    def __init__(self):
        pygame.init()
        self.settings = Settings()  # An instance of the Settings class

        # Set screen size and game title
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Set the background color
        # self.bg_color = (230, 230, 230) # Not needed since already initialized in the Settings module

        # Create an instance of the Ship class
        # Gives Ship class access to the game’s resources
        self.ship = Ship(self)

    # Create the function to start the main loop for the game
    def run_game(self):
        while True:
            # Call the helper method to check events
            self._check_events()

            # Call the update method from the Ship class
            self.ship.update()

            # Call the helper method to update the screen
            self._update_screen()

    def _check_events(self):
        # Respond to keypresses and mouse events
        for event in pygame.event.get():
            # Check if the player quit the game
            if event.type == pygame.QUIT:
                sys.exit()
            # Moves the ship right and ensures continuous movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.type == pygame.K_RIGHT:
                    self.ship.moving_right = False

    def _update_screen(self):
        # Update images on the screen, and flip to the new screen.

        # Fill the screen with the background color
        self.screen.fill(self.settings.bg_color)

        # Draw the ship on the screen
        self.ship.blitme()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
