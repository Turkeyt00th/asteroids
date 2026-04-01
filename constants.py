SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_ACCELERATION = 400
PLAYER_FRICTION = 300
PLAYER_LIVES = 3
LINE_WIDTH = 2

POWERUP_RADIUS = 12
POWERUP_SHIELD = "shield"
POWERUP_SPEED = "speed"
POWERUP_BOMB = "bomb"
POWERUP_TYPES = [POWERUP_SHIELD, POWERUP_SPEED, POWERUP_BOMB]
POWERUP_DURATION = 5.0
POWERUP_SPEED_MULTIPLIER = 1.5
POWERUP_SPAWN_CHANCE = 0.2

BOMB_RADIUS = 8
BOMB_SPEED = 400
BOMB_COOLDOWN_SECONDS = 0.5
BOMB_EXPLOSION_RADIUS = PLAYER_RADIUS * 10

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

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3
DIFFICULTY_EXTREME = 4
DIFFICULTY_NAMES = {
    DIFFICULTY_EASY: "Easy",
    DIFFICULTY_MEDIUM: "Medium",
    DIFFICULTY_HARD: "Hard",
    DIFFICULTY_EXTREME: "Extreme",
}
DIFFICULTY_SETTINGS = {
    DIFFICULTY_EASY: {
        "spawn_rate": 1.2,
        "speed_min": 40,
        "speed_max": 70,
        "initial_asteroids": 3,
    },
    DIFFICULTY_MEDIUM: {
        "spawn_rate": 0.8,
        "speed_min": 50,
        "speed_max": 90,
        "initial_asteroids": 5,
    },
    DIFFICULTY_HARD: {
        "spawn_rate": 0.6,
        "speed_min": 70,
        "speed_max": 110,
        "initial_asteroids": 7,
    },
    DIFFICULTY_EXTREME: {
        "spawn_rate": 0.4,
        "speed_min": 90,
        "speed_max": 140,
        "initial_asteroids": 10,
    },
}