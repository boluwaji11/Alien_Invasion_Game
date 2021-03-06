# Track statistics for Alien Invasion
class GameStats:
    def __init__(self, ai_game):
        # Initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = True

    # Initialize statistics that can change during the game
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit