import pygame
from circleshape import CircleShape
from constants import POWERUP_RADIUS, POWERUP_SHIELD, POWERUP_SPEED, POWERUP_BOMB, LINE_WIDTH


class PowerUp(CircleShape):
    def __init__(self, x, y, kind):
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        if self.kind == POWERUP_SHIELD:
            color = "cyan"
        elif self.kind == POWERUP_SPEED:
            color = "yellow"
        else:
            color = "orange"

        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)

        icon_color = "black"
        if self.kind == POWERUP_SHIELD:
            pygame.draw.circle(screen, icon_color, self.position, self.radius // 2, LINE_WIDTH)
        elif self.kind == POWERUP_SPEED:
            points = [
                (self.position.x - 4, self.position.y + 4),
                (self.position.x + 4, self.position.y),
                (self.position.x - 4, self.position.y - 4),
            ]
            pygame.draw.polygon(screen, icon_color, points)
        else:
            points = [
                (self.position.x - 4, self.position.y - 4),
                (self.position.x + 4, self.position.y - 4),
                (self.position.x + 4, self.position.y + 4),
                (self.position.x - 4, self.position.y + 4),
            ]
            pygame.draw.polygon(screen, icon_color, points, LINE_WIDTH)

    def update(self, dt):
        pass
