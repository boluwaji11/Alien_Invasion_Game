import pygame.font  # Lets pygame render text to screen


class Button:
    def __init__(self, ai_game, msg):
        # Initialize button attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # Bright green color
        self.text_color = (255, 255, 255)  # White color
        self.font = pygame.font.SysFont(None, 48)  # (Default font, font size)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once. Handles the text rendering on the button
        self._prep_msg(msg)