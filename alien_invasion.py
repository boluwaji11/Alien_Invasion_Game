import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# Overall class to manage game assets and behavior
class AlienInvasion:
    # Initializes background settings
    def __init__(self):
        pygame.init()
        self.settings = Settings()  # An instance of the Settings class

        # Set screen size to fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Set screen size to window size and game title
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance of the Ship class
        # Gives Ship class access to the game’s resources
        self.ship = Ship(self)

        # Add an instance of the Group class to manage the bullets
        self.bullets = pygame.sprite.Group()

        # Add an instance of the Group class to manage the aliens
        self.aliens = pygame.sprite.Group()

        # Helper method to hold the fleet of aliens
        self._create_fleet()

    # Create the function to start the main loop for the game
    def run_game(self):
        while True:
            # Call the helper method to check events
            self._check_events()

            # Call the update method from the Ship class
            self.ship.update()

            # Call the bullet update method to update position of the bullet
            self._update_bullets()

            # Call the helper method to update the screen
            self._update_screen()

    # Method to hold the various key events
    def _check_events(self):
        # Respond to keypresses and mouse events
        for event in pygame.event.get():
            # Quit the game using the close (X) button
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Call the keydown helper method
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # Call the keyup helper method
                self._check_keyup_events(event)

    # Method to hold the KEYDOWN events
    def _check_keydown_events(self, event):
        # Respond to keypresses
        # Moves the ship to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # Moves the ship left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Quit the game with a shortcut
        elif event.key == pygame.K_q:
            sys.exit()
        # Fire the bullet with the spacebar using the helper method
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Method to hold the KEYUP events
    def _check_keyup_events(self, event):
        # Respond to key release
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Helper method to create a new bullet and add it to the bullets group
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            # Create an instance of the Bullet class
            new_bullet = Bullet(self)
            # Add a group of bullets using add(). Similar to append()
            self.bullets.add(new_bullet)

    # Update position of bullets and get ride of old bullets
    def _update_bullets(self):
        # Update bullet positions
        self.bullets.update()
        # Remove the fired bullets for performance and memory efficiency using a copy of the group of bullets
        for bullet in self.bullets.copy():
            # Check if the bullet has disappeared from screen
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

    # Helper method to create a new aliens and add it to the fleet of aliens
    def _create_fleet(self):
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to on alien width
        alien = Alien(self)
        alien_width = alien.rect.width  # Gets the alien's width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create the first row of aliens
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            alien = Alien(self)
            # Each alien is pushed one alien width to the left
            alien.x = alien_width + 2 * alien_width * alien_number
            # Set the current position of the alien's rect
            alien.rect.x = alien.x
            # Add a group of aliens using add(). Similar to append()
            self.aliens.add(alien)

    # Update the screen
    def _update_screen(self):
        # Update images on the screen, and flip to the new screen.

        # Fill the screen with the background color
        self.screen.fill(self.settings.bg_color)

        # Draw the ship on the screen
        self.ship.blitme()

        # Draw the bullets on the screen from the bullet sprites
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the alien on the screen
        # The draw() method requires one argument:
        # a surface on which to draw the elements from the group.
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
