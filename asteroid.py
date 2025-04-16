import pygame
import circleshape
import constants
import random

class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
          super().__init__(x, y, radius)
        
    def draw(self, screen):
            pygame.draw.circle(screen, (195,177,225), (self.position.x, self.position.y), self.radius, 2)
        
    def update(self, dt):
          self.position += self.velocity * dt

    def split(self):
          self.kill()
          if self.radius <= constants.ASTEROID_MIN_RADIUS:
                return
          else:
                random_angle = random.uniform(20, 50)
                new_velocity_1 = self.velocity.rotate(random_angle)
                new_velocity_2 = self.velocity.rotate(-random_angle)
                new_radius = self.radius - constants.ASTEROID_MIN_RADIUS
                new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
                new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
                new_asteroid_1.velocity = new_velocity_1 * 1.2
                new_asteroid_2.velocity = new_velocity_2 * 1.2
          
