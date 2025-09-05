# rl_utils.py
import json
import math
from typing import Dict, Tuple, List

# Actions: 0=left, 1=stay, 2=right
ACTIONS = [0, 1, 2]

# ---- State discretization ----
# Distances are in [0,1]; we bucket them to keep the Q-table small.
# You can tweak these cut points later if you like.
DISTANCE_BINS = [0.10, 0.25, 0.50, 0.75, 1.01]  # 5 bins

def bin_index(x: float) -> int:
    for i, b in enumerate(DISTANCE_BINS):
        if x <= b: 
            return i
    return len(DISTANCE_BINS) - 1

def encode_state(obs: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
    """
    obs = (lane, dL, dM, dR)
    Returns a discrete state key: (lane, bL, bM, bR)
    """
    lane = int(round(obs[0]))
    bL = bin_index(obs[1])
    bM = bin_index(obs[2])
    bR = bin_index(obs[3])
    return (lane, bL, bM, bR)

# ---- Q-table ----
class QTable:
    def __init__(self):
        # Dict[(lane, bL, bM, bR)] -> [Q_left, Q_stay, Q_right]
        self.Q: Dict[Tuple[int,int,int,int], List[float]] = {}

    def get(self, state: Tuple[int,int,int,int]) -> List[float]:
        if state not in self.Q:
            self.Q[state] = [0.0, 0.0, 0.0]
        return self.Q[state]

    def best_action(self, state) -> int:
        q = self.get(state)
        # Tie-break toward "stay" to reduce jitter
        best = max(range(3), key=lambda a: (q[a], 1 if a == 1 else 0))
        return best

    def update(self, s, a, r, s_next, alpha: float, gamma: float):
        q = self.get(s)
        max_next = max(self.get(s_next))
        q[a] += alpha * (r + gamma * max_next - q[a])

    # ---- save/load ----
    @staticmethod
    def _key_to_str(k: Tuple[int,int,int,int]) -> str:
        return f"{k[0]}|{k[1]}|{k[2]}|{k[3]}"

    @staticmethod
    def _str_to_key(s: str) -> Tuple[int,int,int,int]:
        a,b,c,d = s.split("|")
        return (int(a), int(b), int(c), int(d))

    def save_json(self, path: str):
        ser = { self._key_to_str(k): v for k, v in self.Q.items() }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ser, f)

    def load_json(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            ser = json.load(f)
        self.Q = { self._str_to_key(k): [float(x) for x in v] for k, v in ser.items() }

# ---- Epsilon schedules ----
def linear_epsilon(ep: int, start: float, end: float, decay_episodes: int) -> float:
    if ep >= decay_episodes:
        return end
    t = ep / max(1, decay_episodes)
    return start + t * (end - start)

def epsilon_greedy(qtab: QTable, state, epsilon: float) -> int:
    import random
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    return qtab.best_action(state)
