import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, difficulty=DIFFICULTY_MEDIUM):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        difficulty_settings = DIFFICULTY_SETTINGS.get(
            difficulty, DIFFICULTY_SETTINGS[DIFFICULTY_MEDIUM]
        )
        self.spawn_rate = difficulty_settings["spawn_rate"]
        self.speed_min = difficulty_settings["speed_min"]
        self.speed_max = difficulty_settings["speed_max"]
        self.initial_asteroids = difficulty_settings["initial_asteroids"]

        for _ in range(self.initial_asteroids):
            self.spawn_random_edge()

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def spawn_random_edge(self):
        edge = random.choice(self.edges)
        speed = random.randint(self.speed_min, self.speed_max)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, ASTEROID_KINDS)
        self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            self.spawn_random_edge()
