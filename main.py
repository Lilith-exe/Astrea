# Planned updates:
# Weapon powerups
# Shield powerups (rainbow?)
# Triangular hitbox
# High score system
# More visuals
# Audio
# Start screen
# Difficulty progression
# Hardcore mode (asteroids wrap)
# Invulnerability when wrapping
# Resolution select

import enum
import pygame
import constants
import asteroid 
import player
import asteroidfield
import sys
import bullet
import time
import version
import game_data
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Shot
from ui import UI
from game_data import save_game_data, load_game_data, settings_menu

class GameState(enum.Enum):
    START_SCREEN = 0
    PLAYING = 1
    HIGH_SCORES = 2
    SETTINGS = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        self.state = GameState.START_SCREEN
        pygame.init()
        pygame.display.set_caption(f"Astrea - v{version.VERSION}")
        game_data = load_game_data()
        self.high_score = game_data["high_score"]
        self.settings = game_data["settings"]
        print("Starting Asteroids!")
        print("Resolution:", self.settings["resolution"])
        self.screen = pygame.display.set_mode(self.settings["resolution"])
        self.clock = pygame.time.Clock()
        # Flash timer for start screen
        self.flash_timer = 0
        self.show_start_text = True
        self.flash_speed = 0.5


        # Groups setup
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group() 

        # Container assignments   
        Player.containers = (self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        Shot.containers = (self.updatable)   

        # Initialize variables  
        self.score = 0
        self.ui = UI()
        self.dt = 0
        self.respawn_time = PLAYER_RESPAWN_TIME
        self.shot_timer = 0
        self.running = True 
        self.game_over = False

    # Reset handler
    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.asteroids.empty()
        self.shots.empty()
        self.drawable.empty()
        self.updatable.empty()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.shots)  
        self.asteroid_field = AsteroidField()
        self.state = GameState.PLAYING          

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
            elif self.state == GameState.START_SCREEN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_o:
                        self.settings = settings_menu(self.screen, self.settings, self.high_score)
                        self.state = GameState.START_SCREEN
            elif self.state == GameState.SETTINGS:
                pass
        
    def update(self, dt):
        self.dt = dt
        self.updatable.update(dt)
        if self.state == GameState.PLAYING and not self.game_over:
            # Collision handler
            for asteroid in self.asteroids:
                if self.player.collision(asteroid):
                    if self.player.invincibility_timer <=0:
                        self.game_over = self.player.hit()
                        if self.game_over:
                            self.state = GameState.GAME_OVER
                        if not self.game_over:
                            asteroid.kill()
            for asteroid in self.asteroids:
                for shot in self.shots:
                    if shot.collision(asteroid):
                        asteroid.split()
                        shot.kill()
                        self.score += ASTEROID_POINTS
        if self.state == GameState.START_SCREEN:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_speed:
                self.flash_timer = 0
                self.show_start_text = not self.show_start_text

    def render(self):
        self.screen.fill(color=(31, 31, 31))

        if self.state == GameState.START_SCREEN:
            self.ui.draw_start_screen(self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            if self.show_start_text:
                self.ui.draw_start_text(self.screen)
        
        elif self.state == GameState.PLAYING:
            self.ui.draw_score(self.screen, self.score, 10, 10)
            self.ui.draw_lives(self.screen, self.player)
            for item in self.drawable:
                item.draw(self.screen)
            for shot in self.shots:
                shot.draw(self.screen)

        elif self.state == GameState.SETTINGS:
            pass
        
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_game_over(self.screen, self.score, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.ui.draw_version(self.screen)        
        pygame.display.flip()

    def run(self):
        self.running = True

        while self.running:
            self.handle_events()
            dt = self.clock.tick(60) / 1000
            self.update(dt)
            self.render()

        pygame.quit()

def main():
    # Game loop
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
