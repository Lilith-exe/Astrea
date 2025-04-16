import pygame.font

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