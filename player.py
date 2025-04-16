import pygame
import circleshape
import constants
import bullet
import math
from bullet import Shot

class Player(circleshape.CircleShape):
    def __init__(self, x, y, shots):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.shots = shots
        self.shot_timer = 0
        self.lives = 3
        self.invincibility_timer = 0
        self.respawn_time = constants.PLAYER_RESPAWN_TIME
        self.max_speed = constants.PLAYER_MAX_SPEED
        self.acceleration = constants.PLAYER_ACCELERATION
        self.friction = constants.PLAYER_FRICTION

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.invincibility_timer > 0 and int(self.invincibility_timer * 5) % 2 == 0:
            pygame.draw.polygon(screen, (255, 0, 0), self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, (255, 192, 203), self.triangle(), 2)
        super().draw(screen)
    
    def rotate(self, dt, PLAYER_TURN_SPEED):
        self.rotation = self.rotation + (PLAYER_TURN_SPEED * dt)
    
    def update(self, dt):
        self.wrap_position()
        self.shot_timer -= dt
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * constants.PLAYER_TURN_SPEED, -1)
        if keys[pygame.K_d]:
            self.rotate(dt * constants.PLAYER_TURN_SPEED, 1)
        self.move(dt)
#        if keys[pygame.K_w]:
#            self.move(dt)
#        if keys[pygame.K_s]:
#            self.move(dt*-1)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        radians = math.radians(self.rotation + 90)
        forward = pygame.Vector2(math.cos(radians), math.sin(radians))
        keys = pygame.key.get_pressed()
        accelerating_forward = keys[pygame.K_w]
        accelerating_backward = keys[pygame.K_s]

        if accelerating_forward:
            self.velocity += forward * self.acceleration * dt
        if accelerating_backward:
            self.velocity -= forward * (self.acceleration * 0.7) * dt
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        

        if not accelerating_forward and not accelerating_backward:
            if self.velocity.length() > 0:
                friction_force = self.velocity.normalize() * self.friction * dt
                if friction_force.length() > self.velocity.length():
                    self.velocity = pygame.Vector2(0, 0)
                else:
                    self.velocity -= friction_force
        self.position += self.velocity * dt

#        self.position += forward * constants.PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_timer <= 0:
            new_shot = Shot(self.position.x, self.position.y)
            direction = pygame.Vector2(0, 1)
            direction = direction.rotate(self.rotation)
            new_shot.velocity = direction * constants.PLAYER_SHOOT_SPEED
            self.shots.add(new_shot)
            self.shot_timer = constants.PLAYER_SHOOT_COOLDOWN

    def hit(self):
        if self.invincibility_timer <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.position.x = constants.SCREEN_WIDTH / 2
                self.position.y = constants.SCREEN_HEIGHT / 2
                self.invincibility_timer = self.respawn_time
            return self.lives <= 0
        return False
