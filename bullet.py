import pygame
import circleshape
import constants
from constants import SHOT_RADIUS

class Shot(circleshape.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
            
    def draw(self, screen):
        pygame.draw.circle(screen, (179,235,242), (self.position.x, self.position.y), self.radius, 2)
#        super().draw(screen)
        
    def update(self, dt):
#        self.lifetime -= dt
#        if self.lifetime <= 0:
#            self.alive = False
#            return
        self.position += self.velocity * dt
#        self.wrap_position()