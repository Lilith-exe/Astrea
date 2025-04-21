import pygame.font
import constants
import player
import version
import game_data
import pygame

pygame.font.init()

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("Copperplate Gothic", 36)
        self.title_font = pygame.font.SysFont("Copperplate Gothic", 172, bold=1)
        self.version_font = pygame.font.SysFont("Lucida Console", 20)
        self.heading_font = pygame.font.SysFont("Copperplate Gothic", 52, bold=1)
        self.version = version.VERSION

    def draw_version(self, screen):
        version_text = self.version_font.render(f"v{self.version}", True, (70, 70, 70))
        version_rect = version_text.get_rect(bottomright=(constants.SCREEN_WIDTH -10 , constants.SCREEN_HEIGHT -10))
        screen.blit(version_text, version_rect)
        


    def draw_score(self, screen, score, x, y):
        score_text = self.font.render(f"Score: {score}", True, (255, 192, 203))
        screen.blit(score_text, (x, y))

    def draw_game_over(self, screen, score, x, y):
#        self.screen.fill(color=(31, 31, 31))

        game_over_text = self.font.render("GAME OVER!", True, (255, 192, 203))
        text_rect = game_over_text.get_rect(center=(x, y - 60))
        screen.blit(game_over_text, text_rect)

        final_score_text = self.font.render(f"Final Score: {score}", True, (255, 192, 203))
        score_rect = final_score_text.get_rect(center=(x, y - 20))
        screen.blit(final_score_text, score_rect)

        reset_text = self.font.render("Press 'R' to reset", True, (195, 177, 225))
        reset_rect = reset_text.get_rect(center=(x, y + 100))
        screen.blit(reset_text, reset_rect)

    def draw_start_screen(self, screen, x, y):
        title_text = self.title_font.render("ASTREA", True, (255, 192, 203))
        title_rect = title_text.get_rect(center=(x, y - 120))
        screen.blit(title_text, title_rect)

        start_options = self.font.render("Highscores (H) | Settings (O)", True, (255, 192, 203))
        screen.blit(start_options, (10, 10))

    def draw_start_text(self, screen):
        start_text = self.font.render("Press F to Start", True, (195, 177, 225))
        start_text_rect = start_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + 100))
        screen.blit(start_text, start_text_rect)

    def draw_settings_menu(self, screen, options, selected_option, settings, name_selected=False, flash_visible=True):
        screen.fill((31, 31, 31))
        settings_text = self.heading_font.render("Settings", True, (255, 192, 203))
        settings_text_rect = settings_text.get_rect(center=(constants.SCREEN_WIDTH // 2, 80))
        screen.blit(settings_text, settings_text_rect)
        for i, option in enumerate(options):
            if i == 0:
                text = option.format(int(settings["sound_volume"] * 100))
            elif i == 1:
                text = option.format(settings["difficulty"])
            elif i == 2:
                text = option.format(settings["player_name"])
                if name_selected and flash_visible:
                    text += "|"                    
            elif i == 3:
                text = option.format(settings["resolution"][0], settings["resolution"][1])
            else:
                text = option
            color = (179, 235, 242) if i == selected_option else (195, 177, 225)
            settings_body = self.font.render(text, True, color)
            screen.blit(settings_body, (constants.SCREEN_WIDTH // 2 - constants.SCREEN_WIDTH // 2, 150 + i * 50))


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