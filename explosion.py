import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, EXPLOSION_LIFETIME, EXPLOSION_MAX_RADIUS


class Explosion(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.age = 0.0

    def draw(self, screen):
        if self.radius > 0:
            pygame.draw.circle(screen, "white", self.position, int(self.radius), LINE_WIDTH)

    def update(self, dt):
        self.age += dt
        if self.age >= EXPLOSION_LIFETIME:
            self.kill()
            return

        self.radius = (self.age / EXPLOSION_LIFETIME) * EXPLOSION_MAX_RADIUS
