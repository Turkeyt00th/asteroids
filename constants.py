SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_ACCELERATION = 400
PLAYER_FRICTION = 300
PLAYER_LIVES = 3
LINE_WIDTH = 2

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
WEAPON_NORMAL = "normal"
WEAPON_SPREAD = "spread"
WEAPON_HEAVY = "heavy"
WEAPON_RAPID = "rapid"
WEAPON_DEFAULT = WEAPON_NORMAL
WEAPON_SETTINGS = {
    WEAPON_NORMAL: {
        "radius": SHOT_RADIUS,
        "speed": PLAYER_SHOOT_SPEED,
        "cooldown": PLAYER_SHOOT_COOLDOWN_SECONDS,
        "count": 1,
        "spread": 0,
        "damage": 1,
    },
    WEAPON_SPREAD: {
        "radius": 4,
        "speed": 450,
        "cooldown": 0.8,
        "count": 3,
        "spread": 15,
        "damage": 1,
    },
    WEAPON_HEAVY: {
        "radius": 10,
        "speed": 350,
        "cooldown": 1.2,
        "count": 1,
        "spread": 0,
        "damage": 3,
    },
    WEAPON_RAPID: {
        "radius": 3,
        "speed": 650,
        "cooldown": 0.15,
        "count": 1,
        "spread": 0,
        "damage": 1,
    },
}
SCORE_PER_ASTEROID = 100
EXPLOSION_LIFETIME = 0.3
EXPLOSION_MAX_RADIUS = 40