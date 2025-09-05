# game.py
import random
import pygame
from config import WIDTH, HEIGHT, FPS, BG, ROAD, LANE_LINE, HUD, HUD_SHADOW, ROAD_MARGIN, LANE_LINE_WIDTH, LANES, SCROLL_SPEED, SPAWN_EVERY_FRAMES, FONT_SMALL, FONT_BIG
from sprites import LaneHelper, Car, Obstacle
from assets import load_assets

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lane Dodge — Cars & Obstacles")
        self.clock = pygame.time.Clock()
        self.assets = load_assets()
        self.lanes = LaneHelper()
        self.player = Car(self.assets["car.png"], self.lanes)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacles = pygame.sprite.Group()
        self.frame = 0
        self.score = 0
        self.game_over = False
        self.road_scroll = 0
        self._next_uid = 1  # <-- NEW: unique IDs for obstacles

        self.obs_images = [
            self.assets["trashcan.png"],
            self.assets["rock.png"],
            self.assets["old_lady.png"],
            self.assets["broken_car.png"],
        ]

    def reset(self):
        self.all_sprites.empty()
        self.obstacles.empty()
        self.player = Car(self.assets["car.png"], self.lanes)
        self.all_sprites.add(self.player)
        self.frame = 0
        self.score = 0
        self.game_over = False
        self.road_scroll = 0

    def spawn_obstacle(self):
        lane = random.randrange(LANES)
        img = random.choice(self.obs_images)
        speed = SCROLL_SPEED + random.randint(0, 2)
        ob = Obstacle(img, lane, speed)
        y = -random.randint(80, 220)
        ob.set_position(self.lanes, y)
        ob.uid = self._next_uid  # <-- NEW
        self._next_uid += 1       # <-- NEW
        self.obstacles.add(ob)
        self.all_sprites.add(ob)

    def update(self):
        if self.game_over:
            return
        self.frame += 1
        if self.frame % SPAWN_EVERY_FRAMES == 0:
            self.spawn_obstacle()

        self.all_sprites.update()
        self.road_scroll = (self.road_scroll + SCROLL_SPEED) % 40
        self.score += 1  # simple frame-based score

        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True

    def draw_road(self):
        road_rect = pygame.Rect(ROAD_MARGIN, 0, WIDTH - 2*ROAD_MARGIN, HEIGHT)
        pygame.draw.rect(self.screen, ROAD, road_rect, border_radius=12)
        lane_w = road_rect.width // LANES
        for i in range(1, LANES):
            x = ROAD_MARGIN + i * lane_w
            seg_h, gap = 20, 20
            y = -self.road_scroll
            while y < HEIGHT:
                pygame.draw.rect(self.screen, LANE_LINE, (x - LANE_LINE_WIDTH//2, y, LANE_LINE_WIDTH, seg_h), border_radius=2)
                y += seg_h + gap

    def _blit_text(self, text: str, x: int, y: int, align="topleft"):
        surf = FONT_SMALL.render(text, True, HUD)
        shadow = FONT_SMALL.render(text, True, HUD_SHADOW)
        rect = surf.get_rect()
        srect = shadow.get_rect()
        setattr(rect, align, (x, y))
        setattr(srect, align, (x+1, y+1))
        self.screen.blit(shadow, srect)
        self.screen.blit(surf, rect)

    def draw(self):
        self.screen.fill(BG)
        self.draw_road()
        self.all_sprites.draw(self.screen)
        self._blit_text(f"Score: {self.score}", 16, 16)

        if self.game_over:
            title = FONT_BIG.render("CRASH!", True, HUD)
            trect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
            self.screen.blit(title, trect)
            prompt = FONT_SMALL.render("Press R to restart • ESC to quit", True, HUD)
            prect = prompt.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            self.screen.blit(prompt, prect)

        pygame.display.flip()

    # Keep human controls intact
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                if self.game_over and e.key == pygame.K_r:
                    self.reset()
                if not self.game_over:
                    if e.key in (pygame.K_LEFT, pygame.K_a):
                        self.player.move_left()
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        self.player.move_right()
        return True

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
