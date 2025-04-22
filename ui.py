import pygame.font
import constants
import player
import version
import game_data
import pygame

pygame.font.init()

class UI:
    def __init__(self):
        self.version = version.VERSION
        self.base_width = 1280
        self.base_height = 720
        self.title_font_size = 172
        self.heading_font_size = 52
        self.base_font_size = 36
        self.version_font_size = 20

        self.update_scale()

    def update_scale(self, resolution=None):
        if resolution == None:
            resolution = pygame.display.get_surface().get_size()
        
        self.scale_x = resolution[0] / self.base_width
        self.scale_y = resolution[1] / self.base_height
        self.scale = min(self.scale_x, self.scale_y)

        self.update_fonts()

    def update_fonts(self):
        self.font = pygame.font.SysFont("Copperplate Gothic", int(self.base_font_size * self.scale))
        self.title_font = pygame.font.SysFont("Copperplate Gothic", int(self.title_font_size * self.scale), bold=1)
        self.version_font = pygame.font.SysFont("Lucida Console", int(self.version_font_size * self.scale))
        self.heading_font = pygame.font.SysFont("Copperplate Gothic", int(self.heading_font_size * self.scale), bold=1)
        

    def scale_position(self, x, y):
#        scaled_x = x * self.scale_x
#        scaled_y = y * self.scale_y
#        return scaled_x, scaled_y
        return (int(x * self.scale), int(y * self.scale))
    
    def scale_rect(self, rect):
        scaled_rect = pygame.Rect(
            int(rect.x * self.scale_x),
            int(rect.y * self.scale_y),
            int(rect.width * self.scale_x),
            int(rect.height * self.scale_y)
        )
        return scaled_rect


    def draw_version(self, screen):
        version_text = self.version_font.render(f"v{self.version}", True, (70, 70, 70))
        screen_width, screen_height = screen.get_size()
        pos = self.scale_position(screen_width - 10, screen_height - 10)
        version_rect = version_text.get_rect(bottomright = pos)
        screen.blit(version_text, version_rect)
        


    def draw_score(self, screen, score, x, y):
        score_text = self.font.render(f"Score: {score}", True, (255, 192, 203))
        pos = self.scale_position(x, y)
        screen.blit(score_text, pos)

    def draw_game_over(self, screen, score, x, y):
        center_pos = self.scale_position(x, y)
        text_pos = self.scale_position(x, y - 60)
        score_pos = self.scale_position(x, y - 20)
        reset_pos = self.scale_position(x, y + 100)

        game_over_text = self.font.render("GAME OVER!", True, (255, 192, 203))
        text_rect = game_over_text.get_rect(center = text_pos)
        screen.blit(game_over_text, text_rect)

        final_score_text = self.font.render(f"Final Score: {score}", True, (255, 192, 203))
        score_rect = final_score_text.get_rect(center = score_pos)
        screen.blit(final_score_text, score_rect)

        reset_text = self.font.render("Press 'R' to reset", True, (195, 177, 225))
        reset_rect = reset_text.get_rect(center = reset_pos)
        screen.blit(reset_text, reset_rect)

    def draw_start_screen(self, screen, x, y):
        title_pos = self.scale_position(x, y - (120* self.scale))
        options_pos = self.scale_position(10, 10)

        title_text = self.title_font.render("ASTREA", True, (255, 192, 203))
        title_rect = title_text.get_rect(center = title_pos)
        screen.blit(title_text, title_rect)

        start_options = self.font.render("Highscores (H) | Settings (O)", True, (255, 192, 203))
        screen.blit(start_options, options_pos)

    def draw_start_text(self, screen):
        base_width = self.base_width
        base_height = self.base_height
        center_pos = self.scale_position(base_width // 2, base_height // 2 + (100 * self.scale))
        start_text = self.font.render("Press F to Start", True, (195, 177, 225))
        start_text_rect = start_text.get_rect(center = center_pos)
        screen.blit(start_text, start_text_rect)

    def draw_settings_menu(self, screen, options, selected_option, settings, name_selected=False, flash_visible=True):
        screen.fill((31, 31, 31))
        base_width = self.base_width
        base_height = self.base_height
        header_pos = self.scale_position(base_width // 2, 80)
        left_margin = self.scale_position(base_width // 2 - base_width // 2, 0)[0]
        settings_text = self.heading_font.render("Settings", True, (255, 192, 203))
        settings_text_rect = settings_text.get_rect(center = header_pos)
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
            option_pos = self.scale_position(left_margin, 150 + i * 50)
            screen.blit(settings_body, option_pos)


    def draw_lives(self, screen, player):
        base_life_x = self.base_width - 30
        base_life_y = 30
        life_x, life_y = self.scale_position(base_life_x, base_life_y)
        triangle_size = 10 * self.scale
        side_size = 5 * self.scale
        spacing = 25 * self.scale

        # Create triangle
        for i in range(player.lives):
            forward = pygame.Vector2(0, 1).rotate(-90)
            right = pygame.Vector2(0, 1).rotate(0) * side_size
            a = pygame.Vector2(life_x, life_y) + forward * triangle_size
            b = pygame.Vector2(life_x, life_y) - forward * triangle_size - right
            c = pygame.Vector2(life_x, life_y) - forward * triangle_size + right
            # Draw lives indicator
            pygame.draw.polygon(screen, (255, 192, 203), [a, b, c], 2)
            # Space horizontally
            life_x -= spacing