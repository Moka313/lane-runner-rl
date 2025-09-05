# sprites.py
import pygame
from config import WIDTH, HEIGHT, LANES, ROAD_MARGIN

class LaneHelper:
    def __init__(self):
        lane_w = (WIDTH - 2*ROAD_MARGIN) // LANES
        self.centers = [ROAD_MARGIN + lane_w//2 + lane_w*i for i in range(LANES)]
        self.lane_w = lane_w

    def x_for_lane(self, lane_idx: int) -> int:
        return self.centers[lane_idx]

class Car(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, lane_helper: LaneHelper):
        super().__init__()
        self.raw = image
        scale = 0.2
        w = int(self.raw.get_width() * scale)
        h = int(self.raw.get_height() * scale)
        self.image = pygame.transform.smoothscale(self.raw, (w, h))
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 30))
        self.lane_helper = lane_helper
        self.lane = 1  # middle

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < len(self.lane_helper.centers) - 1:
            self.lane += 1

    def update(self):
        target_x = self.lane_helper.x_for_lane(self.lane)
        self.rect.centerx = target_x

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, lane_idx: int, speed: int):
        super().__init__()
        maxw = 40
        scale = min(1.0, maxw / max(1, surf.get_width()))
        w = int(surf.get_width()*scale)
        h = int(surf.get_height()*scale)
        self.image = pygame.transform.smoothscale(surf, (w, h))
        self.rect = self.image.get_rect(midtop=(0, -h))
        self.speed = speed
        self.lane_idx = lane_idx

    def set_position(self, lane_helper: LaneHelper, y: int):
        self.rect.midtop = (lane_helper.x_for_lane(self.lane_idx), y)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 10:
            self.kill()
