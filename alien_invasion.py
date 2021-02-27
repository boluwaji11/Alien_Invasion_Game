import sys
import pygame

# Create the Alien Invasion class
#Overall class to manage game assets and behavior
class AlienInvasion:
    # Initialize game and create game resources
    def __init__(self):
        pygame.init()

        # Set screen size and game title
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

    # Create the function to start the main loop for the game
    def run_game(self):
        while True:
            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
