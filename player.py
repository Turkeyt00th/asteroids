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
    POWERUP_DURATION,
    POWERUP_SPEED_MULTIPLIER,
    POWERUP_SHIELD,
    POWERUP_SPEED,
    POWERUP_BOMB,
    BOMB_RADIUS,
    BOMB_SPEED,
    BOMB_COOLDOWN_SECONDS,
)
from shot import Shot
from bomb import Bomb

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0
        self.bomb_cooldown_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.weapon_type = WEAPON_DEFAULT
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_timer = 0
        self.bomb_count = 1

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def collides_with(self, other):
        circle_center = other.position
        circle_radius = other.radius
        triangle = self.triangle()

        if self._point_in_triangle(circle_center, triangle):
            return True

        for i in range(3):
            a = triangle[i]
            b = triangle[(i + 1) % 3]
            if self._distance_point_to_segment(circle_center, a, b) <= circle_radius:
                return True

        return False

    def _point_in_triangle(self, point, triangle):
        a, b, c = triangle

        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(point, a, b) < 0.0
        b2 = sign(point, b, c) < 0.0
        b3 = sign(point, c, a) < 0.0
        return (b1 == b2) and (b2 == b3)

    def _distance_point_to_segment(self, point, a, b):
        ab = b - a
        t = (point - a).dot(ab)
        ab_len_sq = ab.length_squared()
        if ab_len_sq != 0:
            t /= ab_len_sq
        t = max(0, min(1, t))
        closest = a + ab * t
        return point.distance_to(closest)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += direction * PLAYER_ACCELERATION * dt
        max_speed = PLAYER_SPEED * (POWERUP_SPEED_MULTIPLIER if self.speed_boost_timer > 0 else 1)
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def apply_friction(self, dt):
        if self.velocity.length_squared() == 0:
            return

        friction = PLAYER_FRICTION * dt
        speed = self.velocity.length()
        if friction >= speed:
            self.velocity = pygame.Vector2(0, 0)
        else:
            self.velocity.scale_to_length(speed - friction)

    def update_powerups(self, dt):
        if self.shield_active:
            self.shield_timer = max(self.shield_timer - dt, 0)
            if self.shield_timer <= 0:
                self.shield_active = False

        self.speed_boost_timer = max(self.speed_boost_timer - dt, 0)

    def select_weapon(self, weapon_type):
        self.weapon_type = weapon_type

    def drop_bomb(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        bomb = Bomb(self.position.x, self.position.y, BOMB_RADIUS)
        bomb.velocity = direction * BOMB_SPEED

    def apply_powerup(self, powerup_type):
        if powerup_type == POWERUP_SHIELD:
            self.shield_active = True
            self.shield_timer = POWERUP_DURATION
        elif powerup_type == POWERUP_SPEED:
            self.speed_boost_timer = POWERUP_DURATION
        elif powerup_type == POWERUP_BOMB:
            self.bomb_count += 1

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
        self.update_powerups(dt)
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

        if keys[pygame.K_b] and self.bomb_count > 0 and self.bomb_cooldown_timer <= 0:
            self.bomb_cooldown_timer = BOMB_COOLDOWN_SECONDS
            self.bomb_count -= 1
            self.drop_bomb()

        self.bomb_cooldown_timer = max(self.bomb_cooldown_timer - dt, 0)

    def draw(self, screen):
        if self.shield_active:
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 6, 1)
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)