import pygame
import sys
import math
import random
from enum import Enum
import json

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# ============================================
# HAL LABORATORY SUPER SMASH BROS 64 ENGINE
# ============================================

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GRAVITY = 0.9
MAX_FALL_SPEED = 18

# N64 Color Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
BLUE = (30, 30, 200)
GREEN = (30, 200, 30)
YELLOW = (255, 220, 0)
PURPLE = (200, 30, 200)
CYAN = (30, 200, 200)
ORANGE = (255, 140, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
N64_BLUE = (70, 90, 120)
N64_RED = (180, 60, 60)

# Game States
class GameState(Enum):
    INTRO = 1
    MAIN_MENU = 2
    CHARACTER_SELECT = 3
    STAGE_SELECT = 4
    BATTLE = 5
    PAUSE = 6
    RESULTS = 7
    OPTIONS = 8

class PlayerState(Enum):
    IDLE = 1
    WALKING = 2
    RUNNING = 3
    JUMPING = 4
    FALLING = 5
    ATTACKING = 6
    STUNNED = 7
    SHIELDING = 8
    DODGING = 9
    GRABBING = 10
    THROWN = 11

class MenuOption(Enum):
    SINGLE_PLAYER = 1
    VS_MODE = 2
    OPTIONS = 3
    DATA = 4

# ============================================
# STAGE DEFINITIONS - All 9 N64 Stages
# ============================================

class Stage:
    def __init__(self, name, stage_id, platforms, blast_zones, spawn_points, bg_color):
        self.name = name
        self.stage_id = stage_id
        self.platforms = platforms
        self.blast_zones = blast_zones  # left, right, top, bottom
        self.spawn_points = spawn_points
        self.bg_color = bg_color
        self.ground_y = 500

    def draw(self, screen):
        # Draw background
        screen.fill(self.bg_color)
        
        # Draw stage-specific elements
        if self.stage_id == "peachs_castle":
            self.draw_peachs_castle(screen)
        elif self.stage_id == "congo_jungle":
            self.draw_congo_jungle(screen)
        elif self.stage_id == "hyrule_castle":
            self.draw_hyrule_castle(screen)
        elif self.stage_id == "super_happy_tree":
            self.draw_yoshis_island(screen)
        elif self.stage_id == "dream_land":
            self.draw_dream_land(screen)
        elif self.stage_id == "sector_z":
            self.draw_sector_z(screen)
        elif self.stage_id == "planet_zebes":
            self.draw_planet_zebes(screen)
        elif self.stage_id == "saffron_city":
            self.draw_saffron_city(screen)
        elif self.stage_id == "mushroom_kingdom":
            self.draw_mushroom_kingdom(screen)
        
        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(screen, platform['color'], 
                           (platform['x'], platform['y'], platform['width'], platform['height']))

    def draw_peachs_castle(self, screen):
        # Castle structure
        pygame.draw.rect(screen, (255, 182, 193), (350, 400, 300, 100))
        # Castle towers
        pygame.draw.polygon(screen, (255, 105, 180), [(350, 400), (380, 350), (410, 400)])
        pygame.draw.polygon(screen, (255, 105, 180), [(590, 400), (620, 350), (650, 400)])
        # Bumper platform
        pygame.draw.ellipse(screen, (255, 255, 100), (480, 380, 40, 20))

    def draw_congo_jungle(self, screen):
        # Barrel cannon platforms
        pygame.draw.circle(screen, (139, 69, 19), (200, 450), 30)
        pygame.draw.circle(screen, (139, 69, 19), (824, 450), 30)
        # Jungle trees
        for x in range(0, SCREEN_WIDTH, 150):
            pygame.draw.rect(screen, (101, 67, 33), (x, 500, 30, 200))
            pygame.draw.circle(screen, (34, 139, 34), (x + 15, 480), 40)

    def draw_hyrule_castle(self, screen):
        # Castle walls
        pygame.draw.rect(screen, (105, 105, 105), (100, 400, 824, 100))
        # Triforce symbol
        pygame.draw.polygon(screen, (255, 215, 0), [(512, 300), (462, 380), (562, 380)])
        # Tornado spawn area
        pygame.draw.circle(screen, (200, 200, 255, 50), (700, 450), 40)

    def draw_yoshis_island(self, screen):
        # Happy clouds
        for cloud in [(200, 200), (600, 150), (800, 250)]:
            pygame.draw.ellipse(screen, WHITE, (cloud[0], cloud[1], 80, 40))
            pygame.draw.ellipse(screen, WHITE, (cloud[0]-20, cloud[1]+10, 60, 30))
            pygame.draw.ellipse(screen, WHITE, (cloud[0]+40, cloud[1]+10, 60, 30))

    def draw_dream_land(self, screen):
        # Whispy Woods tree
        pygame.draw.rect(screen, (139, 69, 19), (100, 300, 80, 200))
        pygame.draw.circle(screen, (34, 139, 34), (140, 280), 100)
        # Dream Land clouds
        for i in range(3):
            x = 300 + i * 200
            pygame.draw.ellipse(screen, (255, 182, 193), (x, 100, 100, 50))

    def draw_sector_z(self, screen):
        # Great Fox ship outline
        pygame.draw.polygon(screen, (192, 192, 192), 
                           [(200, 450), (824, 450), (750, 500), (274, 500)])
        # Arwing fighters in background
        for i in range(3):
            x = 100 + i * 300
            y = 100 + i * 50
            pygame.draw.polygon(screen, (100, 100, 150), 
                               [(x, y), (x+40, y+10), (x+30, y+20), (x+10, y+20)])

    def draw_planet_zebes(self, screen):
        # Acid lava at bottom
        pygame.draw.rect(screen, (255, 100, 0), (0, 550, SCREEN_WIDTH, 50))
        # Bubbling effect
        for i in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(screen, (255, 150, 0), (x, 555), random.randint(3, 8))

    def draw_saffron_city(self, screen):
        # City buildings
        for i in range(5):
            height = random.randint(100, 300)
            x = i * 200
            pygame.draw.rect(screen, (100, 100, 100), (x, 500-height, 150, height))
            # Windows
            for w in range(0, height-20, 30):
                for wx in range(10, 140, 30):
                    pygame.draw.rect(screen, YELLOW, (x+wx, 510-height+w, 20, 20))

    def draw_mushroom_kingdom(self, screen):
        # Retro pipes
        pygame.draw.rect(screen, (0, 200, 0), (150, 420, 60, 80))
        pygame.draw.rect(screen, (0, 255, 0), (150, 400, 60, 30))
        pygame.draw.rect(screen, (0, 200, 0), (814, 420, 60, 80))
        pygame.draw.rect(screen, (0, 255, 0), (814, 400, 60, 30))
        # Retro blocks
        for i in range(3):
            x = 350 + i * 100
            pygame.draw.rect(screen, (200, 100, 0), (x, 350, 40, 40))
            pygame.draw.rect(screen, YELLOW, (x+15, 365, 10, 10))

# Initialize all stages
STAGES = {
    "peachs_castle": Stage(
        "Peach's Castle", "peachs_castle",
        [{'x': 300, 'y': 500, 'width': 400, 'height': 20, 'color': (200, 150, 100)},
         {'x': 460, 'y': 380, 'width': 80, 'height': 10, 'color': (255, 255, 100)}],
        (-100, 1124, -200, 700),
        [(400, 300), (600, 300)],
        (135, 206, 235)
    ),
    "congo_jungle": Stage(
        "Congo Jungle", "congo_jungle",
        [{'x': 300, 'y': 500, 'width': 424, 'height': 20, 'color': (101, 67, 33)},
         {'x': 170, 'y': 420, 'width': 60, 'height': 10, 'color': (139, 69, 19)},
         {'x': 794, 'y': 420, 'width': 60, 'height': 10, 'color': (139, 69, 19)}],
        (-100, 1124, -200, 700),
        [(400, 300), (600, 300)],
        (34, 100, 34)
    ),
    "hyrule_castle": Stage(
        "Hyrule Castle", "hyrule_castle",
        [{'x': 100, 'y': 500, 'width': 824, 'height': 20, 'color': (105, 105, 105)},
         {'x': 350, 'y': 350, 'width': 100, 'height': 10, 'color': (128, 128, 128)},
         {'x': 574, 'y': 350, 'width': 100, 'height': 10, 'color': (128, 128, 128)}],
        (-150, 1174, -250, 700),
        [(400, 300), (600, 300)],
        (70, 50, 100)
    ),
    "super_happy_tree": Stage(
        "Super Happy Tree", "super_happy_tree",
        [{'x': 350, 'y': 500, 'width': 324, 'height': 20, 'color': (150, 255, 150)},
         {'x': 250, 'y': 400, 'width': 80, 'height': 10, 'color': (200, 255, 200)},
         {'x': 694, 'y': 400, 'width': 80, 'height': 10, 'color': (200, 255, 200)},
         {'x': 450, 'y': 300, 'width': 124, 'height': 10, 'color': (200, 255, 200)}],
        (-100, 1124, -200, 700),
        [(400, 300), (600, 300)],
        (135, 206, 250)
    ),
    "dream_land": Stage(
        "Dream Land", "dream_land",
        [{'x': 250, 'y': 500, 'width': 524, 'height': 20, 'color': (255, 182, 193)},
         {'x': 350, 'y': 370, 'width': 100, 'height': 10, 'color': (255, 200, 200)},
         {'x': 574, 'y': 370, 'width': 100, 'height': 10, 'color': (255, 200, 200)},
         {'x': 462, 'y': 250, 'width': 100, 'height': 10, 'color': (255, 200, 200)}],
        (-100, 1124, -200, 700),
        [(400, 300), (600, 300)],
        (255, 200, 255)
    ),
    "sector_z": Stage(
        "Sector Z", "sector_z",
        [{'x': 200, 'y': 475, 'width': 624, 'height': 30, 'color': (192, 192, 192)}],
        (-200, 1224, -300, 700),
        [(400, 350), (600, 350)],
        (20, 20, 40)
    ),
    "planet_zebes": Stage(
        "Planet Zebes", "planet_zebes",
        [{'x': 350, 'y': 500, 'width': 324, 'height': 20, 'color': (100, 50, 50)},
         {'x': 200, 'y': 380, 'width': 80, 'height': 10, 'color': (150, 75, 75)},
         {'x': 744, 'y': 380, 'width': 80, 'height': 10, 'color': (150, 75, 75)},
         {'x': 450, 'y': 280, 'width': 124, 'height': 10, 'color': (150, 75, 75)}],
        (-100, 1124, -200, 600),
        [(400, 300), (600, 300)],
        (50, 25, 25)
    ),
    "saffron_city": Stage(
        "Saffron City", "saffron_city",
        [{'x': 300, 'y': 500, 'width': 424, 'height': 20, 'color': (100, 100, 100)},
         {'x': 200, 'y': 350, 'width': 100, 'height': 10, 'color': (150, 150, 150)},
         {'x': 724, 'y': 350, 'width': 100, 'height': 10, 'color': (150, 150, 150)}],
        (-100, 1124, -200, 700),
        [(400, 300), (600, 300)],
        (50, 50, 100)
    ),
    "mushroom_kingdom": Stage(
        "Mushroom Kingdom", "mushroom_kingdom",
        [{'x': 0, 'y': 500, 'width': 1024, 'height': 20, 'color': (200, 100, 0)},
         {'x': 350, 'y': 390, 'width': 40, 'height': 10, 'color': (200, 100, 0)},
         {'x': 450, 'y': 390, 'width': 40, 'height': 10, 'color': (200, 100, 0)},
         {'x': 550, 'y': 390, 'width': 40, 'height': 10, 'color': (200, 100, 0)}],
        (0, 1024, -200, 700),  # Walk-off stage
        [(400, 300), (600, 300)],
        (100, 150, 255)
    )
}

# ============================================
# CHARACTER DEFINITIONS - Original 12
# ============================================

class CharacterData:
    def __init__(self, name, color, speed, jump_power, weight, fall_speed):
        self.name = name
        self.color = color
        self.speed = speed
        self.jump_power = jump_power
        self.weight = weight
        self.fall_speed = fall_speed

CHARACTER_ROSTER = {
    "Mario": CharacterData("Mario", RED, 5, 17, 1.0, 1.0),
    "DK": CharacterData("Donkey Kong", (139, 69, 19), 4, 18, 1.3, 1.2),
    "Link": CharacterData("Link", GREEN, 4.5, 16, 1.1, 1.1),
    "Samus": CharacterData("Samus", ORANGE, 3.5, 16, 1.2, 1.0),
    "Yoshi": CharacterData("Yoshi", (50, 205, 50), 6, 19, 0.9, 0.8),
    "Kirby": CharacterData("Kirby", (255, 182, 193), 4, 20, 0.7, 0.6),
    "Fox": CharacterData("Fox", (255, 140, 0), 7, 18, 0.8, 1.5),
    "Pikachu": CharacterData("Pikachu", YELLOW, 6.5, 17, 0.75, 0.9),
    "Luigi": CharacterData("Luigi", (0, 200, 0), 5, 19, 0.95, 0.8),
    "Ness": CharacterData("Ness", (255, 0, 100), 4.5, 17, 0.9, 0.95),
    "C.Falcon": CharacterData("Captain Falcon", (0, 0, 200), 8, 17, 1.1, 1.3),
    "Jigglypuff": CharacterData("Jigglypuff", (255, 200, 255), 4, 22, 0.6, 0.5)
}

class Fighter:
    def __init__(self, character_data, x, y, player_num):
        self.name = character_data.name
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 40
        self.height = 60
        self.color = character_data.color
        self.player_num = player_num
        
        # Character stats from data
        self.speed = character_data.speed
        self.jump_power = character_data.jump_power
        self.weight = character_data.weight
        self.fall_speed_multiplier = character_data.fall_speed
        
        # Combat stats
        self.damage = 0
        self.stocks = 4
        self.state = PlayerState.IDLE
        self.facing_right = True
        self.invulnerable = False
        self.invuln_timer = 0
        
        # Movement
        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.fast_falling = False
        
        # Timers
        self.attack_timer = 0
        self.stun_timer = 0
        self.shield_health = 100
        self.dodge_timer = 0
        
        # Visual effects
        self.hit_particles = []
        
    def update(self, stage):
        # Handle invulnerability
        if self.invulnerable:
            self.invuln_timer -= 1
            if self.invuln_timer <= 0:
                self.invulnerable = False
        
        # Handle stun
        if self.state == PlayerState.STUNNED:
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.state = PlayerState.IDLE
        
        # Handle attacks
        if self.state == PlayerState.ATTACKING:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.state = PlayerState.IDLE
        
        # Handle dodge
        if self.state == PlayerState.DODGING:
            self.dodge_timer -= 1
            if self.dodge_timer <= 0:
                self.state = PlayerState.IDLE
                self.invulnerable = False
        
        # Apply gravity
        if self.y < stage.ground_y:
            gravity = GRAVITY * self.fall_speed_multiplier
            if self.fast_falling:
                gravity *= 2
            self.vy += gravity
            if self.vy > MAX_FALL_SPEED * self.fall_speed_multiplier:
                self.vy = MAX_FALL_SPEED * self.fall_speed_multiplier
        
        # Apply movement
        if self.state != PlayerState.STUNNED:
            self.x += self.vx
        self.y += self.vy
        
        # Ground collision
        if self.y >= stage.ground_y:
            self.y = stage.ground_y
            self.vy = 0
            self.jumps_left = self.max_jumps
            self.fast_falling = False
            if self.state in [PlayerState.JUMPING, PlayerState.FALLING]:
                self.state = PlayerState.IDLE
        
        # Platform collisions
        for platform in stage.platforms:
            if (self.vy > 0 and 
                self.x + self.width > platform['x'] and 
                self.x < platform['x'] + platform['width'] and
                self.y < platform['y'] and 
                self.y + self.height >= platform['y']):
                self.y = platform['y'] - self.height
                self.vy = 0
                self.jumps_left = self.max_jumps
                self.fast_falling = False
                if self.state in [PlayerState.JUMPING, PlayerState.FALLING]:
                    self.state = PlayerState.IDLE
        
        # Check blast zones
        if (self.x < stage.blast_zones[0] or 
            self.x > stage.blast_zones[1] or 
            self.y < stage.blast_zones[2] or 
            self.y > stage.blast_zones[3]):
            self.respawn(stage)
        
        # Update particles
        self.hit_particles = [(x, y, size, life - 1) 
                              for x, y, size, life in self.hit_particles if life > 0]
    
    def move(self, direction):
        if self.state == PlayerState.STUNNED:
            return
        
        if direction == 'left':
            self.vx = -self.speed
            self.facing_right = False
            if self.state == PlayerState.IDLE:
                self.state = PlayerState.WALKING
        elif direction == 'right':
            self.vx = self.speed
            self.facing_right = True
            if self.state == PlayerState.IDLE:
                self.state = PlayerState.WALKING
        else:
            self.vx *= 0.85
            if abs(self.vx) < 0.5:
                self.vx = 0
                if self.state == PlayerState.WALKING:
                    self.state = PlayerState.IDLE
    
    def jump(self):
        if self.state == PlayerState.STUNNED:
            return
        
        if self.jumps_left > 0:
            self.vy = -self.jump_power
            self.jumps_left -= 1
            self.state = PlayerState.JUMPING
    
    def attack(self, attack_type='neutral'):
        if self.state in [PlayerState.STUNNED, PlayerState.ATTACKING]:
            return
        
        self.state = PlayerState.ATTACKING
        self.attack_timer = 20
    
    def shield(self, active):
        if self.state == PlayerState.STUNNED:
            return
        
        if active and self.shield_health > 0:
            self.state = PlayerState.SHIELDING
            self.shield_health -= 0.5
        else:
            if self.state == PlayerState.SHIELDING:
                self.state = PlayerState.IDLE
            if self.shield_health < 100:
                self.shield_health += 0.3
    
    def take_hit(self, damage, knockback_x, knockback_y):
        if self.invulnerable or self.state == PlayerState.SHIELDING:
            if self.state == PlayerState.SHIELDING:
                self.shield_health -= damage * 2
            return
        
        self.damage += damage
        
        # N64-style knockback calculation
        kb_multiplier = 1 + (self.damage / 80) / self.weight
        self.vx = knockback_x * kb_multiplier
        self.vy = knockback_y * kb_multiplier
        
        self.state = PlayerState.STUNNED
        self.stun_timer = min(60, int(damage * 1.5))
        self.invulnerable = True
        self.invuln_timer = 60
        
        # Add hit effect
        for i in range(12):
            self.hit_particles.append((
                self.x + self.width//2,
                self.y + self.height//2,
                random.randint(3, 8),
                20
            ))
    
    def respawn(self, stage):
        self.stocks -= 1
        if self.stocks > 0:
            spawn = random.choice(stage.spawn_points)
            self.x = spawn[0]
            self.y = spawn[1]
            self.vx = 0
            self.vy = 0
            self.damage = 0
            self.state = PlayerState.IDLE
            self.invulnerable = True
            self.invuln_timer = 120
    
    def draw(self, screen):
        # Draw character with N64-style rendering
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            color = WHITE
        else:
            color = self.color
        
        # Character body
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Direction indicator
        eye_y = self.y + 15
        if self.facing_right:
            pygame.draw.circle(screen, WHITE, (self.x + 30, eye_y), 4)
        else:
            pygame.draw.circle(screen, WHITE, (self.x + 10, eye_y), 4)
        
        # Shield
        if self.state == PlayerState.SHIELDING:
            shield_alpha = int(self.shield_health * 2.55)
            shield_surface = pygame.Surface((self.width + 30, self.height + 30), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surface, (*CYAN, shield_alpha), 
                              (0, 0, self.width + 30, self.height + 30))
            screen.blit(shield_surface, (self.x - 15, self.y - 15))
        
        # Attack hitbox
        if self.state == PlayerState.ATTACKING:
            attack_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
            hitbox_x = self.x + (self.width if self.facing_right else -60)
            pygame.draw.circle(attack_surface, (*YELLOW, 100), (30, 30), 30)
            screen.blit(attack_surface, (hitbox_x, self.y))
        
        # Hit particles
        for x, y, size, life in self.hit_particles:
            alpha = life / 20
            pygame.draw.circle(screen, (255, int(255*alpha), int(255*alpha)), 
                             (int(x), int(y)), size)
        
        # Damage percentage
        font = pygame.font.Font(None, 32)
        damage_text = font.render(f"{int(self.damage)}%", True, WHITE)
        text_x = self.x + self.width // 2 - damage_text.get_width() // 2
        screen.blit(damage_text, (text_x, self.y - 30))

# ============================================
# MENU SYSTEM
# ============================================

class MainMenu:
    def __init__(self):
        self.options = ["1P MODE", "VS MODE", "OPTIONS", "DATA"]
        self.selected = 0
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.copyright_font = pygame.font.Font(None, 24)
        
    def update(self, keys_pressed):
        if pygame.K_UP in keys_pressed:
            self.selected = (self.selected - 1) % len(self.options)
        elif pygame.K_DOWN in keys_pressed:
            self.selected = (self.selected + 1) % len(self.options)
        elif pygame.K_RETURN in keys_pressed:
            return self.selected
        return None
    
    def draw(self, screen):
        screen.fill(N64_BLUE)
        
        # Draw title
        title = self.title_font.render("SUPER SMASH BROS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        # Draw N64 subtitle
        subtitle = self.menu_font.render("64", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 210))
        screen.blit(subtitle, subtitle_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 350 + i * 60))
            screen.blit(text, text_rect)
            
            # Draw selection indicator
            if i == self.selected:
                pygame.draw.polygon(screen, YELLOW, 
                                  [(text_rect.left - 40, text_rect.centery),
                                   (text_rect.left - 20, text_rect.centery - 10),
                                   (text_rect.left - 20, text_rect.centery + 10)])
        
        # Draw copyright
        copyright_text = "© 1999 HAL Laboratory, Inc. / Nintendo"
        copyright = self.copyright_font.render(copyright_text, True, WHITE)
        copyright_rect = copyright.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(copyright, copyright_rect)

