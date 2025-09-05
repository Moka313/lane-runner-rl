# config.py
import os
import pygame

# Screen / game
WIDTH, HEIGHT = 480, 720
FPS = 60
LANES = 3
ROAD_MARGIN = 60
LANE_LINE_WIDTH = 6
SCROLL_SPEED = 6
SPAWN_EVERY_FRAMES = 38  # smaller = more obstacles

# Colors
BG = (25, 25, 25)
ROAD = (44, 44, 44)
LANE_LINE = (200, 200, 200)
HUD = (240, 240, 240)
HUD_SHADOW = (0, 0, 0)

# Asset caching
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSET_DIR, exist_ok=True)

# Robust, CC0/PD image URLs
ASSET_URLS = {
    # player car (top-down, CC0, OpenGameArt)
    "car.png": "https://opengameart.org/sites/default/files/car1.png",  # :contentReference[oaicite:0]{index=0}
    # rock (spritesheet; we auto-crop one cell)
    "rock.png": "https://opengameart.org/sites/default/files/asteroid_01_no_moblur.png",  # :contentReference[oaicite:1]{index=1}
    # elderly person with cane (we crop the left half to get one person)
    "old_lady.png": "https://openclipart.org/image/2000px/256947",  # :contentReference[oaicite:2]{index=2}
    # a stationary broken car (use a different car sprite as obstacle)
    "broken_car.png": "https://opengameart.org/sites/default/files/car2.png",  # :contentReference[oaicite:3]{index=3}
    # trashcan
    "trashcan.png": "https://openclipart.org/image/800px/svg_to_png/261058/trash-can.png",  # :contentReference[oaicite:4]{index=4}
}

# Drawing helpers
pygame.font.init()
FONT_SMALL = pygame.font.SysFont("arial", 20)
FONT_BIG = pygame.font.SysFont("arial", 42, bold=True)
