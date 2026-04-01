import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
    SHOT_RADIUS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    WEAPON_DEFAULT,
    WEAPON_SETTINGS,
    WEAPON_NORMAL,
    WEAPON_SPREAD,
    WEAPON_HEAVY,
    WEAPON_RAPID,
)
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon_type = WEAPON_DEFAULT

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += direction * PLAYER_ACCELERATION * dt
        if self.velocity.length() > PLAYER_SPEED:
            self.velocity.scale_to_length(PLAYER_SPEED)

    def apply_friction(self, dt):
        if self.velocity.length_squared() == 0:
            return

        friction = PLAYER_FRICTION * dt
        speed = self.velocity.length()
        if friction >= speed:
            self.velocity = pygame.Vector2(0, 0)
        else:
            self.velocity.scale_to_length(speed - friction)

    def select_weapon(self, weapon_type):
        self.weapon_type = weapon_type

    def shoot(self):
        settings = WEAPON_SETTINGS[self.weapon_type]
        for i in range(settings["count"]):
            angle = 0
            if settings["count"] > 1:
                angle = -settings["spread"] * (settings["count"] - 1) / 2 + i * settings["spread"]
            direction = pygame.Vector2(0, 1).rotate(self.rotation + angle)
            shot = Shot(
                self.position.x,
                self.position.y,
                settings["radius"],
                settings["damage"],
            )
            shot.velocity = direction * settings["speed"]

    def update(self, dt):
        self.shoot_cooldown_timer = max(self.shoot_cooldown_timer - dt, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            self.select_weapon(WEAPON_NORMAL)
        if keys[pygame.K_2]:
            self.select_weapon(WEAPON_SPREAD)
        if keys[pygame.K_3]:
            self.select_weapon(WEAPON_HEAVY)
        if keys[pygame.K_4]:
            self.select_weapon(WEAPON_RAPID)

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        elif keys[pygame.K_s]:
            self.move(-dt)
        else:
            self.apply_friction(dt)

        self.position += self.velocity * dt
        self.wrap()

        if keys[pygame.K_SPACE] and self.shoot_cooldown_timer <= 0:
            self.shoot_cooldown_timer = WEAPON_SETTINGS[self.weapon_type]["cooldown"]
            self.shoot()

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)