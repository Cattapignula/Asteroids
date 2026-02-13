import pygame
import random
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * random.uniform(50, 150)
        
        self.max_lifetime = random.uniform(0.2, 0.5)
        self.lifetime = self.max_lifetime

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        ratio = self.lifetime / self.max_lifetime
        r = int(255 * ratio)
        g = int(165 * ratio)
        b = 0
        current_radius = self.radius * ratio
        pygame.draw.circle(screen, (r, g, b), self.position, current_radius)