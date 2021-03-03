import pygame
from pygame.sprite import Sprite

# Sprite group related elements in the game and act on all the grouped elements at once

# A class to manage bullets fired from the ship
class Bullet(Sprite):
    def __init__(self, ai_game):
        # Create a bullet object at the ship's current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    # Manages the bullet's position
    def update(self):
        # Update the decimal position of the bullet and move the bullet up the screen
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    # Draw the bullet to the screen
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)