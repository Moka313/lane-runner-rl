# q_train.py
import argparse
import time
import random
from rl_utils import QTable, encode_state, epsilon_greedy, linear_epsilon
from env import LaneDodgeEnv, LEFT, STAY, RIGHT

def train(episodes: int, alpha: float, gamma: float, eps_start: float, eps_end: float,
          eps_decay_episodes: int, seed: int | None, save_path: str, render_every: int):

    random.seed(seed if seed is not None else 0)

    # Headless (fast) training: render_mode != "human"
    env = LaneDodgeEnv(render_mode="none", seed=seed)
    qtab = QTable()

    log_every = max(1, episodes // 20)
    best_return = float("-inf")

    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        s = encode_state(obs)
        done = False
        total_r = 0.0
        total_passed = 0
        steps = 0
        last_action = STAY

        epsilon = linear_epsilon(ep, eps_start, eps_end, eps_decay_episodes)

        while not done:
            a = epsilon_greedy(qtab, s, epsilon)
            obs2, r, done, info = env.step(a)
            s2 = encode_state(obs2)

            # Optional tiny penalty to discourage frantic lane changes
            if a != STAY and last_action != STAY:
                r -= 0.002

            qtab.update(s, a, r, s2, alpha, gamma)

            total_r += r
            total_passed += info.get("passed", 0)
            steps += 1
            s = s2
            last_action = a

        if total_r > best_return:
            best_return = total_r

        # Render a quick visual episode every N episodes to "peek" at progress
        if render_every > 0 and ep % render_every == 0:
            peek(env, qtab)

        if ep % log_every == 0 or ep == 1 or ep == episodes:
            print(f"[ep {ep:4d}/{episodes}] "
                  f"eps={epsilon:.3f}  return={total_r:7.2f}  passed={total_passed:4d}  steps={steps:5d}  bestR={best_return:7.2f}")

    env.close()
    qtab.save_json(save_path)
    print(f"\nSaved Q-table to {save_path}")

def peek(env: LaneDodgeEnv, qtab: QTable):
    # One quick greedy run (no learning) with drawing ON for ~1 episode.
    # We reuse the same env by temporarily drawing a few frames.
    # (The env only draws when render_mode == 'human'.)
    prev_mode = env.render_mode
    env.render_mode = "human"
    obs, _ = env.reset()
    done = False
    steps = 0
    total_r = 0.0
    while not done and steps < 3000:
        s = encode_state(obs)
        a = qtab.best_action(s)
        obs, r, done, info = env.step(a)
        total_r += r
        steps += 1
    print(f"  ↳ peek run: steps={steps}, return={total_r:.2f}")
    env.render_mode = prev_mode

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=800, help="number of training episodes")
    ap.add_argument("--alpha", type=float, default=0.20, help="learning rate")
    ap.add_argument("--gamma", type=float, default=0.95, help="discount factor")
    ap.add_argument("--eps_start", type=float, default=1.0, help="initial epsilon")
    ap.add_argument("--eps_end", type=float, default=0.05, help="final epsilon")
    ap.add_argument("--eps_decay", type=int, default=600, help="episodes to decay epsilon")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--save", type=str, default="q_table.json")
    ap.add_argument("--render_every", type=int, default=0, help="render a visual peek every N episodes (0=never)")
    args = ap.parse_args()

    train(args.episodes, args.alpha, args.gamma, args.eps_start, args.eps_end,
          args.eps_decay, args.seed, args.save, args.render_every)