class CharacterSelect:
    def __init__(self):
        self.characters = list(CHARACTER_ROSTER.keys())
        self.selected = [0, 1]  # P1 and P2 selections
        self.confirmed = [False, False]
        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 32)
        
    def update(self, keys_pressed):
        # Player 1 controls (WASD)
        if not self.confirmed[0]:
            if pygame.K_a in keys_pressed:
                self.selected[0] = (self.selected[0] - 1) % len(self.characters)
            elif pygame.K_d in keys_pressed:
                self.selected[0] = (self.selected[0] + 1) % len(self.characters)
            elif pygame.K_SPACE in keys_pressed:
                self.confirmed[0] = True
        
        # Player 2 controls (Arrows)
        if not self.confirmed[1]:
            if pygame.K_LEFT in keys_pressed:
                self.selected[1] = (self.selected[1] - 1) % len(self.characters)
            elif pygame.K_RIGHT in keys_pressed:
                self.selected[1] = (self.selected[1] + 1) % len(self.characters)
            elif pygame.K_RETURN in keys_pressed:
                self.confirmed[1] = True
        
        # Check if both players confirmed
        if self.confirmed[0] and self.confirmed[1]:
            return (self.characters[self.selected[0]], self.characters[self.selected[1]])
        return None
    
    def draw(self, screen):
        screen.fill(DARK_GRAY)
        
        # Draw title
        title = self.title_font.render("CHARACTER SELECT", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Draw character grid
        cols = 4
        rows = 3
        box_width = 120
        box_height = 120
        start_x = (SCREEN_WIDTH - cols * box_width) // 2
        start_y = 150
        
        for i, char_name in enumerate(self.characters):
            row = i // cols
            col = i % cols
            x = start_x + col * box_width
            y = start_y + row * box_height
            
            # Draw character box
            color = GRAY
            if i == self.selected[0]:
                color = RED if not self.confirmed[0] else (255, 100, 100)
            elif i == self.selected[1]:
                color = BLUE if not self.confirmed[1] else (100, 100, 255)
            
            pygame.draw.rect(screen, color, (x, y, box_width - 10, box_height - 10), 3)
            
            # Draw character preview
            char_data = CHARACTER_ROSTER[char_name]
            pygame.draw.rect(screen, char_data.color, 
                           (x + 30, y + 20, 50, 60))
            
            # Draw character name
            name = self.name_font.render(char_name[:8], True, WHITE)
            name_rect = name.get_rect(center=(x + box_width//2 - 5, y + box_height - 20))
            screen.blit(name, name_rect)
        
        # Draw player indicators
        p1_text = self.name_font.render("P1", True, RED)
        screen.blit(p1_text, (50, 300))
        
        p2_text = self.name_font.render("P2", True, BLUE)
        screen.blit(p2_text, (SCREEN_WIDTH - 80, 300))

class StageSelect:
    def __init__(self):
        self.stages = list(STAGES.keys())
        self.selected = 0
        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 32)
        
    def update(self, keys_pressed):
        if pygame.K_LEFT in keys_pressed:
            self.selected = (self.selected - 1) % len(self.stages)
        elif pygame.K_RIGHT in keys_pressed:
            self.selected = (self.selected + 1) % len(self.stages)
        elif pygame.K_RETURN in keys_pressed:
            return self.stages[self.selected]
        return None
    
    def draw(self, screen):
        screen.fill(DARK_GRAY)
        
        # Draw title
        title = self.title_font.render("STAGE SELECT", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Draw stage preview
        stage = STAGES[self.stages[self.selected]]
        preview_surface = pygame.Surface((600, 400))
        stage.draw(preview_surface)
        preview_surface = pygame.transform.scale(preview_surface, (450, 300))
        screen.blit(preview_surface, (SCREEN_WIDTH//2 - 225, 150))
        
        # Draw stage name
        name = self.name_font.render(stage.name.upper(), True, YELLOW)
        name_rect = name.get_rect(center=(SCREEN_WIDTH//2, 480))
        screen.blit(name, name_rect)
        
        # Draw navigation arrows
        if self.selected > 0:
            pygame.draw.polygon(screen, YELLOW, 
                              [(200, 300), (230, 280), (230, 320)])
        if self.selected < len(self.stages) - 1:
            pygame.draw.polygon(screen, YELLOW, 
                              [(SCREEN_WIDTH - 200, 300), 
                               (SCREEN_WIDTH - 230, 280), 
                               (SCREEN_WIDTH - 230, 320)])

# ============================================
# GAME ENGINE
# ============================================

class SmashBros64Engine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Smash Bros 64 - HAL Laboratory")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.main_menu = MainMenu()
        self.character_select = CharacterSelect()
        self.stage_select = StageSelect()
        
        # Battle state
        self.current_stage = None
        self.players = []
        self.game_time = 0
        self.pause = False
        
        # Input handling
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        
    def handle_events(self):
        self.keys_just_pressed.clear()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys_just_pressed.add(event.key)
                self.keys_pressed.add(event.key)
                
                # Global controls
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.BATTLE:
                        self.state = GameState.MAIN_MENU
                    elif self.state != GameState.MAIN_MENU:
                        self.state = GameState.MAIN_MENU
                
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
    
    def update(self):
        if self.state == GameState.MAIN_MENU:
            selection = self.main_menu.update(self.keys_just_pressed)
            if selection is not None:
                if selection == 1:  # VS MODE
                    self.state = GameState.CHARACTER_SELECT
                    self.character_select = CharacterSelect()
        
        elif self.state == GameState.CHARACTER_SELECT:
            characters = self.character_select.update(self.keys_just_pressed)
            if characters:
                # Create fighters
                char1_data = CHARACTER_ROSTER[characters[0]]
                char2_data = CHARACTER_ROSTER[characters[1]]
                self.players = [
                    Fighter(char1_data, 400, 300, 1),
                    Fighter(char2_data, 600, 300, 2)
                ]
                self.state = GameState.STAGE_SELECT
                self.stage_select = StageSelect()
        
        elif self.state == GameState.STAGE_SELECT:
            stage_id = self.stage_select.update(self.keys_just_pressed)
            if stage_id:
                self.current_stage = STAGES[stage_id]
                # Position players at spawn points
                for i, player in enumerate(self.players):
                    spawn = self.current_stage.spawn_points[i]
                    player.x = spawn[0]
                    player.y = spawn[1]
                self.state = GameState.BATTLE
                self.game_time = 0
        
        elif self.state == GameState.BATTLE:
            if not self.pause:
                self.update_battle()
                self.game_time += 1
    
    def update_battle(self):
        # Player 1 controls
        p1 = self.players[0]
        if pygame.K_a in self.keys_pressed:
            p1.move('left')
        elif pygame.K_d in self.keys_pressed:
            p1.move('right')
        else:
            p1.move('stop')
        
        if pygame.K_w in self.keys_just_pressed:
            p1.jump()
        
        if pygame.K_s in self.keys_pressed and p1.y < self.current_stage.ground_y:
            p1.fast_falling = True
        
        if pygame.K_f in self.keys_just_pressed:
            p1.attack()
        
        p1.shield(pygame.K_LSHIFT in self.keys_pressed)
        
        # Player 2 controls
        p2 = self.players[1]
        if pygame.K_LEFT in self.keys_pressed:
            p2.move('left')
        elif pygame.K_RIGHT in self.keys_pressed:
            p2.move('right')
        else:
            p2.move('stop')
        
        if pygame.K_UP in self.keys_just_pressed:
            p2.jump()
        
        if pygame.K_DOWN in self.keys_pressed and p2.y < self.current_stage.ground_y:
            p2.fast_falling = True
        
        if pygame.K_COMMA in self.keys_just_pressed:
            p2.attack()
        
        p2.shield(pygame.K_RSHIFT in self.keys_pressed)
        
        # Update players
        for player in self.players:
            player.update(self.current_stage)
        
        # Check collisions
        self.check_attack_collisions()
        
        # Check for game over
        for player in self.players:
            if player.stocks <= 0:
                self.state = GameState.RESULTS
    
    def check_attack_collisions(self):
        for i, attacker in enumerate(self.players):
            if attacker.state == PlayerState.ATTACKING:
                for j, defender in enumerate(self.players):
                    if i != j:
                        # Simple collision check
                        hitbox_x = attacker.x + (attacker.width if attacker.facing_right else -60)
                        if (defender.x < hitbox_x + 60 and
                            defender.x + defender.width > hitbox_x and
                            abs(defender.y - attacker.y) < 60):
                            
                            knockback_x = 10 * (1 if attacker.facing_right else -1)
                            knockback_y = -8
                            defender.take_hit(12, knockback_x, knockback_y)
    
    def draw(self):
        if self.state == GameState.MAIN_MENU:
            self.main_menu.draw(self.screen)
        
        elif self.state == GameState.CHARACTER_SELECT:
            self.character_select.draw(self.screen)
        
        elif self.state == GameState.STAGE_SELECT:
            self.stage_select.draw(self.screen)
        
        elif self.state == GameState.BATTLE:
            # Draw stage
            self.current_stage.draw(self.screen)
            
            # Draw players
            for player in self.players:
                player.draw(self.screen)
            
            # Draw HUD
            self.draw_hud()
        
        elif self.state == GameState.RESULTS:
            self.draw_results()
        
        pygame.display.flip()
    
    def draw_hud(self):
        hud_font = pygame.font.Font(None, 36)
        stock_font = pygame.font.Font(None, 24)
        
        # Player 1 HUD
        p1 = self.players[0]
        p1_name = hud_font.render(p1.name, True, RED)
        self.screen.blit(p1_name, (50, 20))
        
        # P1 Stocks
        for i in range(p1.stocks):
            pygame.draw.circle(self.screen, RED, (60 + i * 25, 60), 8)
        
        # Player 2 HUD
        p2 = self.players[1]
        p2_name = hud_font.render(p2.name, True, BLUE)
        self.screen.blit(p2_name, (SCREEN_WIDTH - 200, 20))
        
        # P2 Stocks
        for i in range(p2.stocks):
            pygame.draw.circle(self.screen, BLUE, (SCREEN_WIDTH - 150 + i * 25, 60), 8)
        
        # Timer
        minutes = self.game_time // 3600
        seconds = (self.game_time // 60) % 60
        timer_text = hud_font.render(f"{minutes:02d}:{seconds:02d}", True, WHITE)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(timer_text, timer_rect)
    
    def draw_results(self):
        self.screen.fill(BLACK)
        
        # Determine winner
        winner = None
        for player in self.players:
            if player.stocks > 0:
                winner = player
                break
        
        if winner:
            result_font = pygame.font.Font(None, 72)
            winner_text = result_font.render(f"{winner.name} WINS!", True, YELLOW)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(winner_text, winner_rect)
        
        restart_font = pygame.font.Font(None, 32)
        restart_text = restart_font.render("Press ESC to return to menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("==============================================")
    print("  SUPER SMASH BROS 64 - HAL LABORATORY ENGINE")
    print("==============================================")
    print("Loading assets and initializing...")
    
    game = SmashBros64Engine()
    game.run()
