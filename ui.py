import pygame.font
import constants
import player

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)

    def draw_score(self, screen, score, x, y):
        score_text = self.font.render(f"Score: {score}", True, (255, 192, 203))
        screen.blit(score_text, (x, y))

    def draw_game_over(self, screen, score, x, y):
        game_over_text = self.font.render("GAME OVER!", True, (255, 192, 203))
        text_rect = game_over_text.get_rect(center=(x, y - 60))
        screen.blit(game_over_text, text_rect)

        final_score_text = self.font.render(f"Final Score: {score}", True, (255, 192, 203))
        score_rect = final_score_text.get_rect(center=(x, y - 20))
        screen.blit(final_score_text, score_rect)

        reset_text = self.font.render("Press 'R' to reset", True, (195,177,225))
        reset_rect = reset_text.get_rect(center=(x, y + 100))
        screen.blit(reset_text, reset_rect)

    def draw_lives(self, screen, player):
        life_x = constants.SCREEN_WIDTH - 30
        life_y = 30
        # Create triangle
        for i in range(player.lives):
            forward = pygame.Vector2(0, 1).rotate(-90)
            right = pygame.Vector2(0, 1).rotate(0) * 5
            a = pygame.Vector2(life_x, life_y) + forward * 10
            b = pygame.Vector2(life_x, life_y) - forward * 10 - right
            c = pygame.Vector2(life_x, life_y) - forward * 10 + right
            # Draw lives indicator
            pygame.draw.polygon(screen, (255, 192, 203), [a, b, c], 2)
            # Space horizontally
            life_x -= 25