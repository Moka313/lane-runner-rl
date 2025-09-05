# env.py
import random
import pygame
from typing import Tuple, Dict, Any, List
from game import Game
from config import LANES, HEIGHT

# Actions: 0=left, 1=stay, 2=right
LEFT, STAY, RIGHT = 0, 1, 2

class LaneDodgeEnv:
    """
    Minimal Gym-like wrapper around the Game.
    Observation: (lane, dist_left, dist_mid, dist_right),
    where distances are normalized [0..1] to the nearest upcoming obstacle
    in each lane (1.0 means clear; 0.0 means very close).
    """
    def __init__(self, render_mode: str = "human", seed: int | None = None):
        self.render_mode = render_mode
        if seed is not None:
            random.seed(seed)
        self.game = Game()  # creates window
        self._counted_pass: set[int] = set()
        self._closed = False

    def close(self):
        if not self._closed:
            pygame.quit()
            self._closed = True

    def reset(self, seed: int | None = None) -> Tuple[Tuple[float, ...], Dict[str, Any]]:
        if seed is not None:
            random.seed(seed)
        self.game.reset()
        self._counted_pass.clear()
        obs = self._observe()
        info = {"score": self.game.score}
        return obs, info

    def step(self, action: int) -> Tuple[Tuple[float, ...], float, bool, Dict[str, Any]]:
        """One environment step = one game frame."""
        # Minimal event pump (so the window doesn't freeze)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._closed = True
                self.game.game_over = True

        # Apply action
        if action == LEFT:
            self.game.player.move_left()
        elif action == RIGHT:
            self.game.player.move_right()
        # STAY -> no-op

        # Tick game
        self.game.update()
        if self.render_mode == "human":
            self.game.draw()
            self.game.clock.tick(60)

        # Reward: small survival +1 per newly passed obstacle, large - on crash
        passed_now = self._compute_newly_passed_count()
        reward = 0.01 + 1.0 * passed_now
        done = self.game.game_over
        if done:
            reward -= 10.0

        obs = self._observe()
        info = {
            "passed": passed_now,
            "score": self.game.score,
            "closed": self._closed,
        }
        return obs, reward, done, info

    # ---------------------- Helpers ---------------------- #

    def _compute_newly_passed_count(self) -> int:
        """Counts obstacles that moved below the car this frame (not yet counted)."""
        count = 0
        car_bottom = self.game.player.rect.bottom
        for ob in self.game.obstacles:
            uid = getattr(ob, "uid", id(ob))
            if ob.rect.top > car_bottom and uid not in self._counted_pass:
                self._counted_pass.add(uid)
                count += 1
        return count

    def _observe(self) -> Tuple[float, ...]:
        """Lane index + normalized distances to nearest obstacle ahead in each lane."""
        ptop = self.game.player.rect.top
        # init with far (1.0 means clear)
        dists = [1.0 for _ in range(LANES)]

        for ob in self.game.obstacles:
            lane = getattr(ob, "lane_idx", None)
            if lane is None or not (0 <= lane < LANES):
                continue
            # Only obstacles AHEAD of the car (above it on screen)
            if ob.rect.bottom <= ptop:
                pix = ptop - ob.rect.bottom
                norm = max(0.0, min(1.0, pix / HEIGHT))
                dists[lane] = min(dists[lane], norm)

        lane_idx = getattr(self.game.player, "lane", 1)
        return (float(lane_idx), *[float(x) for x in dists])

