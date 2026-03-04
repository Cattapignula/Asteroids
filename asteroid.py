import pygame
import random
import math
from logger import log_event
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self._generate_lumpy_points()
        self.mask = self._create_mask()
    
    def _generate_lumpy_points(self):
        points = []
        num_points = random.randint(8, 12)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            distance = self.radius * random.uniform(0.7, 1.0)
            
            point_x = distance * math.cos(angle)
            point_y = distance * math.sin(angle)
            points.append(pygame.Vector2(point_x, point_y))
        return points

    def _create_mask(self):
        size = int(self.radius * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        shifted_points = []
        for p in self.points:
            shifted_points.append((p.x + self.radius, p.y + self.radius))
            
        pygame.draw.polygon(surface, "white", shifted_points)
        return pygame.mask.from_surface(surface)

    def draw(self, screen):
        world_points = []
        for p in self.points:
            world_points.append(self.position + p)
            
        pygame.draw.polygon(screen, "white", world_points, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        self_top_left = (self.position.x - self.radius, self.position.y - self.radius)
        other_top_left = (other.position.x - other.radius, other.position.y - other.radius)
        offset = (other_top_left[0] - self_top_left[0], other_top_left[1] - self_top_left[1])
        return self.mask.overlap(other.mask, offset) is not None

    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            new_positive_vector = self.velocity.rotate(angle)
            new_negative_vector = self.velocity.rotate(-angle)
            self.new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, self.new_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, self.new_radius)
            new_asteroid_1.velocity = new_positive_vector * 1.2
            new_asteroid_2.velocity = new_negative_vector * 1.2
            

