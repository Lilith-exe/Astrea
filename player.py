import pygame
import circleshape
import constants
import bullet
from bullet import Shot

class Player(circleshape.CircleShape):
    def __init__(self, x, y, shots):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shots

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 192, 203), self.triangle(), 2)
    
    def rotate(self, dt, PLAYER_TURN_SPEED):
        self.rotation = self.rotation + (PLAYER_TURN_SPEED * dt)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt*-1, constants.PLAYER_TURN_SPEED)
        if keys[pygame.K_d]:
            self.rotate(dt, constants.PLAYER_TURN_SPEED)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt*-1)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

    def shoot(self):
        print("Shooting!")
        new_shot = Shot(self.position.x, self.position.y)
        direction = pygame.Vector2(0, 1)
        direction = direction.rotate(self.rotation)
        new_shot.velocity = direction * constants.PLAYER_SHOOT_SPEED
        self.shots.add(new_shot)