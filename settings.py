# A class to store all settings for Alien Invasion
class Settings:
    # Initialize the game's static settings
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship speed setting. Ship moves by 1.5 pixels
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # Dark grey color
        self.bullets_allowed = 3  # limited bullets

        # Alien Settings
        self.fleet_drop_speed = 10  # Controls how quickly the fleet drops down

        # How quickly the game speeds up
        self.speedup_scale = 1.1  # Increases the speed at a reasonable pace

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Call the dynamic settings
        self.initialize_dynamic_settings()

    # Initialize settings that change throughout the game
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        # So the aliens move right at the beginning of a new game
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    # Increase speed settings and alien point values
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
