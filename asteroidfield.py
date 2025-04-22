import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.screen = screen

    def get_edges(self, screen):
        screen_width, screen_height = screen.get_size()
        return [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * screen_height),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                screen_width + ASTEROID_MAX_RADIUS, y * screen_height
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * screen_width, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * screen_width, screen_height + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def spawn(self, radius, position, velocity, screen):
        screen_width, screen_height = screen.get_size()
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt, screen = None):
        if screen is None:
            screen = self.screen
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            edges = self.get_edges(screen)

            # spawn a new asteroid at a random edge
            edge = random.choice(edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, screen)