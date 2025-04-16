import pygame
import constants

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, other_shape):
        return self.position.distance_to(other_shape.position) <= self.radius + other_shape.radius
    
    def wrap_position(self):
        screen_width = constants.SCREEN_WIDTH
        screen_height = constants.SCREEN_HEIGHT

        # Horizontal Wrapping
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

        # Verticle Wrapping
        if self.position.y < 0:
            self.position.y = screen_height
        elif self.position.y > screen_height:
            self.position.y = 0
