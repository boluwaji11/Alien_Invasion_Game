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
        self.font = pygame.font.SysFont(None, 30)

        # Prepare the initial score images and level
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    # Turn the score into a rendered image
    def prep_score(self):
        rounded_score = round(self.stats.score, -1)  # round to the nearest 10
        score_str = "Score: " + "{:,}".format(rounded_score)  # Add text and commas
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        # 20 pixel from the right of the screen
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # Turn the high score into a rendered image
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)  # round to the nearest 10
        # Add text and commas
        high_score_str = "High Score: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    # Turn the level into a rendered image
    def prep_level(self):
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = (
            self.score_rect.bottom + 10
        )  # 10 pixels below the current score

    # Check to see if there's a new high score
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # Draw scores and level to the screen
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)