import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, POWERUP_TYPES, POWERUP_SPAWN_CHANCE
from explosion import Explosion
from logger import log_event
from powerup import PowerUp


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self._shape_points = []
        point_count = 10
        for i in range(point_count):
            angle = 360 / point_count * i
            offset = random.uniform(-self.radius * 0.35, self.radius * 0.35)
            self._shape_points.append((angle, self.radius + offset))

    def draw(self, screen):
        points = []
        for angle, distance in self._shape_points:
            offset = pygame.Vector2(0, -1).rotate(angle) * distance
            points.append((self.position.x + offset.x, self.position.y + offset.y))

        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap()

    def bounce_off(self, other):
        if not self.collides_with(other):
            return

        displacement = self.position - other.position
        distance = displacement.length()
        if distance == 0:
            displacement = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            distance = displacement.length()

        normal = displacement / distance
        overlap = self.radius + other.radius - distance
        if overlap > 0:
            self.position += normal * (overlap / 2)
            other.position -= normal * (overlap / 2)

        relative_velocity = self.velocity - other.velocity
        impact_speed = relative_velocity.dot(normal)
        if impact_speed > 0:
            return

        impulse = normal * impact_speed
        self.velocity -= impulse
        other.velocity += impulse

    def split(self):
        Explosion(self.position.x, self.position.y)
        self.kill()

        if random.random() < POWERUP_SPAWN_CHANCE:
            PowerUp(self.position.x, self.position.y, random.choice(POWERUP_TYPES))

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        first_velocity = self.velocity.rotate(angle) * 1.2
        second_velocity = self.velocity.rotate(-angle) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first = Asteroid(self.position.x, self.position.y, new_radius)
        second = Asteroid(self.position.x, self.position.y, new_radius)
        first.velocity = first_velocity
        second.velocity = second_velocity
