import pygame.font

# A class to report scoring information
class Scoreboard:
    # Initialize scorekeeping attributes
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()

    # Turn the score into a rendered image
    def prep_score(self):
        score_str = str(self.stats.score)  # converted to string
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        # 20 pixel from the right of the screen
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
