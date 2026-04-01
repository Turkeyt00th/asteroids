import sys

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_PER_ASTEROID, PLAYER_LIVES
from logger import log_event, log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from explosion import Explosion


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)

    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print("Screen width:",SCREEN_WIDTH)
    print("Screen height:",SCREEN_HEIGHT)

    score = 0
    lives = PLAYER_LIVES
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Explosion.containers = (updatable, drawable)

    clock = pygame.time.Clock()
    dt = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)

        asteroid_list = list(asteroids)
        for i in range(len(asteroid_list)):
            for j in range(i + 1, len(asteroid_list)):
                asteroid_list[i].bounce_off(asteroid_list[j])

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                lives -= 1
                if lives <= 0:
                    print(f"Game over! Score: {score}")
                    sys.exit()
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.rotation = 0
                player.shoot_cooldown_timer = 0
                break

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += SCORE_PER_ASTEROID
                    asteroid.split()
                    shot.kill()

        for powerup in list(powerups):
            if player.collides_with(powerup):
                player.apply_powerup(powerup.kind)
                log_event(f"powerup_{powerup.kind}")
                powerup.kill()

        for sprite in drawable:
            sprite.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surface, (10, 10))
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_surface, (10, 40))
        weapon_surface = font.render(f"Weapon: {player.weapon_type}", True, "white")
        screen.blit(weapon_surface, (10, 70))
        shield_surface = font.render(
            f"Shield: {'ON' if player.shield_active else 'OFF'}", True, "white"
        )
        screen.blit(shield_surface, (10, 100))
        speed_surface = font.render(
            f"Speed Boost: {round(player.speed_boost_timer, 1)}", True, "white"
        )
        screen.blit(speed_surface, (10, 130))
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
