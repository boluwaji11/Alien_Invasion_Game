import sys
from time import sleep  # Sleep() pauses the game for a moment

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # Create an instance to store game statistics,
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create an instance of the Ship class
        # Gives Ship class access to the game’s resources
        self.ship = Ship(self)

        # Add an instance of the Group class to manage the bullets
        self.bullets = pygame.sprite.Group()

        # Add an instance of the Group class to manage the aliens
        self.aliens = pygame.sprite.Group()

        # Helper method to hold the fleet of aliens
        self._create_fleet()

        # Make the Play button
        self.play_button = Button(self, "Play")

    # Create the function to start the main loop for the game
    def run_game(self):
        while True:
            # Call the helper method to check events
            self._check_events()

            # Parts of the game that should run only when game is active
            if self.stats.game_active:

                # Call the update method from the Ship class
                self.ship.update()

                # Call the bullet update method to update position of the bullet
                self._update_bullets()

                # Call the aliens update method to update position of the aliens
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    # Method to hold the mouse click on play button
    def _check_play_button(self, mouse_pos):
        # Start a new game when the player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()  # Resets the score back to 0

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

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

    # Update position of bullets and get rid of old bullets
    def _update_bullets(self):
        # Update bullet positions
        self.bullets.update()
        # Remove the fired bullets for performance and memory efficiency using a copy of the group of bullets
        for bullet in self.bullets.copy():
            # Check if the bullet has disappeared from screen
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        # Call the bullet-alien collision method
        self._check_bullet_alien_collisions()

    # Respond to bullet-alien collisions
    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullet and the alien in a dictionary created by groupcollide()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    # Respond to the ship being hit by an alien
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause by half a second
            sleep(0.5)
        else:
            self.stats.game_active = False

            # Make mouse visible
            pygame.mouse.set_visible(True)

    # Check if aliens have reached the bottom of the screen
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got it
                self._ship_hit()
                break

    # Update the positions of all aliens in the fleet
    def _update_aliens(self):
        # Check if the fleet is at an edge, then update the position of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alien hitting the bottom of the screen
        self._check_aliens_bottom()

    # Helper method for the fleet of aliens
    def _create_fleet(self):
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to on alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # Gets the alien's width and height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens and call the _create_alien method
        for row_number in range(number_rows):
            # Creates one row of aliens
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    # Helper method to create one row of aliens
    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # Gets the alien's width and height
        # Each alien is pushed one alien width to the left
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        # Set the current position of the alien's rect
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        # Add a group of aliens using add(). Similar to append()
        self.aliens.add(alien)

    # Check aliens on the edge of the screen
    def _check_fleet_edges(self):
        # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():  # This is True by default
                self._change_fleet_direction()
                break

    # Drop the fleet of aliens
    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1  # Moves kinda like a zigzag motion

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

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
