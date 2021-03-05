# Ship module to manage most of the behavior of the player's ship
import pygame

# A class to manage the ship
class Ship:
    def __init__(self, ai_game):
        # Initialize the ship and set its starting position
        # ai_game -- current instance of the game
        self.screen = ai_game.screen

        # Initialize ship setting
        self.settings = ai_game.settings

        # Doing this allows us to place the ship in the correct location on the screen.
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position because
        # the speed is set as a decimal
        self.x = float(self.rect.x)

        # Movement flag to the right
        self.moving_right = False

        # Movement flag to the left
        self.moving_left = False

    # Update the ship's position based on the movement flag
    def update(self):
        # Two separate if blocks rather than an elif to allow the ship’s x value to be
        # increased and then decreased when both arrow keys are held down.

        # Update the x value of the ship and ensure the ship doesn't disappear from screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    # Center the ship on the screen
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)