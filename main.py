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

import pygame
import constants
import asteroid 
import player
import asteroidfield
import sys
import bullet
import time
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Shot
from ui import UI



def main():
    pygame.init()
    print("Starting Asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Groups setup
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group() 

    # Container assignments   
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (updatable, drawable, asteroids)
    Shot.containers = (updatable)

    # Reset handler
    def reset_game():
        nonlocal score, game_over, player, asteroid_field
        score = 0
        game_over = False
        asteroids.empty()
        shots.empty()
        drawable.empty()
        updatable.empty()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)  
        asteroid_field = AsteroidField()
        return player, asteroids, shots    

    # Initialize variables  
    score = 0
    ui = UI()
    dt = 0
    respawn_time = PLAYER_RESPAWN_TIME
    shot_timer = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots) 
    asteroid_field = AsteroidField() 
    running = True 
    game_over = False
    player, asteroids, shots = reset_game() 

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   
            if not game_over:
                pass
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        player, asteroids, shots = reset_game()
        if not game_over: 
            # Draw section  
            screen.fill(color=(31,31,31))
            ui.draw_score(screen, score, 10, 10)
            ui.draw_lives(screen, player)
            for item in drawable:
                item.draw(screen)
            # Update handler
            updatable.update(dt)
            # Collision handler
            for asteroid in asteroids:
                if player.collision(asteroid):
                    if player.invincibility_timer <=0:
                        game_over = player.hit()
                        if not game_over:
                            asteroid.kill()
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collision(asteroid):
                        asteroid.split()
                        shot.kill()
                        score += ASTEROID_POINTS
            for shot in shots:
                shot.draw(screen)
        if game_over:
            screen.fill((31,31,31))
            ui.draw_game_over(screen, score, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip() 
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
